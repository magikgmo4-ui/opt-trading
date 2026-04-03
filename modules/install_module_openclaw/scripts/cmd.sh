#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REG="$BASE/app/modules_registry.json"
BUNDLE_ROOT="${OPENCLAW_MODULE_SOURCE_ROOT:-$(cd "$BASE/../.." && pwd)}"
TARGET_ROOT="${OPENCLAW_MODULE_TARGET_ROOT:-/opt/trading}"

python_list() {
python3 - <<PY
import json, pathlib
data = json.loads(pathlib.Path(r"$REG").read_text())
for item in data["modules"]:
    print(f'{item["id"]}\t{item["description"]}\t{item["source_rel"]}\t{item["target_rel"]}')
PY
}

get_field() {
  local module_id="$1"
  local field="$2"
  python3 - <<PY
import json, pathlib, sys
data = json.loads(pathlib.Path(r"$REG").read_text())
for item in data["modules"]:
    if item["id"] == r"$module_id":
        print(item[r"$field"])
        sys.exit(0)
sys.exit(1)
PY
}

help_msg() {
  cat <<'EOF'
Usage:
  cmd.sh sanity
  cmd.sh list
  cmd.sh status
  cmd.sh install <module_id>
  cmd.sh paths
EOF
}

case "${1:-help}" in
  sanity)
    "$BASE/scripts/sanity.sh"
    ;;
  list)
    printf '%s\n' "ID | DESCRIPTION | SOURCE_REL | TARGET_REL"
    python_list | while IFS=$'\t' read -r a b c d; do
      printf '%s | %s | %s | %s\n' "$a" "$b" "$c" "$d"
    done
    ;;
  status)
    echo "BUNDLE_ROOT=$BUNDLE_ROOT"
    echo "TARGET_ROOT=$TARGET_ROOT"
    echo
    "$BASE/scripts/cmd.sh" list
    ;;
  install)
    mod="${2:-}"
    [ -n "$mod" ] || { echo "FAIL: module_id requis" >&2; exit 1; }
    src_rel="$(get_field "$mod" source_rel)"
    dst_rel="$(get_field "$mod" target_rel)"
    src="$BUNDLE_ROOT/$src_rel"
    dst="$TARGET_ROOT/$dst_rel"
    [ -d "$src" ] || { echo "FAIL: source introuvable: $src" >&2; exit 1; }
    echo "Installation de $mod"
    echo "Source: $src"
    echo "Cible : $dst"
    sudo mkdir -p "$(dirname "$dst")"
    sudo rm -rf "$dst"
    sudo cp -r "$src" "$dst"
    sudo chown -R "$USER":"$USER" "$dst" || true
    echo "PASS: module copié"
    if [ -f "$dst/scripts/install_shortcuts.sh" ]; then
      echo "Shortcuts disponibles:"
      echo "  bash \"$dst/scripts/install_shortcuts.sh\""
    fi
    ;;
  paths)
    echo "BASE=$BASE"
    echo "REG=$REG"
    echo "BUNDLE_ROOT=$BUNDLE_ROOT"
    echo "TARGET_ROOT=$TARGET_ROOT"
    ;;
  *)
    help_msg
    exit 1
    ;;
esac
