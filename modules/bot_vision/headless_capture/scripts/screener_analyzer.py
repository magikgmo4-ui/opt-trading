#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from PIL import Image
except ImportError:
    Image = None

REPO_ROOT = Path(__file__).resolve().parents[4]

SCREENER_CATEGORIES = [
    "SCREENER_BIGGEST_CAPS", "SCREENER_TRENDING", "SCREENER_AI",
    "SCREENER_DEFENSE", "SCREENER_SPATIAL", "SCREENER_CRYPTO_STOCKS", "SCREENER_ENERGY",
]

SCREENER_URL_LABELS: dict[str, str] = {
    "SCREENER_BIGGEST_CAPS": "biggest_caps",
    "SCREENER_TRENDING": "trending",
    "SCREENER_AI": "ai",
    "SCREENER_DEFENSE": "defense",
    "SCREENER_SPATIAL": "spatial",
    "SCREENER_CRYPTO_STOCKS": "crypto_stocks",
    "SCREENER_ENERGY": "energy",
}

_STUB_STOCKS: dict[str, list[dict[str, Any]]] = {
    "SCREENER_BIGGEST_CAPS": [
        {"symbol": "AAPL", "name": "Apple Inc", "price": 198.50, "change_pct": 1.25, "volume": 52_400_000},
        {"symbol": "MSFT", "name": "Microsoft Corp", "price": 425.30, "change_pct": 0.85, "volume": 28_100_000},
        {"symbol": "GOOGL", "name": "Alphabet Inc", "price": 175.80, "change_pct": -0.32, "volume": 19_800_000},
        {"symbol": "AMZN", "name": "Amazon.com Inc", "price": 198.20, "change_pct": 1.52, "volume": 35_600_000},
        {"symbol": "NVDA", "name": "NVIDIA Corp", "price": 875.40, "change_pct": 2.80, "volume": 45_200_000},
        {"symbol": "TSLA", "name": "Tesla Inc", "price": 245.60, "change_pct": -1.10, "volume": 98_500_000},
        {"symbol": "META", "name": "Meta Platforms", "price": 512.70, "change_pct": 0.45, "volume": 22_300_000},
        {"symbol": "BRK.B", "name": "Berkshire Hathaway", "price": 418.90, "change_pct": 0.12, "volume": 5_200_000},
        {"symbol": "JPM", "name": "JPMorgan Chase", "price": 198.40, "change_pct": 0.78, "volume": 12_100_000},
        {"symbol": "V", "name": "Visa Inc", "price": 285.60, "change_pct": 0.55, "volume": 9_800_000},
    ],
    "SCREENER_TRENDING": [
        {"symbol": "PLTR", "name": "Palantir Technologies", "price": 28.50, "change_pct": 5.20, "volume": 78_500_000},
        {"symbol": "SMCI", "name": "Super Micro Computer", "price": 1024.80, "change_pct": 4.50, "volume": 15_200_000},
        {"symbol": "ARM", "name": "Arm Holdings", "price": 145.30, "change_pct": 6.80, "volume": 22_100_000},
        {"symbol": "RDDT", "name": "Reddit Inc", "price": 62.40, "change_pct": 8.20, "volume": 12_500_000},
        {"symbol": "MSTR", "name": "MicroStrategy", "price": 1580.20, "change_pct": 3.50, "volume": 4_800_000},
        {"symbol": "COIN", "name": "Coinbase Global", "price": 245.80, "change_pct": 4.20, "volume": 18_900_000},
        {"symbol": "ASTS", "name": "AST SpaceMobile", "price": 32.60, "change_pct": 12.50, "volume": 25_400_000},
    ],
    "SCREENER_AI": [
        {"symbol": "NVDA", "name": "NVIDIA Corp", "price": 875.40, "change_pct": 2.80, "volume": 45_200_000},
        {"symbol": "AMD", "name": "Advanced Micro Devices", "price": 185.60, "change_pct": 1.80, "volume": 38_500_000},
        {"symbol": "SMCI", "name": "Super Micro Computer", "price": 1024.80, "change_pct": 4.50, "volume": 15_200_000},
        {"symbol": "CRM", "name": "Salesforce Inc", "price": 305.40, "change_pct": 0.95, "volume": 8_200_000},
        {"symbol": "CROX", "name": "CrowdStrike Holdings", "price": 385.20, "change_pct": 1.65, "volume": 5_800_000},
        {"symbol": "PLTR", "name": "Palantir Technologies", "price": 28.50, "change_pct": 5.20, "volume": 78_500_000},
        {"symbol": "SNOW", "name": "Snowflake Inc", "price": 185.30, "change_pct": -0.40, "volume": 7_200_000},
        {"symbol": "AI", "name": "C3.ai Inc", "price": 35.80, "change_pct": 3.20, "volume": 12_800_000},
    ],
    "SCREENER_DEFENSE": [
        {"symbol": "RTX", "name": "RTX Corp", "price": 118.50, "change_pct": 0.45, "volume": 6_500_000},
        {"symbol": "LMT", "name": "Lockheed Martin", "price": 485.60, "change_pct": 0.85, "volume": 2_100_000},
        {"symbol": "GD", "name": "General Dynamics", "price": 305.40, "change_pct": 0.55, "volume": 1_800_000},
        {"symbol": "NOC", "name": "Northrop Grumman", "price": 525.80, "change_pct": 1.20, "volume": 1_200_000},
        {"symbol": "BA", "name": "Boeing Co", "price": 215.30, "change_pct": -0.80, "volume": 8_900_000},
        {"symbol": "HII", "name": "Huntington Ingalls", "price": 285.90, "change_pct": 0.30, "volume": 450_000},
    ],
    "SCREENER_SPATIAL": [
        {"symbol": "ASTS", "name": "AST SpaceMobile", "price": 32.60, "change_pct": 12.50, "volume": 25_400_000},
        {"symbol": "RKLB", "name": "Rocket Lab USA", "price": 8.45, "change_pct": 5.60, "volume": 18_200_000},
        {"symbol": "SPCE", "name": "Virgin Galactic", "price": 2.85, "change_pct": -2.10, "volume": 12_500_000},
        {"symbol": "LUNR", "name": "Intuitive Machines", "price": 15.20, "change_pct": 8.40, "volume": 22_800_000},
        {"symbol": "MAXR", "name": "Maxar Technologies", "price": 52.40, "change_pct": 1.80, "volume": 1_500_000},
        {"symbol": "IRDM", "name": "Iridium Communications", "price": 42.80, "change_pct": 0.65, "volume": 1_200_000},
    ],
    "SCREENER_CRYPTO_STOCKS": [
        {"symbol": "MSTR", "name": "MicroStrategy", "price": 1580.20, "change_pct": 3.50, "volume": 4_800_000},
        {"symbol": "COIN", "name": "Coinbase Global", "price": 245.80, "change_pct": 4.20, "volume": 18_900_000},
        {"symbol": "RIOT", "name": "Riot Platforms", "price": 18.60, "change_pct": 5.80, "volume": 15_200_000},
        {"symbol": "MARA", "name": "Mara Holdings", "price": 22.40, "change_pct": 6.50, "volume": 28_500_000},
        {"symbol": "CLSK", "name": "CleanSpark Inc", "price": 16.80, "change_pct": 7.20, "volume": 12_800_000},
        {"symbol": "WULF", "name": "TeraWulf Inc", "price": 8.50, "change_pct": 4.80, "volume": 22_100_000},
        {"symbol": "IREN", "name": "Iris Energy", "price": 12.40, "change_pct": 3.90, "volume": 8_500_000},
    ],
    "SCREENER_ENERGY": [
        {"symbol": "XOM", "name": "Exxon Mobil", "price": 128.50, "change_pct": 0.35, "volume": 18_500_000},
        {"symbol": "CVX", "name": "Chevron Corp", "price": 165.40, "change_pct": 0.55, "volume": 9_200_000},
        {"symbol": "COP", "name": "ConocoPhillips", "price": 135.80, "change_pct": 0.25, "volume": 5_800_000},
        {"symbol": "EOG", "name": "EOG Resources", "price": 142.50, "change_pct": 0.40, "volume": 3_200_000},
        {"symbol": "OXY", "name": "Occidental Petroleum", "price": 72.80, "change_pct": -0.50, "volume": 8_500_000},
        {"symbol": "SLB", "name": "Schlumberger NV", "price": 58.40, "change_pct": 0.70, "volume": 7_800_000},
        {"symbol": "HAL", "name": "Halliburton Co", "price": 42.30, "change_pct": 0.85, "volume": 6_200_000},
    ],
}


