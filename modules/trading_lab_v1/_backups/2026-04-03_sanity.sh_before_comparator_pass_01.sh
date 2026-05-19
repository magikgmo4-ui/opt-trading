#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app/trading_lab_v1.py"
PROFILE="$BASE/../../docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml"
EVENT_SCHEMA="$BASE/../../docs/ot/trading/schemas/trading_event_v1.schema.json"
TRADE_SCHEMA="$BASE/../../docs/ot/trading/schemas/trading_trade_v1.schema.json"

[ -f "$APP" ] || { echo "FAIL: app/trading_lab_v1.py manquant" >&2; exit 1; }
[ -f "$PROFILE" ] || { echo "FAIL: profil YAML V1 manquant" >&2; exit 1; }
[ -f "$EVENT_SCHEMA" ] || { echo "FAIL: schema event V1 manquant" >&2; exit 1; }
[ -f "$TRADE_SCHEMA" ] || { echo "FAIL: schema trade V1 manquant" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "FAIL: python3 non trouvé" >&2; exit 1; }

echo "PASS: trading_lab_v1 sanity OK"
