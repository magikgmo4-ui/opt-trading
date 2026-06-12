from __future__ import annotations
from typing import Any
from ..io import REPO_ROOT, utc_now, read_json

def collect_bot_vision_context(limit: int = 200) -> dict[str, Any]:
    roots = [
        REPO_ROOT / "data/vision_inbox",
        REPO_ROOT / "data/deskpro/inputs",
        REPO_ROOT / "data/data_center/views",
        REPO_ROOT / "modules/bot_vision/headless_capture",
    ]
    hits = []
    spcx_captures = []
    comparable_captures = []
    for root in roots:
        if not root.exists():
            continue
        files = sorted(root.rglob("*"), key=lambda x: x.stat().st_mtime if x.exists() else 0, reverse=True)
        for p in files:
            if len(hits) >= limit:
                break
            name = p.name.lower()
            if not p.is_file():
                continue
            if any(tok in name for tok in ["spcx", "spacex", "coinglass", "screener", "vision", "profile",
                                              "rklb", "asts", "lunr", "rdw", "tsla", "qqq", "arkx"]):
                item = {"path": str(p.relative_to(REPO_ROOT)), "mtime": p.stat().st_mtime, "suffix": p.suffix}
                if p.suffix == ".json":
                    preview = read_json(p, default={})
                    item["json_preview"] = preview
                    if isinstance(preview, dict):
                        item["page_id"] = preview.get("page_id", "")
                        item["source"] = preview.get("source", "")
                        item["symbol"] = preview.get("symbol", "")
                        item["timeframe"] = preview.get("timeframe", "")
                        item["visual_status"] = preview.get("visual_status", "")
                    else:
                        item["page_id"] = ""
                        item["source"] = ""
                        item["symbol"] = ""
                        item["timeframe"] = ""
                        item["visual_status"] = ""
                hits.append(item)

    # Build structured SPCX context
    spcx_items = [h for h in hits if h.get("symbol", "").upper() == "SPCX"]
    comp_items = [h for h in hits if h.get("symbol", "").upper() in ("RKLB", "ASTS", "LUNR", "RDW", "TSLA", "QQQ", "ARKX")]

    sources_seen = set()
    capture_map = {}
    for h in spcx_items:
        src = h.get("page_id", h.get("source", "unknown"))
        if src not in sources_seen:
            capture_map[src] = {
                "page_id": h.get("page_id", ""),
                "source": h.get("source", ""),
                "timeframe": h.get("timeframe", ""),
                "visual_status": h.get("visual_status", ""),
                "mtime": h["mtime"],
            }
            sources_seen.add(src)

    comp_map = {}
    for h in comp_items:
        sym = h.get("symbol", "").upper()
        if sym not in comp_map:
            comp_map[sym] = {
                "symbol": sym,
                "page_id": h.get("page_id", ""),
                "timeframe": h.get("timeframe", ""),
                "visual_status": h.get("visual_status", ""),
                "mtime": h["mtime"],
            }

    return {
        "source": "bot_vision_adapter",
        "collected_at": utc_now(),
        "ok": True,
        "items": hits,
        "count": len(hits),
        "spcx_capture_count": len(spcx_items),
        "spcx_capture_map": capture_map,
        "comparable_count": len(comp_items),
        "comparable_map": comp_map,
    }
