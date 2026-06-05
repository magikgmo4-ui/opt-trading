#!/usr/bin/env python3
"""tg_resolve_candidates.py — resolve Telegram candidates, never crash."""

import json, sys, os, asyncio, argparse, time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # collector_telegram/
SRC_DIR = str(PROJECT_ROOT / "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from collector_telegram.discovery.resolve import resolve_telegram_input


async def resolve_batch(candidates, join=False, limit=None):
    from telethon import TelegramClient
    api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
    api_hash = os.environ.get("TELEGRAM_API_HASH", "")
    session = os.environ.get("TELEGRAM_SESSION_PATH", str(PROJECT_ROOT / "collector.session"))

    if not api_id or not api_hash:
        raise RuntimeError("TELEGRAM_API_ID and TELEGRAM_API_HASH required")

    client = TelegramClient(session, api_id, api_hash)
    await client.start()

    results = []
    batch = candidates[:limit] if limit else candidates
    total = len(batch)
    for i, raw in enumerate(batch):
        record = await resolve_telegram_input(client, raw, join=join)
        results.append(record)
        st = record.get("status", "?")
        title = (record.get("title") or "")[:30]
        count = "ok" if st == "ok" else ("FAIL" if st != "skipped" else "skip")
        print(f"  [{i+1:>3d}/{total}] {raw[:30]:30s} {count:5s} {title}")

    await client.disconnect()
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--join", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    inp = Path(args.input)
    candidates = []
    if inp.suffix == ".json":
        with open(inp) as f:
            data = json.load(f)
            if isinstance(data, list):
                candidates = [d if isinstance(d, str) else d.get("alias", "") for d in data]
            elif isinstance(data, dict) and "candidates" in data:
                candidates = [c["alias"] for c in data["candidates"] if c.get("alias")]
            else:
                print(f"ERROR: unexpected JSON format"); return
    else:
        with open(inp) as f:
            candidates = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    candidates = [c for c in candidates if c]
    print(f"Resolving {len(candidates)} candidates...")

    results = asyncio.run(resolve_batch(candidates, join=args.join, limit=args.limit))

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    ok = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] in ("resolve_failed", "invite_failed"))
    skip = sum(1 for r in results if r["status"] == "skipped")
    err = len(results) - ok - failed - skip
    print(f"\n{ok} ok, {failed} invalid, {skip} skipped, {err} errors → {out}")


if __name__ == "__main__":
    main()
