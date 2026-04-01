from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .models import Bar
from .config import MODULE_DIR


FIXTURES_DIR = MODULE_DIR / "fixtures"


def _load_fixture(name: str) -> list[dict]:
    path = FIXTURES_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"fixture not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _load_csv(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"csv not found: {p}")
    rows = []
    with open(p, "r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append({
                "ts_open": row["ts_open"],
                "ts_close": row["ts_close"],
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "timeframe": row.get("timeframe", "M1"),
            })
    return rows


def _row_to_bar(row: dict) -> Bar:
    return Bar(
        ts_open=datetime.fromisoformat(row["ts_open"]),
        ts_close=datetime.fromisoformat(row["ts_close"]),
        open=row["open"],
        high=row["high"],
        low=row["low"],
        close=row["close"],
        timeframe=row.get("timeframe", "M1"),
    )


def _filter_and_sort(bars: list[Bar], start_ts: datetime, end_ts: datetime) -> list[Bar]:
    bars = sorted(bars, key=lambda b: b.ts_open)
    return [b for b in bars if start_ts <= b.ts_open <= end_ts]


def _load_ccxt(exchange_id: str, ccxt_symbol: str, timeframe: str,
               start_ts: datetime, end_ts: datetime, limit: int) -> list[Bar]:
    try:
        import ccxt
    except ImportError:
        raise ImportError(
            "ccxt is required for provider.mode=ccxt. "
            "Install with: pip install ccxt"
        )

    exchange_class = getattr(ccxt, exchange_id, None)
    if exchange_class is None:
        raise ValueError(f"unknown ccxt exchange: {exchange_id}")

    exchange = exchange_class({"enableRateLimit": True})

    since_ms = int(start_ts.timestamp() * 1000)
    end_ms = int(end_ts.timestamp() * 1000)

    all_ohlcv = []
    while since_ms < end_ms:
        ohlcv = exchange.fetch_ohlcv(ccxt_symbol, timeframe, since=since_ms, limit=limit)
        if not ohlcv:
            break
        all_ohlcv.extend(ohlcv)
        since_ms = ohlcv[-1][0] + 1

    bars = []
    for candle in all_ohlcv:
        ts_open_ms, o, h, l, c, _v = candle
        ts_open = datetime.fromtimestamp(ts_open_ms / 1000, tz=timezone.utc)
        tf_minutes = _tf_to_minutes(timeframe)
        ts_close = datetime.fromtimestamp((ts_open_ms + tf_minutes * 60 * 1000) / 1000, tz=timezone.utc)
        bars.append(Bar(
            ts_open=ts_open,
            ts_close=ts_close,
            open=o,
            high=h,
            low=l,
            close=c,
            timeframe=timeframe,
        ))

    return bars


def _tf_to_minutes(timeframe: str) -> int:
    if timeframe.endswith("m"):
        return int(timeframe[:-1])
    if timeframe.endswith("h"):
        return int(timeframe[:-1]) * 60
    if timeframe.endswith("d"):
        return int(timeframe[:-1]) * 1440
    return 1


def get_m1_bars(symbol: str, start_ts: datetime, end_ts: datetime, config: dict) -> list[Bar]:
    provider_mode = config.get("provider", {}).get("mode", "fixture")

    if provider_mode == "fixture":
        fixture_file = config.get("provider", {}).get("fixture_file")
        if fixture_file is None:
            fixture_file = "fixture_no_event.json"
        rows = _load_fixture(fixture_file)
        bars = [_row_to_bar(r) for r in rows]
        return _filter_and_sort(bars, start_ts, end_ts)

    if provider_mode == "csv_replay":
        csv_path = config.get("provider", {}).get("csv_replay", {}).get("path")
        if csv_path is None:
            raise ValueError("provider.mode=csv_replay requires provider.csv_replay.path")
        csv_path = MODULE_DIR / csv_path
        rows = _load_csv(csv_path)
        bars = [_row_to_bar(r) for r in rows]
        return _filter_and_sort(bars, start_ts, end_ts)

    if provider_mode == "ccxt":
        ccxt_cfg = config.get("provider", {}).get("ccxt", {})
        exchange_id = ccxt_cfg.get("exchange", "binance")
        ccxt_symbol = ccxt_cfg.get("symbol", "XAUUSDT")
        timeframe = ccxt_cfg.get("timeframe", "1m")
        limit = ccxt_cfg.get("limit", 500)
        bars = _load_ccxt(exchange_id, ccxt_symbol, timeframe, start_ts, end_ts, limit)
        return _filter_and_sort(bars, start_ts, end_ts)

    raise NotImplementedError(f"provider mode not yet implemented: {provider_mode}")


def get_price_at(symbol: str, ts: datetime, config: dict) -> Optional[float]:
    bars = get_m1_bars(symbol, ts, ts, config)
    if not bars:
        return None
    return bars[0].close
