#!/bin/bash
set -euf -o pipefail

# list of tlds to be used
tlds=(com org co.uk net ca de jp fr au us at ch it nl io)

# get a random 64 char hex string
function random_hex() {
  head -c 128 /dev/urandom | base64 | \
    fold -w1 | shuf | grep -Eo '[a-Z0-9]' | tr -d '\n' | cut -c-64 | tr '[:upper:]' '[:lower:]'
}

# get a random domain
function random_domain() {
  tld="${tlds[$(shuf -i 0-$((${#tlds[@]} - 1)) -n 1)]}"
  printf "%.$(shuf -i 1-8 -n 1)s.%.$(shuf -i 3-12 -n 1)s.%s" "$(random_hex)" "$(random_hex)" "${tld}"
}

# number of times to test
rounds="${2:-10}"
server="${1:-$(grep 'nameserver' /etc/resolv.conf | tail -n1 | awk '{ print $2; }')}"
port="${3:-53}"

# check for dig or drill
cmd=$( (hash dig 2>/dev/null && printf dig) || (hash drill 2>/dev/null && printf drill)) || (
  echo 'error: dig or drill required'
  exit 1
)

printf 'testing %s domains on %s:%s\n' "${rounds}" "${server}" "${port} with ${cmd}"

# do the magic
addition=''
for i in $(seq 1 "${rounds}"); do
  domain=$(random_domain)
  time=$(${cmd} -p "${port}" "${domain}" IN A "@${server}" | grep -Eo ';; Query time: [0-9]+(\.[0-9]+)? msec' | grep -Eo '[0-9]+(\.[0-9]+)?') || { echo 'query failed'; exit 1; }
  addition="${addition} + ${time}"
  sleep "0.0$(shuf -i 01-25 -n 1)" # let's not go crazy

  printf '%6.1f ms %s\n' "${time}" "${domain}"
done

# get average
average=$(bc -l <<<"( 0${addition} ) / ${rounds}")
printf '\naverage: %0.1f ms\n' "${average}"
