#!/usr/bin/env python3
"""
Telegram channel discovery via Telethon SearchRequest API.
Runs on admin-trading (requires Telethon session).
Searches keywords, finds channels, samples messages.
"""

import json, sys, os, asyncio
from pathlib import Path

def load_keywords():
    project_root = Path(__file__).resolve().parent.parent.parent
    cfg_path = project_root / "configs" / "telegram" / "discovery_keywords.json"
    # Fallback: check admin-trading path
    if not cfg_path.exists():
        cfg_path = Path("/opt/trading/configs/telegram/discovery_keywords.json")
    with open(cfg_path) as f:
        return json.load(f)

async def search_channels(keyword: str, limit: int = 10):
    """Search Telegram for channels matching a keyword."""
    from telethon import TelegramClient
    from telethon.tl.functions.contacts import SearchRequest

    session_path = os.environ.get("TELEGRAM_SESSION_PATH", "collector.session")
    api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
    api_hash = os.environ.get("TELEGRAM_API_HASH", "")

    if not api_id or not api_hash:
        print("ERROR: TELEGRAM_API_ID and TELEGRAM_API_HASH required", file=sys.stderr)
        return []

    client = TelegramClient(session_path, api_id, api_hash)
    await client.start()

    results = []
    try:
        resp = await client(SearchRequest(q=keyword, limit=limit))
        for chat in resp.chats:
            results.append({
                "username": getattr(chat, "username", None) or "",
                "title": getattr(chat, "title", ""),
                "id": getattr(chat, "id", 0),
                "participants_count": getattr(chat, "participants_count", 0),
                "broadcast": getattr(chat, "broadcast", False),
                "megagroup": getattr(chat, "megagroup", False),
            })
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
    finally:
        await client.disconnect()

    return results


async def discover_all():
    """Search all keywords across all buckets, return unique channels."""
    cfg = load_keywords()
    all_channels = {}  # username → info

    for bucket_name, bucket in cfg.get("buckets", {}).items():
        priority = bucket.get("priority", "P2")
        keywords = bucket.get("keywords", [])
        expected_assets = bucket.get("expected_assets", [])

        print(f"\n=== {bucket_name} ({priority}) — {len(keywords)} keywords ===")

        for kw in keywords[:3]:  # First 3 keywords per bucket (API rate limits)
            print(f"  Searching: '{kw}' ...", end=" ", flush=True)
            results = await search_channels(kw, limit=5)
            print(f"{len(results)} found")

            for ch in results:
                username = ch.get("username", "")
                if not username or username in all_channels:
                    continue
                ch["source_keyword"] = kw
                ch["bucket"] = bucket_name
                ch["priority"] = priority
                ch["expected_assets"] = expected_assets
                all_channels[username] = ch

    return all_channels


def output_candidates(channels: dict):
    """Write discovered channels to discovery_candidates.json."""
    candidates_path = Path(__file__).resolve().parent.parent.parent / "configs" / "telegram" / "discovery_candidates.json"

    candidates = []
    for username, info in channels.items():
        candidates.append({
            "alias": username,
            "source": "telegram_search_api",
            "search_keyword": info.get("source_keyword", ""),
            "bucket": info.get("bucket", ""),
            "priority": info.get("priority", "P2"),
            "title": info.get("title", ""),
            "expected_assets": info.get("expected_assets", []),
            "expected_format": "unknown",
            "sample_limit": 200,
            "status": "DISCOVERY",
            "complete_setups": 0,
            "tp_only_count": 0,
            "parse_rate": 0,
            "candidate_score": 0,
            "next_action": "collect_sample",
        })

    with open(candidates_path, "w") as f:
        json.dump({"version": 1, "candidates": candidates}, f, indent=2)

    print(f"\n=== RESULTS ===")
    print(f"Discovered: {len(candidates)} channels")
    for bucket in sorted(set(c["bucket"] for c in candidates)):
        count = sum(1 for c in candidates if c["bucket"] == bucket)
        print(f"  {bucket}: {count}")
    print(f"\nWritten: {candidates_path}")


if __name__ == "__main__":
    if sys.platform == "linux" and os.path.exists("/opt/trading/.env"):
        # On admin-trading — run search
        channels = asyncio.run(discover_all())
        output_candidates(channels)
    else:
        print("ERROR: This script must run on admin-trading with Telethon session", file=sys.stderr)
        print("Run: scp this file to admin-trading and execute there", file=sys.stderr)
        sys.exit(1)
