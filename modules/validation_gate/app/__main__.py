"""python -m app <request_json> [--dry-run]"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.proposition_engine.app.schema import Proposition
from .gate import ValidationGate
from .schema import GateRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="Validation Gate CLI")
    parser.add_argument("proposition_json", nargs="?", help="JSON string or @file path")
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument("--ticker", default="")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    if args.proposition_json:
        if args.proposition_json.startswith("@"):
            raw = Path(args.proposition_json[1:]).read_text()
        else:
            raw = args.proposition_json
        data = json.loads(raw)
        prop = Proposition(**data)
    else:
        prop = Proposition(
            request_id="cli-req",
            signal_id="CLI-001",
            action="BUY",
            size_pct=0.5,
            entry=65000.0,
            sl=63000.0,
            tp=70000.0,
            confidence=0.85,
            rationale="CLI invocation",
            engines_context={"ticker": args.ticker or "UNKNOWN"},
            status="ok",
        )

    req = GateRequest(
        proposition=prop,
        ticker=args.ticker or "",
        dry_run=args.dry_run,
        timeout_s=args.timeout,
    )
    gate = ValidationGate()
    dec = gate.gate(req)
    output = {
        "request_id": dec.request_id,
        "signal_id": dec.signal_id,
        "verdict": dec.verdict,
        "reason": dec.reason,
        "risk_status": dec.risk_status,
        "risk_reason": dec.risk_reason,
        "operator_approved": dec.operator_approved,
        "duration_ms": dec.duration_ms,
        "dry_run": dec.dry_run,
    }
    print(json.dumps(output, indent=2))
    sys.exit(0 if dec.verdict == "APPROVED" else 1)


if __name__ == "__main__":
    main()
