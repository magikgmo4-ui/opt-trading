#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

die(){ echo "ERR: $*" >&2; exit 1; }

ensure_git_root() {
  git -C "$ROOT_DIR" rev-parse --git-dir >/dev/null 2>&1 || die "not a git repo: $ROOT_DIR"
}

append_unique_lines() {
  local src="$1"
  local dst="$2"
  [ -f "$src" ] || die "missing file: $src"
  touch "$dst"
  while IFS= read -r line; do
    [ -n "${line}" ] || continue
    grep -qxF "$line" "$dst" 2>/dev/null || echo "$line" >> "$dst"
  done < "$src"
}
