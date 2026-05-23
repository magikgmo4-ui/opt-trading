from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Optional, Union

from modules.derivatives_collector.app.market_metrics_v1 import MarketMetricsV1

_MODULE_DIR = Path(__file__).resolve().parent.parent   # modules/derivatives_collector
_PROJECT_ROOT = _MODULE_DIR.parent.parent              # opt-trading root

# Canonical Data Center paths (primary write target)
_DC_DERIVATIVES_BASE = Path("data/data_center/derivatives")

# Legacy / view paths (secondary, backward compat)
_COLLECTORS_LATEST = Path("data/collectors/derivatives/latest.json")
_COLLECTORS_BY_SYMBOL = Path("data/collectors/derivatives/cache/by_symbol")
_DESKPRO_LATEST = Path("data/deskpro/inputs/market_metrics/latest.json")
_DESKPRO_BY_SYMBOL = Path("data/deskpro/inputs/market_metrics/by_symbol")

# Maps market_metrics.v1 provider_id to Data Center producer_id
_PROVIDER_TO_PRODUCER_ID: dict[str, str] = {
    "bitget": "derivatives_collector__bitget",
    "binance_derivatives": "derivatives_collector__binance",
    "binance": "derivatives_collector__binance",
}


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp"
    ) as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def _to_dict(payload: Union[MarketMetricsV1, dict]) -> dict:
    if isinstance(payload, MarketMetricsV1):
        return payload.to_dict()
    return dict(payload)


def _validate_input_class(d: dict) -> None:
    if d.get("input_class") != "market_metrics.v1":
        raise ValueError(
            f"input_class must be 'market_metrics.v1', got '{d.get('input_class')}'"
        )


def _is_not_proven_runtime_adapter(d: dict) -> bool:
    return (
        d.get("provider_coverage", {}).get("status") == "not_proven_runtime_adapter"
    )


def _resolve_producer_id(d: dict) -> Optional[str]:
    """Return Data Center producer_id for the given payload, or None if unknown."""
    return _PROVIDER_TO_PRODUCER_ID.get(d.get("provider_id", ""))


# ---------------------------------------------------------------------------
# Canonical Data Center writer
# ---------------------------------------------------------------------------

def write_market_metrics_to_data_center(
    payload: Union[MarketMetricsV1, dict],
    root: Optional[Path] = None,
) -> Optional[dict]:
    """Write market_metrics.v1 to Data Center canonical paths.

    Writes to:
      data/data_center/derivatives/<producer_id>/latest.json
      data/data_center/derivatives/<producer_id>/cache/by_symbol/<SYMBOL>.json

    Returns dict with 'latest' and 'by_symbol' Path values, or None if
    provider is not_proven_runtime_adapter or producer_id is unknown.
    Raises ValueError for invalid input_class.
    """
    root = Path(root) if root is not None else _PROJECT_ROOT
    d = _to_dict(payload)
    _validate_input_class(d)
    if _is_not_proven_runtime_adapter(d):
        return None
    producer_id = _resolve_producer_id(d)
    if producer_id is None:
        return None
    symbol = d.get("symbol", "UNKNOWN")
    base = root / _DC_DERIVATIVES_BASE / producer_id
    latest_dest = base / "latest.json"
    by_symbol_dest = base / "cache" / "by_symbol" / f"{symbol}.json"
    _atomic_write_json(latest_dest, d)
    _atomic_write_json(by_symbol_dest, d)
    return {"latest": latest_dest, "by_symbol": by_symbol_dest}


# ---------------------------------------------------------------------------
# Full publish pipeline
# ---------------------------------------------------------------------------

