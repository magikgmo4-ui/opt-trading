#!/usr/bin/env bash
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="${MODULE_DIR}/scripts/cmd.sh"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "${TMP_ROOT}"' EXIT

export MEMORY_BRICKS_STATE_ROOT="${TMP_ROOT}/state"

for rel in app config scripts templates docs tests; do
  [ -e "${MODULE_DIR}/${rel}" ] || { echo "FAIL: missing ${rel}"; exit 2; }
done

out_a="$(${CMD} new --type resume_point --title "Sanity source" --ia chatgpt --machine student --surface terminal_linux --project opt-trading --module memory_bricks --status resumed --summary-short "Sanity source brick." --resume-point "Continue sanity." --tags sanity,test --decisions "Keep V1 local" --todo "Run full sanity")"
out_b="$(${CMD} new --type reference --title "Sanity target" --ia claude --machine student --surface terminal_linux --project opt-trading --module memory_bricks --status open --summary-short "Sanity target brick." --resume-point "Use second brick for link.")"

brick_a="$(printf '%s\n' "${out_a}" | awk -F': ' '/^CREATED:/ {print $2}')"
brick_b="$(printf '%s\n' "${out_b}" | awk -F': ' '/^CREATED:/ {print $2}')"
[ -n "${brick_a}" ] && [ -n "${brick_b}" ]

${CMD} show --id "${brick_a}" >/dev/null
${CMD} status --id "${brick_a}" --set closed >/dev/null
${CMD} link --id "${brick_a}" --to "${brick_b}" >/dev/null
${CMD} index rebuild >/dev/null

txt_export="$(${CMD} export --ids "${brick_a},${brick_b}" --format txt | awk '/^ / {print $1}')"
json_export="$(${CMD} export --ids "${brick_a},${brick_b}" --format json | awk '/^ / {print $1}')"
merge_export="$(${CMD} merge --ids "${brick_a},${brick_b}" | awk '/^ / {print $1}')"
handoff_export="$(${CMD} handoff --ids "${brick_a},${brick_b}" --target claude | awk '/^ / {print $1}')"

[ -f "${MEMORY_BRICKS_STATE_ROOT}/index/index_short.md" ] || { echo "FAIL: missing index_short.md"; exit 2; }
[ -f "${MEMORY_BRICKS_STATE_ROOT}/index/index_full.json" ] || { echo "FAIL: missing index_full.json"; exit 2; }
[ -f "${txt_export}" ] || { echo "FAIL: missing txt export"; exit 2; }
[ -f "${json_export}" ] || { echo "FAIL: missing json export"; exit 2; }
[ -f "${merge_export}" ] || { echo "FAIL: missing merge export"; exit 2; }
[ -f "${handoff_export}" ] || { echo "FAIL: missing handoff export"; exit 2; }

echo "PASS: memory_bricks sanity OK"
