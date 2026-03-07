#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student Install
# Installs DeepSeek wrappers for the student machine

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== DeepSeek Student Installer ==="
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
    
    ln -sf "$SCRIPT_DIR/deepseek_student_cmd.sh" /usr/local/bin/deepseek-student
    ln -sf "$SCRIPT_DIR/deepseek_student_menu.sh" /usr/local/bin/menu-deepseek-student
    ln -sf "$SCRIPT_DIR/deepseek_student_sanity_check.sh" /usr/local/bin/sanity-deepseek-student
    
    # Remove old/confusing wrappers
    rm -f /usr/local/bin/deepseek-student-run-logged
    rm -f /usr/local/bin/deepseek-student-tail-log
    
    echo "Installed: deepseek-student, menu-deepseek-student, sanity-deepseek-student"
fi

# 4. Ensure Permissions
chmod +x "$SCRIPT_DIR"/*.sh

echo "Installation Complete."
