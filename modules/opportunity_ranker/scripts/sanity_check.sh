#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
CONFIG_DIR="$MODULE_DIR/config"
SCRIPTS_DIR="$MODULE_DIR/scripts"

echo "Checking Opportunity Ranker Module..."

# 1. Structure Check
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/opportunity_ranker.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_scanner.json" ] || { echo "FAIL: Sample scanner missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_liquidations.json" ] || { echo "FAIL: Sample liq missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_probability.json" ] || { echo "FAIL: Sample prob missing"; exit 1; }
[ -f "$SCRIPTS_DIR/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }

# 2. Python Check
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Execution Check (Sample Rank)
echo "Running sample ranking..."
cd "$ROOT_DIR" || exit 1
# Assuming cmd.sh sample works without args by calling python -m ...
OUTPUT=$(python3 -m modules.opportunity_ranker.app.opportunity_ranker sample 2>&1)
if [[ $? -eq 0 ]]; then
    if echo "$OUTPUT" | grep -q "opportunity_score"; then
        echo "PASS: Ranker processed sample data."
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

echo "Sanity Check Passed."
