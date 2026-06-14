#!/usr/bin/env python3
"""SPCX V2 — Paper-only runner. Detects setups, logs, computes performance.

Usage:
    python -m modules.spcx_v2.runner --once
    python -m modules.spcx_v2.runner --watch
    python -m modules.spcx_v2.runner --replay events.jsonl
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from modules.spcx_v2.config import MarketSnapshot, PROJECT_ROOT
from modules.spcx_v2.setup_detector import detect
from modules.spcx_v2.paper_logger import log_candidate, log_reject, log_result, get_summary
from modules.spcx_v2.perf_calculator import (
    calculate_mfe,
    calculate_mae,
    calculate_r_multiple,
    check_tp1_hit,
    check_tp2_hit,
    check_sl_hit,
)
from shared.logger import setup_logger

logger = setup_logger("spcx_v2.runner")


def parse_args():
    parser = argparse.ArgumentParser(description="SPCX V2 paper-only runner")
    parser.add_argument("--once", action="store_true", help="single-cycle detection + logging")
    parser.add_argument("--watch", action="store_true", help="continuous loop")
    parser.add_argument("--replay", type=str, metavar="FILE", help="replay from events JSONL file")
    parser.add_argument("--pipeline", action="store_true", help="read from enriched pipeline snapshot (end-of-day backtest)")
    parser.add_argument("--summary", action="store_true", help="print current summary and exit")
    return parser.parse_args()


def snapshot_from_event(event: dict) -> MarketSnapshot:
    data = event.get("data", event)
    return MarketSnapshot(
        symbol=data.get("symbol", "SPCX"),
        timestamp=data.get("ts", data.get("timestamp", datetime.now(timezone.utc).isoformat())),
        price=float(data.get("price", 0)),
        price_status=data.get("price_status", "live"),
        bars_count=int(data.get("bars_count", 0)),
        volume=int(data.get("volume", 0)),
        price_trust=int(data.get("price_trust", 0)),
        source_count=int(data.get("source_count", 0)),
        spread_pct=float(data.get("spread_pct", 0)),
        dollar_volume=float(data.get("dollar_volume", 0)),
        vwap=float(data["vwap"]) if data.get("vwap") is not None else None,
        halt_active=bool(data.get("halt_active", False)),
        nasdaq_contradiction=bool(data.get("nasdaq_contradiction", False)),
        yahoo_contradiction=bool(data.get("yahoo_contradiction", False)),
        news_headline=data.get("news_headline"),
        news_sentiment=data.get("news_sentiment"),
        smc_structures=data.get("smc_structures", []),
        orderflow_score=float(data["orderflow_score"]) if data.get("orderflow_score") is not None else None,
        ownership_pressure_score=float(data["ownership_pressure_score"]) if data.get("ownership_pressure_score") is not None else None,
        orderflow_source=data.get("orderflow_source"),
        large_prints_count=int(data.get("large_prints_count", 0)),
    )


def compute_result_for_candidate(candidate, price_series: list[float], direction: str = "long"):
    entry = candidate.entry_price or candidate.scores.trade_ready
    if not entry or not price_series:
        return

    sl = candidate.stop_loss or 0
    tp1 = candidate.tp1
    tp2 = candidate.tp2

    mfe = calculate_mfe(entry, price_series, direction)
    mae = calculate_mae(entry, price_series, direction)

    exit_price = price_series[-1] if price_series else entry
    r_multiple = calculate_r_multiple(entry, sl, exit_price, direction) if sl else 0

    hit_tp1 = check_tp1_hit(price_series, tp1, direction) if tp1 else False
    hit_tp2 = check_tp2_hit(price_series, tp2, direction) if tp2 else False
    hit_sl = check_sl_hit(price_series, sl, direction) if sl else False

    return {
        "candidate_id": candidate.candidate_id,
        "entry": entry,
        "exit": exit_price,
        "mfe": mfe,
        "mae": mae,
        "r_multiple": r_multiple,
        "hit_tp1": hit_tp1,
        "hit_tp2": hit_tp2,
        "hit_sl": hit_sl,
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }


def run_once():
    logger.info("SPCX V2 runner --once started")
    state_file = PROJECT_ROOT / "state" / "events.jsonl"

    if not state_file.exists():
        logger.warning("no state/events.jsonl found")
        return

    with open(state_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        logger.info("events.jsonl is empty")
        return

    last_line = lines[-1]
    try:
        event = json.loads(last_line)
    except json.JSONDecodeError:
        logger.error("failed to parse last event")
        return

    snapshot = snapshot_from_event(event)
    candidate = detect(snapshot)

    if candidate.grade == "reject":
        cid = log_reject(candidate)
        logger.info("rejected | %s | reasons=%s", cid, candidate.reason_codes)
    else:
        cid = log_candidate(candidate)
        logger.info("accepted | %s | %s | grade=%s", cid, candidate.setup_type, candidate.grade)

    summary = get_summary()
    print(json.dumps(summary, indent=2, default=str))


def run_replay(filepath: str):
    logger.info("SPCX V2 runner --replay %s", filepath)
    p = Path(filepath)
    if not p.exists():
        logger.error("file not found: %s", filepath)
        sys.exit(1)

    with open(p, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    accepted = 0
    rejected = 0
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        snapshot = snapshot_from_event(event)
        candidate = detect(snapshot)

        if candidate.grade == "reject":
            log_reject(candidate)
            rejected += 1
        else:
            log_candidate(candidate)
            accepted += 1

    logger.info("replay done | accepted=%d rejected=%d", accepted, rejected)
    summary = get_summary()
    print(json.dumps(summary, indent=2, default=str))


def run_watch(interval: int = 5):
    logger.info("SPCX V2 runner --watch started (interval=%ds)", interval)
    state_file = PROJECT_ROOT / "state" / "events.jsonl"
    last_pos = state_file.stat().st_size if state_file.exists() else 0

    try:
        while True:
            if not state_file.exists():
                time.sleep(interval)
                continue

            current_size = state_file.stat().st_size
            if current_size > last_pos:
                with open(state_file, "r") as f:
                    f.seek(last_pos)
                    new_lines = [line.strip() for line in f if line.strip()]

                for line in new_lines:
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    snapshot = snapshot_from_event(event)
                    candidate = detect(snapshot)

                    if candidate.grade == "reject":
                        log_reject(candidate)
                    else:
                        log_candidate(candidate)

                last_pos = current_size

            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("watch stopped by user")
        summary = get_summary()
        print(json.dumps(summary, indent=2, default=str))


def main():
    args = parse_args()

    if args.summary:
        summary = get_summary()
        print(json.dumps(summary, indent=2, default=str))
    elif args.replay:
        run_replay(args.replay)
    elif args.pipeline:
        run_pipeline_backtest()
    elif args.watch:
        run_watch()
    elif args.once:
        run_once()
    else:
        print("Usage: runner.py --once | --watch | --replay FILE | --pipeline | --summary")
        sys.exit(1)


def run_pipeline_backtest():
    """End-of-day backtest: read enriched snapshot with orderflow/ownership,
    run detection, log results, print summary with stats."""
    logger.info("SPCX V2 runner --pipeline (end-of-day backtest) started")

    from modules.spcx_v2.pipeline_adapter import load_enriched_snapshot

    snap = load_enriched_snapshot()
    candidate = detect(snap)

    if candidate.grade == "reject":
        cid = log_reject(candidate)
        logger.info("backtest reject | %s | reasons=%s | of=%.1f ow=%.1f",
                    cid, candidate.reason_codes,
                    snap.orderflow_score or 0, snap.ownership_pressure_score or 0)
    else:
        cid = log_candidate(candidate)
        logger.info("backtest accepted | %s | %s | grade=%s | of=%.1f ow=%.1f",
                    cid, candidate.setup_type, candidate.grade,
                    snap.orderflow_score or 0, snap.ownership_pressure_score or 0)

    summary = get_summary()
    summary["orderflow_score"] = snap.orderflow_score
    summary["ownership_pressure_score"] = snap.ownership_pressure_score
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
