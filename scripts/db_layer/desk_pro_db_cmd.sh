#!/usr/bin/env bash
set -euo pipefail
# Desk Pro DB Layer - CMD Wrapper

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
    echo "=== DESK PRO DB-LAYER STATUS ==="
    echo "Repo Root:    $ROOT_DIR"
    echo "Host:         $(hostname)"
    echo "Date:         $(date -u)"
    
    # Check shared mount
    if mount | grep -q "/shared"; then
        echo "Shared Drive: MOUNTED"
    elif [ -d "/shared" ]; then
        echo "Shared Drive: EXISTS (Check contents)"
    else
        echo "Shared Drive: MISSING (/shared)"
    fi

    # Check Shared Latest
    if [ -d "/shared/desk_pro/latest" ] && [ -f "/shared/desk_pro/latest/run_summary.json" ]; then
        echo "Shared Latest: AVAILABLE"
    else
        echo "Shared Latest: MISSING"
    fi
    
    # Check Python
    if command -v python3 &> /dev/null; then
        echo "Python:       OK"
    else
        echo "Python:       MISSING"
    fi

    echo "Summary:      DB-Layer pack ready for shared artifact consultation."
    echo "================================"
    ;;
    
  sanity)
    bash "$SCRIPT_DIR/desk_pro_db_sanity_check.sh"
    ;;
    
  shared-info)
    bash "$SCRIPT_DIR/desk_pro_db_latest_shared_info.sh"
    ;;
    
  explain)
    echo "Desk Pro DB Layer Wrapper"
    echo "Allows viewing shared artifacts and checking local health."
    echo "Use 'shared-info' to see latest run data from admin-trading."
    ;;
    
  *)
    echo "Usage: desk_pro_db_cmd.sh status|sanity|shared-info|summary|explain"
    exit 1
    ;;
esac
