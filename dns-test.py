#!/usr/bin/env python3
import random
import re
import statistics
import string
import sys
import time
from random import randint

import click
import yaml
from dns import rdataclass, rdatatype, resolver

tlds = ['com', 'org', 'co.uk', 'net', 'ca', 'de', 'jp', 'fr', 'au', 'us', 'at', 'ch', 'it', 'nl', 'io']
local_servers = list(resolver.get_default_resolver().nameservers) if len(resolver.get_default_resolver().nameservers) > 0 else ['127.0.0.1']


def random_string(size=6, chars=string.ascii_lowercase + string.digits):
    """generate random string in a given range"""
    return ''.join(random.choice(chars) for _ in range(size))


def reset_line_print(x):
    """reset the current line in a shell if interactive, else print normally"""
    if sys.stdout.isatty():
        print('\x1b[2K' + x, end='\r')
    else:
        print(x)
        sys.stdout.flush()


def random_domain():
    """generate a random domain with the following format: {random subdomain}.{random domain}.{random tld from list}"""
    return '{}.{}.{}'.format(random_string(randint(1, 8)), random_string(randint(3, 12)), tlds[randint(0, len(tlds) - 1)])


def run_test(res, domain):
    """run a single dns query test on a server. Query time can be recovered from successful and NXDOMAIN responses"""
    try:
        return res.query(domain, rdtype=rdatatype.A, rdclass=rdataclass.IN).response.time * 1000
    except resolver.NXDOMAIN as e:
        return e.kwargs['responses'][list(filter(lambda a: str(a) == (domain + '.'), e.kwargs['responses']))[0]].time * 1000
    except (resolver.NoAnswer, resolver.Timeout, resolver.NoNameservers, resolver.NoNameservers):
        return -1


def load_domains(path):
    """load domains from a file"""
    domain_regex = re.compile('(?:[A-Za-z0-9_.\-~]+\.)+(?:[A-Za-z0-9_.\-~]+)')
    with open(path, 'r') as file:
        domains = []

        i = 0
        for line in file:
            domains += domain_regex.findall(line)

        if len(domains) >= 0:
            print("found {} domains in {}".format(len(domains), path))
            return domains
        else:
            raise Exception("couldn't find any domains in {}".format(path))


def truncate_string(s, length=32):
    """truncate a string to max length"""
    return (s[:length - 3] + '...') if len(s) > length else s


@click.command(context_settings={'help_option_names': ['--help', '-h']})
@click.option('--server', '-s', type=click.STRING, help='the nameserver to test', multiple=True)
@click.option('--server-file', '-f', type=click.Path(exists=True), help='YAML file to read servers from', multiple=True)
@click.option('--report-file', '-o', type=click.Path(exists=False), help='file to save results to')
@click.option('--rounds', '-r', default=100, type=click.INT, help='number of tests', show_default=True)
@click.option('--local/--no-local', '-l', default=False, help='include local server', show_default=True)
@click.option('--domain-file', '-d', type=click.Path(exists=True), help='try to load random domains from list')
def main(server, server_file, report_file, rounds, local, domain_file):
    """main function. loads server list from file and cmdline arguments, or loads system default if none specified"""
    start_time = time.localtime()
    server_list = {}
    final_results = {}
    domain_list = []

    # parse yaml file and load servers from list
    if server_file and len(server_file) > 0:
        for p in server_file:
            try:
                with open(p, 'r') as stream:
                    conf = yaml.load(stream)
                    if len(conf) > 0 and type(conf[0]) is dict:
                        for k, v in conf[0]['servers'].items():
                            server_list[k] = v

            except Exception as exc:
                print(exc)
                sys.exit(1)

    # load servers from cmdline args
    if server and len(server) > 0:
        server_list['input'] = server

    # include local server if desired
    if len(server_list.items()) == 0 or local is True:
        server_list['local'] = local_servers

    # load domains from file if desired
    if domain_file and len(domain_file) > 0:
        domain_list = load_domains(domain_file)

    # loop through servers
    for name, host_list in server_list.items():
        print('testing {:s} ({:s}) with {:d} rounds per host'.format(name, ', '.join(host_list), rounds))

        # initiate final result object for current server
        final_results[name] = {}

        # loop through hosts of current server
        for i in range(0, len(host_list)):

            # initiate DNS host
            res = resolver.Resolver(configure=False)
            res.nameservers = [host_list[i]]
            res.timeout = 3
            res.lifetime = 1.5
            res.port = 53
            res.cache = False

            failed = False
            max_tries = 3
            try_count = 0
            results = []

            # loop through amount of rounds
            for r in range(0, rounds):
                domain = random_domain() if len(domain_list) <= 0 else domain_list[randint(0, len(domain_list) - 1)]

                # run test
                ms = run_test(res, domain)

                # if ms is smaller than 0, increment retry counter and retry round
                if ms <= 0:
                    try_count += 1
                    if try_count <= max_tries:
                        r -= 1
                        reset_line_print('=> {:s} {:4d}    -    {:s}'.format(host_list[i], r + 1, truncate_string(domain)))
                        continue
                    else:
                        print('host failed: {}'.format(host_list[i]))
                        failed = True
                        break
                else:
                    try_count = 0

                results.append(ms)

                # print status line
                reset_line_print('=> {:s} {:4d} {:7.2f} {:s}'.format(host_list[i], r + 1, ms, truncate_string(domain)))

                # let's wait for a random time at the end to prevent flooding
                time.sleep(randint(25, 150) / 1000)

            if failed is False:
                # construct final result object for current host
                final_results[name][host_list[i]] = {
                        'avg': round(statistics.mean(results), 2),
                        'stdev': round(statistics.stdev(results), 2),
                        'min': round(min(results), 2),
                        'max': round(max(results), 2)
                }

    reset_line_print('\n=== RESULTS ===\n')

    # loop through results and print them formatted
    for k, v in final_results.items():
        print('{}:'.format(k))
        for i, j in v.items():
            stats = []
            for x, y in j.items():
                stats.append('{}: {:7.2f}ms'.format(x, y))
            print(' {:16}: {}'.format(i, ' - '.join(stats)))

    # if report file was specified, append yaml to report file
    if report_file:
        with open(report_file, 'a') as yaml_file:
            yaml.safe_dump({
                    'date': time.strftime('%d-%m-%Y %H:%M:%S %Z', start_time).strip(),
                    'rounds': rounds,
                    'results': final_results
            },
                           yaml_file,
                           explicit_start=True,
                           encoding='UTF-8',
                           default_flow_style=False,
                           indent=2,
                           line_break=True)


if __name__ == '__main__':
    main()
