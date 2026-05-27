"""python -m app"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.result_tracker.app.schema import TradeRecord
from .writer import DatasheetWriter


def main() -> None:
    parser = argparse.ArgumentParser(description="Datasheet Writer CLI")
    parser.add_argument("--ticker", default="BTCUSDT")
    parser.add_argument("--dry-run", action="store_true", default=True)
    args = parser.parse_args()

    record = TradeRecord(
        trade_id=f"paper_{args.ticker}_cli",
        request_id="cli-req", signal_id=f"{args.ticker}-001",
        ticker=args.ticker, action="BUY",
        entry_price=65000.0, close_price=67000.0,
        fill_qty=0.5, size_pct=0.5,
        sl=63000.0, tp=70000.0,
        gross_pnl=1000.0, net_pnl=960.4, fees=39.6,
        duration_s=120.0, outcome="win",
        opened_at="2026-05-25T10:00:00+00:00",
        closed_at="2026-05-25T10:02:00+00:00",
        dry_run=args.dry_run,
    )
    result = DatasheetWriter().write(record, dry_run=args.dry_run)
    print(json.dumps({"ok": result.ok, "dry_run": result.dry_run, "written": result.written}, indent=2))
    sys.exit(0 if result.ok else 1)


if __name__ == "__main__":
    main()
