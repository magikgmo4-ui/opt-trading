#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR/../app"
CMD="$SCRIPT_DIR/cmd.sh"

echo "Checking Registry Router..."

# 1. Structure
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/registry_router.py" ] || { echo "FAIL: Main script missing"; exit 1; }

# 2. Python execution (Status)
echo -n "Checking Status... "
if bash "$CMD" status | grep -q "Role: Central Navigation"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

# 3. Logic check (List Entries)
echo -n "Checking Entries... "
if bash "$CMD" show-entries | grep -q "machines_registry_reader"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

echo "Sanity Check Passed."
