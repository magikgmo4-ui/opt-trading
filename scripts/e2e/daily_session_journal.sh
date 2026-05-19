#!/usr/bin/env bash
set -euo pipefail
# Daily Session Journal — bash wrapper
# Usage: ./daily_session_journal.sh [run|show|list|latest] [args...]

if command -v readlink >/dev/null 2>&1; then
    SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
else
    SCRIPT_PATH="${BASH_SOURCE[0]}"
fi
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
JOURNAL_DIR="$ROOT_DIR/data/journal/daily"

cmd="${1:-run}"
shift || true

case "$cmd" in
    run)
        echo "=== Daily Session Journal: run ==="
        export DRY_RUN="${DRY_RUN:-1}"
        export PAPER_MODE="${PAPER_MODE:-1}"
        python "$SCRIPT_DIR/daily_session_journal.py" "$@"
        ;;
    show)
        if [ -n "$1" ]; then
            RUN_ID="$1"
            FILE="$JOURNAL_DIR/$RUN_ID.json"
        else
            FILE=$(ls -t "$JOURNAL_DIR"/*.json 2>/dev/null | head -1)
        fi
        if [ -f "$FILE" ]; then
            python -m json.tool "$FILE"
        else
            echo "No journal entry found: ${FILE:-no files}"
            exit 1
        fi
        ;;
    list)
        echo "=== Daily Session Journals ==="
        if [ -d "$JOURNAL_DIR" ] && [ "$(ls -A "$JOURNAL_DIR"/*.json 2>/dev/null)" ]; then
            printf "%-20s %-8s %-10s %-10s %s\n" "RUN_ID" "ALL_OK" "CLOSEOUT" "DURATION" "STARTED"
            for f in $(ls -t "$JOURNAL_DIR"/*.json 2>/dev/null); do
                RUN_ID=$(basename "$f" .json)
                ALL_OK=$(python -c "import json; d=json.load(open('$f')); print(d.get('all_ok','?'))" 2>/dev/null || echo "?")
                CLOSEOUT=$(python -c "import json; d=json.load(open('$f')); print(d.get('closeout_acknowledged','?'))" 2>/dev/null || echo "?")
                DURATION=$(python -c "import json; d=json.load(open('$f')); print(f\"{d.get('duration_s',0):.1f}s\")" 2>/dev/null || echo "?")
                STARTED=$(python -c "import json; d=json.load(open('$f')); print(d.get('started_at','?')[:19])" 2>/dev/null || echo "?")
                printf "%-20s %-8s %-10s %-10s %s\n" "$RUN_ID" "$ALL_OK" "$CLOSEOUT" "$DURATION" "$STARTED"
            done
        else
            echo "(No journal entries yet)"
        fi
        ;;
    latest)
        FILE=$(ls -t "$JOURNAL_DIR"/*.json 2>/dev/null | head -1)
        if [ -f "$FILE" ]; then
            RUN_ID=$(basename "$FILE" .json)
            python -c "
import json
d = json.load(open('$FILE'))
print('='*60)
print(f'LATEST: {d.get(\"run_id\",\"?\")}')
print('='*60)
print(f'Started : {d.get(\"started_at\",\"?\")[:19]}')
print(f'Duration: {d.get(\"duration_s\",0):.1f}s')
print(f'All OK  : {d.get(\"all_ok\",\"?\")}')
print(f'Closeout: {d.get(\"closeout_acknowledged\",\"?\")}')
print(f'Sessions: {d.get(\"tmux_after\",{}).get(\"count\",\"?\")}')
print(f'LocalCMS: {d.get(\"localcms_ok\",\"?\")}')
pnl = d.get('pnl_paper', {})
print(f'P&L     : {pnl.get(\"outcome\",\"?\")} net={pnl.get(\"net_pnl\",\"?\")}')
print(f'Verdict : {d.get(\"validation_verdict\",\"?\")}')
print(f'Signal  : {d.get(\"signal_source\",{}).get(\"signal\",\"?\")} {d.get(\"signal_source\",{}).get(\"symbol\",\"?\")}')
print('='*60)
"
        else
            echo "(No journal entries yet)"
        fi
        ;;
    *)
        echo "Usage: $0 [run|show <run_id>|list|latest] [args...]"
        echo ""
        echo "Commands:"
        echo "  run              Run a new daily session journal (default)"
        echo "  show [run_id]    Show JSON for a run (latest if no id)"
        echo "  list             List all journal entries"
        echo "  latest           Show latest summary"
        exit 1
        ;;
esac
