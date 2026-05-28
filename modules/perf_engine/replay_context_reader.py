from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


_PROJECT_ROOT = Path(__file__).resolve().parent.parent
MARKET_METRICS_HISTORY = Path("data/data_center/views/market_metrics/history")


def read_replay_context(
    symbol: str,
    *,
    root: Optional[Path] = None,
    history_dir: Optional[Path] = None,
) -> list[dict]:
    resolved_root = Path(root) if root is not None else _PROJECT_ROOT
    base = history_dir if history_dir is not None else resolved_root / MARKET_METRICS_HISTORY / symbol
    if not base.exists():
        raise FileNotFoundError(str(base))

    payloads: list[dict] = []
    for path in sorted(base.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise ValueError(f"invalid JSON in {path}") from exc
        if not isinstance(data, dict):
            raise ValueError(f"invalid payload in {path}")
        if data.get("input_class") != "market_metrics.v1":
            raise ValueError(f"input_class must be 'market_metrics.v1' in {path}")
        if data.get("symbol") != symbol:
            raise ValueError(f"symbol mismatch in {path}")
        payloads.append(data)
    return payloads
