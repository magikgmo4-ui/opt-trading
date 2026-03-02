#!/usr/bin/env bash
set -euo pipefail

echo "=== DeepSeek Hub Sanity ==="
date

need() { command -v "$1" >/dev/null 2>&1 || { echo "MISSING: $1"; exit 1; }; }

need curl
need jq
need ollama

mkdir -p /opt/trading/_student_archive/thinking /opt/trading/_student_archive/response

echo "[ollama]"
if ! systemctl is-active --quiet ollama; then
  echo "WARN: ollama service not active"
  systemctl --no-pager status ollama || true
else
  echo "OK: ollama service active"
fi

echo "[api]"
curl -s http://127.0.0.1:11434/api/version | jq -e . >/dev/null || { echo "FAIL: cannot read /api/version"; exit 1; }
curl -s http://127.0.0.1:11434/api/tags    | jq -e . >/dev/null || { echo "FAIL: cannot read /api/tags"; exit 1; }

echo "[commands]"
for c in cmd-deepseek_thinking cmd-deepseek_response cmd-deepseek_student; do
  if ! command -v "$c" >/dev/null 2>&1; then
    echo "WARN: missing $c (shortcuts not installed yet?)"
  else
    echo "OK: $c"
  fi
done

echo "PASS: deepseek_hub sanity OK"
