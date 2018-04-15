# dns-test [![Build Status](https://travis-ci.org/fekle/dns-test.svg?branch=master)](https://travis-ci.org/fekle/dns-test)

A simple utility to test multiple DNS servers for their average resolve time.
For more information please consult the comments in `dns-test.py`.

## Installation

### Docker
The easiest way to run this is by using the pre-built docker image [fekle/dns-test:latest](https://hub.docker.com/r/fekle/dns-test/)
or building the image yourself with `./cli docker-build`. You can then run via `./cli docker-run <cmd>` or simply:
```bash
docker run --rm -t --user "$(id -u):$(id -g)" \
     -v "${workdir}:/workdir:rw" \
     fekle/dns-test:latest <cmd>
```
### Local
To install locally, use `pipenv install` and `pipenv run ./dns-test.py`.
For development, you can start a shell in the venv with `pipenv shell`.

## Usage
```
Usage: dns-test.py [OPTIONS]

  main function. loads server list from file and cmdline arguments, or loads
  system default if none specified

Options:
  -s, --server TEXT         the nameserver to test
  -f, --server-file PATH    YAML file to read servers from
  -o, --report-file PATH    file to save results to
  -r, --rounds INTEGER      number of tests  [default: 100]
  -l, --local / --no-local  include local server  [default: False]
  -d, --domain-file PATH    try to load random domains from list
  -h, --help                Show this message and exit.             Show this message and exit.
```
[![asciicast](https://asciinema.org/a/176374.png)](https://asciinema.org/a/176374)

If the program is started with no arguments, the local default DNS server will be tested for 100 rounds.
To choose the amount of test rounds, specify a number with `--rounds`.

Custom DNS servers can either be passed via the `--server` option (can occur multiple tiems) and/or with
the `--server-file` option. Latter option requires a YAML formatted file, see servers/example.yml.

If `--report-file` is specified, a report will be appended to the specified file, also in YAML format.

If you are performing comparisons of multiple servers, the flag `--local` can come in handy to compare your local server as well.

By default, this program generates random domains to combat caching. However if you want to achieve even more realistic test results,
you should aquire a big domain list like Cisco Umbrella (see `./dev download-umbrella`) and include it with the `--domain-file` flag.

## Example
```bash
$ ./dns-test.py --rounds 32 --local --server-file servers/example.yml --domain-file domains/umbrella.csv --report-file report.yml
found 998932 domains in domains/umbrella.csv
testing google (8.8.8.8, 8.8.4.4) with 32 rounds per host
testing cloudflare (1.1.1.1, 1.0.0.1) with 32 rounds per host
testing quad9 (9.9.9.9, 149.112.112.112) with 32 rounds per host
testing opendns (208.67.222.222, 208.67.220.220) with 32 rounds per host
testing local (127.0.0.1) with 32 rounds per hostideo.com

=== RESULTS ===
google:
 8.8.8.8         : avg:   48.05ms - stdev:   59.17ms - min:   13.51ms - max:  302.98ms
 8.8.4.4         : avg:   72.66ms - stdev:  119.46ms - min:   14.06ms - max:  588.35ms
cloudflare:
 1.1.1.1         : avg:  119.74ms - stdev:  131.38ms - min:   10.33ms - max:  474.37ms
 1.0.0.1         : avg:  139.96ms - stdev:  193.33ms - min:   12.99ms - max:  747.68ms
quad9:
 9.9.9.9         : avg:  125.45ms - stdev:  140.16ms - min:   11.56ms - max:  450.91ms
 149.112.112.112 : avg:   87.40ms - stdev:   95.00ms - min:   11.37ms - max:  330.68ms
opendns:
 208.67.222.222  : avg:   87.64ms - stdev:  165.20ms - min:    9.97ms - max:  880.42ms
 208.67.220.220  : avg:   60.33ms - stdev:   77.27ms - min:   10.50ms - max:  321.28ms
local:
 127.0.0.1       : avg:  429.83ms - stdev:  288.15ms - min:  107.99ms - max: 1228.39ms
 
$ cat report.yml
---
date: 15-04-2018 22:17:01 CEST
results:
  cloudflare:
    1.0.0.1:
      avg: 139.96
      max: 747.68
      min: 12.99
      stdev: 193.33
    1.1.1.1:
      avg: 119.74
      max: 474.37
      min: 10.33
      stdev: 131.38
  google:
    8.8.4.4:
      avg: 72.66
      max: 588.35
      min: 14.06
      stdev: 119.46
    8.8.8.8:
      avg: 48.05
      max: 302.98
      min: 13.51
      stdev: 59.17
  local:
    127.0.0.1:
      avg: 429.83
      max: 1228.39
      min: 107.99
      stdev: 288.15
  opendns:
    208.67.220.220:
      avg: 60.33
      max: 321.28
      min: 10.5
      stdev: 77.27
    208.67.222.222:
      avg: 87.64
      max: 880.42
      min: 9.97
      stdev: 165.2
  quad9:
    149.112.112.112:
      avg: 87.4
      max: 330.68
      min: 11.37
      stdev: 95.0
    9.9.9.9:
      avg: 125.45
      max: 450.91
      min: 11.56
      stdev: 140.16
rounds: 32
```