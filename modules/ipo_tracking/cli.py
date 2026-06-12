from __future__ import annotations
import argparse
import json
from pathlib import Path
from .config import load_config
from .collectors.sec_edgar import collect_sec_edgar
from .collectors.yahoo_public import collect_yahoo_quote
from .collectors.rss_news import collect_yahoo_rss
from .collectors.bot_vision_adapter import collect_bot_vision_context
from .collectors.tradingview_webhook import normalize_tradingview_payload
from .storage import persist_event, persist_snapshot, read_raw_events, read_normalized_events
from .scoring import score_snapshot
from .reports import write_daily_report, write_ui
from .io import REPO_ROOT, read_json, atomic_write_json, utc_now
from .backtest import load_ohlcv_csv, backtest_orb
from .pipeline import run_full_pipeline, replay_from_raw
from .normalizer import normalize_events, normalized_summary
from .verify import validate_full_pipeline, validate_raw_events, validate_normalized_events, validate_scored_snapshot
from .backtest_engine import run_backtest, run_all_setups, run_scan, BacktestRun
from .setups import get_setup, list_setups, SETUPS, CATEGORIES
from .accumulation import compute_accumulation_score, accumulation_summary, classify_zone
from .scoring_engine import compute_composite_score
from .playbook import generate_playbook
from .enrichment import enrich_from_snapshot, CANDLE_SCHEMA, ENRICHED_CANDLE_FEATURES


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="spacex-super-desk")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("smoke")
    c = sub.add_parser("collect-once")
    c.add_argument("--offline", action="store_true")
    c.add_argument("--tradingview-json")
    sub.add_parser("report")
    b = sub.add_parser("backtest-orb")
    b.add_argument("--csv", required=True)
    b.add_argument("--minutes", type=int, default=15)
    sub.add_parser("replay")
    v = sub.add_parser("verify")
    v.add_argument("--stage", choices=["raw", "normalized", "scored", "full"], default="full")
    h = sub.add_parser("history")
    h.add_argument("--stage", choices=["raw", "normalized", "scored", "verifications"], default="scored")
    h.add_argument("--limit", type=int, default=10)

    bt = sub.add_parser("backtest")
    bt.add_argument("--setup", choices=list(SETUPS.keys()), default="IPO_ORB_5M")
    bt.add_argument("--csv", required=True)
    bt.add_argument("--rr", type=float, default=None)

    sc = sub.add_parser("scan")
    sc.add_argument("--csv")
    sc.add_argument("--category", choices=list(CATEGORIES.keys()), default=None)

    sub.add_parser("setups")
    sub.add_parser("playbook")
    sub.add_parser("enrich")

    ac = sub.add_parser("accumulation")
    ac.add_argument("--price", type=float, default=None)

    args = p.parse_args(argv)
    cfg = load_config()
    if args.cmd == "smoke":
        return smoke(cfg)
    if args.cmd == "collect-once":
        result = run_full_pipeline(offline=args.offline, tv_json=args.tradingview_json)
        print(json.dumps(result, indent=2, default=str))
        return 0 if result.get("ok") else 1
    if args.cmd == "report":
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        if not snap:
            collect_once(cfg, offline=True)
            snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        print(write_daily_report(snap))
        print(write_ui(snap))
        return 0
    if args.cmd == "backtest-orb":
        result = backtest_orb(load_ohlcv_csv(args.csv), minutes=args.minutes)
        out = REPO_ROOT / "reports/ipo/spacex/backtests" / f"orb_{args.minutes}m_latest.json"
        atomic_write_json(out, result)
        print(json.dumps(result, indent=2))
        return 0
    if args.cmd == "replay":
        result = replay_from_raw()
        print(json.dumps(result, indent=2, default=str))
        return 0 if result.get("ok") else 1
    if args.cmd == "verify":
        events = read_raw_events(cfg)
        normalized = read_normalized_events(cfg)
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        if args.stage == "raw":
            result = validate_raw_events(events)
        elif args.stage == "normalized":
            result = validate_normalized_events(normalized)
        elif args.stage == "scored":
            result = validate_scored_snapshot(snap)
        else:
            result = validate_full_pipeline(events, normalized, snap)
        print(json.dumps(result, indent=2, default=str))
        return 0 if result.get("ok") else 1
    if args.cmd == "history":
        stage = args.stage
        history_dir = REPO_ROOT / "data/ipo/spacex" / stage / "history"
        if not history_dir.exists():
            print(json.dumps({"ok": False, "error": f"no history for stage={stage}", "path": str(history_dir)}, default=str))
            return 1
        files = sorted(history_dir.glob("*.json"), reverse=True)[:args.limit]
        entries = []
        for fp in files:
            entries.append({"file": fp.name, "size": fp.stat().st_size, "mtime": utc_now(), "snapshot": read_json(fp)})
        print(json.dumps({"ok": True, "stage": stage, "count": len(entries), "entries": entries}, indent=2, default=str))
        return 0
    if args.cmd == "backtest":
        bars = load_ohlcv_csv(args.csv)
        setup = get_setup(args.setup)
        if not setup:
            print(json.dumps({"ok": False, "error": f"unknown setup: {args.setup}"}))
            return 1
        result = run_backtest(bars, setup, rr=args.rr)
        print(json.dumps({
            "setup_id": result.setup_id,
            "total_trades": result.total_trades,
            "wins": result.wins,
            "losses": result.losses,
            "win_rate": result.win_rate,
            "avg_r": result.avg_r,
            "profit_factor": result.profit_factor,
            "expectancy_r": result.expectancy_r,
            "max_dd_r": result.max_dd_r,
            "sharpe": result.sharpe_estimate,
            "best_r": result.best_r,
            "worst_r": result.worst_r,
            "consecutive_losses": result.consecutive_losses,
            "trades": [{"result": t.result, "r": t.r_multiple, "bars": t.bars_held, "exit": t.exit_reason} for t in result.trades],
        }, indent=2))
        return 0
    if args.cmd == "scan":
        bars = []
        if args.csv:
            bars = load_ohlcv_csv(args.csv)
        else:
            snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
            yahoo = (snap.get("latest_events", {}) or {}).get("yahoo_chart", {})
            bars = yahoo.get("bars", [])
        if not bars:
            snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
            bars = _offline_quote(cfg).get("bars", [])
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        result = run_scan(bars, snap)
        print(json.dumps(result, indent=2, default=str))
        return 0
    if args.cmd == "setups":
        setups = list_setups()
        summary = [{"id": s.setup_id, "name": s.name, "category": s.category, "direction": s.direction, "timeframe": s.timeframe, "rr": s.rr_target} for s in setups]
        print(json.dumps({"total": len(summary), "setups": summary}, indent=2))
        return 0
    if args.cmd == "playbook":
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        acc = accumulation_summary(snap)
        composite = compute_composite_score(snap, acc)
        playbook = generate_playbook(snap)
        playbook["composite_score"] = composite
        playbook["accumulation"] = acc
        print(json.dumps(playbook, indent=2, default=str))
        return 0
    if args.cmd == "enrich":
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        events = read_raw_events(cfg)
        enriched = enrich_from_snapshot(snap, events)
        print(json.dumps(enriched, indent=2, default=str))
        return 0
    if args.cmd == "accumulation":
        price = args.price
        if price is None:
            snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
            price = snap.get("price")
        result = compute_accumulation_score(price or 135)
        print(json.dumps(result, indent=2, default=str))
        return 0
    return 2

