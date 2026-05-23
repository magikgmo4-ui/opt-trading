#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

usage() {
  cat <<'USAGE'
Usage:
  tools/session_transport/bootstrap_patch_inbox.sh <patch-file> <GO_ID> [slug]

Purpose:
  Move/copy a root-level session patch into its canonical location:
  bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch

Behavior:
  - verifies Git repo
  - creates bundles/<GO_ID>/patches
  - copies patch to canonical path
  - removes root patch only when source is at repo root and copy succeeds
  - does not apply the patch
  - does not commit
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || $# -lt 2 ]]; then
  usage
  exit 0
fi

PATCH_FILE="$1"
GO_ID="$2"
SLUG="${3:-session_patch}"

if [[ ! -f "$PATCH_FILE" ]]; then
  echo "Patch file not found: $PATCH_FILE" >&2
  exit 2
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

DATE_STAMP="$(date +%Y%m%d)"
SAFE_SLUG="$(echo "$SLUG" | tr ' ' '_' | tr -cd 'A-Za-z0-9._-')"
DEST_DIR="bundles/$GO_ID/patches"
DEST_FILE="$DEST_DIR/${DATE_STAMP}_${GO_ID}_${SAFE_SLUG}.patch"

mkdir -p "$DEST_DIR"

SRC_ABS="$(realpath "$PATCH_FILE")"
DEST_ABS="$(realpath -m "$DEST_FILE")"

if [[ "$SRC_ABS" == "$DEST_ABS" ]]; then
  echo "Patch already in canonical location: $DEST_FILE"
  exit 0
fi

cp "$SRC_ABS" "$DEST_FILE"

ROOT_ABS="$(realpath "$REPO_ROOT")"
SRC_DIR="$(dirname "$SRC_ABS")"

if [[ "$SRC_DIR" == "$ROOT_ABS" ]]; then
  rm "$SRC_ABS"
  echo "Moved root patch to: $DEST_FILE"
else
  echo "Copied patch to: $DEST_FILE"
fi

echo "PATCH_CANONICAL_PATH=$DEST_FILE"
