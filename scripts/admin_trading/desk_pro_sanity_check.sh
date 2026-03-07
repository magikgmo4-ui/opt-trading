#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Admin Sanity Check

if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CMD="$SCRIPT_DIR/desk_pro_cmd.sh"

echo "Checking Admin Trading Environment..."

# 1. File Structure
[ -f "$CMD" ] || { echo "FAIL: CMD script missing"; exit 1; }
[ -f "$SCRIPT_DIR/desk_pro_copy_latest_to_shared.sh" ] || { echo "FAIL: Copy script missing"; exit 1; }

# 2. Python Availability
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Runner Module
echo "Checking Runner..."
cd "$ROOT_DIR" || exit 1
if python3 -c "import modules.desk_pro_runner.app.desk_pro_runner" 2>/dev/null; then
    echo "PASS: Runner module importable."
else
    echo "FAIL: Cannot import desk_pro_runner."
    exit 1
fi

# 4. Shared Directory
if [ -d "/shared" ]; then
    echo "PASS: /shared directory exists."
else
    echo "WARN: /shared directory not found (normal if not on admin-trading)."
fi

# 5. Status Execution
echo "Running status check..."
OUTPUT=$(bash "$CMD" status 2>&1)
if [[ $? -eq 0 ]]; then
    if echo "$OUTPUT" | grep -q "runner_status"; then
        echo "PASS: Status check successful."
    else
        echo "FAIL: Status output invalid."
        echo "$OUTPUT"
        exit 1
    fi
else
    echo "FAIL: Status execution failed."
    exit 1
fi

# 6. Logs Directory
if [ -d "$ROOT_DIR/data/logs/desk_pro" ]; then
    echo "PASS: Logs directory exists."
else
    echo "WARN: Logs directory missing (will be created on first logged run)."
fi

echo "Admin Sanity Check Passed."
