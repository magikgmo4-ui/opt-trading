"""
Perf Reader — HTTP wrapper around perf_app endpoints
GO_DESKPRO_VOICE_OPERATOR_01 — Lot B

Reads from:
  - /perf/summary   (trading KPIs)
  - /perf/open      (open trades)
  - /perf/trades    (trade history)

All functions return dicts. No trading logic.
"""
from __future__ import annotations
import json
import urllib.request
from typing import Any

PERF_BASE = "http://127.0.0.1:8010"


def _get(path: str, timeout: int = 8) -> dict:
    try:
        url = f"{PERF_BASE}{path}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return {"ok": False, "error": f"unreachable: {path}"}


def read_summary() -> dict:
    """Read trading KPIs: winrate, PnL, total trades, avg R, profit factor."""
    return _get("/perf/summary")


def read_open_trades() -> dict:
    """Read currently open trades."""
    return _get("/perf/open")


def read_trades(limit: int = 20, engine: str = "", status: str = "") -> dict:
    """Read trade history with optional filters."""
    params = []
    if limit:
        params.append(f"limit={limit}")
    if engine:
        params.append(f"engine={engine}")
    if status:
        params.append(f"status={status}")
    qs = "&".join(params)
    path = f"/perf/trades?{qs}" if qs else f"/perf/trades?limit={limit}"
    return _get(path)
