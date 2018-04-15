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
[![asciicast](https://asciinema.org/a/nskUckwjFapY8aN6GTVo6ZAuB.png)](https://asciinema.org/a/nskUckwjFapY8aN6GTVo6ZAuB)

If the program is started with no arguments, the local default DNS server will be tested for 100 rounds.
To choose the amount of test rounds, specify a number with `--rounds`.

Custom DNS servers can either be passed via the `--server` option (can occur multiple tiems) and/or with
the `--server-file` option. Latter option requires a YAML formatted file, see servers/example.yml.

If `--report-file` is specified, a report will be appended to the specified file, also in YAML format.


## Example
```bash
$ ./dns-test.py --server-file servers/example.yml --rounds 32 --report-file report.yml
esting google (8.8.8.8, 8.8.4.4) with 32 rounds per host
testing cloudflare (1.1.1.1, 1.0.0.1) with 32 rounds per host
testing quad9 (9.9.9.9, 149.112.112.112) with 32 rounds per host
testing opendns (208.67.222.222, 208.67.220.220) with 32 rounds per host

=== RESULTS ===
google:
 8.8.8.8         : avg:  69.62ms - stdev:  31.23ms - min:  49.46ms - max: 209.57ms
 8.8.4.4         : avg:  60.03ms - stdev:  11.19ms - min:  49.61ms - max: 100.45ms
cloudflare:
 1.1.1.1         : avg:  86.47ms - stdev:  82.77ms - min:  30.43ms - max: 317.45ms
 1.0.0.1         : avg:  67.66ms - stdev:  42.37ms - min:  33.98ms - max: 185.58ms
quad9:
 9.9.9.9         : avg:  68.42ms - stdev:  43.75ms - min:  34.85ms - max: 257.11ms
 149.112.112.112 : avg:  79.77ms - stdev:  52.78ms - min:  36.44ms - max: 218.77ms
opendns:
 208.67.222.222  : avg:  91.79ms - stdev:  80.58ms - min:  33.36ms - max: 309.31ms
 208.67.220.220  : avg: 151.69ms - stdev: 155.14ms - min:  28.48ms - max: 565.12ms
 
$ cat report.yml
date: 15-04-2018 15:48:31 CEST
results:
  cloudflare:
    1.0.0.1:
      avg: 67.66
      max: 185.58
      min: 33.98
      stdev: 42.37
    1.1.1.1:
      avg: 86.47
      max: 317.45
      min: 30.43
      stdev: 82.77
  google:
    8.8.4.4:
      avg: 60.03
      max: 100.45
      min: 49.61
      stdev: 11.19
    8.8.8.8:
      avg: 69.62
      max: 209.57
      min: 49.46
      stdev: 31.23
  opendns:
    208.67.220.220:
      avg: 151.69
      max: 565.12
      min: 28.48
      stdev: 155.14
    208.67.222.222:
      avg: 91.79
      max: 309.31
      min: 33.36
      stdev: 80.58
  quad9:
    149.112.112.112:
      avg: 79.77
      max: 218.77
      min: 36.44
      stdev: 52.78
    9.9.9.9:
      avg: 68.42
      max: 257.11
      min: 34.85
      stdev: 43.75
rounds: 32
```