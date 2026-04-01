#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
CONFIG_DIR="$MODULE_DIR/config"
SCRIPTS_DIR="$MODULE_DIR/scripts"

echo "Checking Decision Engine Module..."

# 1. Structure Check
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/decision_engine.py" ] || { echo "FAIL: Main script missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_ranker.json" ] || { echo "FAIL: Sample ranker missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_probability.json" ] || { echo "FAIL: Sample prob missing"; exit 1; }
[ -f "$CONFIG_DIR/sample_liquidations.json" ] || { echo "FAIL: Sample liq missing"; exit 1; }
[ -f "$SCRIPTS_DIR/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }

# 2. Python Check
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Execution Check (Sample Decision)
echo "Running sample decision..."
cd "$ROOT_DIR" || exit 1
OUTPUT=$(python3 -m modules.decision_engine.app.decision_engine sample 2>&1)
if [[ $? -eq 0 ]]; then
    if echo "$OUTPUT" | grep -q "GO_LONG"; then
        echo "PASS: Engine made a GO_LONG decision."
        echo "$OUTPUT" | head -n 15
    else
        echo "WARN: No GO_LONG in sample? Checking structure..."
        if echo "$OUTPUT" | grep -q "decision"; then
            echo "PASS: Output valid but different decision."
        else
            echo "FAIL: Output missing decision keys."
            echo "$OUTPUT"
            exit 1
        fi
    fi
else
    echo "FAIL: Module execution failed."
    echo "$OUTPUT"
    exit 1
fi

# 4. Explain Check (No Args)
echo "Testing explain (defaults)..."
python3 -m modules.decision_engine.app.decision_engine explain >/dev/null
if [[ $? -eq 0 ]]; then
    echo "PASS: Explain works without args."
fi

echo "Sanity Check Passed."
