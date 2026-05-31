#!/usr/bin/env python3
"""
vision_analysis_writer — transforms bot_vision_step2 output → vision_analysis.v1
and writes to DeskPro and Data Center consumer paths.

Usage:
  python3 scripts/vision_analysis_writer.py
  python3 scripts/vision_analysis_writer.py --run-dir /opt/trading/data/desk_pro/vision/runs/2026-05-30_12-00-00
  python3 scripts/vision_analysis_writer.py --dry-run

Input:  bot_vision_step2 run directory containing summary.json
Output: DeskPro path  → data/deskpro/inputs/vision_analysis/latest.json
        Data Center    → data/data_center/views/vision_analysis/latest.json

Integration with run_vision_pipeline.py:
  After bot_vision_step2 completes, call this script to publish the
  vision_analysis.v1 contract that DeskPro readers can consume.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]

DESKPRO_VISION_ANALYSIS_DIR = REPO_ROOT / "data" / "deskpro" / "inputs" / "vision_analysis"
DC_VISION_ANALYSIS_DIR = REPO_ROOT / "data" / "data_center" / "views" / "vision_analysis"
DC_VISION_HISTORY_DIR = DC_VISION_ANALYSIS_DIR / "history"
DC_VISION_BY_SYMBOL_DIR = DC_VISION_ANALYSIS_DIR / "by_symbol"

RUN_DIR_DEFAULT = REPO_ROOT / "data" / "deskpro" / "vision" / "latest"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _capture_id(symbol: str, timeframe: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"cap_{ts}_{symbol}_{timeframe}"


def read_summary(summary_path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(summary_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR reading summary.json: {e}", file=sys.stderr)
        return None


def extract_signals_from_text(analysis_text: str) -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = []

    patterns = [
        (r"(?:support|S\b)\s*(?:à|:)?\s*(\d+[\d,.]*)", "support_level", 0.70),
        (r"(?:résistance|resistance|R\b)\s*(?:à|:)?\s*(\d+[\d,.]*)", "resistance_level", 0.70),
        (r"(?:tendance|trend)\s*[:=]?\s*(haussier|bullish|baissier|bearish)", "trend_direction", 0.65),
        (r"(?:zone|level)\s*(?:clé|key)\s*[:=]?\s*(\d+[\d,.]*)", "key_level", 0.60),
        (r"(?:invalidation|invalid)\s*(?:si|below|above|en dessous de|au dessus de)\s*(\d+[\d,.]*)", "invalidation_level", 0.55),
        (r"(?:objectif|target)\s*(?:à|:)?\s*(\d+[\d,.]*)", "price_target", 0.50),
    ]

    for pattern, signal_type, default_conf in patterns:
        for match in re.finditer(pattern, analysis_text, re.IGNORECASE):
            raw = match.group(1).replace(",", "")
            try:
                value = float(raw)
                signals.append({
                    "type": signal_type,
                    "value": value,
                    "confidence": round(default_conf, 2),
                    "note": match.group(0).strip()[:120],
                })
            except ValueError:
                signals.append({
                    "type": signal_type,
                    "value": raw[:60],
                    "confidence": round(default_conf, 2),
                    "note": match.group(0).strip()[:120],
                })

    return signals


def extract_signals_from_json(text: str) -> list[dict[str, Any]]:
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.S)
    if not m:
        m = re.search(r"(\{[\s\S]*\})", text)

    if m:
        blob = m.group(1)
        last = blob.rfind("}")
        blob = blob[:last+1] if last != -1 else blob
        try:
            parsed = json.loads(blob)
            charts = parsed.get("charts", [])
            deskpro_signals = []
            for chart in charts:
                base = {
                    "symbol": chart.get("symbol", chart.get("bias", "unknown")),
                    "bias": chart.get("bias", ""),
                    "structure": chart.get("structure", ""),
                }
                for sr_key, stype in [("supports", "support_level"), ("resistances", "resistance_level")]:
                    for level in chart.get(sr_key, []):
                        if isinstance(level, (int, float)):
                            deskpro_signals.append({
                                "type": stype,
                                "value": float(level),
                                "confidence": 0.75,
                                "note": f"{stype} from DeskPro chart analysis",
                            })
                        elif isinstance(level, str) and level.replace(",", "").replace(".", "").isdigit():
                            deskpro_signals.append({
                                "type": stype,
                                "value": float(level.replace(",", "")),
                                "confidence": 0.75,
                                "note": f"{stype} from DeskPro chart analysis",
                            })
                for key in ["plan", "invalidation"]:
                    val = chart.get(key, "")
                    if val:
                        deskpro_signals.append({
                            "type": "analysis_note",
                            "value": val[:200],
                            "confidence": 0.60,
                            "note": f"{key} from chart analysis",
                        })
            return deskpro_signals
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
    return []


def build_vision_analysis(
    summary: dict[str, Any],
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    analysis_text = summary.get("analysis_text", "")
    existing_signals = summary.get("signals", {})

    symbols_found = set()
    symbol_str = "BTCUSDT"
    timeframe_str = "1h"

    if meta:
        symbol_str = str(meta.get("symbol", symbol_str))
        timeframe_str = str(meta.get("timeframe", timeframe_str))

    signals_json = extract_signals_from_json(analysis_text)
    signals_text = extract_signals_from_text(analysis_text)

    all_signals = signals_json if signals_json else signals_text
    if isinstance(existing_signals, dict) and existing_signals.get("charts"):
        for chart in existing_signals.get("charts", []):
            s = chart.get("symbol", "")
            if s:
                symbols_found.add(s)

    if not all_signals:
        all_signals = [{
            "type": "raw_analysis",
            "value": analysis_text[:500] if analysis_text else "No structured analysis available",
            "confidence": 0.50,
            "note": "Extracted from raw analysis text; no structured signals found",
        }]

    return {
        "input_class": "vision_analysis.v1",
        "capture_id": _capture_id(symbol_str, timeframe_str),
        "screen_type": str(meta.get("screen_type", "CHART_TECHNICAL")) if meta else "CHART_TECHNICAL",
        "symbol": symbol_str,
        "timeframe": timeframe_str,
        "analysis_ts": summary.get("ts", _utc_now_iso()),
        "source_module": "bot_vision_step2",
        "source_module_version": "1.0.0",
        "freshness_state": "fresh",
        "capture_status": "ready",
        "run_id": summary.get("run_id", ""),
        "signals": all_signals,
        "analysis_summary": analysis_text[:1000] if analysis_text else "",
        "symbols_found": list(symbols_found) if symbols_found else [symbol_str],
        "refs": {
            "summary_json": summary.get("run_id", ""),
            "source_screenshot": str(summary.get("source_screenshot", "")),
        },
    }


def write_deskpro(data: dict[str, Any]) -> Path:
    DESKPRO_VISION_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    path = DESKPRO_VISION_ANALYSIS_DIR / "latest.json"
    tmp = path.with_suffix(".json.uploading")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)
    print(f"OK: DeskPro <- {path}")
    return path


def _load_symbol_analyses(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(existing, list):
        return [item for item in existing if isinstance(item, dict)]
    if isinstance(existing, dict):
        return [existing]
    return []


def _merge_symbol_analyses(existing: list[dict[str, Any]], new_data: dict[str, Any]) -> list[dict[str, Any]]:
    new_capture_id = str(new_data.get("capture_id", ""))
    merged = [item for item in existing if str(item.get("capture_id", "")) != new_capture_id]
    merged.append(new_data)
    return sorted(merged, key=lambda item: str(item.get("analysis_ts", "")))


def write_data_center(data: dict[str, Any]) -> Path:
    DC_VISION_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    DC_VISION_BY_SYMBOL_DIR.mkdir(parents=True, exist_ok=True)
    DC_VISION_HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    path = DC_VISION_ANALYSIS_DIR / "latest.json"
    tmp = path.with_suffix(".json.uploading")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)
    print(f"OK: DataCenter <- {path}")

    symbol = data.get("symbol", "UNKNOWN")
    sym_path = DC_VISION_BY_SYMBOL_DIR / f"{symbol}.json"
    merged = _merge_symbol_analyses(_load_symbol_analyses(sym_path), data)
    sym_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: DataCenter <- {sym_path}")

    ts = data.get("analysis_ts", _utc_now_iso()).replace(":", "-").replace("T", "_")[:19]
    run_id = data.get("run_id", ts)
    history_path = DC_VISION_HISTORY_DIR / f"{symbol}_{run_id}.json"
    history_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"OK: DataCenter <- {history_path}")

    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Publish vision_analysis.v1 from bot_vision_step2 output")
    ap.add_argument("--run-dir", default=None, help="Path to bot_vision_step2 run directory")
    ap.add_argument("--metadata", default=None, help="Path to capture metadata JSON (sidecar)")
    ap.add_argument("--dry-run", action="store_true", help="Print output without writing")
    args = ap.parse_args()

    if args.run_dir:
        run_dir = Path(args.run_dir)
    else:
        latest_link = REPO_ROOT / "data" / "deskpro" / "vision" / "latest"
        if latest_link.exists():
            run_dir = latest_link.resolve()
        else:
            run_dir = RUN_DIR_DEFAULT

    summary_path = run_dir / "summary.json"
    if not summary_path.exists():
        print(f"ERROR: summary.json not found in {run_dir}", file=sys.stderr)
        return 1

    summary = read_summary(summary_path)
    if not summary:
        return 1

    meta = None
    if args.metadata:
        try:
            meta = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
        except Exception as e:
            print(f"WARN: could not read metadata: {e}", file=sys.stderr)

    data = build_vision_analysis(summary, meta)

    if args.dry_run:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0

    write_deskpro(data)
    write_data_center(data)

    print(f"\nOK: vision_analysis.v1 published ({len(data.get('signals', []))} signals)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
