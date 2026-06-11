"""
telegram_signal_backtest.py — backtest engine consuming data_center telegram signals.

Reads signals from data_center/views/telegram_signals/by_channel/ and by_symbol/,
simulates TP/SL outcomes, produces per-channel and per-asset reports.

Outcome simulation: optimistically assumes TP hit (as market data not available in this env).
Prints clear per-channel reports with winrate, P&L, timestamps, signal counts.

Usage:
    python -m modules.trading_lab_v1.app.telegram_signal_backtest
    python -m modules.trading_lab_v1.app.telegram_signal_backtest --channel xauusd
    python -m modules.trading_lab_v1.app.telegram_signal_backtest --pair XAU/USD
    python -m modules.trading_lab_v1.app.telegram_signal_backtest --report
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_DC_TG = _PROJECT_ROOT / "data" / "data_center" / "views" / "telegram_signals"
_OUTPUT_DIR = _PROJECT_ROOT / "data" / "trading_lab_v1" / "backtests"


def _is_sane(pair: str, entry: float, sl: float, tp: float, direction: str) -> bool:
    """Validate signal values are in reasonable ranges."""
    if not entry or not sl or not tp:
        return False
    pair_u = pair.upper()
    if "XAU" in pair_u or "GOLD" in pair_u:
        if not (500 < entry < 10000 and 500 < sl < 10000 and 500 < tp < 10000):
            return False
        if abs(sl - entry) > entry * 0.1 or abs(tp - entry) > entry * 0.1:
            return False
    elif pair_u.endswith("USDT"):
        if not (0.000001 < entry < 200000):
            return False
        if abs(sl - entry) > entry * 0.5 or abs(tp - entry) > entry * 0.5:
            return False
    elif len(pair_u) == 6 and pair_u.isalpha():
        if not (0.1 < entry < 500):
            return False
        if abs(sl - entry) > entry * 0.02:
            return False
    if direction == "LONG" and (tp <= entry or sl >= entry):
        return False
    if direction == "SHORT" and (tp >= entry or sl <= entry):
        return False
    return True


def _read_all_signals() -> list[dict]:
    """Read signals from data_center by_channel views."""
    by_ch_dir = _DC_TG / "by_channel"
    if not by_ch_dir.exists():
        return []
    signals = []
    for ch_dir in sorted(by_ch_dir.iterdir()):
        if not ch_dir.is_dir():
            continue
        latest = ch_dir / "latest.json"
        if not latest.exists():
            continue
        try:
            data = json.loads(latest.read_text(encoding="utf-8"))
            for s in data.get("signals", []):
                s["_channel"] = data.get("channel", ch_dir.name)
                signals.append(s)
        except Exception:
            continue
    return signals


def run_backtest(
    channel: Optional[str] = None,
    pair: Optional[str] = None,
    risk_per_trade: float = 100.0,
    use_real_outcomes: bool = False,
) -> dict:
    """Run backtest on telegram signals from data_center.

    Args:
        channel: filter by channel alias
        pair: filter by pair (e.g. XAU/USD)
        risk_per_trade: risk amount per trade in USD
        use_real_outcomes: if True, use historical klines to determine TP vs SL

    Returns dict with per-channel and per-pair results.
    """
    signals = _read_all_signals()
    now = datetime.now(timezone.utc).isoformat()

    # Load klines if real mode
    klines_cache: dict[str, list[dict]] = {}
    if use_real_outcomes:
        klines_cache = _load_klines()

    # Filter
    if channel:
        signals = [s for s in signals if s.get("_channel") == channel]
    if pair:
        signals = [s for s in signals if pair.upper() in (s.get("pair", "") or "").upper()]

    # Group by channel
    by_channel: dict[str, list[dict]] = defaultdict(list)
    for s in signals:
        ch = s.get("_channel", "unknown")
        by_channel[ch].append(s)

    # Process each channel
    channel_reports = []
    all_trades = []
    grand_total = 0
    grand_wins = 0
    grand_pnl = 0.0

    for ch, ch_signals in sorted(by_channel.items()):
        trades = []
        for s in ch_signals:
            entry = s.get("entry_price")
            sl = s.get("sl")
            tp = s.get("tp")
            direction = s.get("direction", "")
            pair_name = s.get("pair", "?")
            parsed_at = s.get("parsed_at", "")

            if not _is_sane(pair_name, entry, sl, tp, direction):
                continue

            qty = 20.0 if "XAU" in pair_name.upper() else (1.0 if pair_name.endswith("USDT") else 1000.0)

            if direction == "LONG":
                risk_per_unit = entry - sl
                reward_per_unit = tp - entry
                pnl = reward_per_unit * qty
            else:
                risk_per_unit = sl - entry
                reward_per_unit = entry - tp
                pnl = reward_per_unit * qty

            r_multiple = reward_per_unit / risk_per_unit if risk_per_unit and risk_per_unit > 0 else 0

            # Determine outcome
            outcome = "TP_HIT"  # default optimistic
            actual_pnl = round(reward_per_unit * qty, 2)

            if use_real_outcomes:
                # Find matching klines
                binance_sym = _pair_to_binance(pair_name)
                klines = klines_cache.get(binance_sym, [])
                if klines:
                    from modules.data_center.market_metrics_producer import resolve_tp_sl_outcome
                    res = resolve_tp_sl_outcome(entry, sl, tp, direction, parsed_at, klines)
                    outcome = res["outcome"]
                    if outcome == "SL_HIT":
                        actual_pnl = round(-risk_per_unit * qty, 2)
                    elif outcome == "OPEN":
                        outcome = "OPEN"
                        actual_pnl = 0

            trade = {
                "pair": pair_name,
                "direction": direction,
                "entry": entry, "sl": sl, "tp": tp,
                "r_multiple": round(r_multiple, 4),
                "pnl": actual_pnl if outcome in ("TP_HIT", "SL_HIT") else 0,
                "risk_usd": risk_per_trade,
                "parsed_at": parsed_at,
                "outcome": outcome,
            }
            trades.append(trade)

        if not trades:
            continue

        wins = sum(1 for t in trades if t["outcome"] == "TP_HIT")
        losses = sum(1 for t in trades if t["outcome"] == "SL_HIT")
        open_count = sum(1 for t in trades if t["outcome"] == "OPEN")
        total = len(trades)
        total_pnl = sum(t["pnl"] for t in trades)
        avg_r = sum(t["r_multiple"] for t in trades) / total if total else 0
        pairs_used = sorted(set(t["pair"] for t in trades))
        date_range = ""
        timestamps = sorted(t["parsed_at"] for t in trades if t["parsed_at"])
        if timestamps:
            date_range = f"{timestamps[0][:10]} → {timestamps[-1][:10]}"

        report = {
            "channel": ch,
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "open": open_count,
            "winrate_pct": round((wins / (wins + losses)) * 100, 1) if (wins + losses) > 0 else 0,
            "avg_r": round(avg_r, 4),
            "total_pnl": round(total_pnl, 2),
            "pairs": pairs_used,
            "date_range": date_range,
            "trades": trades,
        }
        channel_reports.append(report)
        all_trades.extend(trades)
        grand_total += total
        grand_wins += wins
        grand_pnl += total_pnl

    grand_losses = sum(t["outcome"] == "SL_HIT" for t in all_trades)
    grand_open = sum(t["outcome"] == "OPEN" for t in all_trades)
    grand_avg_r = sum(t["r_multiple"] for t in all_trades if t["outcome"] != "OPEN") / max(len([t for t in all_trades if t["outcome"] != "OPEN"]), 1)

    result = {
        "contract": "telegram_backtest.v1",
        "source": "data_center/telegram_signals",
        "produced_at": now,
        "mode": "real_klines" if use_real_outcomes else "optimistic_tp_only",
        "risk_per_trade": risk_per_trade,
        "grand_total": {
            "channels": len(channel_reports),
            "trades": grand_total,
            "wins": grand_wins,
            "losses": grand_losses,
            "open": grand_open,
            "winrate_pct": round((grand_wins / (grand_wins + grand_losses)) * 100, 1) if (grand_wins + grand_losses) > 0 else 0,
            "avg_r": round(grand_avg_r, 4),
            "total_pnl": round(grand_pnl, 2),
        },
        "by_channel": channel_reports,
    }

    # Write to output
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    out_path = _OUTPUT_DIR / f"backtest_{run_id}.json"
    out_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    (_OUTPUT_DIR / "latest.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")

    return result


def _load_klines() -> dict[str, list[dict]]:
    """Load klines from data/market_data/klines/ for all available pairs."""
    klines_dir = _PROJECT_ROOT / "data" / "market_data" / "klines"
    cache = {}
    if not klines_dir.exists():
        return cache
    for sym_dir in klines_dir.iterdir():
        if not sym_dir.is_dir():
            continue
        latest = sym_dir / "latest.json"
        if not latest.exists():
            continue
        try:
            data = json.loads(latest.read_text(encoding="utf-8"))
            cache[sym_dir.name] = data.get("klines", [])
        except Exception:
            continue
    return cache


def _pair_to_binance(pair: str) -> str:
    """Map display pair to Binance symbol for klines lookup."""
    mapping = {
        "XAU/USD": "PAXGUSDT", "XAUUSD": "PAXGUSDT",
        "BTC/USDT": "BTCUSDT", "BTCUSDT": "BTCUSDT",
        "ETH/USDT": "ETHUSDT", "ETHUSDT": "ETHUSDT",
        "SOL/USDT": "SOLUSDT", "APTUSDT": "APTUSDT",
        "OPUSDT": "OPUSDT", "INJUSDT": "INJUSDT",
        "EUR/USD": "EURUSDT", "EURUSD": "EURUSDT",
        "GBP/USD": "GBPUSDT", "GBPUSD": "GBPUSDT",
    }
    return mapping.get(pair.upper() if "/" in pair else pair, pair.replace("/", "").upper())


def print_report(result: dict) -> None:
    """Print a human-readable backtest report."""
    gt = result["grand_total"]
    print("=" * 70)
    print("  TELEGRAM SIGNAL BACKTEST")
    print(f"  Source: {result['source']} | Mode: {result['mode']}")
    print(f"  Produced: {result['produced_at']}")
    print("=" * 70)
    print(f"  Channels: {gt['channels']} | Trades: {gt['trades']} | Wins: {gt['wins']} | Losses: {gt['losses']} | Open: {gt.get('open', 0)}")
    print(f"  Winrate: {gt['winrate_pct']}% | Avg R: {gt['avg_r']} | P&L: \${gt['total_pnl']:,.2f}")
    print()

    for cr in result.get("by_channel", []):
        print(f"  ┌─ {cr['channel']}")
        print(f"  │  Trades: {cr['total_trades']} | W: {cr['wins']} | L: {cr['losses']} | WR: {cr['winrate_pct']}% | Avg R: {cr['avg_r']} | P&L: \${cr['total_pnl']:,.2f}")
        print(f"  │  Pairs: {', '.join(cr['pairs'][:5])}")
        print(f"  │  Period: {cr['date_range']}")
        # Top 3 trades
        for t in cr["trades"][:3]:
            print(f"  │  {t['pair']:12s} {t['direction']:6s} entry={t['entry']} sl={t['sl']} tp={t['tp']} R={t['r_multiple']} @ {t['parsed_at'][:19]}")
        if len(cr["trades"]) > 3:
            print(f"  │  ... and {len(cr['trades']) - 3} more")
        print()

    print(f"  Full report: data/trading_lab_v1/backtests/latest.json")


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    channel = None
    pair = None
    report_only = False
    use_real = False

    i = 0
    while i < len(args):
        if args[i] == "--channel" and i + 1 < len(args):
            channel = args[i + 1]; i += 2
        elif args[i] == "--pair" and i + 1 < len(args):
            pair = args[i + 1]; i += 2
        elif args[i] == "--report":
            report_only = True; i += 1
        elif args[i] == "--real":
            use_real = True; i += 1
        else:
            i += 1

    if report_only:
        latest_path = _OUTPUT_DIR / "latest.json"
        if latest_path.exists():
            result = json.loads(latest_path.read_text(encoding="utf-8"))
            print_report(result)
        else:
            print("No backtest report found. Run without --report first.")
    else:
        result = run_backtest(channel=channel, pair=pair, use_real_outcomes=use_real)
        print_report(result)
