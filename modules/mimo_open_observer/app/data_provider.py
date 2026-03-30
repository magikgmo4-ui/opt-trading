from __future__ import annotations

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


def get_m1_bars(symbol: str, start_ts: datetime, end_ts: datetime, config: dict) -> list[Bar]:
    provider_mode = config.get("provider", {}).get("mode", "fixture")
    if provider_mode != "fixture":
        raise NotImplementedError(f"provider mode not yet implemented: {provider_mode}")

    fixture_file = config.get("provider", {}).get("fixture_file")
    if fixture_file is None:
        fixture_file = "fixture_no_event.json"

    rows = _load_fixture(fixture_file)
    bars = [_row_to_bar(r) for r in rows]
    bars = sorted(bars, key=lambda b: b.ts_open)
    bars = [b for b in bars if start_ts <= b.ts_open <= end_ts]
    return bars


def get_price_at(symbol: str, ts: datetime, config: dict) -> Optional[float]:
    bars = get_m1_bars(symbol, ts, ts, config)
    if not bars:
        return None
    return bars[0].close
