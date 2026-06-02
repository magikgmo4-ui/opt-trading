#!/usr/bin/env bash
# Check .env file presence and non-emptiness.
set -euo pipefail

REPORT=reports/ai/env_file_presence_check.json
mkdir -p "$(dirname "$REPORT")"

status="PASS"
findings=()

if [[ ! -f ".env" ]]; then
    findings+=("MISSING: .env")
    status="WARN"
elif [[ ! -s ".env" ]]; then
    findings+=("EMPTY: .env")
    status="WARN"
fi

if [[ ! -f ".env.example" ]]; then
    findings+=("MISSING: .env.example")
    status="WARN"
fi

# Build JSON findings array
json_findings=$(printf '%s\n' "${findings[@]+"${findings[@]}"}" | jq -R . | jq -s .)

jq -n \
  --arg job "env-file-presence-check" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg status "$status" \
  --argjson findings "$json_findings" \
  '{job_id: $job, checked_at: $ts, findings: $findings, status: $status}' \
  | tee "$REPORT"
