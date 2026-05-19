#!/usr/bin/env bash
set -euo pipefail
# Desk Pro DB Layer Sanity Check
# Verifies local setup and shared access

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Checking Desk Pro DB Layer Environment..."

# 1. Python
if command -v python3 &> /dev/null; then
    echo "PASS: Python 3 found"
else
    echo "FAIL: Python 3 missing"
    exit 1
fi

# 2. Repo Structure
if [ -d "$ROOT_DIR/modules" ]; then
    echo "PASS: Modules directory exists"
else
    echo "FAIL: Modules directory missing"
    exit 1
fi

# 3. Scripts
if [ -f "$SCRIPT_DIR/desk_pro_db_cmd.sh" ]; then
    echo "PASS: DB Layer command wrapper exists"
else
    echo "FAIL: DB Layer scripts missing"
    exit 1
fi

# 4. Shared Access
if [ -d "/shared" ]; then
    if [ -d "/shared/desk_pro/latest" ]; then
        echo "PASS: Shared artifacts directory accessible"
    else
        echo "WARN: Shared root exists, but desk_pro/latest is missing"
    fi
else
    echo "WARN: /shared directory not found (check mount)"
fi

echo "DB Layer Sanity Check Passed."
