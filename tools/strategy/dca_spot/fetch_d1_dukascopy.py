#!/usr/bin/env python3
"""fetch_d1_dukascopy.py — Download XAUUSD D1 bars from Dukascopy tick data.

Streams tick data day-by-day: each day's 24 hourly bi5 files are fetched,
decoded, aggregated to one D1 bar, written to CSV, then discarded.

Peak RAM: <1MB (1 day of ticks, typically 3–8k ticks).
Output: D1 canonical CSV — same column format as M5 canonical (timeframe=D1).

vs M5 batch approach: 8× smaller file, no intermediate resample step needed,
suitable for strategies that operate solely on D1 bars (DCA spot).

Usage:
    python tools/strategy/dca_spot/fetch_d1_dukascopy.py \
        --start 2020-01-01 \
        --end   2023-12-31 \
        --out   data/market/xauusd_d1_2020_2023.csv

Estimated time: ~30 min for 4 years (35k HTTP requests at 50ms/req).
"""
from __future__ import annotations

import argparse
import csv
import datetime
import lzma
import struct
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

DUKASCOPY_URL = (
    "https://datafeed.dukascopy.com/datafeed/{symbol}/{year}/{month:02d}/{day:02d}/{hour:02d}h_ticks.bi5"
)
DIVISOR = 1000          # XAUUSD: 3 decimal places
SLEEP = 0.05            # 50ms between requests — stay under rate limit
SYMBOL = "XAUUSD"


def _fetch_hour(symbol: str, year: int, month: int, day: int, hour: int) -> bytes:
    url = DUKASCOPY_URL.format(symbol=symbol, year=year, month=month - 1, day=day, hour=hour)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except Exception:
        return b""


def _decode_bi5(raw_bytes: bytes, base_ms: int) -> list[tuple[float, float, float]]:
    """Returns list of (mid, ask, bid) tuples."""
    if not raw_bytes:
        return []
    try:
        raw = lzma.decompress(raw_bytes)
    except Exception:
        return []
    ticks = []
    for i in range(0, len(raw) - 19, 20):
        ms_off, ask_raw, bid_raw, _av, _bv = struct.unpack(">IIIff", raw[i : i + 20])
        ask = ask_raw / DIVISOR
        bid = bid_raw / DIVISOR
        ticks.append(((ask + bid) / 2, ask, bid))
    return ticks


def _fetch_day_d1(symbol: str, date: datetime.date) -> dict | None:
    """Fetch all 24 hourly files for one day, return single D1 OHLCV bar or None."""
    all_mids: list[float] = []
    last_ask = last_bid = None

    for hour in range(24):
        base_ms = int(
            datetime.datetime(date.year, date.month, date.day, hour,
                              tzinfo=datetime.timezone.utc).timestamp() * 1000
        )
        raw = _fetch_hour(symbol, date.year, date.month, date.day, hour)
        ticks = _decode_bi5(raw, base_ms)
        if ticks:
            all_mids.extend(t[0] for t in ticks)
            last_ask = ticks[-1][1]
            last_bid = ticks[-1][2]
        time.sleep(SLEEP)

    if not all_mids:
        return None

    spread = round(last_ask - last_bid, 5) if last_ask is not None else 0.0
    return {
        "timestamp": datetime.datetime(date.year, date.month, date.day,
                                       tzinfo=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S+00:00"),
        "open":   round(all_mids[0], 5),
        "high":   round(max(all_mids), 5),
        "low":    round(min(all_mids), 5),
        "close":  round(all_mids[-1], 5),
        "volume": len(all_mids),
        "bid":    round(last_bid, 5) if last_bid else None,
        "ask":    round(last_ask, 5) if last_ask else None,
        "spread": spread,
        "source": "dukascopy",
        "symbol": symbol,
        "timeframe": "D1",
    }


COLUMNS = ["timestamp", "open", "high", "low", "close", "volume",
           "bid", "ask", "spread", "source", "symbol", "timeframe"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2020-01-01")
    parser.add_argument("--end",   default="2023-12-31")
    parser.add_argument("--out",   required=True, help="Output CSV path")
    parser.add_argument("--symbol", default=SYMBOL)
    args = parser.parse_args()

    start = datetime.date.fromisoformat(args.start)
    end   = datetime.date.fromisoformat(args.end)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total_days = (end - start).days + 1
    est_min = total_days * 24 * SLEEP / 60
    print(f"[fetch] {args.symbol} D1  {args.start} → {args.end}  ({total_days} calendar days)")
    print(f"  timeframe : D1  (stream tick→D1 per day, peak RAM <1MB)")
    print(f"  estimated : {est_min:.0f} min  ({total_days * 24} HTTP requests at {SLEEP*1000:.0f}ms)")
    print(f"  output    : {out_path}")

    written = 0
    skipped = 0
    t0 = time.time()

    with open(out_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()

        date = start
        day_num = 0
        while date <= end:
            day_num += 1
            bar = _fetch_day_d1(args.symbol, date)
            if bar:
                writer.writerow(bar)
                fh.flush()
                written += 1
            else:
                skipped += 1

            if day_num % 30 == 0 or day_num == 1:
                elapsed = time.time() - t0
                pct = day_num / total_days * 100
                eta_s = elapsed / day_num * (total_days - day_num) if day_num > 0 else 0
                print(f"  [{pct:5.1f}%] {date}  bars={written}  skipped={skipped}"
                      f"  ETA {eta_s/60:.1f}min", flush=True)

            date += datetime.timedelta(days=1)

    elapsed = time.time() - t0
    print(f"\n[done] {written} D1 bars written  ({skipped} days empty — weekend/holiday)")
    print(f"  elapsed: {elapsed/60:.1f} min")
    print(f"  output : {out_path}  ({out_path.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
