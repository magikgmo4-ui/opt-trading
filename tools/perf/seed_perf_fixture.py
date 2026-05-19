"""
Seed perf.db with simulated trades via POST /perf/event.
Usage: python3 tools/perf/seed_perf_fixture.py [--base http://127.0.0.1:8010]
Requires Desk Pro running on port 8010.
"""
from __future__ import annotations
import json, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta

BASE = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith("http") else "http://127.0.0.1:8010"
EVENT_URL = f"{BASE}/perf/event"

now = datetime.now(timezone.utc)

TRADES = [
    {"engine": "FIXTURE_SEED", "symbol": "BTCUSDT", "side": "LONG",  "entry": 45000, "stop": 44000, "qty": 0.1,  "risk_usd": 100},
    {"engine": "FIXTURE_SEED", "symbol": "BTCUSDT", "side": "SHORT", "entry": 48000, "stop": 48500, "qty": 0.2,  "risk_usd": 100},
    {"engine": "FIXTURE_SEED", "symbol": "ETHUSDT", "side": "LONG",  "entry": 3200,  "stop": 3150,  "qty": 1.0,  "risk_usd": 50},
    {"engine": "FIXTURE_SEED", "symbol": "SOLUSDT", "side": "LONG",  "entry": 120,   "stop": 115,   "qty": 5.0,  "risk_usd": 25},
    {"engine": "FIXTURE_SEED", "symbol": "BTCUSDT", "side": "LONG",  "entry": 50000, "stop": 49500, "qty": 0.15, "risk_usd": 75},
]

CLOSES = [
    {"trade_id": None, "exit": 46500},  # will fill trade_id from OPEN response
    {"trade_id": None, "exit": 47800},
    {"trade_id": None, "exit": 3400},
    {"trade_id": None, "exit": 130},
]

def post_event(payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    try:
        req = urllib.request.Request(EVENT_URL, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  ERROR {e.code}: {body}")
        return {}
    except Exception as e:
        print(f"  ERROR: {e}")
        return {}

def main():
    print(f"Seeding {len(TRADES)} trades via {EVENT_URL}")
    trade_ids: list[str] = []

    for i, t in enumerate(TRADES):
        mins_ago = (len(TRADES) - i) * 30
        ts = (now - timedelta(minutes=mins_ago)).isoformat()
        payload = {
            "type": "OPEN",
            "ts": ts,
            "engine": t["engine"],
            "symbol": t["symbol"],
            "side": t["side"],
            "entry": t["entry"],
            "stop": t["stop"],
            "qty": t["qty"],
            "risk_usd": t["risk_usd"],
        }
        print(f"  OPEN {t['symbol']} {t['side']} @ {t['entry']}...", end=" ")
        resp = post_event(payload)
        tid = resp.get("trade_id")
        if tid:
            trade_ids.append(tid)
            print(f"trade_id={tid}")
        else:
            trade_ids.append(None)
            print("no trade_id")
        time.sleep(0.2)

    for i, c in enumerate(CLOSES):
        if i >= len(trade_ids) or not trade_ids[i]:
            print(f"  SKIP CLOSE #{i} (no open trade)")
            continue
        mins_ago = (len(TRADES) - i) * 10
        ts = (now - timedelta(minutes=mins_ago)).isoformat()
        payload = {
            "type": "CLOSE",
            "ts": ts,
            "trade_id": trade_ids[i],
            "exit": c["exit"],
        }
        print(f"  CLOSE trade {trade_ids[i]} @ {c['exit']}...", end=" ")
        resp = post_event(payload)
        print(f"ok" if resp.get("ok") else f"response: {resp}")

    print("\nDone. Check /perf/summary, /perf/open, /perf/equity, /perf/trades")

if __name__ == "__main__":
    main()
