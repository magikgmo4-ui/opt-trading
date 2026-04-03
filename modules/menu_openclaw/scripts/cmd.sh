#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODULES_ROOT="${OPENCLAW_MODULE_TARGET_ROOT:-/opt/trading}/modules"
REGISTRY="$MODULES_ROOT/install_module_openclaw/app/modules_registry.json"
USEFUL="$BASE/scripts/commandes_utiles.sh"

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity
  cmd.sh status
  cmd.sh list-menus
  cmd.sh list-menus-numbered
  cmd.sh open-menu <module_id>
  cmd.sh useful <action>
  cmd.sh paths
EOF
}

registry_ids() {
python3 - <<PY
import json, pathlib
data = json.loads(pathlib.Path(r"$REGISTRY").read_text())
for item in data.get("modules", []):
    print(item["id"])
PY
}

list_menus() {
  registry_ids | while read -r mod_id; do
    [ -n "$mod_id" ] || continue
    local shortcut="/usr/local/bin/menu-$mod_id"
    local module_menu="$MODULES_ROOT/$mod_id/scripts/menu.sh"
    if [ -x "$shortcut" ]; then
      printf '%s | %s\n' "$mod_id" "$shortcut"
    elif [ -x "$module_menu" ]; then
      printf '%s | %s\n' "$mod_id" "$module_menu"
    fi
  done
}

list_menus_numbered() {
  local i=1
  registry_ids | while read -r mod_id; do
    [ -n "$mod_id" ] || continue
    printf '%s) %s\n' "$i" "$mod_id"
    i=$((i+1))
  done
}

is_allowed_module() {
  local wanted="$1"
  registry_ids | grep -Fxq "$wanted"
}

open_menu() {
  local mod_id="$1"
  local shortcut="/usr/local/bin/menu-$mod_id"
  local module_menu="$MODULES_ROOT/$mod_id/scripts/menu.sh"

  is_allowed_module "$mod_id" || {
    echo "FAIL: module non déclaré dans la registry OpenClaw: $mod_id" >&2
    exit 1
  }

  if [ -x "$shortcut" ]; then
    exec "$shortcut"
  elif [ -x "$module_menu" ]; then
    exec "$module_menu"
  else
    echo "FAIL: menu introuvable pour $mod_id" >&2
    exit 1
  fi
}

case "${1:-help}" in
  sanity)
    "$BASE/scripts/sanity.sh"
    ;;
  status)
    echo "Module: menu_openclaw"
    echo "Modules root: $MODULES_ROOT"
    echo "Registry: $REGISTRY"
    echo
    list_menus
    ;;
  list-menus)
    list_menus
    ;;
  list-menus-numbered)
    list_menus_numbered
    ;;
  open-menu)
    [ -n "${2:-}" ] || { echo "FAIL: module_id requis" >&2; exit 1; }
    open_menu "$2"
    ;;
  useful)
    shift || true
    "$USEFUL" "${1:-list}"
    ;;
  paths)
    printf '%s\n' \
      "BASE=$BASE" \
      "MODULES_ROOT=$MODULES_ROOT" \
      "REGISTRY=$REGISTRY" \
      "USEFUL=$USEFUL"
    ;;
  *)
    help_msg
    exit 1
    ;;
esac
