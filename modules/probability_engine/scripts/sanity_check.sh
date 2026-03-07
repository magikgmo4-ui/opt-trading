#!/usr/bin/env bash
set -euo pipefail
MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROOT_DIR="$(cd "$MODULE_DIR/../.." && pwd)"
APP_DIR="$MODULE_DIR/app"
CONFIG_DIR="$MODULE_DIR/config"
SCRIPTS_DIR="$MODULE_DIR/scripts"

echo "Checking Probability Engine Module..."

# 1. Structure Check
[ -d "$APP_DIR" ] || { echo "FAIL: App dir missing"; exit 1; }
[ -f "$APP_DIR/probability_engine.py" ] || { echo "FAIL: Main script missing"; exit 1; }
# Check for template or actual file
if [ ! -f "$CONFIG_DIR/example.env.sample" ] && [ ! -f "$CONFIG_DIR/example.env" ]; then
    echo "FAIL: Config template missing (example.env.sample or example.env)"; exit 1;
fi
[ -f "$CONFIG_DIR/example_input.json" ] || { echo "FAIL: Example input missing"; exit 1; }
[ -f "$SCRIPTS_DIR/cmd.sh" ] || { echo "FAIL: cmd.sh missing"; exit 1; }

# 2. Python Check
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 3. Execution Check (Sample)
echo "Running sample scoring..."
cd "$ROOT_DIR" || exit 1
OUTPUT=$(python3 -m modules.probability_engine.app.probability_engine sample 2>&1)
if [[ $? -eq 0 ]]; then
    # Check for expected keys in JSON output
    if echo "$OUTPUT" | grep -q "probability_long"; then
        echo "PASS: Module executed correctly."
        echo "$OUTPUT" | head -n 10
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
