from __future__ import annotations
from ..io import REPO_ROOT, append_jsonl, atomic_write_json, utc_now


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


def persist_normalized(normalized_events: list[dict], cfg: dict) -> None:
    storage = cfg.get("storage", {})
    nl_path = REPO_ROOT / storage.get("normalized_jsonl", "data/ipo/spacex/normalized/events.jsonl")
    for e in normalized_events:
        append_jsonl(nl_path, e)


def write_history_snapshot(payload: dict, stage: str, base_path: str, cfg: dict) -> str:
    storage = cfg.get("storage", {})
    ts = utc_now().replace(":", "-").replace("T", "_")[:19]
    root = storage.get("root", "data/ipo/spacex")
    history_path = f"{root}/{stage}/history/{ts}.json"
    atomic_write_json(REPO_ROOT / history_path, payload)
    return history_path


def write_pipeline_verification(verification: dict, cfg: dict) -> str:
    storage = cfg.get("storage", {})
    ts = utc_now().replace(":", "-").replace("T", "_")[:19]
    root = storage.get("root", "data/ipo/spacex")
    vpath = f"{root}/_verifications/{ts}.json"
    atomic_write_json(REPO_ROOT / vpath, verification)
    return vpath


def read_raw_events(cfg: dict) -> list[dict]:
    from modules.ipo_tracking.storage.jsonl_store import read_all_jsonl
    storage = cfg.get("storage", {})
    path = REPO_ROOT / storage.get("raw_jsonl", "data/ipo/spacex/raw/events.jsonl")
    return read_all_jsonl(path)


def read_normalized_events(cfg: dict) -> list[dict]:
    from modules.ipo_tracking.storage.jsonl_store import read_all_jsonl
    storage = cfg.get("storage", {})
    path = REPO_ROOT / storage.get("normalized_jsonl", "data/ipo/spacex/normalized/events.jsonl")
    return read_all_jsonl(path)
