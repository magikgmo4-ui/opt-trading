#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Root Wrapper (Bash)
# Delegates to desk_pro_runner python module

# Resolve root relative to script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT_DIR" || exit 1

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found."
    exit 1
fi

# Delegate to Runner
python3 -m modules.desk_pro_runner.app.desk_pro_runner "$@"
