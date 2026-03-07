#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Show Latest AI Report

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

ARCHIVE_DIR="$ROOT_DIR/_student_archive/response/ai_daily"

if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "No AI daily archive directory found at $ARCHIVE_DIR"
    exit 1
fi

LATEST_FILE=$(ls -t "$ARCHIVE_DIR"/*.md 2>/dev/null | head -n 1)

if [ -z "$LATEST_FILE" ]; then
    echo "No AI report files found in $ARCHIVE_DIR"
    exit 1
fi

echo "=== Latest AI Report: $(basename "$LATEST_FILE") ==="
echo "Path: $LATEST_FILE"
echo "----------------------------------------"
cat "$LATEST_FILE"
echo "----------------------------------------"
echo "(End of AI report)"
