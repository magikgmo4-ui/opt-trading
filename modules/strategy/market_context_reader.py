from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MARKET_CONTEXT_BY_SYMBOL = Path("data/data_center/views/market_metrics/by_symbol")


def read_market_context(
    symbol: str,
    *,
    root: Optional[Path] = None,
    path: Optional[Path] = None,
) -> Optional[dict]:
    resolved_root = Path(root) if root is not None else _PROJECT_ROOT
    target = path if path is not None else resolved_root / MARKET_CONTEXT_BY_SYMBOL / f"{symbol}.json"
    if not target.exists():
        return None
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    if data.get("input_class") != "market_metrics.v1":
        return None
    if data.get("symbol") != symbol:
        return None
    return data
