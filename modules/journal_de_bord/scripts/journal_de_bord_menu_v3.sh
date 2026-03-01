\
#!/usr/bin/env bash
# journal_de_bord_menu_v3.sh
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while true; do
  echo "=== Journal_De_Bord Menu (v3) ==="
  echo "1) Sanity"
  echo "2) Canon FULL -> push student (1-click)"
  echo "3) Canon latest (top 10)"
  echo "q) Quit"
  echo -n "> "
  read -r choice || true
  case "$choice" in
    1) "$DIR/sanity_check_journal_de_bord.sh" ;;
    2) "$DIR/canon_full_push_student.sh" ;;
    3) "$DIR/canon_latest.sh" 10 ;;
    q|Q) exit 0 ;;
    *) echo "?" ;;
  esac
  echo
done
