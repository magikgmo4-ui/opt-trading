#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_export_daily_v2] failed at line ${LINENO}" >&2' ERR
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "=== SPCX V2 — daily export ==="

echo "--- [1/4] Generating Desk JSON ---"
python3 -c "from modules.spcx_v2.export_desk import export_desk_json; p = export_desk_json(); print(f'Desk JSON written to {p}')"

echo "--- [2/4] Sending Telegram EOD summary ---"
python3 -c "from modules.spcx_v2.export_telegram import send_a_plus_alerts, send_eod_summary; n = send_a_plus_alerts(); print(f'Sent {n} A+ alerts'); msg = send_eod_summary(); print('EOD summary sent')"

echo "--- [3/4] Exporting to CSV for Sheets ---"
python3 -c "from modules.spcx_v2.export_sheets import export_to_csv; p = export_to_csv(); print(f'CSV written to {p}')"

echo "--- [4/4] Writing daily markdown report ---"
python3 -c "from modules.spcx_v2.daily_summary import write_daily_markdown; p = write_daily_markdown(); print(f'Daily report written to {p}')"

echo "=== daily export complete ==="
