#!/usr/bin/env bash
set -euo pipefail

echo "Legacy student migration checklist"
echo "1. Copy retained scripts into /opt/trading/student"
echo "2. Validate student_cmd.sh, student_menu.sh, student_sanity_check.sh"
echo "3. Repoint global shortcuts"
echo "4. Keep legacy wrappers until all callers are updated"
