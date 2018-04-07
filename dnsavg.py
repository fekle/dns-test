#!/usr/bin/env python3

import random
import statistics
import string
import sys
import time
from random import randint

import click
from dns import rdataclass, rdatatype, resolver

default_server = resolver.get_default_resolver().nameservers[0] if len(resolver.get_default_resolver().nameservers) > 0 else '127.0.0.1'
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
@click.option('--server', '-s', default=default_server, type=click.STRING, help='the nameserver to test', show_default=True)
@click.option('--rounds', '-r', default=100, type=click.INT, help='number of tests', show_default=True)
def main(server, rounds):
    if len(server) > 0 and server[0] == "fight":
        server = {"google-1": "8.8.8.8", "google-2": "8.8.4.4", "cloudflare-1": "1.1.1.1", "cloudflare-2": "1.0.0.1", "quad9-1": "9.9.9.9",
                  "quad9-2": "149.112.112.112", "opendns-1": "208.67.222.222", "opendns-2": "208.67.220.220"
                  }.values()

    for s in server.split(','):
        res = resolver.Resolver()
        res.nameservers = [s]
        res.timeout = 3
        res.lifetime = 1
        res.port = 53

        results = []

        max_tries = 3
        try_count = 0

        print('=> testing {:s} with {:d} rounds'.format(s, rounds))

        for i in range(0, rounds):
            domain = random_domain()

            ms = run_test(res, domain)
            try_count += 1

            if ms <= 0:
                # retry
                if try_count <= max_tries:
                    i -= 1
                    continue
                else:
                    print('query failed', ms)
                    exit(1)
            else:
                try_count = 0

            time.sleep(randint(10, 75) / 1000)

            reset_line_print('{: 8.2f} {}'.format(ms, domain))

            results.append(ms)

        r_avg = statistics.mean(results)
        r_stddev = statistics.stdev(results)
        r_min = min(results)
        r_max = max(results)

        reset_line_print('=> {:s}: min: {:.2f}ms, max: {:.2f}ms, average: {:.2f}ms, stddev: {:.2f}ms\n'.format(s, r_min, r_max, r_avg, r_stddev))


if __name__ == '__main__':
    main()
