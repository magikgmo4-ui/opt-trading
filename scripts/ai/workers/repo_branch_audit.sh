#!/usr/bin/env bash
# Audit git branches — merged, orphan (stale >14d), open.
set -euo pipefail

REPORT=reports/ai/repo_branch_audit.json
mkdir -p "$(dirname "$REPORT")"

merged=$(git branch -r --merged origin/sot/mainline 2>/dev/null | grep -v 'sot/mainline\|HEAD' | wc -l | tr -d ' ')
total=$(git branch -r 2>/dev/null | grep -v HEAD | wc -l | tr -d ' ')

# Stale: remote branches with last commit > 14 days
stale=0
stale_list=()
while IFS= read -r branch; do
    branch="${branch#  }"
    last=$(git log -1 --format="%ct" "$branch" 2>/dev/null || echo 0)
    now=$(date +%s)
    age=$(( (now - last) / 86400 ))
    if [[ $age -gt 14 ]]; then
        stale=$(( stale + 1 ))
        stale_list+=("${branch}(${age}d)")
    fi
done < <(git branch -r 2>/dev/null | grep -v 'sot/mainline\|HEAD' | head -30)

json_stale=$(printf '%s\n' "${stale_list[@]+"${stale_list[@]}"}" | jq -R . | jq -s .)

status="PASS"
if [[ $merged -gt 5 ]]; then status="WARN"; fi

jq -n \
  --arg job "repo-branch-audit" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --argjson total "$total" \
  --argjson merged "$merged" \
  --argjson stale "$stale" \
  --argjson stale_list "$json_stale" \
  --arg status "$status" \
  '{job_id: $job, checked_at: $ts, total_remote: $total, merged_count: $merged, stale_count: $stale, stale_branches: $stale_list, status: $status}' \
  | tee "$REPORT"
