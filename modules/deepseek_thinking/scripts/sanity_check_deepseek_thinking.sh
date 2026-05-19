#!/usr/bin/env bash
set -euo pipefail
echo "=== DeepSeek Thinking Sanity ==="
command -v ollama >/dev/null || { echo "FAIL: ollama missing"; exit 1; }
systemctl is-active --quiet ollama || { echo "FAIL: ollama inactive"; exit 1; }
curl -sS http://127.0.0.1:11434/api/tags >/dev/null || { echo "FAIL: ollama api down"; exit 1; }
echo "PASS"
