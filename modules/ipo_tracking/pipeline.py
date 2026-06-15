from __future__ import annotations
from typing import Any

from .config import load_config
from .collectors.sec_edgar import collect_sec_edgar
from .collectors.yahoo_public import collect_yahoo_quote
from .collectors.rss_news import collect_yahoo_rss
from .collectors.bot_vision_adapter import collect_bot_vision_context
from .collectors.tradingview_webhook import normalize_tradingview_payload
from .collectors.spcx_sip_tape import collect_spcx_sip_tape, bucket_tape_1m
from .collectors.spcx_l2_depth import collect_spcx_l2_depth
from .collectors.spcx_auction_imbalance import collect_spcx_auction_imbalance
from .collectors.spcx_sec_ownership import collect_spcx_sec_ownership
from .storage import persist_event, persist_snapshot, persist_normalized, write_history_snapshot, write_pipeline_verification
from .scoring import score_snapshot
from .scoring.spcx_orderflow_score import score_orderflow
from .scoring.spcx_ownership_pressure_score import score_ownership_pressure
from .normalizer import normalize_events, normalized_summary
from .verify import validate_full_pipeline
from .reports import write_daily_report, write_ui, write_orderflow_report
from .io import REPO_ROOT, utc_now, read_json, append_jsonl, atomic_write_json
from .enrichment import enrich_candles, enrich_from_snapshot
from .source_quality import classify_source_quality, cap_trade_ready_from_quality
from .freshness_watchdog import check_freshness, apply_degraded_caps


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

    # --- Orderflow + Ownership collection ---
    orderflow_events = _collect_orderflow(cfg, offline=offline)
    for e in orderflow_events:
        persist_event(e, cfg)
    pipeline_result["orderflow_sources"] = sorted(set(e.get("source", "unknown") for e in orderflow_events))

    # Orderflow scoring
    tape_data = next((e for e in orderflow_events if e.get("source") == "spcx_sip_tape"), None)
    depth_data = next((e for e in orderflow_events if e.get("source") == "spcx_l2_depth"), None)
    auction_data = next((e for e in orderflow_events if e.get("source") == "spcx_auction_imbalance"), None)
    ownership_data = next((e for e in orderflow_events if e.get("source") == "spcx_sec_ownership"), None)

    orderflow_score = score_orderflow(tape_data, depth_data, auction_data)
    pipeline_result["orderflow_score"] = orderflow_score

    current_price = snap.get("price")
    ownership_score = score_ownership_pressure(ownership_data, current_price)
    pipeline_result["ownership_score"] = ownership_score

    # Orderflow bucket generation
    tape_bars = _extract_bars_for_bucketing(events)
    buckets = bucket_tape_1m(tape_bars)
    pipeline_result["orderflow_bucket_count"] = len(buckets)
    if buckets:
        buckets_dir = REPO_ROOT / "state" / "ipo" / "spacex" / "orderflow_buckets"
        buckets_dir.mkdir(parents=True, exist_ok=True)
        atomic_write_json(buckets_dir / "latest.json", {"buckets": buckets, "generated_at": utc_now(), "bucket_seconds": 60, "count": len(buckets), "symbol": "SPCX"})

    # --- Source quality classification ---
    price_status = snap.get("price_status", "missing")
    source_quality = classify_source_quality(tape_data, depth_data, auction_data, ownership_data, price_status)
    pipeline_result["source_quality"] = source_quality

    # --- Freshness watchdog ---
    freshness = check_freshness()
    pipeline_result["freshness"] = freshness

    # --- Apply degraded caps to scores ---
    snap_scores = snap.get("scores", {})
    if freshness.get("degraded") or not source_quality.get("can_affect_trade_ready"):
        snap["scores"] = apply_degraded_caps(snap_scores, freshness)
        snap["scores"]["trade_ready_capped_by_quality"] = not source_quality.get("can_affect_trade_ready")
        pipeline_result["degraded"] = True
        pipeline_result["degraded_reasons"] = freshness.get("warnings", []) + source_quality.get("degraded_reasons", [])
    else:
        pipeline_result["degraded"] = False

    # Inject source_quality into snapshot
    snap["source_quality"] = source_quality
    snap["pipeline_state"] = freshness.get("pipeline_state", "healthy")

    report_path = write_daily_report(snap)
    of_report_path = write_orderflow_report(snap, orderflow_score, ownership_score)
    ui_path = write_ui(snap)
    pipeline_result["report_path"] = str(report_path.relative_to(REPO_ROOT)) if report_path else None
    pipeline_result["orderflow_report_path"] = str(of_report_path.relative_to(REPO_ROOT)) if of_report_path else None
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


def _collect_orderflow(cfg: dict, *, offline: bool = False) -> list[dict[str, Any]]:
    if offline:
        return [
            {"source": "spcx_sip_tape", "ok": False, "offline": True},
            {"source": "spcx_l2_depth", "ok": False, "offline": True},
            {"source": "spcx_auction_imbalance", "ok": False, "offline": True},
            {"source": "spcx_sec_ownership", "ok": False, "offline": True},
        ]
    return [
        collect_spcx_sip_tape(),
        collect_spcx_l2_depth(),
        collect_spcx_auction_imbalance(),
        collect_spcx_sec_ownership(),
    ]


def _extract_bars_for_bucketing(events: list[dict]) -> list[dict]:
    for e in events:
        if e.get("source") == "yahoo_chart" and e.get("bars"):
            return _normalize_bars(e["bars"])
    return []


def _normalize_bars(bars: list[dict]) -> list[dict]:
    out = []
    for b in bars:
        ts = b.get("ts") or b.get("timestamp")
        out.append({
            "timestamp": ts,
            "open": b.get("open"),
            "high": b.get("high"),
            "low": b.get("low"),
            "close": b.get("close"),
            "volume": b.get("volume") or 0,
        })
    return out
