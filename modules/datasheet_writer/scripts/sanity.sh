#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== datasheet_writer SANITY ==="

echo "--- tests ---"
python3 -m unittest modules.datasheet_writer.tests.test_writer -v 2>&1

echo "--- dry-run write (no file created) ---"
python3 - <<'EOF'
import sys, json, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))

from modules.result_tracker.app.schema import TradeRecord
from modules.datasheet_writer.app.writer import DatasheetWriter

record = TradeRecord(
    trade_id="paper_BTCUSDT_sanity", request_id="req-001", signal_id="sig-001",
    ticker="BTCUSDT", action="BUY",
    entry_price=65000.0, close_price=67000.0,
    fill_qty=0.5, size_pct=0.5,
    sl=63000.0, tp=70000.0,
    gross_pnl=1000.0, net_pnl=961.0, fees=39.0,
    duration_s=120.0, outcome="win",
    opened_at="2026-05-16T10:00:00+00:00",
    closed_at="2026-05-16T10:02:00+00:00",
    dry_run=True,
)
with tempfile.TemporaryDirectory() as d:
    w = DatasheetWriter(output_dir=Path(d))
    r = w.write(record, dry_run=True)
    print(json.dumps({"ok": r.ok, "dry_run": r.dry_run, "written": r.written}, indent=2))
    assert not r.written
    assert list(Path(d).iterdir()) == []

    # live write
    r2 = w.write(record, dry_run=False)
    print(json.dumps({"ok": r2.ok, "written": r2.written, "jsonl": Path(r2.jsonl_path).name, "csv": Path(r2.csv_path).name}, indent=2))
    assert r2.written
    assert Path(r2.jsonl_path).exists()
    assert Path(r2.csv_path).exists()
EOF

echo ""
echo "=== SANITY PASS — datasheet_writer V1 (13 tests, JSONL+CSV write OK) ==="