def collect_once(cfg, offline=False, tv_json=None):
    events = []
    if tv_json:
        payload = json.loads(Path(tv_json).read_text(encoding="utf-8"))
        events.append(normalize_tradingview_payload(payload))
    if offline:
        events += [_offline_quote(cfg), {"source": "sec_edgar", "ok": False, "filings": [], "offline": True}, {"source": "yahoo_news_rss", "ok": False, "articles": [], "offline": True}]
    else:
        events += [collect_yahoo_quote((cfg.get("asset") or {}).get("primary_symbol", "SPCX")), collect_sec_edgar(int((cfg.get("asset") or {}).get("sec_cik", 1181412))), collect_yahoo_rss("SpaceX OR SPCX OR Starlink OR Starship")]
    events.append(collect_bot_vision_context())
    for e in events:
        persist_event(e, cfg)
    snap = score_snapshot(events, cfg)
    persist_snapshot(snap, cfg)
    write_daily_report(snap)
    write_ui(snap)
    print(json.dumps({"ok": True, "events": len(events), "snapshot": snap}, indent=2, default=str))
    return 0

def smoke(cfg):
    return collect_once(cfg, offline=True)

def _offline_quote(cfg):
    ipo = (cfg.get("asset") or {}).get("ipo_price_usd", 135)
    return {"source": "yahoo_chart", "ok": True, "symbol": "SPCX", "regular_market_price": ipo, "previous_close": ipo, "bars": [{"open": ipo, "high": ipo, "low": ipo, "close": ipo, "volume": 1000}]}

if __name__ == "__main__":
    raise SystemExit(main())
