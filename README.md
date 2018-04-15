# dns-test

A simple utility to test multiple DNS servers for their average resolve time.
To disable caching, this tool generates random domains. For more information please consult the comments in `dns-test.py`.

## Installation

### Docker
The easiest way to run this is by using the pre-build docker image (`fekle/dns-test:latest`) or building the 
image yourself with `./cli docker-build`. You can then run via `./cli docker-run <cmd>` or simply:
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

Options:
  -s, --server TEXT       the nameserver to test
  -f, --server-file PATH  YAML file to read servers from
  -o, --report-file PATH  file to save results to
  -r, --rounds INTEGER    number of tests  [default: 100]
  -h, --help              Show this message and exit.
```
[![asciicast](https://asciinema.org/a/rFEJB81CIyBqJovXYR0nPcCjm.png)](https://asciinema.org/a/rFEJB81CIyBqJovXYR0nPcCjm)

If the program is started with no arguments, the local default DNS server will be tested for 100 rounds.
To choose the amount of test rounds, specify a number with `--rounds`.

Custom DNS servers can either be passed via the `--server` option (can occur multiple tiems) and/or with
the `--server-file` option. Latter option requires a YAML formatted file, see servers/example.yml.

If `--report-file` is specified, a report will be appended to the specified file, also in YAML format.


## Example
```bash
$ ./dns-test.py --server-file servers/example.yml --rounds 32 --report-file report.yml
testing google (8.8.8.8, 8.8.4.4) with 32 rounds per host
testing cloudflare (1.1.1.1, 1.0.0.1) with 32 rounds per host
testing quad9 (9.9.9.9, 149.112.112.112) with 32 rounds per host
testing opendns (208.67.222.222, 208.67.220.220) with 32 rounds per host

=== RESULTS ===
google:
 8.8.8.8         : avg:  30.89ms - stdev:  41.36ms - min:  15.96ms - max: 252.51ms
 8.8.4.4         : avg:  31.71ms - stdev:  34.91ms - min:  15.25ms - max: 171.95ms
cloudflare:
 1.1.1.1         : avg:  39.32ms - stdev:  41.02ms - min:   9.49ms - max: 207.42ms
 1.0.0.1         : avg:  67.18ms - stdev: 136.04ms - min:   9.97ms - max: 736.64ms
quad9:
 9.9.9.9         : avg:  25.83ms - stdev:  23.96ms - min:  10.60ms - max: 128.43ms
 149.112.112.112 : avg:  39.24ms - stdev:  46.15ms - min:  10.90ms - max: 174.87ms
opendns:
 208.67.222.222  : avg:  62.19ms - stdev: 124.86ms - min:  11.08ms - max: 669.67ms
 208.67.220.220  : avg:  88.69ms - stdev: 129.48ms - min:  11.08ms - max: 505.67ms
 
$ cat report.yml
---
date: 15-04-2018 16:55:42 CEST
results:
  cloudflare:
    1.0.0.1:
      avg: 67.18
      max: 736.64
      min: 9.97
      stdev: 136.04
    1.1.1.1:
      avg: 39.32
      max: 207.42
      min: 9.49
      stdev: 41.02
  google:
    8.8.4.4:
      avg: 31.71
      max: 171.95
      min: 15.25
      stdev: 34.91
    8.8.8.8:
      avg: 30.89
      max: 252.51
      min: 15.96
      stdev: 41.36
  opendns:
    208.67.220.220:
      avg: 88.69
      max: 505.67
      min: 11.08
      stdev: 129.48
    208.67.222.222:
      avg: 62.19
      max: 669.67
      min: 11.08
      stdev: 124.86
  quad9:
    149.112.112.112:
      avg: 39.24
      max: 174.87
      min: 10.9
      stdev: 46.15
    9.9.9.9:
      avg: 25.83
      max: 128.43
      min: 10.6
      stdev: 23.96
rounds: 32
```