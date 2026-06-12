from __future__ import annotations
from pathlib import Path
from typing import Any
from ..io import REPO_ROOT, utc_now, read_json

def collect_bot_vision_context(limit: int = 200) -> dict[str, Any]:
    roots = [
        REPO_ROOT / "data" / "vision_inbox",
        Path("/srv/sftp/shared_files/shared/vision_inbox"),
        REPO_ROOT / "data" / "deskpro" / "inputs",
        REPO_ROOT / "data" / "data_center" / "views",
        REPO_ROOT / "modules" / "bot_vision" / "headless_capture",
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
                        # Surface DOM-extracted data
                        dom = preview.get("dom_extracted", {})
                        if dom and isinstance(dom, dict):
                            item["dom_price"] = dom.get("price") or dom.get("regularMarketPrice") or dom.get("close")
                            item["dom_open"] = dom.get("open")
                            item["dom_high"] = dom.get("high")
                            item["dom_low"] = dom.get("low")
                            item["dom_close"] = dom.get("close")
                            item["dom_volume"] = dom.get("volume")
                            item["dom_change"] = dom.get("change")
                            item["dom_change_percent"] = dom.get("changePercent") or dom.get("regularMarketChangePercent")
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

    # Extract visual price from DOM data
    visual_price = None
    for h in spcx_items:
        dp = h.get("dom_price")
        if dp:
            try:
                visual_price = float(str(dp).replace(",", ""))
                break
            except (ValueError, TypeError):
                pass

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
        "visual_price": visual_price,
    }
