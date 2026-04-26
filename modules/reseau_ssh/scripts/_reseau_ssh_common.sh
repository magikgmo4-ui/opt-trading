#!/usr/bin/env bash
set -euo pipefail

reseau_ssh__realpath() {
  local src="$1"
  while [ -L "$src" ]; do
    local dir
    dir="$(cd "$(dirname "$src")" && pwd -P)"
    src="$(readlink "$src")"
    case "$src" in
      /*) ;;
      *) src="$dir/$src" ;;
    esac
  done
  printf '%s\n' "$(cd "$(dirname "$src")" && pwd -P)/$(basename "$src")"
}

RESEAU_SSH_ENTRY_REAL="$(reseau_ssh__realpath "${RESEAU_SSH_ENTRY_SOURCE:-${BASH_SOURCE[1]}}")"
RESEAU_SSH_TOP_DIR="$(cd "$(dirname "$RESEAU_SSH_ENTRY_REAL")" && pwd -P)"
RESEAU_SSH_MODULE_DIR="$(cd "$RESEAU_SSH_TOP_DIR/.." && pwd -P)"
RESEAU_SSH_MODULE_NAME="$(basename "$RESEAU_SSH_MODULE_DIR")"
RESEAU_SSH_CANONICAL_NAME="reseau_ssh"
RESEAU_SSH_REPO_ROOT="$(cd "$RESEAU_SSH_MODULE_DIR/../.." && pwd -P)"

RESEAU_SSH_ARCHIVE_RUNTIME_DIR="$RESEAU_SSH_REPO_ROOT/_archive/legacy_modules/reseau_ssh_runtime_rollback_only"
RESEAU_SSH_WIREGUARD_DIR="$RESEAU_SSH_MODULE_DIR/wireguard"
RESEAU_SSH_BASELINE_DIR="$RESEAU_SSH_MODULE_DIR/baseline"

RESEAU_SSH_TOP_CMD="$RESEAU_SSH_TOP_DIR/cmd.sh"
RESEAU_SSH_TOP_MENU="$RESEAU_SSH_TOP_DIR/menu.sh"
RESEAU_SSH_TOP_SANITY="$RESEAU_SSH_TOP_DIR/sanity_check.sh"

reseau_ssh_require_exec() {
  local target="$1"
  [ -x "$target" ] || {
    echo "FAIL: missing executable: $target" >&2
    exit 2
  }
}

reseau_ssh_readme() {
  local f
  for f in "$RESEAU_SSH_MODULE_DIR/README.md" "$RESEAU_SSH_MODULE_DIR/README.txt" "$RESEAU_SSH_MODULE_DIR/README"; do
    [ -f "$f" ] && {
      sed -n '1,260p' "$f"
      return 0
    }
  done
  echo "(no README found)"
}

reseau_ssh_print_info() {
  cat <<EOF
name=$RESEAU_SSH_CANONICAL_NAME
entry_real=$RESEAU_SSH_ENTRY_REAL
module_root=$RESEAU_SSH_MODULE_DIR
repo_root=$RESEAU_SSH_REPO_ROOT
wireguard_dir=$RESEAU_SSH_WIREGUARD_DIR
baseline_dir=$RESEAU_SSH_BASELINE_DIR
archive_runtime_dir=$RESEAU_SSH_ARCHIVE_RUNTIME_DIR
EOF
}
