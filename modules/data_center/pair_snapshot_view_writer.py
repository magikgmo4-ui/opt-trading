from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_DC_VIEWS_BASE = Path("data/data_center/views")


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp"
    ) as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def _validate_entity_type(d: dict) -> None:
    if d.get("entity_type") != "pair_market_snapshot":
        raise ValueError(
            f"entity_type must be 'pair_market_snapshot', got '{d.get('entity_type')}'"
        )


def write_pair_market_snapshot_view(
    payload: dict,
    root: Optional[Path] = None,
) -> Optional[dict]:
    """Write pair_market_snapshot to data/data_center/views/pair_market_snapshot/.

    Neutral consumer path — decoupled from any specific producer_id.

    Writes to:
      data/data_center/views/pair_market_snapshot/latest.json       (full payload)
      data/data_center/views/pair_market_snapshot/by_symbol/<SYM>.json  (per record)

    Returns dict with:
      'latest': Path to latest.json
      'by_symbol': dict mapping pair_symbol → Path for each record written

    Raises ValueError for invalid entity_type.
    """
    root = Path(root) if root is not None else _PROJECT_ROOT
    d = dict(payload)
    _validate_entity_type(d)

    base = root / _DC_VIEWS_BASE / "pair_market_snapshot"
    latest_dest = base / "latest.json"
    _atomic_write_json(latest_dest, d)

    by_symbol: dict[str, Path] = {}
    meta = {
        "contract_version": d.get("contract_version"),
        "schema_version": d.get("schema_version"),
        "module_id": d.get("module_id"),
        "provider_id": d.get("provider_id"),
        "run_id": d.get("run_id"),
        "generated_at": d.get("generated_at"),
        "entity_type": d.get("entity_type"),
    }
    for record in d.get("records", []):
        symbol = record.get("pair_symbol", "UNKNOWN")
        by_symbol_doc = {**meta, **record}
        dest = base / "by_symbol" / f"{symbol}.json"
        _atomic_write_json(dest, by_symbol_doc)
        by_symbol[symbol] = dest

    return {"latest": latest_dest, "by_symbol": by_symbol}
