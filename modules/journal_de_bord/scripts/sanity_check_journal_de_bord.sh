#!/usr/bin/env bash
set -euo pipefail
test -d /opt/trading || { echo "FAIL: /opt/trading missing"; exit 1; }
test -f /opt/trading/modules/journal_de_bord/scripts/generate_go_matrix.py || { echo "FAIL: generate_go_matrix.py missing"; exit 1; }
test -f /opt/trading/docs/ot/kanban/opt_trading_kanban_source_of_truth.md || { echo "FAIL: kanban missing"; exit 1; }
test -f /opt/trading/docs/ot/trae/OT_TRAE_SESSION_REPRISE.md || { echo "FAIL: session reprise missing"; exit 1; }
echo "PASS"
