#!/usr/bin/env bash
set -euo pipefail

# Desk Pro - Wrapper Sanity Check
# Verifies that all expected wrappers are installed and executable

BIN_DIR="/usr/local/bin"
MODULES=(
    "derivatives_collector"
    "derivatives_analyzer"
    "probability_engine"
    "decision_engine"
    "risk_engine"
    "execution_engine"
    "position_engine"
    "portfolio_engine"
    "journal_engine"
    "market_scanner"
    "opportunity_ranker"
    "liquidation_analyzer"
    "desk_pro_dashboard"
    "desk_pro_orchestrator"
    "desk_pro_runner"
    "perf_engine"
)

echo "=== Desk Pro Wrapper Sanity Check ==="

missing_count=0
total_checked=0

check_wrapper() {
    local wrapper_name=$1
    total_checked=$((total_checked + 1))
    
    if [ -x "$BIN_DIR/$wrapper_name" ]; then
        echo "  [OK] $wrapper_name"
    else
        echo "  [MISSING/NO EXEC] $wrapper_name"
        missing_count=$((missing_count + 1))
    fi
}

for mod in "${MODULES[@]}"; do
    echo "Checking module: $mod"
    check_wrapper "menu-$mod"
    check_wrapper "cmd-$mod"
    check_wrapper "sanity-$mod"
    echo ""
done

echo "=== Summary ==="
echo "Total checked: $total_checked"
echo "Missing/Invalid: $missing_count"

if [ $missing_count -eq 0 ]; then
    echo "SUCCESS: All wrappers appear correct."
    exit 0
else
    echo "FAILURE: Some wrappers are missing."
    exit 1
fi
