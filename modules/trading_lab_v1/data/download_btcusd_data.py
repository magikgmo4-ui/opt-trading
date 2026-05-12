#!/usr/bin/env python3
"""Download BTC COIN-M 1H historical data from Bitget public API."""
from __future__ import annotations

import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_BASE = "https://api.bitget.com/api/v2/mix/market"
CANDLES_URL = f"{API_BASE}/candles"
FUNDING_URL = f"{API_BASE}/history-fund-rate"
SYMBOL = "BTCUSD"
PRODUCT = "COIN-FUTURES"
GRANULARITY = "1H"
OUT_PATH = Path(__file__).resolve().parent / "btcusd_coinm_backtest_data.jsonl"
CANDLE_LIMIT = 200
FUNDING_LIMIT = 100
SLEEP = 0.2  # seconds between requests (rate limit friendly)


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "opt-trading/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def _iso(ts_ms: int) -> str:
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def download_candles(start_ms: int, end_ms: int) -> list[dict]:
    candles: list[dict] = []
    cursor = start_ms
    total = 0
    while cursor < end_ms:
        url = (f"{CANDLES_URL}?symbol={SYMBOL}&productType={PRODUCT}"
               f"&granularity={GRANULARITY}&startTime={cursor}&endTime={end_ms}"
               f"&limit={CANDLE_LIMIT}")
        data = _get(url)
        rows = data.get("data", [])
        if not rows:
            break
        for row in rows:
            ts_ms = int(row[0])
            candles.append({
                "ts": _iso(ts_ms),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume_btc": float(row[5]),
                "volume_usd": float(row[6]),
                "mark_price": float(row[4]),   # proxy: LastPrice
                "index_price": float(row[4]),  # proxy: LastPrice
                "funding_rate": None,
                "funding_settled": False,
            })
        total += len(rows)
        cursor = int(rows[-1][0]) + 1
        print(f"  candles: {total} rows (latest: {_iso(int(rows[-1][0]))})")
        time.sleep(SLEEP)
    print(f"  candles done: {total} total")
    return sorted(candles, key=lambda c: c["ts"])


def download_funding() -> dict[str, float]:
    """Return dict mapping funding_time_iso -> funding_rate."""
    rates: dict[str, float] = {}
    page = 1
    while True:
        url = (f"{FUNDING_URL}?symbol={SYMBOL}&productType={PRODUCT}"
               f"&pageSize={FUNDING_LIMIT}&pageNo={page}")
        data = _get(url)
        rows = data.get("data", [])
        if not rows:
            break
        for row in rows:
            ts = _iso(int(row["fundingTime"]))
            rates[ts] = float(row["fundingRate"])
        print(f"  funding: page {page}, {len(rows)} rows, total {len(rates)}")
        if len(rows) < FUNDING_LIMIT:
            break
        page += 1
        time.sleep(SLEEP)
    print(f"  funding done: {len(rates)} total settlements")
    return rates


def merge(candles: list[dict], funding: dict[str, float]) -> list[dict]:
    for c in candles:
        ts_hour = c["ts"][:13]  # e.g. "2025-01-01T08"
        for ft, rate in funding.items():
            ft_hour = ft[:13]
            if ft_hour == ts_hour:
                c["funding_rate"] = rate
                c["funding_settled"] = True
                break
    return candles


def main():
    # 2025-01-01 to now
    start = int(datetime(2025, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
    end = int(datetime.now(tz=timezone.utc).timestamp() * 1000)

    print(f"Downloading BTC COIN-M 1H data from {_iso(start)} to {_iso(end)}")
    print(f"Output: {OUT_PATH}")

    print("\n[1/3] Downloading candles...")
    candles = download_candles(start, end)

    print("\n[2/3] Downloading funding rates...")
    funding = download_funding()

    print("\n[3/3] Merging...")
    merged = merge(candles, funding)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        for c in merged:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    funded = sum(1 for c in merged if c["funding_settled"])
    print(f"\nDone: {len(merged)} candles, {funded} with funding, saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
