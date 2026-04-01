#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CMD="$BASE/scripts/cmd.sh"
MODULES_ROOT="${OPENCLAW_MODULE_TARGET_ROOT:-/opt/trading}/modules"
REGISTRY="$MODULES_ROOT/install_module_openclaw/app/modules_registry.json"

choose_numbered_menu() {
  echo
  echo "--- Menus OpenClaw ---"
  "$CMD" list-menus-numbered
  echo "0) retour"
  read -r -p "numéro > " n

  case "$n" in
    0|"") return 0 ;;
  esac

  if ! [[ "$n" =~ ^[0-9]+$ ]]; then
    echo "Choix invalide"
    return 0
  fi

  mod_id="$(
    python3 - <<PY 2>/dev/null
import json, pathlib, sys
data = json.loads(pathlib.Path(r"$REGISTRY").read_text())
mods = [x["id"] for x in data.get("modules", [])]
idx = int(r"$n")
if idx < 1 or idx > len(mods):
    sys.exit(1)
print(mods[idx-1])
PY
  )" || {
    echo "Numéro invalide"
    return 0
  }

  exec "$CMD" open-menu "$mod_id"
}

useful_submenu() {
  while true; do
    echo
    echo "--- Commandes utiles OpenClaw ---"
    echo "1) validate"
    echo "2) health"
    echo "3) probe"
    echo "4) audit"
    echo "5) agents"
    echo "6) doctor"
    echo "7) logs"
    echo "8) status"
    echo "0) retour"
    read -r -p "utile > " u
    case "$u" in
      1) "$CMD" useful validate || true ;;
      2) "$CMD" useful health || true ;;
      3) "$CMD" useful probe || true ;;
      4) "$CMD" useful audit || true ;;
      5) "$CMD" useful agents || true ;;
      6) "$CMD" useful doctor || true ;;
      7) "$CMD" useful logs || true ;;
      8) "$CMD" useful status || true ;;
      0) return 0 ;;
      *) echo "Choix invalide" ;;
    esac
  done
}

while true; do
  echo
  echo "=== menu_openclaw ==="
  echo "1) sanity"
  echo "2) status hub"
  echo "3) liste numérotée des menus OpenClaw"
  echo "4) ouvrir menu install_module_openclaw"
  echo "5) ouvrir menu openclaw_config_modulaire"
  echo "6) sous-menu commandes utiles"
  echo "7) ouvrir un autre menu OpenClaw par module_id"
  echo "0) quit"
  read -r -p "> " choice
  case "$choice" in
    1) "$CMD" sanity ;;
    2) "$CMD" status ;;
    3) choose_numbered_menu ;;
    4) "$CMD" open-menu install_module_openclaw ;;
    5) "$CMD" open-menu openclaw_config_modulaire ;;
    6) useful_submenu ;;
    7)
      read -r -p "module_id > " mid
      "$CMD" open-menu "$mid"
      ;;
    0) exit 0 ;;
    *) echo "Choix invalide" ;;
  esac
done
