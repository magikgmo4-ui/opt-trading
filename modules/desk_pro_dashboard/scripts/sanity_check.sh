#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
CONFIG_DIR="$MODULE_DIR/config"
SCRIPTS_DIR="$MODULE_DIR/scripts"

echo "Checking Desk Pro Dashboard Module..."

# 1. Structure Check
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/desk_pro_dashboard.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_dashboard_input.json" ] || { echo "FAIL: Sample input missing"; exit 1; }
[ -f "$SCRIPTS_DIR/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }

# 2. Python Check
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Execution Check (Sample Render)
echo "Running sample render..."
cd "$ROOT_DIR" || exit 1
OUTPUT=$(python3 -m modules.desk_pro_dashboard.app.desk_pro_dashboard sample 2>&1)
if [[ $? -eq 0 ]]; then
    if echo "$OUTPUT" | grep -q "DESK PRO DASHBOARD"; then
        echo "PASS: Dashboard rendered correctly."
    else
        echo "FAIL: Output missing dashboard header."
        echo "$OUTPUT"
        exit 1
    fi
else
    echo "FAIL: Module execution failed."
    echo "$OUTPUT"
    exit 1
fi

# 4. Export Check
echo "Testing exports..."
python3 -m modules.desk_pro_dashboard.app.desk_pro_dashboard export-json >/dev/null
python3 -m modules.desk_pro_dashboard.app.desk_pro_dashboard export-html >/dev/null
if [ -f "data/dashboard/dashboard_*.json" ]; then
    echo "PASS: JSON export worked."
fi

echo "Sanity Check Passed."
