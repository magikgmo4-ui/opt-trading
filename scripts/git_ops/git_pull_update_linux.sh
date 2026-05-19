#!/usr/bin/env bash
set -euo pipefail
# Git Pull Update (Linux)
# Updates the repository, optionally restoring specific paths first.

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR" || exit 1

RESTORE_PATHS=()

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --paths)
            shift
            while [[ $# -gt 0 && ! "$1" =~ ^- ]]; do
                RESTORE_PATHS+=("$1")
                shift
            done
            ;;
        *)
            echo "Unknown argument: $1"
            echo "Usage: $0 [--paths path1 path2 ...]"
            exit 1
            ;;
    esac
done

echo "=== Git Pull Update ==="
echo "Repo: $ROOT_DIR"
echo "Date: $(date -u)"
echo "-----------------------"

# 1. Status
echo "Checking status..."
git status --short

# 2. Restore (if requested)
if [ ${#RESTORE_PATHS[@]} -gt 0 ]; then
    echo "-----------------------"
    echo "Restoring specified paths..."
    for path in "${RESTORE_PATHS[@]}"; do
        if [ -e "$path" ] || git ls-files --error-unmatch "$path" >/dev/null 2>&1; then
            echo "  Restoring: $path"
            git restore "$path" || echo "  WARN: Failed to restore $path"
        else
            echo "  WARN: Path not tracked or missing: $path"
        fi
    done
fi

echo "-----------------------"

# 3. Fetch & Pull
echo "Fetching updates..."
git fetch --tags

echo "Pulling changes (fast-forward only)..."
if git pull --ff-only; then
    echo "PASS: Update successful."
else
    echo "FAIL: Update failed (conflict or diverge)."
    echo "      Check 'git status' and resolve manually."
    exit 1
fi

echo "-----------------------"
echo "New HEAD:"
git log -1 --oneline --no-decorate --color=always
echo "======================="
exit 0
