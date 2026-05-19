#!/usr/bin/env bash
set -euo pipefail
# Desk Pro DB Layer - Shared Info
# Reads and displays information from the shared drive

SHARED_DIR="/shared/desk_pro/latest"

echo "=== Desk Pro DB Layer - Shared Info ==="
echo "Checking shared directory: $SHARED_DIR"

if [ ! -d "$SHARED_DIR" ]; then
    echo "WARN: Shared directory not found or not mounted."
    echo "      Ensure /shared is mounted from admin-trading."
    exit 0
fi

echo "----------------------------------------"
echo "Artifacts found:"
ls -lh "$SHARED_DIR" | grep -v "total" | awk '{print "  " $9 " (" $5 ")"}'

echo "----------------------------------------"
if [ -f "$SHARED_DIR/run_summary.json" ]; then
    echo "Latest Run Summary:"
    grep -E "run_id|run_timestamp|modules_ok|modules_failed|summary" "$SHARED_DIR/run_summary.json" | sed 's/^/  /'
else
    echo "WARN: run_summary.json missing."
fi

echo "----------------------------------------"
if [ -f "$SHARED_DIR/portfolio_engine.json" ]; then
    echo "Portfolio State:"
    grep -E "portfolio_state|exposure_profile|total_max_risk_pct|summary" "$SHARED_DIR/portfolio_engine.json" | sed 's/^/  /'
else
    echo "NOTE: portfolio_engine.json missing."
fi

echo "========================================"
