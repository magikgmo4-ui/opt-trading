\
#!/usr/bin/env bash
set -euo pipefail
BASE="/opt/trading"
echo "=== Install Student Shortcuts ==="
sudo ln -sf "$BASE/scripts/student_menu.sh" /usr/local/bin/menu-student
sudo ln -sf "$BASE/scripts/student_cmd.sh" /usr/local/bin/cmd-student
sudo ln -sf "$BASE/scripts/student_sanity_check.sh" /usr/local/bin/sanity-student
sudo ln -sf "$BASE/scripts/runlog" /usr/local/bin/runlog
echo "OK: /usr/local/bin/menu-student, cmd-student, sanity-student, runlog"
