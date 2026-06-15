"""
LocalCMS Reader — HTTP wrapper around LocalCMS endpoints
GO_DESKPRO_VOICE_OPERATOR_01 — Lot B

Reads from:
  - /cms/signals/summary  (Telegram signal summary)
  - /cms/spacex/json      (SpaceX data)
  - /cms/menu/state       (menu state)
  - /cms/health           (health check)

All functions return dicts. No trading logic.
"""
from __future__ import annotations
import json
import urllib.request
from typing import Any

CMS_BASE = "http://127.0.0.1:8010"


def _get(path: str, timeout: int = 8) -> dict:
    try:
        url = f"{CMS_BASE}{path}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return {"ok": False, "error": f"unreachable: {path}"}


def read_signals_summary() -> dict:
    """Read Telegram signal summary."""
    return _get("/cms/signals/summary")


def read_signals(channel: str = "", pair: str = "", direction: str = "") -> dict:
    """Read filtered signal list."""
    params = []
    if channel:
        params.append(f"channel={channel}")
    if pair:
        params.append(f"pair={pair}")
    if direction:
        params.append(f"direction={direction}")
    qs = "&".join(params)
    path = f"/cms/signals?{qs}" if qs else "/cms/signals"
    return _get(path)


def read_spacex_json() -> dict:
    """Read SpaceX JSON data from LocalCMS."""
    return _get("/cms/spacex/json")


def read_menu_state() -> dict:
    """Read navigation menu state."""
    return _get("/cms/menu/state")
