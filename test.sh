#!/bin/bash
set -euf -o pipefail

declare -A servers
servers=(
  ["google-1"]="8.8.8.8"
  ["google-2"]="8.8.4.4"
  ["cloudflare-1"]="1.1.1.1"
  ["cloudflare-2"]="1.0.0.1"
  ["quad9-1"]="9.9.9.9"
  ["quad9-2"]="149.112.112.112"
  ["opendns-1"]="208.67.222.222"
  ["opendns-2"]="208.67.220.220"
)

rounds=${1:-50}
result=""

for server in "${!servers[@]}"; do
  ip=${servers[$server]}
  echo "=> testing server '$server'"
  tmp=$(python3 -O ./dnsavg.py --server "${ip}" --rounds "${rounds}")
  result="${result}
${server} $(tail -n1 <<<"${tmp}")"
done
result="$(sort <<<"${result}")"

printf '\n=== RESULTS ===%s\n' "${result}"
