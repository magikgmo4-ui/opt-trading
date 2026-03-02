#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ME_USER="$(id -un)"
ME_GROUP="$(id -gn)"

die(){ echo "ERR: $*" >&2; exit 1; }

need() { command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"; }

ensure_git_root() {
  git -C "$ROOT_DIR" rev-parse --git-dir >/dev/null 2>&1 || die "not a git repo: $ROOT_DIR"
}

# Print a header with current context
ctx() {
  echo "[root] $ROOT_DIR"
  echo "[user] $ME_USER:$ME_GROUP"
}

# Exclude .git and local-only folders; keep it conservative.
find_targets() {
  find "$ROOT_DIR" \
    -path "$ROOT_DIR/.git" -prune -o \
    -path "$ROOT_DIR/_student_archive" -prune -o \
    -path "$ROOT_DIR/_worktrees" -prune -o \
    -path "$ROOT_DIR/_inbox" -prune -o \
    -path "$ROOT_DIR/_hold_untracked_before_merge_" -prune -o \
    -print
}
