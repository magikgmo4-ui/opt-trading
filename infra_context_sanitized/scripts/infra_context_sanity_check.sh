#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

echo "=== Infra Context Sanity Check ==="
echo "Repo: $(pwd)"
echo "Date: $(date -Iseconds)"

req=(
  "machines/admin-trading"
  "machines/cursor-ai"
  "machines/db-layer"
  "machines/student"
  "scripts/linux_snapshot_sanitized.sh"
  "scripts/windows_snapshot_sanitized.ps1"
  "SECURITY_REDACTION_RULES.md"
)

ok=1
for p in "${req[@]}"; do
  if [[ -e "$p" ]]; then
    echo "[OK] $p"
  else
    echo "[MISS] $p"
    ok=0
  fi
done

if [[ "$ok" -ne 1 ]]; then
  echo "FAIL: missing required files/dirs"
  exit 1
fi

echo "PASS: infra-context scaffold OK"
