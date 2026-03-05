#!/usr/bin/env bash
set -euo pipefail

HOST="$(hostname)"
ROOT="/opt/trading"
MODULES_DIR="$ROOT/modules"
BIN_DIR="/usr/local/bin"

role() {
  case "$HOST" in
    admin-trading*) echo "admin-trading" ;;
    student*) echo "student" ;;
    db-layer*) echo "db-layer" ;;
    *) echo "unknown" ;;
  esac
}

hint_for() {
  local mod="$1"
  case "$mod" in
    bot_vision_step2|desk_bridge|desk_snapshot_ingest|desk_analyze|desk_retention|desk_state|desk_capture_inputs)
      echo "admin-trading (desk pipeline)" ;;
    deepseek_hub|student)
      echo "student (LLM hub)" ;;
    reseau_ssh)
      echo "admin-trading + student + db-layer" ;;
    workflow_ai)
      echo "admin-trading (repo workflow) + cursor-ai (Windows side)" ;;
    *)
      echo "any (check README)" ;;
  esac
}

list_modules() {
  echo "=== modules detected (scripts present) ==="
  echo "host=$HOST role=$(role)"
  echo
  [ -d "$MODULES_DIR" ] || { echo "ERROR: $MODULES_DIR not found"; return 2; }
  local found=0
  for d in "$MODULES_DIR"/*; do
    [ -d "$d" ] || continue
    local mod; mod="$(basename "$d")"
    if [ -f "$d/scripts/menu.sh" ] || [ -f "$d/scripts/cmd.sh" ] || [ -f "$d/scripts/sanity_check.sh" ]; then
      found=$((found+1))
      printf "%-28s  hint=%s\n" "$mod" "$(hint_for "$mod")"
    fi
  done
  echo
  echo "count=$found"
}

list_shortcuts() {
  echo "=== shortcuts in $BIN_DIR ==="
  echo "host=$HOST role=$(role)"
  echo
  ls -1 "$BIN_DIR"/menu-* "$BIN_DIR"/cmd-* "$BIN_DIR"/sanity-* 2>/dev/null | sed 's#^#/usr/local/bin/#' || true
}

bootstrap_shortcuts() {
  echo "=== bootstrap shortcuts ==="
  echo "Creates symlinks for modules with standard scripts/ (requires sudo)."
  [ -d "$MODULES_DIR" ] || { echo "ERROR: $MODULES_DIR not found"; return 2; }
  local made=0
  for d in "$MODULES_DIR"/*; do
    [ -d "$d" ] || continue
    local mod; mod="$(basename "$d")"
    local m="$d/scripts/menu.sh"
    local c="$d/scripts/cmd.sh"
    local s="$d/scripts/sanity_check.sh"
    if [ -f "$m" ]; then sudo ln -sf "$m" "$BIN_DIR/menu-$mod"; made=$((made+1)); fi
    if [ -f "$c" ]; then sudo ln -sf "$c" "$BIN_DIR/cmd-$mod"; made=$((made+1)); fi
    if [ -f "$s" ]; then sudo ln -sf "$s" "$BIN_DIR/sanity-$mod"; made=$((made+1)); fi
  done
  echo "OK: updated symlinks (count=$made)"
}

run_menu() {
  local mod="$1"
  local p="$MODULES_DIR/$mod/scripts/menu.sh"
  [ -f "$p" ] || { echo "No menu for module: $mod"; return 2; }
  bash "$p"
}

case "${1:-}" in
  list) list_modules ;;
  shortcuts) list_shortcuts ;;
  bootstrap_shortcuts) bootstrap_shortcuts ;;
  run) run_menu "${2:-}" ;;
  *)
    cat <<'EOF'
Usage: ops_menu_hub.sh <command>

Commands:
  list
  shortcuts
  bootstrap_shortcuts
  run <module>
EOF
    exit 1
    ;;
esac
