"""
data_center_router — prove data collectability, route proven data to data_center.

Scans available data sources, validates they are reachable, and produces a
data_center_coverage report listing what's collectable, what's missing, and
routing information.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .vision_analysis_reader import list_available_symbols, read_vision_analysis_freshness

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

_SOURCE_CHECKS = {
    "vision_analysis": {
        "path": "data/data_center/views/vision_analysis/by_symbol/",
        "input_class": "vision_analysis.v1",
        "status": "ESTABLISHED",
        "description": "Chart screenshots analyzed via bot_vision_step2 (DeskPro)",
    },
    "coinglass_ocr": {
        "path": "data/deskpro/inputs/vision_context/coinglass/latest.json",
        "input_class": "vision_context.coinglass.v1",
        "status": "ESTABLISHED",
        "description": "Coinglass OI/Funding/Liquidations via headless OCR",
    },
    "market_metrics": {
        "path": "data/data_center/views/market_metrics/latest.json",
        "input_class": "market_metrics.v1",
        "status": "HYPOTHESIS",
        "description": "Market metrics from Binance/Bitget/Coinglass (not proven in this env)",
    },
    "telegram_screener": {
        "path": "data/telegram_screener/signals/",
        "input_class": "telegram_signal.v1",
        "status": "HYPOTHESIS",
        "description": "Parsed Telegram signals from screener pipeline",
    },
    "telegram_collector": {
        "path": "modules/collector_telegram/outputs/channel_results/",
        "input_class": None,
        "status": "HYPOTHESIS",
        "description": "Raw Telegram messages from collector_telegram",
    },
    "runtime_health": {
        "path": "data/runtime_health/ledger/events.jsonl",
        "input_class": None,
        "status": "ESTABLISHED",
        "description": "Runtime health events (webhook, mobile control, gate)",
    },
}


def _check_path(path_str: str) -> dict:
    p = _PROJECT_ROOT / path_str
    exists = p.exists()
    is_file = p.is_file() if exists else False
    is_dir = p.is_dir() if exists else False
    count = None
    if is_dir:
        count = len(list(p.glob("*")))
    elif is_file:
        count = 1
    return {
        "path": path_str,
        "exists": exists,
        "is_file": is_file,
        "is_dir": is_dir,
        "item_count": count,
    }


def _check_vision_symbols(symbols: list[str]) -> dict:
    result = {}
    for sym in symbols:
        freshness = read_vision_analysis_freshness(sym)
        result[sym] = freshness
    return result


def produce_data_center_coverage() -> dict:
    now = datetime.now(timezone.utc).isoformat()

    sources = {}
    for source_id, config in _SOURCE_CHECKS.items():
        path_check = _check_path(config["path"])
        reachable = path_check["exists"]
        provenance = "PROVEN" if reachable else "MISSING"
        if config["status"] == "HYPOTHESIS":
            provenance = "HYPOTHESIS" if reachable else "MISSING"

        sources[source_id] = {
            **config,
            **path_check,
            "provenance": provenance,
        }

    vision_symbols = list_available_symbols()
    vision_details = _check_vision_symbols(vision_symbols)

    return {
        "contract": "data_center_coverage.v1",
        "produced_at": now,
        "total_sources": len(_SOURCE_CHECKS),
        "proven_sources": sum(1 for s in sources.values() if s["provenance"] == "PROVEN"),
        "hypothesis_sources": sum(1 for s in sources.values() if s["provenance"] == "HYPOTHESIS"),
        "missing_sources": sum(1 for s in sources.values() if s["provenance"] == "MISSING"),
        "sources": sources,
        "vision_analysis": {
            "total_symbols": len(vision_symbols),
            "symbols": vision_symbols,
            "by_symbol": vision_details,
        },
    }


def route_to_data_center(output_path: Optional[Path] = None) -> dict:
    """Produce coverage report and write to data_center."""
    coverage = produce_data_center_coverage()
    path = output_path or (_PROJECT_ROOT / "data" / "data_center" / "views" / "data_center_coverage" / "latest.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(coverage, indent=2, default=str), encoding="utf-8")
    return coverage
