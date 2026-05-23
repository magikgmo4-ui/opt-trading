#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

usage() {
  cat <<'USAGE'
Usage:
  tools/session_transport/apply_session_patch.sh <patch-file> [branch]

Purpose:
  Apply a ChatGPT session-generated .patch safely.

Behavior:
  - verifies Git repo
  - optionally switches/creates the target branch
  - refuses tracked/staged local changes before applying
  - runs git apply --check
  - applies the patch
  - runs git diff --check
  - lists changed files
  - warns if root-level .patch files remain
  - does not commit
  - does not push
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || $# -lt 1 ]]; then
  usage
  exit 0
fi

PATCH_FILE="$1"
TARGET_BRANCH="${2:-}"

if [[ ! -f "$PATCH_FILE" ]]; then
  echo "Patch file not found: $PATCH_FILE" >&2
  exit 2
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

echo "REPO_ROOT=$REPO_ROOT"

if ! git diff --quiet; then
  echo "Tracked working tree changes detected before patch. Commit/stash/clean first." >&2
  git status --short
  exit 3
fi

if ! git diff --cached --quiet; then
  echo "Staged changes detected before patch. Commit/stash/clean first." >&2
  git status --short
  exit 4
fi

if [[ -n "$TARGET_BRANCH" ]]; then
  git switch "$TARGET_BRANCH" 2>/dev/null || git switch -c "$TARGET_BRANCH"
fi

echo "BRANCH=$(git branch --show-current)"
echo "PATCH_FILE=$PATCH_FILE"

git apply --check "$PATCH_FILE"
git apply "$PATCH_FILE"
git diff --check

echo
echo "FILES_CHANGED:"
git diff --name-only

echo
echo "ROOT_PATCHES_REMAINING:"
find . -maxdepth 1 -type f -name '*.patch' -print || true

echo
echo "STATUS:"
git status --short --untracked-files=all

echo
echo "NEXT:"
echo "Inspect the diff, run no-secret checks if needed, ensure root patches are not staged, then commit manually."
