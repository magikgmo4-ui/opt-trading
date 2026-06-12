from __future__ import annotations
from typing import Any

from .config import load_config
from .collectors.sec_edgar import collect_sec_edgar
from .collectors.yahoo_public import collect_yahoo_quote
from .collectors.rss_news import collect_yahoo_rss
from .collectors.bot_vision_adapter import collect_bot_vision_context
from .collectors.tradingview_webhook import normalize_tradingview_payload
from .storage import persist_event, persist_snapshot, persist_normalized, write_history_snapshot, write_pipeline_verification
from .scoring import score_snapshot
from .normalizer import normalize_events, normalized_summary
from .verify import validate_full_pipeline
from .reports import write_daily_report, write_ui
from .io import REPO_ROOT, utc_now, read_json, append_jsonl, atomic_write_json
from .enrichment import enrich_candles, enrich_from_snapshot


def run_full_pipeline(*, offline: bool = False, tv_json: str | None = None, config_path: str | None = None, symbol_override: str | None = None) -> dict[str, Any]:
    cfg = load_config(config_path)
    pipeline_id = utc_now()
    pipeline_result: dict[str, Any] = {
        "pipeline_id": pipeline_id,
        "mode": "offline" if offline else "live",
        "symbol_override": symbol_override,
        "started_at": pipeline_id,
    }

    events = _collect(cfg, offline=offline, tv_json=tv_json, symbol_override=symbol_override)
    for e in events:
        persist_event(e, cfg)
    pipeline_result["raw_events_count"] = len(events)
    pipeline_result["raw_sources"] = sorted(set(e.get("source", "unknown") for e in events))

    normalized = normalize_events(events)
    persist_normalized(normalized, cfg)
    write_history_snapshot(
        {"pipeline_id": pipeline_id, "normalized_at": utc_now(), "events": normalized, "summary": normalized_summary(normalized)},
        "normalized", "data/ipo/spacex/normalized", cfg,
    )
    pipeline_result["normalized_events_count"] = len(normalized)
    pipeline_result["normalized_summary"] = normalized_summary(normalized)

    snap = score_snapshot(events, cfg)
    persist_snapshot(snap, cfg)
    write_history_snapshot(
        {"pipeline_id": pipeline_id, "snapshot": snap},
        "scored", "data/ipo/spacex/scored", cfg,
    )
    pipeline_result["scored"] = snap

    verification = validate_full_pipeline(events, normalized, snap)
    vpath = write_pipeline_verification(verification, cfg)
    pipeline_result["verification"] = verification
    pipeline_result["verification_path"] = vpath

    enriched = enrich_from_snapshot(snap, events)
    enriched_path = REPO_ROOT / "data/ipo/spacex/enriched/latest.json"
    atomic_write_json(enriched_path, enriched)
    write_history_snapshot(
        {"pipeline_id": pipeline_id, "enriched": enriched},
        "enriched", "data/ipo/spacex/enriched", cfg,
    )
    pipeline_result["enriched_features"] = len(enriched.get("indicators", {}))
    pipeline_result["enriched_path"] = str(enriched_path.relative_to(REPO_ROOT))

    report_path = write_daily_report(snap)
    ui_path = write_ui(snap)
    pipeline_result["report_path"] = str(report_path.relative_to(REPO_ROOT)) if report_path else None
    pipeline_result["ui_path"] = str(ui_path.relative_to(REPO_ROOT)) if ui_path else None

    pipeline_result["completed_at"] = utc_now()
    pipeline_result["ok"] = verification["ok"]

    write_history_snapshot(
        {"pipeline_id": pipeline_id, "result": pipeline_result},
        "raw", "data/ipo/spacex", cfg,
    )

    return pipeline_result


def replay_from_raw(*, config_path: str | None = None) -> dict[str, Any]:
    from .storage import read_raw_events
    cfg = load_config(config_path)
    pipeline_id = utc_now()
    events = read_raw_events(cfg)
    if not events:
        return {"ok": False, "error": "no raw events to replay", "pipeline_id": pipeline_id}

    normalized = normalize_events(events)
    persist_normalized(normalized, cfg)
    write_history_snapshot(
        {"pipeline_id": pipeline_id, "replay": True, "normalized_at": utc_now(), "events": normalized, "summary": normalized_summary(normalized)},
        "normalized", "data/ipo/spacex/normalized", cfg,
    )

    snap = score_snapshot(events, cfg)
    persist_snapshot(snap, cfg)
    write_history_snapshot(
        {"pipeline_id": pipeline_id, "replay": True, "snapshot": snap},
        "scored", "data/ipo/spacex/scored", cfg,
    )

    verification = validate_full_pipeline(events, normalized, snap)
    write_pipeline_verification(verification, cfg)

    enriched = enrich_from_snapshot(snap, events)
    enriched_path = REPO_ROOT / "data/ipo/spacex/enriched/latest.json"
    atomic_write_json(enriched_path, enriched)

    return {
        "ok": verification["ok"],
        "pipeline_id": pipeline_id,
        "replay": True,
        "raw_events": len(events),
        "normalized_events": len(normalized),
        "scored": snap,
        "enriched_features": len(enriched.get("indicators", {})),
        "verification": verification,
    }


def _collect(cfg: dict, *, offline: bool = False, tv_json: str | None = None, symbol_override: str | None = None) -> list[dict[str, Any]]:
    import json
    from pathlib import Path
    symbol = symbol_override or (cfg.get("asset") or {}).get("primary_symbol", "SPCX")
    cik = int((cfg.get("asset") or {}).get("sec_cik", 1181412)) if not symbol_override else _cik_for_symbol(symbol_override)
    ipo_price = (cfg.get("asset") or {}).get("ipo_price_usd", 135)
    events: list[dict[str, Any]] = []
    if tv_json:
        payload = json.loads(Path(tv_json).read_text(encoding="utf-8"))
        events.append(normalize_tradingview_payload(payload))
    if offline:
        events += [
            {"source": "yahoo_chart", "ok": True, "symbol": symbol, "regular_market_price": ipo_price, "previous_close": ipo_price, "bars": [{"open": ipo_price, "high": ipo_price, "low": ipo_price, "close": ipo_price, "volume": 1000}]},
            {"source": "sec_edgar", "ok": False, "filings": [], "offline": True},
            {"source": "yahoo_news_rss", "ok": False, "articles": [], "offline": True},
        ]
    else:
        events += [
            collect_yahoo_quote(symbol),
            collect_sec_edgar(cik),
            collect_yahoo_rss(f"{symbol} OR SpaceX OR Starlink"),
        ]
    events.append(collect_bot_vision_context())
    return events


def _cik_for_symbol(symbol: str) -> int:
    mapping = {"RKLB": 1818644, "TSLA": 1318605, "NVDA": 1045810, "SPCX": 1181412}
    return mapping.get(symbol.upper(), 0)
