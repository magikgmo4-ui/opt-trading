#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
CONFIG_DIR="$MODULE_DIR/config"
SCRIPTS_DIR="$MODULE_DIR/scripts"

echo "Checking Market Scanner Module..."

# 1. Structure Check
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/market_scanner.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_markets.json" ] || { echo "FAIL: Sample markets missing"; exit 1; }
[ -f "$SCRIPTS_DIR/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }

# 2. Python Check
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Execution Check (Sample Scan)
echo "Running sample scan..."
cd "$ROOT_DIR" || exit 1
OUTPUT=$(python3 -m modules.market_scanner.app.market_scanner sample 2>&1)
if [[ $? -eq 0 ]]; then
    if echo "$OUTPUT" | grep -q "BTCUSDT"; then
        echo "PASS: Scanner processed sample data."
        echo "$OUTPUT" | head -n 10
    else
        echo "FAIL: Output missing expected symbol."
        echo "$OUTPUT"
        exit 1
    fi
else
    echo "FAIL: Module execution failed."
    echo "$OUTPUT"
    exit 1
fi

echo "Sanity Check Passed."
