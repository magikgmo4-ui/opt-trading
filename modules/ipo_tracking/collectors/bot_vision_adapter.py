from __future__ import annotations
from typing import Any
from ..io import REPO_ROOT, utc_now, read_json

def collect_bot_vision_context(limit: int = 25) -> dict[str, Any]:
    roots = [REPO_ROOT / "data/deskpro/inputs", REPO_ROOT / "data/data_center/views", REPO_ROOT / "modules/bot_vision/headless_capture"]
    hits = []
    for root in roots:
        if not root.exists():
            continue
        files = sorted(root.rglob("*"), key=lambda x: x.stat().st_mtime if x.exists() else 0, reverse=True)
        for p in files:
            if len(hits) >= limit:
                break
            name = p.name.lower()
            if p.is_file() and any(tok in name for tok in ["spcx", "spacex", "coinglass", "screener", "vision", "profile"]):
                item = {"path": str(p.relative_to(REPO_ROOT)), "mtime": p.stat().st_mtime, "suffix": p.suffix}
                if p.suffix == ".json":
                    item["json_preview"] = read_json(p, default={})
                hits.append(item)
    return {"source": "bot_vision_adapter", "collected_at": utc_now(), "ok": True, "items": hits, "count": len(hits)}
