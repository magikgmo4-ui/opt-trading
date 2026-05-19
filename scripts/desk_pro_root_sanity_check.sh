#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Root Sanity Check

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CMD="$SCRIPT_DIR/desk_pro_root_cmd.sh"

echo "Checking Desk Pro Root Wrappers..."

# 1. File Structure
[ -f "$CMD" ] || { echo "FAIL: Root cmd script missing"; exit 1; }
[ -f "$SCRIPT_DIR/desk_pro_root.ps1" ] || { echo "FAIL: PowerShell wrapper missing"; exit 1; }

# 2. Python Availability
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Runner Module Availability
echo "Checking Runner Module..."
cd "$ROOT_DIR" || exit 1
if python3 -c "import modules.desk_pro_runner.app.desk_pro_runner" 2>/dev/null; then
    echo "PASS: Runner module importable."
else
    echo "FAIL: Cannot import desk_pro_runner."
    exit 1
fi

# 4. Status Execution
echo "Running status check via wrapper..."
OUTPUT=$(bash "$CMD" status 2>&1)
if [[ $? -eq 0 ]]; then
    if echo "$OUTPUT" | grep -q "runner_status"; then
        echo "PASS: Wrapper status check successful."
    else
        echo "FAIL: Wrapper output missing expected keys."
        echo "$OUTPUT"
        exit 1
    fi
else
    echo "FAIL: Wrapper execution failed."
    echo "$OUTPUT"
    exit 1
fi

echo "Root Sanity Check Passed."
