#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
CONFIG_DIR="$MODULE_DIR/config"
SCRIPTS_DIR="$MODULE_DIR/scripts"

echo "Checking Perf Engine Module..."

# 1. Structure Check
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/perf_engine.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_positions.json" ] || { echo "FAIL: Sample positions missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_execution.json" ] || { echo "FAIL: Sample execution missing"; exit 1; }
[ -f "$SCRIPTS_DIR/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }

# 2. Python Check
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Execution Check (Sample Track)
echo "Running sample track..."
cd "$ROOT_DIR" || exit 1
OUTPUT=$(python3 -m modules.perf_engine.app.perf_engine sample 2>&1)
if [[ $? -eq 0 ]]; then
    if echo "$OUTPUT" | grep -q "perf_status"; then
        echo "PASS: Perf Engine processed sample data."
        echo "$OUTPUT" | head -n 15
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

# 4. Explain Check (No Args)
echo "Testing explain (defaults)..."
python3 -m modules.perf_engine.app.perf_engine explain >/dev/null
if [[ $? -eq 0 ]]; then
    echo "PASS: Explain works without args."
fi

echo "Sanity Check Passed."
