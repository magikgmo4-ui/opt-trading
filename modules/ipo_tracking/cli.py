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
from .storage import persist_event, persist_snapshot
from .scoring import score_snapshot
from .reports import write_daily_report, write_ui
from .io import REPO_ROOT, read_json, atomic_write_json
from .backtest import load_ohlcv_csv, backtest_orb

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
    args = p.parse_args(argv)
    cfg = load_config()
    if args.cmd == "smoke":
        return smoke(cfg)
    if args.cmd == "collect-once":
        return collect_once(cfg, offline=args.offline, tv_json=args.tradingview_json)
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
