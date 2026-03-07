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

# 2. Python execution
echo "Running status..."
if bash "$CMD" status | grep -q "Module: ui_registry_msi"; then
    echo "PASS: Status OK"
else
    echo "FAIL: Status check failed"
    exit 1
fi

# 3. Logic check
echo "Running show-msi..."
if bash "$CMD" show-msi | grep -q "msi_db_layer"; then
    echo "PASS: Logic OK"
else
    echo "FAIL: Logic check failed"
    exit 1
fi

echo "Sanity Check Passed."
