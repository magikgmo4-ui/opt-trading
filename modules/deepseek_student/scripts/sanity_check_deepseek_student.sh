#!/usr/bin/env bash
set -euo pipefail
echo "=== DeepSeek Student Sanity Check ==="
command -v ollama >/dev/null || { echo "FAIL: ollama missing"; exit 1; }
systemctl is-active --quiet ollama || { echo "FAIL: ollama service inactive"; exit 1; }
curl -sS http://127.0.0.1:11434/api/tags >/dev/null || { echo "FAIL: ollama api not responding"; exit 1; }
test -d /opt/trading/_student_archive/events || { echo "FAIL: missing events dir"; exit 1; }
test -x /opt/trading/.venv/bin/python || { echo "FAIL: missing venv python"; exit 1; }
echo "PASS"
