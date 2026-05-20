#!/usr/bin/env python3
"""
Perf Engine Module
Tracks performance of paper trading positions.

Usage:
    python -m modules.perf_engine.app.perf_engine [command] [args]
"""
import sys
import os
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --- Configuration ---
MODULE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MODULE_DIR.parent.parent
CONFIG_DIR = MODULE_DIR / "config"

def get_output_dir(path_str):
    """Resolve output directory relative to project root if not absolute."""
    p = Path(path_str)
    if p.is_absolute():
        return p
    return PROJECT_ROOT / p

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/perf"))

# --- Core Logic ---
class PerfEngine:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def load_input(self, input_path):
        """Load and parse input JSON."""
        p = Path(input_path)
        if not p.exists():
            # Try relative to project root
            p = PROJECT_ROOT / input_path
            if not p.exists():
                print(f"Error: Input file not found: {input_path}")
                sys.exit(1)
        
        with open(p, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print(f"Error: Input JSON must be a list of objects ({input_path}).")
                sys.exit(1)
            return data

    def merge_data(self, positions, execution):
        """Merge data sources by symbol."""
        merged = {}
        
        def merge_list(source_list, source_name):
            for item in source_list:
                sym = item.get("symbol")
                if not sym: continue
                if sym not in merged: merged[sym] = {"symbol": sym}
                merged[sym][source_name] = item

        merge_list(positions, "position")
        merge_list(execution, "execution")
        
        return merged

    def track_symbol(self, symbol, data):
        """Derive performance state for a single symbol."""
        
        pos = data.get("position", {})
        exe = data.get("execution", {})
        
        pos_status = pos.get("position_status", "FLAT")
        side = pos.get("side", "NONE")
        size_hint = pos.get("size_hint", "NONE")
        max_risk_pct = pos.get("max_risk_pct", 0.0)
        pos_mode = pos.get("position_mode", "PAPER")
        
        exe_status = exe.get("execution_status", "BLOCKED")
        
        perf_status = "INACTIVE"
        tracking_mode = pos_mode
        pnl_status = "NO_POSITION"
        progress_state = "IDLE"
        rationale = []
        
        # Logic
        if pos_status == "OPEN_CANDIDATE" and exe_status == "READY":
            perf_status = "TRACKING"
            pnl_status = "OPEN_SIMULATED"
            progress_state = "AWAITING_MARK_TO_MARKET"
            rationale.append(f"Tracking {side} position ({size_hint}).")
            
        elif pos_status == "HOLD":
            perf_status = "WATCHLIST"
            pnl_status = "WATCHING"
            progress_state = "REVIEW"
            rationale.append("Watching symbol (Hold state).")
            
        elif pos_status == "BLOCKED":
            perf_status = "BLOCKED"
            pnl_status = "BLOCKED"
            progress_state = "BLOCKED"
            rationale.append("Symbol blocked.")
            
        else:
            perf_status = "INACTIVE"
            pnl_status = "NO_POSITION"
            progress_state = "IDLE"
            rationale.append("No active position.")

        return {
            "symbol": symbol,
            "perf_status": perf_status,
            "tracking_mode": tracking_mode,
            "side": side,
            "exposure_hint": size_hint,
            "max_risk_pct": max_risk_pct,
            "pnl_status": pnl_status,
            "progress_state": progress_state,
            "rationale": "; ".join(rationale),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def track_performance(self, merged_data):
        states = []
        for sym, data in merged_data.items():
            res = self.track_symbol(sym, data)
            states.append(res)
            
        # Sort: TRACKING first
        status_map = {"TRACKING": 3, "WATCHLIST": 2, "INACTIVE": 1, "BLOCKED": 0}
        states.sort(key=lambda x: status_map.get(x["perf_status"], 0), reverse=True)
        return states

    def run_track(self, positions_path, execution_path):
        p_data = self.load_input(positions_path)
        e_data = self.load_input(execution_path)
        
        merged = self.merge_data(p_data, e_data)
        states = self.track_performance(merged)
        
        print(json.dumps(states, indent=2))
        return states

    def run_sample(self):
        """Run with internal sample files."""
        return self.run_track(
            CONFIG_DIR / "sample_positions.json",
            CONFIG_DIR / "sample_execution.json"
        )

    def export_results(self, states=None, output_path=None):
        if not states:
            states = self.run_sample()
            
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"perf_states_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(states, f, indent=2)
        print(f"Exported performance states to: {output_path}")

    def explain_results(self, positions_path, execution_path):
        states = self.run_track(positions_path, execution_path)
        print("\n=== Perf Engine Explanation ===\n")
        print("Mode: PAPER ONLY (PnL Simulation)\n")
        
        for item in states:
            print(f"Symbol: {item['symbol']}")
            print(f"  Status: {item['perf_status']} ({item['pnl_status']})")
            print(f"  Progress: {item['progress_state']}")
            print(f"  Rationale: {item['rationale']}")
            print("-" * 30)


def _get_in(d: dict, path: list[str]) -> Any:
    cur: Any = d
    for k in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(k)
    return cur


def _first_non_empty(*vals: Any) -> Any:
    for v in vals:
        if v is None:
            continue
        if isinstance(v, str) and not v.strip():
            continue
        return v
    return None


def _parse_iso(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def _extract_observation_date(evt: dict) -> str | None:
    ts = _first_non_empty(evt.get("produced_at"), evt.get("timestamp"), evt.get("_ts"))
    dt = _parse_iso(str(ts)) if ts else None
    if dt and dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    if dt:
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d")

    run_id = _first_non_empty(evt.get("run_id"), evt.get("source_run_id"))
    if isinstance(run_id, str) and len(run_id) >= 8 and run_id[:8].isdigit():
        return f"{run_id[:4]}-{run_id[4:6]}-{run_id[6:8]}"
    return None


def _as_float(x: Any) -> float | None:
    if x is None or x == "":
        return None
    try:
        return float(x)
    except Exception:
        return None


def _load_events(path: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        p = PROJECT_ROOT / path
        if not p.exists():
            raise FileNotFoundError(path)

    raw = p.read_text(encoding="utf-8", errors="replace").strip()
    if not raw:
        return []

    if raw.lstrip().startswith("["):
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("Input JSON must be a list")
        return [x for x in data if isinstance(x, dict)]

    out: list[dict] = []
    for ln in raw.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            obj = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def score_strategy_events(
    events: list[dict],
    *,
    strategy_id: str,
    strategy_version: str | None = None,
    min_sample_size: int = 30,
    min_observation_days: int = 14,
    min_pass_rate: float = 0.80,
) -> dict[str, Any]:
    filtered: list[dict] = []
    for e in events:
        sid = _first_non_empty(e.get("strategy_id"), _get_in(e, ["strategy", "strategy_id"]))
        if sid != strategy_id:
            continue
        if strategy_version:
            sv = _first_non_empty(e.get("strategy_version"), _get_in(e, ["strategy", "strategy_version"]))
            if sv != strategy_version:
                continue
        filtered.append(e)

    verdicts = []
    outcomes = []
    pnls: list[tuple[str, float]] = []
    observation_days = set()

    for e in filtered:
        day = _extract_observation_date(e)
        if day:
            observation_days.add(day)

        v = _first_non_empty(e.get("verdict"), e.get("pipeline_verdict"), e.get("validation_verdict"))
        if v:
            verdicts.append(str(v).upper())

        o = _first_non_empty(e.get("outcome"), _get_in(e, ["pnl_paper", "outcome"]))
        if o is not None and str(o).strip():
            outcomes.append(str(o).lower())

        pnl = _first_non_empty(e.get("pnl_net"), _get_in(e, ["pnl_paper", "net_pnl"]))
        pnl_f = _as_float(pnl)
        if pnl_f is not None:
            produced_at = _first_non_empty(e.get("produced_at"), e.get("timestamp"), e.get("_ts"), "")
            pnls.append((str(produced_at), pnl_f))

    sample_size = len(filtered)
    pass_count = sum(1 for v in verdicts if v in ("PASS", "APPROVED"))
    pass_rate = (pass_count / len(verdicts)) if verdicts else None

    win_count = sum(1 for o in outcomes if o in ("win", "won", "tp", "profit"))
    loss_count = sum(1 for o in outcomes if o in ("loss", "lost", "sl", "stop", "fail"))
    win_rate = (win_count / (win_count + loss_count)) if (win_count + loss_count) else None

    pnl_cumulative = sum(p for _, p in pnls) if pnls else None
    expectancy = (pnl_cumulative / len(pnls)) if pnls else None

    max_dd = None
    if pnls:
        pnls_sorted = sorted(pnls, key=lambda t: t[0])
        eq = 0.0
        peak = 0.0
        dd = 0.0
        for _, p in pnls_sorted:
            eq += p
            if eq > peak:
                peak = eq
            dd = min(dd, eq - peak)
        max_dd = dd

    promotion_verdict = "INSUFFICIENT_SAMPLE"
    promotion_reason = "sample_size_below_threshold"
    if sample_size >= min_sample_size and len(observation_days) >= min_observation_days:
        if pass_rate is not None and pass_rate < min_pass_rate:
            promotion_verdict = "BLOCKED_LOW_PASS_RATE"
            promotion_reason = "pass_rate_below_threshold"
        else:
            promotion_verdict = "PROMOTE_RECOMMENDED"
            promotion_reason = "thresholds_met"
    elif sample_size >= min_sample_size and len(observation_days) < min_observation_days:
        promotion_reason = "observation_days_below_threshold"

    return {
        "strategy_id": strategy_id,
        "strategy_version": strategy_version or "",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "sample_size": sample_size,
        "observation_days": len(observation_days),
        "metrics": {
            "pass_rate": pass_rate,
            "win_rate": win_rate,
            "pnl_cumulative": pnl_cumulative,
            "expectancy": expectancy,
            "max_drawdown": max_dd,
        },
        "promotion_gate": {
            "verdict": promotion_verdict,
            "reason": promotion_reason,
            "thresholds": {
                "min_sample_size": min_sample_size,
                "min_observation_days": min_observation_days,
                "min_pass_rate": min_pass_rate,
            },
        },
        "retirement_gate": {
            "verdict": "KEEP_OBSERVING",
        },
    }


# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Perf Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    track_parser = subparsers.add_parser("track", help="Track performance")
    track_parser.add_argument("--positions", help="Position results JSON")
    track_parser.add_argument("--execution", help="Execution results JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--positions", help="Position results JSON")
    exp_parser.add_argument("--execution", help="Execution results JSON")
    exp_parser.add_argument("--output", help="Output file path")

    explain_parser = subparsers.add_parser("explain", help="Explain perf logic")
    explain_parser.add_argument("--positions", help="Position results JSON")
    explain_parser.add_argument("--execution", help="Execution results JSON")

    score_parser = subparsers.add_parser("strategy-score", help="Compute strategy score from Observation Events (JSONL/JSON list)")
    score_parser.add_argument("--input", required=True, help="Path to events.jsonl or events.json (list)")
    score_parser.add_argument("--strategy-id", required=True, help="Filter strategy_id")
    score_parser.add_argument("--strategy-version", help="Optional filter strategy_version")
    score_parser.add_argument("--min-sample-size", type=int, default=30)
    score_parser.add_argument("--min-observation-days", type=int, default=14)
    score_parser.add_argument("--min-pass-rate", type=float, default=0.80)

    args = parser.parse_args()
    engine = PerfEngine()

    if args.command == "status":
        print("Perf Engine Status: OK")
        print(f"Output Dir: {engine.output_dir}")
        print("Mode: PAPER ONLY")
    elif args.command == "sample":
        engine.run_sample()
    elif args.command == "track":
        # Use provided args or defaults
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        engine.run_track(pos, exe)
    elif args.command == "export":
        # Use provided args or defaults
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        states = engine.run_track(pos, exe)
        engine.export_results(states, output_path=args.output)
    elif args.command == "explain":
        # Use provided args or defaults
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        engine.explain_results(pos, exe)
    elif args.command == "strategy-score":
        events = _load_events(args.input)
        pack = score_strategy_events(
            events,
            strategy_id=args.strategy_id,
            strategy_version=args.strategy_version,
            min_sample_size=args.min_sample_size,
            min_observation_days=args.min_observation_days,
            min_pass_rate=args.min_pass_rate,
        )
        print(json.dumps(pack, indent=2, default=str))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
