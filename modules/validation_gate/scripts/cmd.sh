#!/usr/bin/env bash
# validation_gate CLI helper
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

CMD="${1:-help}"

case "$CMD" in
  sanity)
    bash "$SCRIPT_DIR/sanity.sh"
    ;;
  test)
    cd "$PROJECT_ROOT" && python3 -m unittest modules.validation_gate.tests.test_gate -v
    ;;
  approve)
    # Write operator approval for a request_id
    # Usage: cmd.sh approve <request_id> [APPROVE|REJECT]
    REQ_ID="${2:-}"
    VERDICT="${3:-APPROVE}"
    DIR="${GATE_APPROVAL_DIR:-$PROJECT_ROOT/data/gate_approvals}"
    mkdir -p "$DIR"
    echo "{\"verdict\": \"$VERDICT\"}" > "$DIR/$REQ_ID.json"
    echo "Written: $DIR/$REQ_ID.json  verdict=$VERDICT"
    ;;
  status)
    python3 -c "
import sys; sys.path.insert(0, '.')
from modules.validation_gate.app.gate import ValidationGate
print('ValidationGate: OK')
print('Approval dir:', ValidationGate().approval_dir)
"
    ;;
  help|*)
    echo "Usage: cmd.sh [sanity|test|approve <req_id> [APPROVE|REJECT]|status|help]"
    ;;
esac
