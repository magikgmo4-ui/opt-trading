#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
GITIGNORE="$REPO_ROOT/.gitignore"
REQUIRED_PATTERNS=(
  ".env"
  "*.key"
  "*.pem"
  "id_rsa"
  "id_ed25519"
  "*API_KEY*"
  "*SECRET*"
  "*TOKEN*"
)

missing=0
echo "gitignore=$GITIGNORE"
for pattern in "${REQUIRED_PATTERNS[@]}"; do
  if grep -Fqx "$pattern" "$GITIGNORE"; then
    echo "$pattern=present"
  else
    echo "$pattern=MISSING"
    missing=1
  fi
done

if [[ $missing -eq 1 ]]; then
  echo "status=FAIL"
  exit 1
fi

echo "status=PASS"
