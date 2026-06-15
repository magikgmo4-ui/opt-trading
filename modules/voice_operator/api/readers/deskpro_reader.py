"""
DeskPro Reader — HTTP wrapper around DeskPro endpoints
GO_DESKPRO_VOICE_OPERATOR_01 — Lot B

Reads from:
  - /desk/spacex/command-center  (primary SPCX data)
  - /desk/status                 (pipeline health)
  - /desk/alerts                 (alert state)
  - /desk/spacex/snapshot        (full scored snapshot)

All functions return dicts. No trading logic.
"""
from __future__ import annotations
import json
import urllib.request
from typing import Any

DESKPRO_BASE = "http://127.0.0.1:8010"


def _get(path: str, timeout: int = 8) -> dict:
    try:
        url = f"{DESKPRO_BASE}{path}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception:
        return {"ok": False, "error": f"unreachable: {path}"}


def read_command_center() -> dict:
    """Read SPCX command center — richest single SPCX endpoint."""
    return _get("/desk/spacex/command-center")


def read_status() -> dict:
    """Read full pipeline status — all services health."""
    return _get("/desk/status")


def read_alerts(limit: int = 10) -> dict:
    """Read recent DeskPro alerts."""
    return _get(f"/desk/alerts?limit={limit}")


def read_snapshot() -> dict:
    """Read latest scored SPCX snapshot."""
    return _get("/desk/spacex/snapshot")


def read_snapshot_file() -> dict:
    """Read snapshot directly from file (offline fallback)."""
    from pathlib import Path
    p = Path(__file__).resolve().parents[3] / "data" / "ipo" / "spacex" / "scored" / "latest_snapshot.json"
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            pass
    return {}
