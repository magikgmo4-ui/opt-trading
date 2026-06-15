"""Data Center publisher for stock_true_value scores.

Publishes outputs/stock_true_value/latest/scores.json →
  data/data_center/views/spacex_true_value.v1/latest.json
  data/data_center/views/spacex_true_value.v1/by_symbol/<TICKER>.json

Writes to runtime registry via update_producer_last_write.
Mode: manual trigger via production_runtime.py pipeline.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCORES_PATH = PROJECT_ROOT / "outputs" / "stock_true_value" / "latest" / "scores.json"
DC_VIEW_DIR = PROJECT_ROOT / "data" / "data_center" / "views" / "spacex_true_value.v1"
PRODUCER_ID = "spacex_true_value"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def publish_to_data_center() -> dict[str, Any]:
    """Read scores.json, write to data_center views, update registry."""
    if not SCORES_PATH.exists():
        return {"ok": False, "error": "scores.json not found"}

    scores = json.loads(SCORES_PATH.read_text())
    items = scores.get("items", [])

    # Write latest.json
    DC_VIEW_DIR.mkdir(parents=True, exist_ok=True)
    latest_payload = {
        "written_at": _utc_now(),
        "producer_id": PRODUCER_ID,
        "model_version": scores.get("model_version", "v1"),
        "items_count": len(items),
        "summary": scores.get("summary", {}),
        "items": items,
    }
    (DC_VIEW_DIR / "latest.json").write_text(json.dumps(latest_payload, indent=2))

    # Write by_symbol/<TICKER>.json
    by_symbol_dir = DC_VIEW_DIR / "by_symbol"
    by_symbol_dir.mkdir(parents=True, exist_ok=True)
    for it in items:
        ticker = it.get("ticker", "?")
        (by_symbol_dir / f"{ticker}.json").write_text(json.dumps(it, indent=2))

    # Update runtime registry
    try:
        from modules.data_center.runtime_registry import update_producer_last_write
        update_producer_last_write(
            producer_id=PRODUCER_ID,
            contract_class="spacex_true_value.v1",
            output_path=str(DC_VIEW_DIR / "latest.json"),
            status="ok",
            evidence={"items_count": len(items), "asof": scores.get("asof", "")},
        )
    except Exception as e:
        return {"ok": True, "registry_warning": str(e), "items": len(items), "path": str(DC_VIEW_DIR / "latest.json")}

    return {
        "ok": True,
        "items": len(items),
        "latest": str(DC_VIEW_DIR / "latest.json"),
        "by_symbol": str(by_symbol_dir),
    }


if __name__ == "__main__":
    result = publish_to_data_center()
    print(f"DC publish: ok={result['ok']} items={result.get('items', 0)}")
    if result.get("error"):
        print(f"  error: {result['error']}")
