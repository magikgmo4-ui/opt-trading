#!/usr/bin/env bash
set -euo pipefail

MODULE="${1:-}"
if [[ -z "$MODULE" ]]; then
  echo "Usage: push_module_to_student.sh <module_name>"
  echo "Example: push_module_to_student.sh desk_pro"
  exit 2
fi

SRC="/opt/trading/modules/${MODULE}/"
if [[ ! -d "$SRC" ]]; then
  echo "ERROR: module not found at $SRC"
  exit 1
fi

DEST="student:/opt/trading/_student_archive/modules/${MODULE}/"

echo "==> Sync module '${MODULE}' to student..."
rsync -av --delete \
  --exclude '__pycache__/' --exclude '.pytest_cache/' --exclude '*.pyc' \
  "$SRC" "$DEST"

echo "==> OK"
