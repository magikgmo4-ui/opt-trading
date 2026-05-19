"""CLI entry: python -m app ask "instruction" --context "ctx" --timeout 30"""
from __future__ import annotations
import argparse
import json
import sys
from .bridge import OperatorBridge
from .schema import BridgeRequest


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenClaw Operator Bridge CLI")
    parser.add_argument("action", choices=["ask", "build", "evaluate", "review"])
    parser.add_argument("instruction", help="instruction to send to builder")
    parser.add_argument("--context", default="", help="optional context")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--request-id", default="")
    args = parser.parse_args()

    bridge = OperatorBridge()
    req = BridgeRequest(
        action=args.action,
        instruction=args.instruction,
        context=args.context,
        timeout_s=args.timeout,
        request_id=args.request_id,
    )
    resp = bridge.send(req)
    print(json.dumps(resp.to_dict(), indent=2))
    sys.exit(0 if resp.status == "ok" else 1)


if __name__ == "__main__":
    main()
