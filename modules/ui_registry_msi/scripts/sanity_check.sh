#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/../app"
CONFIG_DIR="$SCRIPT_DIR/../config"
CMD="$SCRIPT_DIR/cmd.sh"

echo "Checking UI Registry MSI..."

# 1. Structure
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/ui_registry_msi.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -f "$CONFIG_DIR/ui_registry_seed.json" ] || { echo "FAIL: Seed missing"; exit 1; }

# 2. Python execution (Status)
echo -n "Checking Status... "
if bash "$CMD" status | grep -q "Module: ui_registry_msi"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

# 3. Logic check (MSI filter)
echo -n "Checking MSI Filter... "
if bash "$CMD" show-msi | grep -q "MSI / DB-LAYER SURFACES"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

# 4. Exports Check
echo -n "Checking JSON Export... "
bash "$CMD" export-json > /dev/null
if [ -f "$SCRIPT_DIR/../output/ui_registry_msi.json" ]; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

echo -n "Checking Markdown Export... "
bash "$CMD" export-md > /dev/null
if [ -f "$SCRIPT_DIR/../output/ui_registry_msi.md" ]; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

echo "Sanity Check Passed."