def _stub_for_screener(screener_symbol: str) -> list[dict[str, Any]]:
    return _STUB_STOCKS.get(screener_symbol, _STUB_STOCKS["SCREENER_BIGGEST_CAPS"])


def _screener_to_url_label(screener_symbol: str) -> str:
    return SCREENER_URL_LABELS.get(screener_symbol, "unknown")


def _tesseract_available() -> bool:
    try:
        import pytesseract
        return True
    except ImportError:
        return False


def _extract_with_ocr(image_path: Path, screener_symbol: str) -> list[dict[str, Any]]:
    if not _tesseract_available() or Image is None:
        return []
    import pytesseract
    try:
        img = Image.open(str(image_path))
        text = pytesseract.image_to_string(img)
        detections: list[dict[str, Any]] = []
        for match in re.finditer(r'([A-Z]{1,5})\s+([A-Z][A-Za-z\s.&]+)\s+(\d+[\d,.]*)\s+([+-]?\d+\.?\d*)', text):
            try:
                symbol = match.group(1).strip()
                name = match.group(2).strip()
                price = float(match.group(3).replace(",", ""))
                change = float(match.group(4))
                if len(symbol) <= 5 and price > 1:
                    detections.append({
                        "symbol": symbol,
                        "name": name[:60],
                        "price": price,
                        "change_pct": change,
                        "confidence": 0.55,
                        "detection_method": "ocr_raw",
                    })
            except (ValueError, IndexError):
                pass
        return detections
    except Exception:
        return []


