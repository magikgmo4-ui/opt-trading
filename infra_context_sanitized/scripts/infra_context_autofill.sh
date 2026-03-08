#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-$HOME/infra-context}"

cd "$ROOT"

echo "=== infra_context autofill ==="
echo "Repo: $(pwd)"
echo "Date: $(date -Iseconds)"

python3 scripts/autofill_fiches.py

echo
echo "=== redaction scan (grep-secrets) ==="
bash scripts/infra_context_cmd.sh grep-secrets || true

echo
echo "OK: autofill done. Review diffs with: git status && git diff"
