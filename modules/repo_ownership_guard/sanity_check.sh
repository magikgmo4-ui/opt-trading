#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$ROOT_DIR/modules/repo_ownership_guard/repo_ownership_guard_lib.sh"

need git
need find
need stat
need awk
need grep

echo "=== repo_ownership_guard sanity ==="
ctx
echo

# A) Any root-owned paths (excluding pruned dirs)?
echo "[A] owner scan (root-owned or not current user)"
bad_owner=0
while IFS= read -r p; do
  # Skip root dir itself (ok) but we still check ownership
  u=$(stat -c '%U' "$p" 2>/dev/null || true)
  g=$(stat -c '%G' "$p" 2>/dev/null || true)
  if [ "$u" = "root" ] || [ "$u" != "$ME_USER" ]; then
    echo "BAD_OWNER $u:$g  $p"
    bad_owner=1
  fi
done < <(find "$ROOT_DIR" \
  -path "$ROOT_DIR/.git" -prune -o \
  -path "$ROOT_DIR/_student_archive" -prune -o \
  -path "$ROOT_DIR/_worktrees" -prune -o \
  -path "$ROOT_DIR/_inbox" -prune -o \
  -path "$ROOT_DIR/_hold_untracked_before_merge_" -prune -o \
  -print)

if [ "$bad_owner" -eq 0 ]; then
  echo "OK: ownership looks consistent (no root-owned / foreign-owned paths)"
fi
echo

# B) Any directories not writable by current user?
echo "[B] directory writability scan (git needs writable dirs to replace/unlink files)"
bad_w=0
while IFS= read -r d; do
  if [ ! -w "$d" ]; then
    perm=$(stat -c '%a %U:%G' "$d" 2>/dev/null || true)
    echo "NOT_WRITABLE $perm  $d"
    bad_w=1
  fi
done < <(find "$ROOT_DIR" \
  -path "$ROOT_DIR/.git" -prune -o \
  -path "$ROOT_DIR/_student_archive" -prune -o \
  -path "$ROOT_DIR/_worktrees" -prune -o \
  -path "$ROOT_DIR/_inbox" -prune -o \
  -path "$ROOT_DIR/_hold_untracked_before_merge_" -prune -o \
  -type d -print)

if [ "$bad_w" -eq 0 ]; then
  echo "OK: all directories are writable by $ME_USER"
fi
echo

# C) Quick git health
echo "[C] git health"
ensure_git_root
git -C "$ROOT_DIR" status -sb | head -n 5
echo

if [ "$bad_owner" -eq 0 ] && [ "$bad_w" -eq 0 ]; then
  echo "PASS: repo_ownership_guard sanity OK"
else
  echo "WARN: repo_ownership_guard found issues (see above)."
  echo "      Run: bash scripts/repo_ownership_guard_cmd.sh fix --dry-run"
  exit 0
fi
