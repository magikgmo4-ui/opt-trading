#!/usr/bin/env bash
set -euo pipefail
# Desk Pro Student - CMD Wrapper

# Resolve root
if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR" || exit 1

cmd="${1:-help}"

case "$cmd" in
  status|summary)
    echo "=== Desk Pro Student Status ==="
    echo "Repo Root: $ROOT_DIR"
    echo "Host: $(hostname)"
    echo "Date: $(date -u)"
    
    # Check shared mount
    if mount | grep -q "/shared"; then
        echo "Shared Drive: MOUNTED"
    else
        if [ -d "/shared" ]; then
             echo "Shared Drive: EXISTS (Check contents)"
        else
             echo "Shared Drive: MISSING (/shared)"
        fi
    fi
    
    # Check runner
    if command -v python3 &> /dev/null; then
        echo "Python: OK"
        python3 -m modules.desk_pro_runner.app.desk_pro_runner status 2>/dev/null | grep "runner_status" || echo "Runner: Module not found or failed"
    else
        echo "Python: MISSING"
    fi
    ;;
    
  sanity)
    bash "$SCRIPT_DIR/desk_pro_student_sanity_check.sh"
    ;;
    
  shared-info)
    bash "$SCRIPT_DIR/desk_pro_student_latest_shared_info.sh"
    ;;
    
  explain)
    echo "Desk Pro Student Wrapper"
    echo "Allows viewing shared artifacts and checking local health."
    echo "Use 'shared-info' to see latest run data from admin-trading."
    ;;
    
  *)
    echo "Usage: desk_pro_student_cmd.sh status|sanity|shared-info|summary|explain"
    exit 1
    ;;
esac
