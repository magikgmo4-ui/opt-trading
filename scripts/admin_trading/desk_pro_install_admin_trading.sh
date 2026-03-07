#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Install Admin Trading
# Sets up convenience wrappers on the admin machine

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

# 3. Install Wrappers (if root/sudo)
if [ -w "/usr/local/bin" ]; then
    echo "Installing global wrappers..."
    
    ln -sf "$SCRIPT_DIR/desk_pro_cmd.sh" /usr/local/bin/desk-pro
    ln -sf "$SCRIPT_DIR/desk_pro_menu.sh" /usr/local/bin/menu-desk-pro
    ln -sf "$SCRIPT_DIR/desk_pro_sanity_check.sh" /usr/local/bin/sanity-desk-pro
    ln -sf "$SCRIPT_DIR/desk_pro_copy_latest_to_shared.sh" /usr/local/bin/desk-pro-copy-latest
    ln -sf "$SCRIPT_DIR/desk_pro_run_logged.sh" /usr/local/bin/desk-pro-run-logged
    ln -sf "$SCRIPT_DIR/desk_pro_tail_latest_log.sh" /usr/local/bin/desk-pro-tail-log
    ln -sf "$SCRIPT_DIR/desk_pro_last_run_info.sh" /usr/local/bin/desk-pro-last-run
    ln -sf "$SCRIPT_DIR/desk_pro_session_journal.sh" /usr/local/bin/desk-pro-session-journal
    
    echo "Installed: desk-pro, menu-desk-pro, sanity-desk-pro, desk-pro-copy-latest, desk-pro-run-logged, desk-pro-tail-log, desk-pro-last-run, desk-pro-session-journal"
fi

echo "Installation Complete."
