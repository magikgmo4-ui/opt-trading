#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
CONFIG_DIR="$MODULE_DIR/config"
SCRIPTS_DIR="$MODULE_DIR/scripts"

echo "Checking Desk Pro Runner Module..."

# 1. Structure Check
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/desk_pro_runner.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -f "$CONFIG_DIR/runner_config.example.json" ] || { echo "FAIL: Example config missing"; exit 1; }
[ -f "$SCRIPTS_DIR/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }

# 2. Python Check
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Status Check
echo "Running status check..."
cd "$ROOT_DIR" || exit 1
OUTPUT=$(python3 -m modules.desk_pro_runner.app.desk_pro_runner status 2>&1)
if [[ $? -eq 0 ]]; then
    if echo "$OUTPUT" | grep -q "runner_status"; then
        echo "PASS: Runner status check passed."
        echo "$OUTPUT" | grep "summary"
    else
        echo "FAIL: Output missing expected keys."
        echo "$OUTPUT"
        exit 1
    fi
else
    echo "FAIL: Module execution failed."
    echo "$OUTPUT"
    exit 1
fi

echo "Sanity Check Passed."
