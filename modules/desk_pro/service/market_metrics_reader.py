from __future__ import annotations
from pathlib import Path
from typing import List, Optional
import json

from modules.desk_pro.models import Metric

# Canonical read path: Data Center contract class view (neutral, no producer_id)
DC_MARKET_METRICS_VIEW = Path("data/data_center/views/market_metrics/latest.json")

# Legacy fallback: transitoire, conservé pendant la période post-migration
MARKET_METRICS_LEGACY = Path("data/deskpro/inputs/market_metrics/latest.json")

# Backward compat alias (monkeypatched by some tests via the old name)
MARKET_METRICS_LATEST = DC_MARKET_METRICS_VIEW

_FRESHNESS_QUALITY = {"fresh": 0.95, "stale": 0.5, "unknown": 0.3}
_METRIC_UNITS = {
    "open_interest": "USD",
    "funding_rate": "",
    "volume_futures": "USD",
    "long_short_ratio": "",
    "liquidations_long": "USD",
    "liquidations_short": "USD",
}


def _normalize_asset(symbol: str) -> str:
    for suffix in ("_UMCBL", "USDT", "USD"):
        if symbol.endswith(suffix):
            return symbol[: -len(suffix)]
    return symbol


def _read_from_path(p: Path) -> List[Metric]:
    """Read market_metrics.v1 from a specific path. Returns [] on any failure."""
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []

    if data.get("input_class") != "market_metrics.v1":
        return []

    provider_id = data.get("provider_id") or "unknown"
    symbol = data.get("symbol", "UNKNOWN")
    asset = _normalize_asset(symbol)
    freshness = data.get("freshness_state", "unknown")
    quality = _FRESHNESS_QUALITY.get(freshness, 0.3)

    coverage = data.get("provider_coverage", {})
    collectable = set(coverage.get("collectable_metrics", []))
    metrics_raw = data.get("metrics", {})

    result: List[Metric] = []
    for field_name, value in metrics_raw.items():
        if value is None or field_name not in collectable:
            continue
        result.append(
            Metric(
                source=provider_id,
                asset=asset,
                metric=field_name,
                value=value,
                unit=_METRIC_UNITS.get(field_name, ""),
                window="futures",
                quality=quality,
                notes=f"market_metrics.v1 {freshness}",
            )
        )
    return result


def read_market_metrics(path: Optional[Path] = None) -> List[Metric]:
    """Read market_metrics.v1 and return Desk Pro Metric objects.

    Default resolution (path=None):
      1. data/data_center/views/market_metrics/latest.json  (DC canonical)
      2. data/deskpro/inputs/market_metrics/latest.json      (legacy fallback)

    When path= is explicit, that path is used directly with no fallback.
    Returns [] if the file is absent, malformed, or carries no proven collectable
    metrics. Never raises — Desk Pro degrades gracefully when no collector has run.
    """
    if path is not None:
        return _read_from_path(path)
    # Default: DC view first, legacy fallback
    result = _read_from_path(DC_MARKET_METRICS_VIEW)
    if result:
        return result
    return _read_from_path(MARKET_METRICS_LEGACY)
