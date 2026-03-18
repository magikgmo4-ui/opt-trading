#!/usr/bin/env bash
set -euo pipefail

ROOT="/opt/trading/student"
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="/home/student/tmp/student_shortcut_backup_${TS}"

mkdir -p "$BACKUP_DIR"

for name in menu-student cmd-student sanity-student; do
  dest="/usr/local/bin/$name"
  if [[ -L "$dest" ]]; then
    ls -l "$dest" > "$BACKUP_DIR/${name}.before.txt"
  elif [[ -e "$dest" ]]; then
    ls -l "$dest" > "$BACKUP_DIR/${name}.before.txt"
  else
    printf 'missing\n' > "$BACKUP_DIR/${name}.before.txt"
  fi
done

sudo ln -sfn "$ROOT/scripts/student_menu.sh" /usr/local/bin/menu-student
sudo ln -sfn "$ROOT/scripts/student_cmd.sh" /usr/local/bin/cmd-student
sudo ln -sfn "$ROOT/scripts/student_sanity_check.sh" /usr/local/bin/sanity-student

ls -l /usr/local/bin/menu-student > "$BACKUP_DIR/menu-student.after.txt"
ls -l /usr/local/bin/cmd-student > "$BACKUP_DIR/cmd-student.after.txt"
ls -l /usr/local/bin/sanity-student > "$BACKUP_DIR/sanity-student.after.txt"

echo "OK: repaired student shortcuts"
echo "Backup: $BACKUP_DIR"
