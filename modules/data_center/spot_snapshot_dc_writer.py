from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_PRODUCER_ID = "collector_binance_spot"
_CONTRACT_CLASS = "pair_market_snapshot.v1"
_PRODUCER_BASE = Path("data/data_center/spot/collector_binance_spot")


def _atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp"
    ) as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def write_spot_snapshot_to_data_center(
    payload: dict,
    root: Optional[Path] = None,
    update_registry: bool = True,
) -> dict:
    """Write a pair_market_snapshot payload to the DC producer path and consumer view.

    Producer path:
      data/data_center/spot/collector_binance_spot/latest.json

    Consumer view (via write_pair_market_snapshot_view):
      data/data_center/views/pair_market_snapshot/latest.json
      data/data_center/views/pair_market_snapshot/by_symbol/<SYM>.json

    Optionally registers the write in the runtime registry.
    Never calls Binance API or any external service.
    """
    root = Path(root) if root is not None else _PROJECT_ROOT

    if payload.get("entity_type") != "pair_market_snapshot":
        raise ValueError(
            f"entity_type must be 'pair_market_snapshot', got '{payload.get('entity_type')}'"
        )

    producer_latest = root / _PRODUCER_BASE / "latest.json"
    _atomic_write_json(producer_latest, payload)

    from modules.data_center.pair_snapshot_view_writer import write_pair_market_snapshot_view
    view_result = write_pair_market_snapshot_view(payload, root=root)

    if update_registry:
        from modules.data_center.runtime_registry import update_producer_last_write
        update_producer_last_write(
            producer_id=_PRODUCER_ID,
            contract_class=_CONTRACT_CLASS,
            output_path=str(producer_latest),
            root=root,
            status="ok",
            evidence={
                "provider_id": payload.get("provider_id"),
                "run_id": payload.get("run_id"),
                "record_count": len(payload.get("records", [])),
                "generated_at": payload.get("generated_at"),
            },
        )

    return {
        "producer_latest": str(producer_latest),
        "view_latest": str(view_result["latest"]) if view_result else None,
        "by_symbol": {k: str(v) for k, v in (view_result.get("by_symbol") or {}).items()},
    }
