from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from .io import REPO_ROOT


@dataclass
class ResolvedPaths:
    raw_jsonl: Path
    normalized_jsonl: Path
    scored_latest: Path
    data_center_view: Path
    desk_latest: Path
    report_dir: Path


def load_config(path: str | Path | None = None) -> dict:
    cfg_path = Path(path) if path else REPO_ROOT / "configs/ipo/spacex_super_desk_v5.yaml"
    text = cfg_path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        return {
            "config_path": str(cfg_path),
            "raw_text": text,
            "asset": {"primary_symbol": "SPCX", "ipo_price_usd": 135, "sec_cik": 1181412},
            "storage": {
                "raw_jsonl": "data/ipo/spacex/raw/events.jsonl",
                "normalized_jsonl": "data/ipo/spacex/normalized/events.jsonl",
                "scored_latest": "data/ipo/spacex/scored/latest_snapshot.json",
                "data_center_view": "data/data_center/views/spacex_super_desk/latest.json",
                "desk_latest": "ui/spacex_desk/latest.json",
            },
        }


def resolve_paths(config: dict) -> ResolvedPaths:
    storage = config.get("storage", {})
    return ResolvedPaths(
        raw_jsonl=REPO_ROOT / storage.get("raw_jsonl", "data/ipo/spacex/raw/events.jsonl"),
        normalized_jsonl=REPO_ROOT / storage.get("normalized_jsonl", "data/ipo/spacex/normalized/events.jsonl"),
        scored_latest=REPO_ROOT / storage.get("scored_latest", "data/ipo/spacex/scored/latest_snapshot.json"),
        data_center_view=REPO_ROOT / storage.get("data_center_view", "data/data_center/views/spacex_super_desk/latest.json"),
        desk_latest=REPO_ROOT / storage.get("desk_latest", "ui/spacex_desk/latest.json"),
        report_dir=REPO_ROOT / "reports/ipo/spacex",
    )
