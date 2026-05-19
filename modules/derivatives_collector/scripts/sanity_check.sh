#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
CONFIG_DIR="$MODULE_DIR/config"
SCRIPTS_DIR="$MODULE_DIR/scripts"

echo "Checking Derivatives Collector Module..."

# 1. Structure Check
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/derivatives_collector.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -f "$CONFIG_DIR/example.env" ] || { echo "FAIL: Config example missing"; exit 1; }
[ -f "$SCRIPTS_DIR/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }

# 2. Python Check
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Execution Check (Mock)
echo "Running mock collection..."
cd "$ROOT_DIR" || exit 1
OUTPUT=$(python3 -m modules.derivatives_collector.app.derivatives_collector sample 2>&1)
if [[ $? -eq 0 ]]; then
    echo "PASS: Module executed correctly."
    echo "$OUTPUT" | head -n 5
else
    echo "FAIL: Module execution failed."
    echo "$OUTPUT"
    exit 1
fi

echo "Sanity Check Passed."
