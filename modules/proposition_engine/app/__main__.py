"""CLI: python3 -m app <ticker> <side> <price> <tf> [--dry-run] [--strategy-id X] [--timeout N]"""
import argparse
import json
import uuid

from .schema import NormalizedSignal, PropositionRequest
from .engine import PropositionEngine


def main():
    parser = argparse.ArgumentParser(description="proposition_engine CLI")
    parser.add_argument("ticker")
    parser.add_argument("side", choices=["BUY", "SELL"])
    parser.add_argument("price", type=float)
    parser.add_argument("tf")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--strategy-id", default="cli")
    parser.add_argument("--sl", type=float, default=None)
    parser.add_argument("--tp", type=float, default=None)
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()

    signal = NormalizedSignal(
        signal_id=str(uuid.uuid4()),
        ticker=args.ticker,
        side=args.side,
        price=args.price,
        timestamp=__import__("time").time(),
        strategy_id=args.strategy_id,
        tf=args.tf,
        sl=args.sl,
        tp=args.tp,
    )
    request = PropositionRequest(signal=signal, dry_run=args.dry_run, timeout_s=args.timeout)
    engine = PropositionEngine()
    prop = engine.propose(request)
    print(json.dumps(prop.to_dict(), indent=2))


if __name__ == "__main__":
    main()
