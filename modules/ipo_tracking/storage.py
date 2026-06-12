from __future__ import annotations
from .io import REPO_ROOT, append_jsonl, atomic_write_json, utc_now

def persist_event(event: dict, cfg: dict) -> None:
    storage = cfg.get("storage", {})
    append_jsonl(REPO_ROOT / storage.get("raw_jsonl", "data/ipo/spacex/raw/events.jsonl"), event)

def persist_snapshot(snapshot: dict, cfg: dict) -> None:
    storage = cfg.get("storage", {})
    snapshot.setdefault("written_at", utc_now())
    for key, default in [("scored_latest", "data/ipo/spacex/scored/latest_snapshot.json"), ("data_center_view", "data/data_center/views/spacex_super_desk/latest.json"), ("desk_latest", "ui/spacex_desk/latest.json")]:
        atomic_write_json(REPO_ROOT / storage.get(key, default), snapshot)
    try:
        from modules.data_center.runtime_registry import update_producer_last_write
        update_producer_last_write("spacex_super_desk_v5", "spacex_super_desk.v1", storage.get("data_center_view", "data/data_center/views/spacex_super_desk/latest.json"), root=REPO_ROOT, status="ok", evidence={"symbol": snapshot.get("symbol"), "score": snapshot.get("scores", {})})
    except Exception:
        pass
