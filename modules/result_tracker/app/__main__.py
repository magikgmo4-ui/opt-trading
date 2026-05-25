"""python -m app <close_price> [--dry-run]"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.trade_executor.app.schema import TradeResult
from .tracker import ResultTracker
from .schema import CloseRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="Result Tracker CLI")
    parser.add_argument("--close-price", type=float, default=67000.0)
    parser.add_argument("--ticker", default="BTCUSDT")
    parser.add_argument("--action", default="BUY", choices=["BUY", "SELL"])
    parser.add_argument("--entry", type=float, default=65000.0)
    parser.add_argument("--dry-run", action="store_true", default=True)
    args = parser.parse_args()

    trade = TradeResult(
        request_id="cli-req",
        signal_id=f"{args.ticker}-001",
        trade_id=f"paper_{args.ticker}_cli001",
        action=args.action,
        ticker=args.ticker,
        fill_price=args.entry,
        fill_qty=0.5,
        size_pct=0.5,
        sl=args.entry * 0.98,
        tp=args.entry * 1.05,
        status="filled",
        reason="cli_trade",
        duration_ms=50,
        dry_run=args.dry_run,
    )
    req = CloseRequest(trade_result=trade, close_price=args.close_price, dry_run=args.dry_run)
    record = ResultTracker().track(req)
    output = {
        "trade_id": record.trade_id,
        "ticker": record.ticker,
        "outcome": record.outcome,
        "gross_pnl": record.gross_pnl,
        "net_pnl": record.net_pnl,
        "fees": record.fees,
        "duration_s": record.duration_s,
        "dry_run": record.dry_run,
    }
    print(json.dumps(output, indent=2))
    sys.exit(0 if record.outcome in ("win", "loss", "breakeven") else 1)


if __name__ == "__main__":
    main()
