#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/app"
INPUT_DIR="$SCRIPT_DIR/inputs"
CMD="$SCRIPT_DIR/cmd.sh"
OUTPUT_DIR="$SCRIPT_DIR/output"

echo "Checking Validated Prompt Factory..."

# 1. Structure
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/validated_prompt_factory.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -d "$INPUT_DIR" ] || { echo "FAIL: Inputs dir missing"; exit 1; }

# 2. Python execution (Help)
echo -n "Checking Help... "
if bash "$CMD" help | grep -q "Usage:"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

# 3. Generation Test (Dry run mostly, but we can generate a file)
echo -n "Checking Generation (chatgpt_session)... "
# Ensure output dir exists
mkdir -p "$OUTPUT_DIR"

if bash "$CMD" generate chatgpt_session "$INPUT_DIR/synthesis_example.txt" > /dev/null; then
    if [ -f "$OUTPUT_DIR/prompt_chatgpt_session.txt" ]; then
        echo "OK"
    else
        echo "FAIL: Output file not created"
        exit 1
    fi
else
    echo "FAIL: Generation command failed"
    exit 1
fi

echo "Sanity Check Passed."
