#!/usr/bin/env bash
set -euo pipefail

# Derivatives Analyzer - Sanity Check

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="$SCRIPT_DIR/cmd.sh"

echo "=== Sanity Check: derivatives_analyzer ==="

# 1. Check Files
echo -n "Checking structure... "
if [ -f "$SCRIPT_DIR/../app/derivatives_analyzer.py" ] && [ -f "$SCRIPT_DIR/../config/sample_input.json" ]; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

# 2. Check Python Execution (Explain)
echo -n "Checking Python execution... "
if bash "$CMD" explain | grep -q "Derivatives Analyzer Logic"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

# 3. Check Analysis
echo -n "Checking Analysis logic... "
if bash "$CMD" analyze | grep -q "squeeze_risk"; then
    echo "OK"
else
    echo "FAIL"
    exit 1
fi

echo "=== All Checks Passed ==="
