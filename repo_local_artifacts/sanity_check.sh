#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

need() { command -v "$1" >/dev/null 2>&1 || { echo "ERR: missing $1" >&2; exit 1; }; }

need git
need grep

echo "=== repo_local_artifacts sanity ==="
echo "root: $ROOT_DIR"

REQ=(
  "_worktrees/"
  "_inbox/"
  "_hold_untracked_before_merge_*/"
)

missing=0
for pat in "${REQ[@]}"; do
  if ! grep -qxF "$pat" "$ROOT_DIR/.gitignore" 2>/dev/null; then
    echo "MISSING in .gitignore: $pat"
    missing=1
  fi
done
[ "$missing" -eq 0 ] || { echo "FAIL: .gitignore missing entries"; exit 1; }
echo "OK: .gitignore entries present"

tracked_bad=$(git -C "$ROOT_DIR" ls-files | grep -E '^(_worktrees/|_inbox/|_hold_untracked_before_merge_)' || true)
if [ -n "$tracked_bad" ]; then
  echo "FAIL: tracked files under local-only folders:"
  echo "$tracked_bad"
  exit 1
fi
echo "OK: no tracked files under local-only folders"

echo "PASS: repo_local_artifacts sanity OK"
