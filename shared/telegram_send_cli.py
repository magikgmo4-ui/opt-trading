#!/usr/bin/env python3
"""CLI wrapper for send_to_channel — callable from bash scripts.

Usage:
    python3 shared/telegram_send_cli.py <channel> <message>
    python3 shared/telegram_send_cli.py --channel <channel> --message <message>

Exit code 0 on success, 1 on failure.
"""
import os, sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _REPO_ROOT)


def main() -> None:
    channel = ""
    message = ""

    if len(sys.argv) >= 3 and not sys.argv[1].startswith("--"):
        channel = sys.argv[1]
        message = sys.argv[2]
    else:
        args = iter(sys.argv[1:])
        for a in args:
            if a == "--channel":
                channel = next(args, "")
            elif a == "--message":
                message = next(args, "")

    if not channel or not message:
        print("Usage: telegram_send_cli.py <channel> <message>", file=sys.stderr)
        sys.exit(1)

    try:
        from modules.env.env import load_env
        load_env()
        from shared.telegram_channels import send_to_channel
        result = send_to_channel(channel, message, source="cli")
        if not result.get("ok"):
            print(f"Error: {result.get('error')}", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
