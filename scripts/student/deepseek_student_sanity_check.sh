#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student Sanity Check

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Checking DeepSeek Student Environment..."

# 1. Python
if command -v python3 &> /dev/null; then
    echo "PASS: Python 3 found"
else
    echo "FAIL: Python 3 missing"
    exit 1
fi

# 2. Repo Structure
if [ -d "$ROOT_DIR/modules/deepseek_hub" ]; then
    echo "PASS: DeepSeek Hub directory exists"
else
    echo "FAIL: DeepSeek Hub module missing"
    exit 1
fi

# 3. Scripts
if [ -f "$SCRIPT_DIR/deepseek_student_cmd.sh" ]; then
    echo "PASS: DeepSeek Student scripts present"
else
    echo "FAIL: DeepSeek Student scripts missing"
    exit 1
fi

# 4. Logs Access
LOGS_DIR="$ROOT_DIR/data/logs/deepseek_student"
if [ -d "$LOGS_DIR" ] || [ -w "$(dirname "$LOGS_DIR")" ]; then
    echo "PASS: Logs directory accessible"
else
    echo "WARN: Cannot write to logs directory"
fi

echo "DeepSeek Student Sanity Check Passed."
