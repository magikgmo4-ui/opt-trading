#!/usr/bin/env python3
"""
Collect XAUUSD M1 BID candles from Dukascopy public datafeed.

Binary format (.bi5): LZMA-compressed, big-endian records of 24 bytes each:
  uint32 time_s  — seconds from UTC day start
  uint32 open    — price * 1000
  uint32 close   — price * 1000
  uint32 low     — price * 1000
  uint32 high    — price * 1000
  float32 volume — lots

Output CSV: timestamp,open,high,low,close,volume
  timestamps are timezone-aware (America/Montreal)
  prices rounded to 3 decimal places

Usage:
  python3 tools/trading_lab/collect_dukascopy_xauusd_m1.py \\
    --start 2026-04-07 --end 2026-04-11 \\
    --out state/trading_lab_v1/inputs/xauusd_m1_broker_20260407_20260411.csv
"""
from __future__ import annotations

import argparse
import csv
import lzma
import struct
import time as time_mod
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

SYMBOL = "XAUUSD"
PRICE_DIVISOR = 1000
TZ_LOCAL = ZoneInfo("America/Montreal")
TZ_UTC = timezone.utc
BASE_URL = "https://datafeed.dukascopy.com/datafeed"
REC_SIZE = 24
REQUEST_DELAY = 0.3


def build_url(symbol: str, d: date) -> str:
    return f"{BASE_URL}/{symbol}/{d.year}/{d.month - 1:02d}/{d.day:02d}/BID_candles_min_1.bi5"


def fetch_raw(url: str, timeout: int = 15) -> bytes | None:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        return None


def decode_day(raw: bytes, d: date) -> list[dict]:
    """Decompress and decode one day of bi5 candles. Returns [] on any error."""
    try:
        data = lzma.decompress(raw)
    except Exception:
        return []

    day_start = datetime(d.year, d.month, d.day, tzinfo=TZ_UTC)
    candles: list[dict] = []

    for offset in range(0, len(data) - REC_SIZE + 1, REC_SIZE):
        t_sec, a, b, c, e, vol = struct.unpack(">IIIIIf", data[offset:offset + REC_SIZE])
        # Field order confirmed empirically: time_s, open, close, low, high
        o  = a / PRICE_DIVISOR
        cl = b / PRICE_DIVISOR
        lo = c / PRICE_DIVISOR
        hi = e / PRICE_DIVISOR
        if hi < max(o, cl) or lo > min(o, cl) or hi < lo:
            continue
        ts_utc = day_start + timedelta(seconds=t_sec)
        ts_local = ts_utc.astimezone(TZ_LOCAL)
        candles.append({
            "ts": ts_local,
            "open":   round(o,   3),
            "high":   round(hi,  3),
            "low":    round(lo,  3),
            "close":  round(cl,  3),
            "volume": round(vol, 4),
        })

    return candles


def fetch_day(symbol: str, d: date) -> list[dict]:
    """Fetch and decode one UTC day. Returns [] if unavailable or malformed."""
    url = build_url(symbol, d)
    raw = fetch_raw(url)
    if not raw:
        return []
    return decode_day(raw, d)


def collect(
    symbol: str,
    start: date,
    end: date,
    out_path: Path,
    tz_out: ZoneInfo = TZ_LOCAL,
    delay: float = REQUEST_DELAY,
) -> dict:
    """
    Download M1 candles for UTC days [start, end+1], write CSV, return summary.

    end+1 captures midnight ET sessions that fall in the next UTC day.
    """
    all_candles: list[dict] = []
    current = start
    end_utc = end + timedelta(days=1)
    days_fetched = 0
    days_empty = 0

    while current <= end_utc:
        candles = fetch_day(symbol, current)
        if candles:
            all_candles.extend(candles)
            days_fetched += 1
        else:
            days_empty += 1
        time_mod.sleep(delay)
        current += timedelta(days=1)

    all_candles.sort(key=lambda x: x["ts"])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["timestamp", "open", "high", "low", "close", "volume"])
        for c in all_candles:
            writer.writerow([
                c["ts"].isoformat(timespec="seconds"),
                c["open"], c["high"], c["low"], c["close"], c["volume"],
            ])

    dates_covered = sorted({c["ts"].date().isoformat() for c in all_candles})
    return {
        "rows": len(all_candles),
        "days_fetched": days_fetched,
        "days_empty": days_empty,
        "dates_covered": dates_covered,
        "first_ts": all_candles[0]["ts"].isoformat(timespec="seconds") if all_candles else None,
        "last_ts":  all_candles[-1]["ts"].isoformat(timespec="seconds") if all_candles else None,
        "out": str(out_path),
    }


def main(argv: list[str] | None = None) -> int:
    import json
    parser = argparse.ArgumentParser(
        description="Collect XAUUSD M1 BID candles from Dukascopy public datafeed"
    )
    parser.add_argument("--symbol", default=SYMBOL, help="Instrument (default: XAUUSD)")
    parser.add_argument("--start",  required=True, help="Start date YYYY-MM-DD (UTC)")
    parser.add_argument("--end",    required=True, help="End date YYYY-MM-DD (UTC)")
    parser.add_argument(
        "--out", required=True,
        help="Output CSV path (recommended: state/trading_lab_v1/inputs/xauusd_m1_broker_<start>_<end>.csv)"
    )
    parser.add_argument("--delay", type=float, default=REQUEST_DELAY, help="Request delay in seconds")
    args = parser.parse_args(argv)

    start = date.fromisoformat(args.start)
    end   = date.fromisoformat(args.end)
    if end < start:
        print("Error: --end must be >= --start", flush=True)
        return 1

    out_path = Path(args.out)
    summary = collect(args.symbol, start, end, out_path, delay=args.delay)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
