#!/usr/bin/env bash
set -euo pipefail
# Git Sync Summary (Linux)
# Displays concise git status

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR" || exit 1

echo "=== Git Sync Summary ==="
echo "Repo Root: $ROOT_DIR"
echo "Branch:    $(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'Unknown')"
echo "Last Commit:"
git log -1 --oneline --no-decorate --color=always 2>/dev/null || echo "No commits."
echo "----------------------------------------"
echo "Status (Short):"
git status --short 2>/dev/null || echo "Status unavailable."
echo "========================"
