#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-/opt/trading}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8010}"

cd "$REPO" 2>/dev/null || true

echo "=============================="
echo "         DESK PRO MENU        "
echo "=============================="
echo "Repo: $REPO"
echo "URL : $BASE_URL/desk/ui"
echo
echo "1) Sanity check"
echo "2) Show UI URL"
echo "3) Health (GET /desk/health)"
echo "4) Tail logs (last 200 lines)"
echo "5) Install global shortcuts (sudo)"
echo "q) Quit"
echo
read -rp "Choice: " c

case "$c" in
  1) bash "$REPO/scripts/sanity_desk_pro.sh" ;;
  2) echo "$BASE_URL/desk/ui" ;;
  3) cmd-desk_pro health || true ;;
  4) cmd-desk_pro logs 200 || true ;;
  5)
     if [[ -f "$REPO/scripts/install_desk_pro_shortcuts.sh" ]]; then
       sudo bash "$REPO/scripts/install_desk_pro_shortcuts.sh"
     else
       echo "Missing $REPO/scripts/install_desk_pro_shortcuts.sh"
       exit 2
     fi
     ;;
  q|Q) exit 0 ;;
  *) echo "Invalid choice" ;;
esac
