#!/usr/bin/env bash
# Verify .gitignore covers expected secret file patterns.
set -euo pipefail

REPORT=reports/ai/gitignore_secrets_policy_check.json
mkdir -p "$(dirname "$REPORT")"

REQUIRED_PATTERNS=(".env" "*.pem" "*.key" "*.p12" "id_rsa" "id_ed25519" "__pycache__")
status="PASS"
findings=()
covered=()

if [[ ! -f ".gitignore" ]]; then
    findings+=("MISSING: .gitignore")
    status="WARN"
else
    gitignore_content=$(cat .gitignore)
    for pat in "${REQUIRED_PATTERNS[@]}"; do
        if echo "$gitignore_content" | grep -qF "$pat"; then
            covered+=("$pat")
        else
            findings+=("NOT_COVERED: $pat")
            status="WARN"
        fi
    done
fi

json_findings=$(printf '%s\n' "${findings[@]+"${findings[@]}"}" | jq -R . | jq -s .)
json_covered=$(printf '%s\n' "${covered[@]+"${covered[@]}"}" | jq -R . | jq -s .)

jq -n \
  --arg job "gitignore-secrets-policy-check" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --arg status "$status" \
  --argjson findings "$json_findings" \
  --argjson covered "$json_covered" \
  '{job_id: $job, checked_at: $ts, covered: $covered, findings: $findings, status: $status}' \
  | tee "$REPORT"
