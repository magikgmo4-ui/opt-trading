#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Incident Checklist
# A quick diagnostic tool for incident recovery

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Desk Pro Incident Recovery Checklist ==="
echo ""

# 1. System Health
echo "[ ] Sanity Check"
if "$SCRIPT_DIR/desk_pro_sanity_check.sh" >/dev/null 2>&1; then
    echo "    PASS: System structure OK"
else
    echo "    FAIL: System structure issues found. Run 'sanity-desk-pro' for details."
fi

# 2. Last Run Status
echo "[ ] Last Run"
if [ -f "$ROOT_DIR/data/logs/desk_pro/latest_status.txt" ]; then
    STATUS=$(cat "$ROOT_DIR/data/logs/desk_pro/latest_status.txt")
    if [ "$STATUS" == "SUCCESS" ]; then
        echo "    PASS: Last run SUCCESS"
    else
        echo "    FAIL: Last run FAILED ($STATUS). Check logs."
    fi
else
    echo "    WARN: No run status found."
fi

# 3. Wrappers
echo "[ ] Global Wrappers"
if command -v desk-pro >/dev/null 2>&1; then
    echo "    PASS: 'desk-pro' command found"
else
    echo "    FAIL: 'desk-pro' command missing. Reinstall via desk_pro_install_admin_trading.sh"
fi

# 4. Shared Access
echo "[ ] Shared Access"
if [ -d "/shared" ]; then
    if [ -w "/shared" ]; then
        echo "    PASS: /shared is writable"
    else
        echo "    WARN: /shared exists but may be read-only"
    fi
else
    echo "    WARN: /shared directory not found"
fi

echo ""
echo "For detailed recovery steps, see: docs/admin_trading_desk_pro_incident_recovery.md"
echo "============================================"
