"""python -m app <request_json> [--dry-run]"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.proposition_engine.app.schema import Proposition
from modules.validation_gate.app.schema import GateDecision
from .executor import TradeExecutor
from .schema import TradeRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="Trade Executor CLI")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--ticker", default="BTCUSDT")
    parser.add_argument("--action", default="BUY", choices=["BUY", "SELL"])
    parser.add_argument("--entry", type=float, default=65000.0)
    parser.add_argument("--sl", type=float, default=63000.0)
    parser.add_argument("--tp", type=float, default=70000.0)
    parser.add_argument("--confidence", type=float, default=0.85)
    args = parser.parse_args()

    prop = Proposition(
        request_id="cli-req",
        signal_id=f"{args.ticker}-001",
        action=args.action,
        size_pct=0.5,
        entry=args.entry,
        sl=args.sl,
        tp=args.tp,
        confidence=args.confidence,
        rationale="CLI invocation",
        engines_context={"ticker": args.ticker},
        status="ok",
    )

    gate = GateDecision(
        request_id="cli-gate",
        signal_id=f"{args.ticker}-001",
        verdict="APPROVED",
        reason="cli_approved",
        risk_status="ALLOW",
        risk_reason="cli_invocation",
        operator_approved=True,
        dry_run=args.dry_run,
    )

    req = TradeRequest(
        gate_decision=gate,
        proposition=prop,
        ticker=args.ticker,
        dry_run=args.dry_run,
    )
    result = TradeExecutor().execute(req)
    output = {
        "status": result.status,
        "trade_id": result.trade_id,
        "action": result.action,
        "ticker": result.ticker,
        "fill_price": result.fill_price,
        "fill_qty": result.fill_qty,
        "reason": result.reason,
        "dry_run": result.dry_run,
        "duration_ms": result.duration_ms,
    }
    print(json.dumps(output, indent=2))
    sys.exit(0 if result.status in ("dry_run", "filled") else 1)


if __name__ == "__main__":
    main()
