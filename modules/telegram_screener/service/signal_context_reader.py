from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SIGNAL_CONTEXT_LATEST = Path("data/data_center/views/market_metrics/latest.json")


def read_signal_context(path: Optional[Path] = None) -> Optional[dict]:
    target = path or (_PROJECT_ROOT / SIGNAL_CONTEXT_LATEST)
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
    return {
        "provider_id": data.get("provider_id"),
        "symbol": data.get("symbol"),
        "freshness_state": data.get("freshness_state"),
        "produced_at": data.get("produced_at"),
        "metrics": data.get("metrics", {}),
        "collectable_metrics": data.get("provider_coverage", {}).get("collectable_metrics", []),
        "warnings": data.get("warnings", []),
        "payload": data,
    }
