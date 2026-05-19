#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/../app"
CMD="$SCRIPT_DIR/cmd.sh"

echo "Checking Wrappers Registry Reader..."

# 1. Structure
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/wrappers_registry_reader.py" ] || { echo "FAIL: Main script missing"; exit 1; }

# 2. Python execution (Status)
echo -n "Checking Status... "
if bash "$CMD" status | grep -q "Module: wrappers_registry_reader"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

# 3. Logic check (List)
echo -n "Checking List... "
if bash "$CMD" list | grep -q "menu-ui_registry_msi"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

# 4. Exports Check
echo -n "Checking JSON Export... "
bash "$CMD" export-json > /dev/null
if [ -f "$SCRIPT_DIR/../output/wrappers_registry.json" ]; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

echo "Sanity Check Passed."
