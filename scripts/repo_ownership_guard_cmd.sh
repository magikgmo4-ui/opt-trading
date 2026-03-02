#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cmd="${1:-help}"; shift || true

source "$ROOT_DIR/modules/repo_ownership_guard/repo_ownership_guard_lib.sh"

usage() {
  cat <<'EOF'
repo_ownership_guard_cmd

Usage:
  bash scripts/repo_ownership_guard_cmd.sh sanity
  bash scripts/repo_ownership_guard_cmd.sh fix [--dry-run]

Notes:
- `fix` uses sudo and changes filesystem metadata (chown/chmod) inside the repo.
EOF
}

sanity() {
  ensure_git_root
  bash "$ROOT_DIR/modules/repo_ownership_guard/sanity_check.sh"
}

fix() {
  ensure_git_root
  local dry=0
  if [ "${1:-}" = "--dry-run" ]; then dry=1; fi

  echo "=== repo_ownership_guard fix ==="
  ctx
  echo

  # 1) Fix ownership for paths owned by root or other users.
  echo "[1] ownership fix (set to $ME_USER:$ME_GROUP) — excludes .git/_student_archive/_worktrees/_inbox/_hold"
  mapfile -t bad < <(find "$ROOT_DIR" \
    -path "$ROOT_DIR/.git" -prune -o \
    -path "$ROOT_DIR/_student_archive" -prune -o \
    -path "$ROOT_DIR/_worktrees" -prune -o \
    -path "$ROOT_DIR/_inbox" -prune -o \
    -path "$ROOT_DIR/_hold_untracked_before_merge_" -prune -o \
    \( ! -user "$ME_USER" -o ! -group "$ME_GROUP" \) -print)

  if [ "${#bad[@]}" -eq 0 ]; then
    echo "OK: no ownership changes needed"
  else
    echo "FOUND ${#bad[@]} paths needing chown"
    if [ "$dry" -eq 1 ]; then
      printf 'DRY-RUN: sudo chown %s:%s -- %q\n' "$ME_USER" "$ME_GROUP" "${bad[0]}"
      echo "DRY-RUN: (showing first item only; will apply to all)"
    else
      # Use xargs -0 to handle spaces safely
      printf '%s\0' "${bad[@]}" | sudo xargs -0 chown "$ME_USER:$ME_GROUP"
      echo "OK: chown applied"
    fi
  fi
  echo

  # 2) Ensure directories are writable by user (git operations).
  echo "[2] directory writability fix (add u+w where needed)"
  mapfile -t dirs < <(find "$ROOT_DIR" \
    -path "$ROOT_DIR/.git" -prune -o \
    -path "$ROOT_DIR/_student_archive" -prune -o \
    -path "$ROOT_DIR/_worktrees" -prune -o \
    -path "$ROOT_DIR/_inbox" -prune -o \
    -path "$ROOT_DIR/_hold_untracked_before_merge_" -prune -o \
    -type d ! -writable -print)

  if [ "${#dirs[@]}" -eq 0 ]; then
    echo "OK: all dirs writable"
  else
    echo "FOUND ${#dirs[@]} non-writable dirs"
    if [ "$dry" -eq 1 ]; then
      printf 'DRY-RUN: sudo chmod u+w -- %q\n' "${dirs[0]}"
      echo "DRY-RUN: (showing first item only; will apply to all)"
    else
      printf '%s\0' "${dirs[@]}" | sudo xargs -0 chmod u+w
      echo "OK: chmod u+w applied"
    fi
  fi
  echo

  echo "[3] re-run sanity"
  bash "$ROOT_DIR/modules/repo_ownership_guard/sanity_check.sh" || true
}

case "$cmd" in
  sanity) sanity ;;
  fix) fix "$@" ;;
  help|-h|--help) usage ;;
  *) usage; exit 2 ;;
esac