_VALID_SCREENER_TYPES = set(SCREENER_CATEGORIES)


def analyze(
    sidecar: dict[str, Any],
    use_real_ocr: bool = False,
) -> dict[str, Any]:
    screener_symbol = str(sidecar.get("symbol", "SCREENER_BIGGEST_CAPS"))
    png_path = sidecar.get("png_path") or sidecar.get("output_png") or ""
    captured_at = sidecar.get("created_at_utc") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if screener_symbol not in _VALID_SCREENER_TYPES:
        screener_symbol = "SCREENER_BIGGEST_CAPS"

    stocks: list[dict[str, Any]] = []
    method = "stub"

    if use_real_ocr and png_path:
        png_full = Path(png_path)
        if not png_full.is_absolute():
            png_full = REPO_ROOT / png_full
        if png_full.exists():
            ocr_stocks = _extract_with_ocr(png_full, screener_symbol)
            if ocr_stocks:
                stocks = ocr_stocks
                method = "ocr_real"

    if not stocks:
        stocks_raw = _stub_for_screener(screener_symbol)
        stocks = [
            {
                "symbol": s["symbol"],
                "name": s["name"],
                "price": s["price"],
                "change_pct": s["change_pct"],
                "volume": s["volume"],
                "confidence": 0.72,
                "detection_method": "stub",
            }
            for s in stocks_raw
        ]

    return {
        "input_class": "vision_context.screener.v1",
        "screener_symbol": screener_symbol,
        "screener_label": _screener_to_url_label(screener_symbol),
        "source_id": "tradingview_screener_headless_bot",
        "captured_at": captured_at,
        "analysis_ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "freshness_state": "fresh",
        "analysis_method": method,
        "stocks": stocks,
        "stock_count": len(stocks),
        "top_gainers": sorted(
            [s for s in stocks if s.get("change_pct", 0) > 0],
            key=lambda x: x["change_pct"], reverse=True,
        )[:3] if stocks else [],
        "top_losers": sorted(
            [s for s in stocks if s.get("change_pct", 0) < 0],
            key=lambda x: x["change_pct"],
        )[:3] if stocks else [],
        "avg_change_pct": round(sum(s.get("change_pct", 0) for s in stocks) / len(stocks), 2) if stocks else 0,
        "refs": {
            "capture_source": str(sidecar.get("source", "tradingview_screener")),
            "image_ref": png_path,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyzer for TradingView screener screenshots")
    ap.add_argument("--sidecar", help="Path to capture sidecar JSON")
    ap.add_argument("--stdin", action="store_true", help="Read sidecar from stdin")
    ap.add_argument("--real-ocr", action="store_true", help="Attempt real OCR (requires pytesseract)")
    args = ap.parse_args()

    sidecar: dict[str, Any] | None = None
    if args.stdin:
        try:
            sidecar = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"ERROR: invalid JSON from stdin: {e}", file=sys.stderr)
            return 1
    elif args.sidecar:
        try:
            sidecar = json.loads(Path(args.sidecar).read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"ERROR: cannot read sidecar: {e}", file=sys.stderr)
            return 1
    else:
        print("ERROR: provide --sidecar or --stdin", file=sys.stderr)
        return 1

    result = analyze(sidecar, use_real_ocr=args.real_ocr)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
