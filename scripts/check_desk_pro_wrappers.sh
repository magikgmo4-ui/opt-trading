#!/usr/bin/env bash
set -euo pipefail

# Desk Pro - Wrapper Sanity Check (Robust V2)
# Verifies presence, executability, and basic runtime viability of wrappers.

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
echo "Target: $BIN_DIR"

missing_count=0
invalid_count=0
total_checked=0

check_wrapper() {
    local wrapper_name=$1
    local expected_target_module=$2
    total_checked=$((total_checked + 1))
    
    local path="$BIN_DIR/$wrapper_name"
    
    if [ ! -f "$path" ]; then
        echo "  [MISSING] $wrapper_name"
        missing_count=$((missing_count + 1))
        return
    fi
    
    if [ ! -x "$path" ]; then
        echo "  [NOT EXEC] $wrapper_name"
        invalid_count=$((invalid_count + 1))
        return
    fi
    
    # Content Check: Must contain 'cd' to module dir
    if ! grep -q "cd \"/opt/trading/modules/$expected_target_module\"" "$path"; then
        echo "  [INVALID CONTENT] $wrapper_name (Does not cd to $expected_target_module)"
        invalid_count=$((invalid_count + 1))
        return
    fi
    
    echo "  [OK] $wrapper_name"
}

for mod in "${MODULES[@]}"; do
    echo "Checking module: $mod"
    check_wrapper "menu-$mod" "$mod"
    check_wrapper "cmd-$mod" "$mod"
    check_wrapper "sanity-$mod" "$mod"
    echo ""
done

echo "=== Summary ==="
echo "Total checked: $total_checked"
echo "Missing: $missing_count"
echo "Invalid Content: $invalid_count"

if [ $missing_count -eq 0 ] && [ $invalid_count -eq 0 ]; then
    echo "SUCCESS: All wrappers appear correct and robust."
    exit 0
else
    echo "FAILURE: Some wrappers are missing or invalid."
    exit 1
fi
