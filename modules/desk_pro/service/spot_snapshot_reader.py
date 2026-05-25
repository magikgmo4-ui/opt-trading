from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

SPOT_SNAPSHOT_LATEST = Path(
    "data/data_center/views/pair_market_snapshot/latest.json"
)


def read_spot_snapshot(path: Optional[Path] = None) -> Optional[dict]:
    """Read pair_market_snapshot.v1 from the Data Center consumer view.

    Default path: data/data_center/views/pair_market_snapshot/latest.json
    When path= is explicit, that path is used directly.

    Returns the payload dict if valid, None otherwise.
    Never raises. Never calls Binance API or any external service.
    Absent or malformed file → None (caller treats as missing).
    """
    p = path or SPOT_SNAPSHOT_LATEST
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    if data.get("entity_type") != "pair_market_snapshot":
        return None
    return data
