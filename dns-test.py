#!/usr/bin/env python3

import random
import statistics
import string
from random import randint

import click
import sys
import time
import yaml
from dns import rdataclass, rdatatype, resolver

tlds = ['com', 'org', 'co.uk', 'net', 'ca', 'de', 'jp', 'fr', 'au', 'us', 'at', 'ch', 'it', 'nl', 'io']


def random_string(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def reset_line_print(x):
    if sys.stdout.isatty():
        print('\x1b[2K' + x, end='\r')
    else:
        print(x)
        sys.stdout.flush()


def random_domain():
    return '{}.{}.{}'.format(random_string(randint(1, 8)), random_string(randint(3, 12)), tlds[randint(0, len(tlds) - 1)])


def run_test(res, domain):
    start = time.time()
    try:
        _ = res.query(domain, rdtype=rdatatype.A, rdclass=rdataclass.IN)
    except resolver.NXDOMAIN:
        pass
    except (resolver.NoAnswer, resolver.Timeout, resolver.NoNameservers, resolver.NoNameservers):
        return -1
    stop = time.time()

    return float((stop - start) * 1000)


@click.command(context_settings={'help_option_names': ['--help', '-h']})
@click.option('--server', '-s', type=click.STRING, help='the nameserver to test', show_default=True, multiple=True)
@click.option('--server-file', type=click.Path(exists=True), help='YAML file to read servers from', multiple=True)
@click.option('--report-file', type=click.Path(exists=False), help='file to save results to')
@click.option('--rounds', '-r', default=100, type=click.INT, help='number of tests', show_default=True)
def main(server, server_file, report_file, rounds):
    start_time = time.localtime()
    server_list = {}

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

    if server and len(server) > 0:
        server_list['input'] = server

    if (len(server_list.items()) == 0):
        default_servers = resolver.get_default_resolver().nameservers if len(resolver.get_default_resolver().nameservers) > 0 else ['127.0.0.1']
        server_list['default'] = default_servers

    final_results = {}

    for name, host_list in server_list.items():
        print('testing {:s} ({:s}) with {:d} rounds per host'.format(name, ', '.join(host_list), rounds))

        final_results[name] = {}

        for i in range(0, len(host_list)):
            res = resolver.Resolver()
            res.nameservers = [host_list[i]]
            res.timeout = 3
            res.lifetime = 1
            res.port = 53

            results = []

            max_tries = 3
            try_count = 0

            for r in range(0, rounds):
                domain = random_domain()

                ms = run_test(res, domain)
                try_count += 1

                if ms <= 0:
                    # retry
                    if try_count <= max_tries:
                        r -= 1
                        continue
                    else:
                        print('query failed', ms)
                        exit(1)
                else:
                    try_count = 0

                time.sleep(randint(10, 75) / 1000)

                reset_line_print('{:7.2f} {}'.format(ms, domain))

                results.append(ms)

            final_results[name][host_list[i]] = {
                    'avg': round(statistics.mean(results), 2),
                    'stdev': round(statistics.stdev(results), 2),
                    'min': round(min(results), 2),
                    'max': round(max(results), 2)
            }

    reset_line_print('\n=== RESULTS ===\n')

    for k, v in final_results.items():
        print('{}:'.format(k))

        for i, j in v.items():
            stats = []
            for x, y in j.items():
                stats.append('{}: {:7.2f}ms'.format(x, y))
            print(' {:16}: {}'.format(i, ', '.join(stats)))

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
