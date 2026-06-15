"""
Voice Operator Read API Client
GO_DESKPRO_VOICE_OPERATOR_01 — Lot C

HTTP client that calls the /read/* endpoints and returns structured results.
Works against localhost or remote voice_operator API.
"""
from __future__ import annotations
import json
import urllib.request
from typing import Any

DEFAULT_BASE = "http://127.0.0.1:8020"


def _get(url: str, timeout: int = 10) -> dict:
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        return {"ok": False, "error": str(e), "one_line": "Service voix indisponible"}


def call(endpoint: str, params: dict | None = None, base: str = DEFAULT_BASE) -> dict:
    """Call a /read/* endpoint and return its JSON payload.

    Args:
        endpoint: e.g. "/read/system", "/read/setup"
        params: optional query params e.g. {"symbol": "BTC", "limit": 10}
        base: base URL of the voice operator API

    Returns:
        JSON dict with at minimum {"one_line": "..."} 
    """
    url = f"{base}{endpoint}"
    if params:
        qs_parts = []
        for k, v in params.items():
            qs_parts.append(f"{k}={urllib.request.quote(str(v))}")
        url += "?" + "&".join(qs_parts)
    return _get(url)