def publish_market_metrics(
    payload: Union[MarketMetricsV1, dict],
    root: Optional[Path] = None,
    include_legacy_mirror: bool = True,
    include_deskpro_view: bool = True,
) -> Optional[dict]:
    """Full publish pipeline: Data Center canonical + optional legacy mirrors.

    Write order:
      1. data/data_center/derivatives/<producer_id>/ (canonical — always)
      2. data/collectors/derivatives/ (legacy mirror — optional)
      3. data/deskpro/inputs/market_metrics/ (Desk Pro view — optional, migration_needed)

    Returns dict with keys 'data_center', 'legacy', 'deskpro' (each a sub-dict
    with 'latest' and 'by_symbol' Path values, or None if skipped/not_proven).
    Returns None if provider is not_proven_runtime_adapter.
    Raises ValueError for invalid input_class.
    """
    root = Path(root) if root is not None else _PROJECT_ROOT
    d = _to_dict(payload)
    _validate_input_class(d)
    if _is_not_proven_runtime_adapter(d):
        return None

    dc = write_market_metrics_to_data_center(d, root=root)

    legacy = None
    if include_legacy_mirror:
        latest_p = write_market_metrics_latest(d, root=root)
        by_sym_p = write_market_metrics_by_symbol(d, root=root)
        if latest_p is not None:
            legacy = {"latest": latest_p, "by_symbol": by_sym_p}

    deskpro = None
    if include_deskpro_view:
        deskpro = publish_market_metrics_for_deskpro(d, root=root)

    return {"data_center": dc, "legacy": legacy, "deskpro": deskpro}


# ---------------------------------------------------------------------------
# Legacy / view writers (backward compat — data/collectors/ and data/deskpro/)
# ---------------------------------------------------------------------------

def write_market_metrics_latest(
    payload: Union[MarketMetricsV1, dict],
    root: Optional[Path] = None,
) -> Optional[Path]:
    """Legacy view: write market_metrics.v1 to data/collectors/derivatives/latest.json.

    Not the canonical Data Center path. Kept for backward compat with consumers
    that have not yet migrated to data/data_center/.
    Returns the path written, or None if provider is not_proven_runtime_adapter.
    Raises ValueError for invalid input_class.
    """
    root = Path(root) if root is not None else _PROJECT_ROOT
    d = _to_dict(payload)
    _validate_input_class(d)
    if _is_not_proven_runtime_adapter(d):
        return None
    dest = root / _COLLECTORS_LATEST
    _atomic_write_json(dest, d)
    return dest


def write_market_metrics_by_symbol(
    payload: Union[MarketMetricsV1, dict],
    root: Optional[Path] = None,
) -> Optional[Path]:
    """Legacy view: write to data/collectors/derivatives/cache/by_symbol/<SYMBOL>.json.

    Not the canonical Data Center path. Kept for backward compat.
    Returns the path written, or None if provider is not_proven_runtime_adapter.
    Raises ValueError for invalid input_class.
    """
    root = Path(root) if root is not None else _PROJECT_ROOT
    d = _to_dict(payload)
    _validate_input_class(d)
    if _is_not_proven_runtime_adapter(d):
        return None
    symbol = d.get("symbol", "UNKNOWN")
    dest = root / _COLLECTORS_BY_SYMBOL / f"{symbol}.json"
    _atomic_write_json(dest, d)
    return dest


def publish_market_metrics_for_deskpro(
    payload: Union[MarketMetricsV1, dict],
    root: Optional[Path] = None,
) -> Optional[dict]:
    """Desk Pro view: write to data/deskpro/inputs/market_metrics/.

    This is a migration_needed consumer view, not the canonical Data Center path.
    Desk Pro currently reads from this path; migration to data/data_center/ is pending.
    Returns dict with 'latest' and 'by_symbol' Path values, or None if
    provider is not_proven_runtime_adapter. Raises ValueError for invalid input_class.
    """
    root = Path(root) if root is not None else _PROJECT_ROOT
    d = _to_dict(payload)
    _validate_input_class(d)
    if _is_not_proven_runtime_adapter(d):
        return None
    symbol = d.get("symbol", "UNKNOWN")
    latest_dest = root / _DESKPRO_LATEST
    by_symbol_dest = root / _DESKPRO_BY_SYMBOL / f"{symbol}.json"
    _atomic_write_json(latest_dest, d)
    _atomic_write_json(by_symbol_dest, d)
    return {"latest": latest_dest, "by_symbol": by_symbol_dest}
