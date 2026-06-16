#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
ENV_FILE="$REPO_ROOT/.env"
REQUIRED_VARS=(TV_WEBHOOK_KEY OPS_ADMIN_KEY TELEGRAM_BOT_TOKEN TELEGRAM_CHAT_ID)

missing=0
echo "env_file=$ENV_FILE"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "status=FAIL"
  echo "missing_file=.env"
  exit 1
fi

for key in "${REQUIRED_VARS[@]}"; do
  if grep -Eq "^${key}=" "$ENV_FILE"; then
    echo "$key=present_in_file"
  elif [[ -n "${!key:-}" ]]; then
    echo "$key=present_in_env"
  else
    echo "$key=MISSING"
    missing=1
  fi
done

if [[ $missing -eq 1 ]]; then
  echo "status=FAIL"
  exit 1
fi

echo "status=PASS"
