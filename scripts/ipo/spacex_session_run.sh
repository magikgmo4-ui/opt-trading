#!/usr/bin/env bash
set -Eeuo pipefail
trap 'echo "[spacex_session_run] failed at line ${LINENO}" >&2' ERR
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

echo "=== SPCX V2 — Session Runner ==="

python3 -c "
from modules.spcx_v2.session_tracker import bump_session, get_session_count, is_test_complete, TARGET_SESSIONS

session = bump_session()
print(f'SPCX V2 session #{session}/{TARGET_SESSIONS}')

if session % 5 == 0:
    print('Interim report generated')
if is_test_complete():
    print('20 sessions complete — running graduation report')
    from modules.spcx_v2.session_tracker import graduation_report
    report = graduation_report()
    passed = report['summary']['passed']
    failed = report['summary']['failed']
    print(f'Setups passed: {passed} | failed: {failed}')
    for st, v in sorted(report['setups'].items()):
        status = 'PASS' if v['passed'] else 'FAIL'
        print(f'  {status} {st}: trades={v[\"metrics\"][\"trades\"]} wr={v[\"metrics\"][\"winrate\"]}% exp={v[\"metrics\"][\"expectancy_R\"]}R')
"

echo "=== session complete ==="
