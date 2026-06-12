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
from .signal_quality import build_signal_quality_matrix, run_feature_ablation, score_source_reliability, evaluate_alert_precision
from .ipo_dataset import IPO_DATASET, compute_analog_match, dataset_stats, query_dataset
from .sector_intelligence import compute_sector_intelligence, sector_summary, compute_correlation_matrix, detect_lead_lag, compute_relative_strength, detect_capital_rotation, compute_sector_health
from .edge_engine import compute_setup_probabilities, edge_summary
from .market_microstructure import detect_market_regime, analyze_opening_auction, compute_volume_curve
from .data_quality_guardian import audit_sources, audit_features
from .command_center import render_command_center, command_center_json


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="spacex-super-desk")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("smoke")
    c = sub.add_parser("collect-once")
    c.add_argument("--offline", action="store_true")
    c.add_argument("--tradingview-json")
    c.add_argument("--symbol", default=None)
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
    sub.add_parser("signal-quality")
    sub.add_parser("ablation")
    sub.add_parser("source-reliability")
    sub.add_parser("alert-precision")
    sub.add_parser("dataset")
    sub.add_parser("analogs")
    sub.add_parser("sector")

    sc2 = sub.add_parser("sector-correlation")
    sc2.add_argument("--tickers", nargs="*", default=["SPCX", "RKLB", "ASTS", "TSLA", "ARKX", "QQQ"])
    sc2.add_argument("--bars", type=int, default=50)

    sl = sub.add_parser("sector-leadlag")
    sl.add_argument("--leader", default="SPCX")
    sl.add_argument("--follower", default="RKLB")

    sr = sub.add_parser("sector-strength")
    sr.add_argument("--benchmark", default="SPY")

    sr2 = sub.add_parser("sector-rotation")

    sh = sub.add_parser("sector-health")

    sub.add_parser("edge")
    sub.add_parser("microstructure")
    sub.add_parser("guardian")
    cc = sub.add_parser("command-center")
    cc.add_argument("--json-out", default=None)
    cc.add_argument("--md-out", default=None)

    ac = sub.add_parser("accumulation")
    ac.add_argument("--price", type=float, default=None)

    args = p.parse_args(argv)
    cfg = load_config()
    if args.cmd == "smoke":
        return smoke(cfg, symbol_override=args.symbol if hasattr(args, 'symbol') else None)
    if args.cmd == "collect-once":
        result = run_full_pipeline(offline=args.offline, tv_json=args.tradingview_json, symbol_override=args.symbol)
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
    if args.cmd == "signal-quality":
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        events = read_raw_events(cfg)
        enriched = enrich_from_snapshot(snap, events)
        matrix = build_signal_quality_matrix([enriched], [snap.get("scores", {})])
        summary = [{"feature": r.feature, "setup": r.setup_id, "quality": r.signal_quality, "corr": r.correlation, "expectancy": r.expectancy} for r in matrix[:20]]
        print(json.dumps({"ok": True, "total_features": len(matrix), "top_20": summary}, indent=2, default=str))
        return 0
    if args.cmd == "ablation":
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        events = read_raw_events(cfg)
        enriched = enrich_from_snapshot(snap, events)
        ablation = run_feature_ablation([enriched], [snap.get("scores", {})])
        summary = [{"setup": r.setup_id, "group": r.ablated_group, "delta": r.delta, "importance": r.importance} for r in ablation[:15]]
        print(json.dumps({"ok": True, "total": len(ablation), "top_15": summary}, indent=2, default=str))
        return 0
    if args.cmd == "source-reliability":
        events = read_raw_events(cfg)
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        reliability = score_source_reliability(events, snap)
        summary = [{"source": r.source_id, "composite": r.composite_score, "grade": r.grade, "freshness": r.freshness_score} for r in reliability]
        print(json.dumps({"ok": True, "sources": summary}, indent=2, default=str))
        return 0
    if args.cmd == "alert-precision":
        alert_log = read_json(REPO_ROOT / "data/ipo/spacex/alerts/log.jsonl", [])
        if isinstance(alert_log, dict):
            alert_log = []
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        precision = evaluate_alert_precision(alert_log, [snap.get("scores", {})])
        summary = [{"event": r.alert_event, "total": r.total_count, "precision": r.precision, "recall": r.recall, "avg_r": r.avg_r_after} for r in precision]
        print(json.dumps({"ok": True, "alerts": summary}, indent=2, default=str))
        return 0
    if args.cmd == "dataset":
        stats = dataset_stats()
        print(json.dumps({"ok": True, "total_ipos": len(IPO_DATASET), "stats": stats, "sectors": list(set(r.sector for r in IPO_DATASET))}, indent=2, default=str))
        return 0
    if args.cmd == "analogs":
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        enriched = read_json(REPO_ROOT / "data/ipo/spacex/enriched/latest.json", {})
        indicators = enriched.get("indicators", {})
        smart_money = enriched.get("smart_money", {})

        result = compute_analog_match(
            spcx_gap_pct=indicators.get("ipo_gap_pct") or 0,
            spcx_rel_vol=indicators.get("relative_volume") or 1,
            spcx_fvg=smart_money.get("fvg_bullish", False),
            spcx_bos=smart_money.get("bos", False),
        )
        print(json.dumps({"ok": True, "analogs": result}, indent=2, default=str))
        return 0
    if args.cmd == "sector":
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        enriched = read_json(REPO_ROOT / "data/ipo/spacex/enriched/latest.json", {})
        indicators = enriched.get("indicators", {})
        scores = snap.get("scores", {})
        vol_class = "NORMAL"

        result = compute_sector_intelligence(
            spcx_gap_pct=indicators.get("ipo_gap_pct") or 0,
            spcx_volume_class=vol_class,
            spcx_scoring=scores,
        )
        result["sector_summary"] = sector_summary()
        print(json.dumps(result, indent=2, default=str))
        return 0
    if args.cmd == "sector-correlation":
        import random
        rng = random.Random(42)
        prices = {}
        for t in args.tickers:
            base = 100.0 if t != "SPCX" else 135.0
            series = [base]
            for _ in range(args.bars):
                series.append(series[-1] * (1 + rng.uniform(-0.03, 0.03)))
            prices[t] = series
        result = compute_correlation_matrix(prices)
        print(json.dumps(result, indent=2, default=str))
        return 0
    if args.cmd == "sector-leadlag":
        import random
        rng = random.Random(42)
        leader_price = 135.0
        follower_price = 10.0
        leader_series = [leader_price]
        follower_series = [follower_price]
        for _ in range(30):
            l_chg = rng.uniform(-0.02, 0.03)
            leader_price *= (1 + l_chg)
            follower_price *= (1 + l_chg * 0.6 + rng.uniform(-0.01, 0.01))
            leader_series.append(leader_price)
            follower_series.append(follower_price)
        result = detect_lead_lag(leader_series, follower_series)
        print(json.dumps(result, indent=2, default=str))
        return 0
    if args.cmd == "sector-strength":
        changes = {
            "SPCX": 0.0, "RKLB": 2.5, "ASTS": 1.8, "RDW": -0.5, "LUNR": -1.2, "PL": 0.3,
            "TSLA": 1.2, "NVDA": 3.1,
            "ARKX": 0.8, "UFO": 0.5, "ITA": -0.2, "XAR": -0.8,
            "QQQ": 0.5, "SPY": 0.3, "IWM": -0.1,
        }
        prices = {t: 100.0 for t in changes}
        result = compute_relative_strength(prices, args.benchmark, changes)
        print(json.dumps(result, indent=2, default=str))
        return 0
    if args.cmd == "sector-rotation":
        flows = {"space_stocks": 5.2, "semiconductors": 12.5, "defense": -3.1, "fintech": -2.8, "consumer": -8.0, "energy": 1.5}
        result = detect_capital_rotation(flows)
        print(json.dumps(result, indent=2, default=str))
        return 0
    if args.cmd == "sector-health":
        changes = {
            "SPCX": 0.0, "RKLB": 2.5, "ASTS": 1.8, "RDW": -0.5, "LUNR": -1.2, "PL": 0.3,
            "TSLA": 1.2, "NVDA": 3.1,
            "ARKX": 0.8, "UFO": 0.5, "ITA": -0.2, "XAR": -0.8,
            "QQQ": 0.5, "SPY": 0.3, "IWM": -0.1,
        }
        prices = {t: 100.0 for t in changes}
        result = compute_sector_health(prices, changes)
        print(json.dumps(result, indent=2, default=str))
        return 0
    if args.cmd == "edge":
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        enriched = read_json(REPO_ROOT / "data/ipo/spacex/enriched/latest.json", {})
        indicators = enriched.get("indicators", {})
        smart_money = enriched.get("smart_money", {})
        consensus = enriched.get("consensus", {})
        scores = snap.get("scores", {})

        from .ipo_analogs import compute_analog_score
        spcx = {"gap_pct": indicators.get("ipo_gap_pct") or 0, "relative_volume": indicators.get("relative_volume") or 1, "fvg_bullish": smart_money.get("fvg_bullish", False), "bos": smart_money.get("bos", False)}
        analog = compute_analog_score(spcx)

        result = compute_setup_probabilities(indicators, smart_money, consensus, scores, enriched, analog)
        print(edge_summary(result))
        return 0
    if args.cmd == "microstructure":
        snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
        enriched = read_json(REPO_ROOT / "data/ipo/spacex/enriched/latest.json", {})
        yahoo = (snap.get("latest_events") or {}).get("yahoo_chart", {})
        bars = yahoo.get("bars", [])
        if not bars:
            bars = [{"open": 135, "high": 135, "low": 135, "close": 135, "volume": 1000}]
        indicators = enriched.get("indicators", {})
        smart_money = enriched.get("smart_money", {})

        regime = detect_market_regime(bars, indicators, smart_money)
        auction = analyze_opening_auction(bars, snap.get("ipo_price", 135))
        vol_curve = compute_volume_curve(bars)
        print(json.dumps({"regime": regime, "auction": auction, "volume_curve": vol_curve}, indent=2, default=str))
        return 0
    if args.cmd == "guardian":
        events = read_raw_events(cfg)
        sources = audit_sources(events)
        print(json.dumps({"source_audit": sources}, indent=2, default=str))
        return 0
    if args.cmd == "command-center":
        output = render_command_center()
        print(output)
        if args.json_out:
            from .io import atomic_write_json
            atomic_write_json(REPO_ROOT / args.json_out, command_center_json())
        if args.md_out:
            from .io import atomic_write_json
            md_path = REPO_ROOT / args.md_out
            md_path.parent.mkdir(parents=True, exist_ok=True)
            lines = []
            for line in output.split("\n"):
                stripped = line.lstrip()
                if stripped.startswith("==") or stripped.startswith("--"):
                    continue
                if stripped and stripped[0].isalpha():
                    lines.append(f"## {stripped}")
                elif stripped:
                    lines.append(stripped)
            md_path.write_text("\n".join(lines))
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

def smoke(cfg, symbol_override=None):
    return collect_once(cfg, offline=True, symbol_override=symbol_override)

def _offline_quote(cfg):
    ipo = (cfg.get("asset") or {}).get("ipo_price_usd", 135)
    return {"source": "yahoo_chart", "ok": True, "symbol": "SPCX", "regular_market_price": ipo, "previous_close": ipo, "bars": [{"open": ipo, "high": ipo, "low": ipo, "close": ipo, "volume": 1000}]}

if __name__ == "__main__":
    raise SystemExit(main())
