#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Install Admin Trading
# Aligns admin machine setup with canonical Desk Pro entrypoints

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Desk Pro Admin Trading Installer ==="
echo "Repo Root: $ROOT_DIR"

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "FAIL: Python 3 not found."
    exit 1
fi

# 2. Check Permissions (Simulated check)
if [ ! -w "/usr/local/bin" ] && [ "$(id -u)" != "0" ]; then
    echo "Note: Cannot write to /usr/local/bin without sudo."
    echo "You can run scripts directly from $SCRIPT_DIR"
    echo "To install global wrappers, run: sudo $0"
    exit 0
fi

# 3. Remove legacy global aliases and defer to canonical entrypoints
if [ -w "/usr/local/bin" ]; then
    echo "Removing non-canonical Desk Pro global aliases..."

    rm -f /usr/local/bin/desk-pro
    rm -f /usr/local/bin/menu-desk-pro
    rm -f /usr/local/bin/sanity-desk-pro
    rm -f /usr/local/bin/desk-pro-copy-latest
    rm -f /usr/local/bin/desk-pro-run-logged
    rm -f /usr/local/bin/desk-pro-tail-log
    rm -f /usr/local/bin/desk-pro-last-run
    rm -f /usr/local/bin/desk-pro-session-journal
    rm -f /usr/local/bin/desk-pro-summary
    rm -f /usr/local/bin/desk-pro-checklist

    echo "No Desk Pro admin global alias installed by this script."
    echo "Use canonical entrypoints instead: menu-ops_menu_hub, cmd-desk_pro_runner, scripts/admin_trading/desk_pro_cmd.sh"
fi

echo "Installation Complete."
