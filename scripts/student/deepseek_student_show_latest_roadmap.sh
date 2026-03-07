#!/usr/bin/env bash
set -euo pipefail
# DeepSeek Student - Show Latest Roadmap

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Assuming roadmap events generate files in a known location or we just find the last output.
# Based on deepseek_student_cmd.sh, 'roadmap' calls python scripts. 
# We need to find where they output. 
# Assuming _student_archive/roadmap/ based on patterns.

ARCHIVE_DIR="$ROOT_DIR/_student_archive/roadmap"

if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "No roadmap archive directory found at $ARCHIVE_DIR"
    exit 1
fi

LATEST_FILE=$(ls -t "$ARCHIVE_DIR"/*.md 2>/dev/null | head -n 1)

if [ -z "$LATEST_FILE" ]; then
    echo "No roadmap files found in $ARCHIVE_DIR"
    exit 1
fi

echo "=== Latest Roadmap: $(basename "$LATEST_FILE") ==="
echo "Path: $LATEST_FILE"
echo "----------------------------------------"
cat "$LATEST_FILE"
echo "----------------------------------------"
echo "(End of roadmap)"
