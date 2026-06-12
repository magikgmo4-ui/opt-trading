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
