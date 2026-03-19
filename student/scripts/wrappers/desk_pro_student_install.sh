#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Student Install
# Installs wrappers for the student machine

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Desk Pro Student Installer ==="
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
    
    ln -sf "$SCRIPT_DIR/desk_pro_student_cmd.sh" /usr/local/bin/desk-pro-student
    ln -sf "$SCRIPT_DIR/desk_pro_student_menu.sh" /usr/local/bin/menu-desk-pro-student
    ln -sf "$SCRIPT_DIR/desk_pro_student_sanity_check.sh" /usr/local/bin/sanity-desk-pro-student
    ln -sf "$SCRIPT_DIR/desk_pro_student_latest_shared_info.sh" /usr/local/bin/desk-pro-student-shared-info
    
    echo "Installed: desk-pro-student, menu-desk-pro-student, sanity-desk-pro-student, desk-pro-student-shared-info"
fi

echo "Installation Complete."
