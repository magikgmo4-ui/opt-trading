#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$BASE/app/trading_lab_v1.py"
EXPORT_APP="$BASE/app/report_export_v1.py"
COMPARATOR_APP="$BASE/app/comparator_v1.py"
LIVE_APP="$BASE/app/live_observation_v1.py"
LIVE_EXPORT_APP="$BASE/app/live_export_v1.py"
SWEEP_ENGINE="$BASE/app/param_sweep_engine_v1.py"
SWEEP_CONFIG="$BASE/app/param_sweep_config_v1.py"
SWEEP_CLASSIFY="$BASE/app/param_sweep_classify_v1.py"
SWEEP_RANK="$BASE/app/param_sweep_rank_v1.py"
PROFILE="$BASE/../../docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml"
EVENT_SCHEMA="$BASE/../../docs/ot/trading/schemas/trading_event_v1.schema.json"
TRADE_SCHEMA="$BASE/../../docs/ot/trading/schemas/trading_trade_v1.schema.json"
SAMPLE_MARKET="$BASE/data/sample_xauusd_m1.csv"
SAMPLE_LIVE="$BASE/data/sample_live_reference_v1.jsonl"

[ -f "$APP" ] || { echo "FAIL: app/trading_lab_v1.py manquant" >&2; exit 1; }
[ -f "$EXPORT_APP" ] || { echo "FAIL: app/report_export_v1.py manquant" >&2; exit 1; }
[ -f "$COMPARATOR_APP" ] || { echo "FAIL: app/comparator_v1.py manquant" >&2; exit 1; }
[ -f "$LIVE_APP" ] || { echo "FAIL: app/live_observation_v1.py manquant" >&2; exit 1; }
[ -f "$LIVE_EXPORT_APP" ] || { echo "FAIL: app/live_export_v1.py manquant" >&2; exit 1; }
[ -f "$PROFILE" ] || { echo "FAIL: profil YAML V1 manquant" >&2; exit 1; }
[ -f "$EVENT_SCHEMA" ] || { echo "FAIL: schema event V1 manquant" >&2; exit 1; }
[ -f "$TRADE_SCHEMA" ] || { echo "FAIL: schema trade V1 manquant" >&2; exit 1; }
[ -f "$SAMPLE_MARKET" ] || { echo "FAIL: sample market CSV manquant" >&2; exit 1; }
[ -f "$SAMPLE_LIVE" ] || { echo "FAIL: sample live JSONL manquant" >&2; exit 1; }
[ -f "$SWEEP_ENGINE" ] || { echo "FAIL: param_sweep_engine_v1.py manquant" >&2; exit 1; }
[ -f "$SWEEP_CONFIG" ] || { echo "FAIL: param_sweep_config_v1.py manquant" >&2; exit 1; }
[ -f "$SWEEP_CLASSIFY" ] || { echo "FAIL: param_sweep_classify_v1.py manquant" >&2; exit 1; }
[ -f "$SWEEP_RANK" ] || { echo "FAIL: param_sweep_rank_v1.py manquant" >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "FAIL: python3 non trouvé" >&2; exit 1; }

echo "PASS: trading_lab_v1 sanity OK"
