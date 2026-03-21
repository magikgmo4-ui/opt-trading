#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <local_space_dir> <hf_space_repo_url>"
  exit 1
fi
LOCAL_DIR="$1"
REMOTE_URL="$2"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT
git clone "$REMOTE_URL" "$WORKDIR/repo"
rsync -a --delete "$LOCAL_DIR"/ "$WORKDIR/repo"/
cd "$WORKDIR/repo"
git add .
git status --short
echo "Ready to commit/push manually after review."
