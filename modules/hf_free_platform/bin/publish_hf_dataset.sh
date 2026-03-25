#!/usr/bin/env bash
set -euo pipefail

KEEP_WORKDIR="${KEEP_WORKDIR:-0}"

cleanup() {
  if [[ "$KEEP_WORKDIR" == "1" ]]; then
    echo "Review mode: temporary repo kept at $WORKDIR/repo"
    echo "Next steps:"
    echo "  cd \"$WORKDIR/repo\""
    echo "  git status --short"
    echo "  git diff --cached"
    echo "  git commit"
    echo "  git push"
    return
  fi
  rm -rf "$WORKDIR"
}

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <local_dataset_dir> <hf_dataset_repo_url>"
  echo "Set KEEP_WORKDIR=1 to keep the temp clone for manual review/commit/push."
  exit 1
fi
LOCAL_DIR="$1"
REMOTE_URL="$2"
WORKDIR="$(mktemp -d)"
trap cleanup EXIT
git clone "$REMOTE_URL" "$WORKDIR/repo"
rsync -a --delete --exclude ".git" "$LOCAL_DIR"/ "$WORKDIR/repo"/
cd "$WORKDIR/repo"
git add .
git status --short
if [[ "$KEEP_WORKDIR" == "1" ]]; then
  echo "Manual review mode enabled. The temp clone will be kept for commit/push."
else
  echo "Preview only: temp clone will be removed on exit. Re-run with KEEP_WORKDIR=1 for manual review."
fi
