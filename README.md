# dns-test

A simple utility to test multiple DNS servers for their average resolve time.
To disable caching, this tool generates random domains. For more information please consult the commends in `dns-test.py`.

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
 8.8.8.8         : avg:   59.29ms, stdev:   10.25ms, min:   34.89ms, max:   84.14ms
 8.8.4.4         : avg:   87.87ms, stdev:   68.63ms, min:   50.30ms, max:  280.44ms
cloudflare:
 1.1.1.1         : avg:   62.71ms, stdev:   33.75ms, min:   33.76ms, max:  185.84ms
 1.0.0.1         : avg:   66.47ms, stdev:   47.05ms, min:   32.38ms, max:  189.15ms
quad9:
 9.9.9.9         : avg:   90.11ms, stdev:   74.28ms, min:   36.74ms, max:  281.42ms
 149.112.112.112 : avg:   75.06ms, stdev:   39.90ms, min:   15.48ms, max:  159.50ms
opendns:
 208.67.222.222  : avg:  113.57ms, stdev:  106.47ms, min:   32.62ms, max:  413.05ms
 208.67.220.220  : avg:  107.64ms, stdev:  103.36ms, min:   32.74ms, max:  379.61ms

$ cat report.yml
---
date: 15-04-2018 15:26:04 CEST
results:
  cloudflare:
    1.0.0.1:
      avg: 66.47
      max: 189.15
      min: 32.38
      stdev: 47.05
    1.1.1.1:
      avg: 62.71
      max: 185.84
      min: 33.76
      stdev: 33.75
  google:
    8.8.4.4:
      avg: 87.87
      max: 280.44
      min: 50.3
      stdev: 68.63
    8.8.8.8:
      avg: 59.29
      max: 84.14
      min: 34.89
      stdev: 10.25
  opendns:
    208.67.220.220:
      avg: 107.64
      max: 379.61
      min: 32.74
      stdev: 103.36
    208.67.222.222:
      avg: 113.57
      max: 413.05
      min: 32.62
      stdev: 106.47
  quad9:
    149.112.112.112:
      avg: 75.06
      max: 159.5
      min: 15.48
      stdev: 39.9
    9.9.9.9:
      avg: 90.11
      max: 281.42
      min: 36.74
      stdev: 74.28
rounds: 32
```