#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Show Latest Response

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Define paths
ARCHIVE_DIR="$ROOT_DIR/_student_archive/response"
DAILY_REPORT="$ROOT_DIR/_student_archive/response/daily/daily_latest.md"

# Check daily report first (Priority 1)
if [ -L "$DAILY_REPORT" ] || [ -f "$DAILY_REPORT" ]; then
    echo "=== Latest Response: Daily Deterministic Report ==="
    echo "Path: $DAILY_REPORT"
    echo "----------------------------------------"
    cat "$DAILY_REPORT"
    echo "----------------------------------------"
    echo "(End of daily report)"
    exit 0
fi

# Fallback to standard response archives (Priority 2)
if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "No response archive directory found at $ARCHIVE_DIR"
    exit 1
fi

LATEST_FILE=$(ls -t "$ARCHIVE_DIR"/*.md 2>/dev/null | head -n 1)

if [ -z "$LATEST_FILE" ]; then
    echo "No response files found in $ARCHIVE_DIR (and no daily report)"
    exit 1
fi

echo "=== Latest Response: Standard Output ==="
echo "Path: $LATEST_FILE"
echo "----------------------------------------"
cat "$LATEST_FILE"
echo "----------------------------------------"
echo "(End of response)"
