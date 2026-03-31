from __future__ import annotations

import csv
import json
from datetime import datetime
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

    raise NotImplementedError(f"provider mode not yet implemented: {provider_mode}")


def get_price_at(symbol: str, ts: datetime, config: dict) -> Optional[float]:
    bars = get_m1_bars(symbol, ts, ts, config)
    if not bars:
        return None
    return bars[0].close
