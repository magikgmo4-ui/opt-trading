#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
APP_DIR="$SCRIPT_DIR/app"
INPUT_DIR="$SCRIPT_DIR/inputs"
CMD="$SCRIPT_DIR/cmd.sh"
OUTPUT_DIR="$SCRIPT_DIR/output"

echo "Checking Validated Prompt Factory..."

[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/validated_prompt_factory.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -d "$INPUT_DIR" ] || { echo "FAIL: Inputs dir missing"; exit 1; }

echo -n "Checking Help... "
if bash "$CMD" help | grep -q "Usage:"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

echo -n "Checking Generation (chatgpt_session)... "
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

echo -n "Checking Failure (missing section)... "
if bash "$CMD" generate trae_patch "$INPUT_DIR/synthesis_failure_missing_section.txt" > /dev/null 2>&1; then
    echo "FAIL: Expected failure but command succeeded"
    exit 1
else
    echo "OK"
fi

echo "Sanity Check Passed."
