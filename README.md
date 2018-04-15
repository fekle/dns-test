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
[![asciicast](https://asciinema.org/a/77D1Z2sxnwJFoqOIIFPFw6moN.png)](https://asciinema.org/a/77D1Z2sxnwJFoqOIIFPFw6moN)

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
 8.8.8.8         : avg:   34.89ms - stdev:   49.91ms - min:   19.67ms - max:  300.79ms
 8.8.4.4         : avg:   31.15ms - stdev:   27.28ms - min:   20.55ms - max:  174.93ms
cloudflare:
 1.1.1.1         : avg:   38.48ms - stdev:   36.42ms - min:   10.87ms - max:  157.50ms
 1.0.0.1         : avg:   62.81ms - stdev:  100.14ms - min:   12.54ms - max:  478.63ms
quad9:
 9.9.9.9         : avg:   31.41ms - stdev:   46.07ms - min:   10.79ms - max:  256.64ms
 149.112.112.112 : avg:   35.09ms - stdev:   49.63ms - min:   11.06ms - max:  268.31ms
opendns:
 208.67.222.222  : avg:   75.86ms - stdev:   88.37ms - min:   13.94ms - max:  304.45ms
 208.67.220.220  : avg:   71.96ms - stdev:   83.27ms - min:   12.87ms - max:  250.16ms

$ cat report.yml
---
date: 15-04-2018 17:11:04 CEST
results:
  cloudflare:
    1.0.0.1:
      avg: 62.81
      max: 478.63
      min: 12.54
      stdev: 100.14
    1.1.1.1:
      avg: 38.48
      max: 157.5
      min: 10.87
      stdev: 36.42
  google:
    8.8.4.4:
      avg: 31.15
      max: 174.93
      min: 20.55
      stdev: 27.28
    8.8.8.8:
      avg: 34.89
      max: 300.79
      min: 19.67
      stdev: 49.91
  opendns:
    208.67.220.220:
      avg: 71.96
      max: 250.16
      min: 12.87
      stdev: 83.27
    208.67.222.222:
      avg: 75.86
      max: 304.45
      min: 13.94
      stdev: 88.37
  quad9:
    149.112.112.112:
      avg: 35.09
      max: 268.31
      min: 11.06
      stdev: 49.63
    9.9.9.9:
      avg: 31.41
      max: 256.64
      min: 10.79
      stdev: 46.07
rounds: 32
```