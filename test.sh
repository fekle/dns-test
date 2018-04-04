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
)

rounds=${1:-50}
tmp=$(mktemp)
result=""

for server in "${!servers[@]}"; do
  ip=${servers[$server]}
  echo "=> testing server '$server'"
  ./dnsavg.sh "${ip}" "${rounds}" | tee "${tmp}"
  result="${result}
${server}: $(tail -n1 <"${tmp}")"
done
result="$(sort <<<"${result}")"

printf '\n=== RESULTS ===%f\n' "${result}"
