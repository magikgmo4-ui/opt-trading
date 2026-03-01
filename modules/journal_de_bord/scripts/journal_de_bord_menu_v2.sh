\
#!/usr/bin/env bash
# journal_de_bord_menu_v2.sh
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while true; do
  echo "=== Journal_De_Bord Menu (v2) ==="
  echo "1) Sanity"
  echo "2) Canon FULL -> push student (1-click)"
  echo "3) Show latest canon_admin local"
  echo "q) Quit"
  echo -n "> "
  read -r choice || true
  case "$choice" in
    1) "$DIR/sanity_check_journal_de_bord.sh" ;;
    2) "$DIR/canon_full_push_student.sh" ;;
    3) ls -1t /opt/trading/_student_archive/journals/canon_admin/JOURNAL_CANON_FULL_*.md 2>/dev/null | head -n 5 || true ;;
    q|Q) exit 0 ;;
    *) echo "?" ;;
  esac
  echo
done
