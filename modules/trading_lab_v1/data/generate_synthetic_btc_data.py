#!/usr/bin/env python3
"""Generate synthetic BTC COIN-M 1H historical data for sweep testing."""
from __future__ import annotations

import json
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parent / "btcusd_coinm_backtest_data.jsonl"

# BTC annualized volatility ~60-80%, translate to 1H
# sigma_hourly = sigma_annual / sqrt(365*24) = 0.70 / sqrt(8760) ~ 0.0075
ANNUAL_VOL = 0.70
HOURLY_SIGMA = ANNUAL_VOL / math.sqrt(365 * 24)
DRIFT_PER_HOUR = 0.00002  # slight upward drift for BTC
START_PRICE = 40000.0
CANDLE_COUNT = 20000
START_DATE = datetime(2024, 1, 1, tzinfo=timezone.utc)
FUNDING_INTERVAL_H = 8
AVG_FUNDING_RATE = 0.00005  # typical positive funding


def _iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def generate() -> list[dict]:
    rng = random.Random(42)
    candles: list[dict] = []
    price = START_PRICE
    funding_rate = AVG_FUNDING_RATE
    dt = START_DATE

    for i in range(CANDLE_COUNT):
        # Geom Brownian: log return = drift + sigma * normal
        log_return = DRIFT_PER_HOUR + HOURLY_SIGMA * rng.gauss(0, 1)
        price *= math.exp(log_return)

        # Add occasional volatility spikes (crash/pump)
        if rng.random() < 0.001:
            price *= 1.0 + rng.choice([-0.08, -0.05, 0.10, 0.07])

        # Simulate OHLC around the closing price
        wick = price * HOURLY_SIGMA * abs(rng.gauss(0, 2))
        high = price + wick
        low = price - wick * rng.uniform(0.5, 3.0)
        open_p = price * (1.0 + rng.uniform(-0.003, 0.003))

        # Funding settlement every 8h at 00, 08, 16 UTC
        hour = dt.hour
        is_settlement = (hour % FUNDING_INTERVAL_H == 0)
        if is_settlement:
            funding_rate = rng.uniform(-0.0003, 0.0003)  # bounded funding

        candle = {
            "ts": _iso(dt),
            "open": round(open_p, 1),
            "high": round(high, 1),
            "low": round(low, 1),
            "close": round(price, 1),
            "volume_btc": round(abs(rng.gauss(8, 3)), 4),
            "volume_usd": round(price * abs(rng.gauss(8, 3)), 2),
            "mark_price": round(price, 1),   # proxy
            "index_price": round(price, 1),  # proxy
            "funding_rate": round(funding_rate, 6) if is_settlement else None,
            "funding_settled": is_settlement,
        }
        candles.append(candle)
        dt += timedelta(hours=1)

    return candles


def main():
    print(f"Generating {CANDLE_COUNT} synthetic BTC COIN-M 1H candles...")
    print(f"Params: annual_vol={ANNUAL_VOL}, drift_h={DRIFT_PER_HOUR}, "
          f"start_price={START_PRICE}, sigma_h={HOURLY_SIGMA:.6f}")
    candles = generate()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        for c in candles:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    funded = sum(1 for c in candles if c["funding_settled"])
    first_p = candles[0]["close"]
    last_p = candles[-1]["close"]
    pct = (last_p - first_p) / first_p * 100
    print(f"Done: {len(candles)} candles, {funded} funding settlements")
    print(f"Price: {first_p} -> {last_p} ({pct:+.1f}%)")
    print(f"Saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
