#!/usr/bin/env python3
"""
coinglass_ocr_analyzer — OCR-based extraction of Coinglass metrics from screenshots.

Coinglass pages captured:
  - LIQUIDITY_COINGLASS  → liquidation heatmap + data table
  - FUNDING_COINGLASS    → funding rate table by exchange
  - OI_COINGLASS         → open interest chart + aggregate
  - LS_RATIO_COINGLASS   → long/short ratio by exchange

Two modes:
  1. REAL_OCR (requires pytesseract + tesseract-ocr) — actual text extraction
  2. STUB (default) — simulated extraction based on capture metadata + screen_type
     Uses canned realistic values for the symbol. Good for pipeline testing.

Output: vision_context.coinglass.v1 format → stdout (for vision_context_writer.py)

Usage:
  python3 scripts/coinglass_ocr_analyzer.py --sidecar /path/to/sidecar.json
  python3 scripts/coinglass_ocr_analyzer.py --sidecar /path/to/sidecar.json --real-ocr
  python3 scripts/coinglass_ocr_analyzer.py --stdin   # read sidecar from pipe
"""
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
    from PIL import ImageOps
except ImportError:
    Image = None
    ImageOps = None

REPO_ROOT = Path(__file__).resolve().parents[4]


# ── Stub data generators per screen type ──────────────────

_STUB_METRICS: dict[str, dict[str, Any]] = {
    "LIQUIDITY_COINGLASS": {
        "detections": [
            {"metric": "liquidations_long", "value": 42_500_000, "unit": "USD", "confidence": 0.78},
            {"metric": "liquidations_short", "value": 38_200_000, "unit": "USD", "confidence": 0.76},
            {"metric": "liquidation_heatmap_level", "value": 67_500, "unit": "USD", "confidence": 0.82},
        ],
    },
    "FUNDING_COINGLASS": {
        "detections": [
            {"metric": "funding_rate", "value": 0.00015, "unit": "rate", "confidence": 0.80},
            {"metric": "funding_rate", "value": 0.00012, "unit": "rate", "confidence": 0.72},
        ],
    },
    "OI_COINGLASS": {
        "detections": [
            {"metric": "open_interest", "value": 72_145_890_000, "unit": "USD", "confidence": 0.85},
            {"metric": "open_interest_change_24h", "value": 1_200_000_000, "unit": "USD", "confidence": 0.70},
        ],
    },
    "LS_RATIO_COINGLASS": {
        "detections": [
            {"metric": "long_short_ratio", "value": 1.25, "unit": "ratio", "confidence": 0.75},
            {"metric": "long_short_ratio", "value": 1.18, "unit": "ratio", "confidence": 0.68},
        ],
    },
}


def _stub_values_for_symbol(symbol: str, screen_type: str) -> list[dict[str, Any]]:
    """Generate realistic stub values based on symbol and screen type."""
    base = _STUB_METRICS.get(screen_type, {}).get("detections", [])

    symbol_adj = {"BTCUSDT.P": 1.0, "ETHUSDT.P": 0.35}
    adj = symbol_adj.get(symbol, 0.5)

    results = []
    for d in base:
        adjusted = round(d["value"] * adj, 2) if isinstance(d["value"], (int, float)) else d["value"]
        results.append({
            "extracted_value": adjusted,
            "detected_metric_type": d["metric"],
            "confidence": d["confidence"],
            "detection_method": "stub",
            "unit": d.get("unit", ""),
        })
    return results


def _coinglass_slug(screen_type: str) -> str:
    return {
        "LIQUIDITY_COINGLASS": "LiquidationData",
        "FUNDING_COINGLASS": "FundingRate",
        "OI_COINGLASS": "OpenInterest",
        "LS_RATIO_COINGLASS": "LongShortRatio",
    }.get(screen_type, "Unknown")


# ── Real OCR extraction (requires pytesseract) ────────────

def _tesseract_available() -> bool:
    try:
        import pytesseract  # noqa
        return True
    except ImportError:
        return False


def _parse_numeric_token(token: str) -> float | None:
    raw = token.strip().replace(",", "")
    multiplier = 1.0
    if raw.lower().endswith("b"):
        multiplier = 1_000_000_000.0
        raw = raw[:-1]
    elif raw.lower().endswith("m"):
        multiplier = 1_000_000.0
        raw = raw[:-1]
    elif raw.lower().endswith("k"):
        multiplier = 1_000.0
        raw = raw[:-1]
    elif raw.endswith("%"):
        raw = raw[:-1]
    try:
        return float(raw) * multiplier
    except ValueError:
        return None


def _extract_with_ocr_text(text: str, screen_type: str) -> list[dict[str, Any]]:
    detections: list[dict[str, Any]] = []
    lowered = screen_type.lower()

    if "liquidity" in lowered or "liquidation" in lowered:
        metric_cycle = ["liquidations_long", "liquidations_short", "liquidation_heatmap_level"]
        for idx, match in enumerate(re.finditer(r'([+-]?\d+(?:[\d,.]*\d)?(?:[KMB%])?)', text, re.IGNORECASE)):
            parsed = _parse_numeric_token(match.group(1))
            if parsed is None:
                continue
            metric = metric_cycle[min(idx, len(metric_cycle) - 1)]
            unit = "USD" if metric != "liquidation_heatmap_level" else "price"
            detections.append({
                "extracted_value": parsed,
                "detected_metric_type": metric,
                "confidence": 0.58 if metric != "liquidation_heatmap_level" else 0.62,
                "detection_method": "ocr_raw",
                "unit": unit,
            })

    elif "funding" in lowered:
        for match in re.finditer(r'([+-]?\d+(?:\.\d+)?%)', text):
            parsed = _parse_numeric_token(match.group(1))
            if parsed is None:
                continue
            detections.append({
                "extracted_value": parsed,
                "detected_metric_type": "funding_rate",
                "confidence": 0.56,
                "detection_method": "ocr_raw",
                "unit": "percent",
            })

    elif "open_interest" in lowered or "oi_" in lowered:
        for idx, match in enumerate(re.finditer(r'([+-]?\d+(?:[\d,.]*\d)?(?:[KMB]))', text, re.IGNORECASE)):
            parsed = _parse_numeric_token(match.group(1))
            if parsed is None:
                continue
            metric = "open_interest" if idx == 0 else "open_interest_change_24h"
            detections.append({
                "extracted_value": parsed,
                "detected_metric_type": metric,
                "confidence": 0.57,
                "detection_method": "ocr_raw",
                "unit": "USD",
            })

    elif "longshortratio" in lowered or "ls_ratio" in lowered:
        for match in re.finditer(r'([+-]?\d+(?:\.\d+)?)', text):
            parsed = _parse_numeric_token(match.group(1))
            if parsed is None:
                continue
            detections.append({
                "extracted_value": parsed,
                "detected_metric_type": "long_short_ratio",
                "confidence": 0.55,
                "detection_method": "ocr_raw",
                "unit": "ratio",
            })

    # Keep signal-rich but bounded output.
    return detections[:3]


def _extract_with_ocr(image_path: Path, screen_type: str) -> list[dict[str, Any]]:
    """Attempt real OCR extraction. Returns list of detections or empty list."""
    if not _tesseract_available():
        return []
    if Image is None or ImageOps is None:
        return []

    import pytesseract

    try:
        img = Image.open(str(image_path))
        variants = [img]

        # Try a couple of cheap preprocessing variants before giving up.
        grayscale = ImageOps.grayscale(img)
        variants.append(grayscale)
        variants.append(ImageOps.autocontrast(grayscale))

        for variant in variants:
            text = pytesseract.image_to_string(variant)
            detections = _extract_with_ocr_text(text, screen_type)
            if detections:
                return detections
        return []

    except Exception as e:
        print(f"WARN: OCR extraction failed: {e}", file=sys.stderr)
        return []


# ── Main analyzer ─────────────────────────────────────────

def analyze(
    sidecar: dict[str, Any],
    use_real_ocr: bool = False,
) -> dict[str, Any]:
    screen_type = str(sidecar.get("screen_type", "LIQUIDITY_COINGLASS"))
    symbol = str(sidecar.get("symbol", "BTCUSDT.P"))
    png_path = sidecar.get("png_path") or sidecar.get("output_png") or ""
    source = str(sidecar.get("source", "coinglass"))

    if not VALID_COINGLASS_TYPES.issuperset({screen_type}):
        screen_type = "LIQUIDITY_COINGLASS"

    captured_at = sidecar.get("created_at_utc") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    capture_id = f"cg_{screen_type.lower()}_{symbol}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

    detections: list[dict[str, Any]] = []
    final_method = "stub"
    warnings: list[str] = []

    # Try real OCR first if requested
    if use_real_ocr and png_path:
        png_full = Path(png_path)
        if not png_full.is_absolute():
            png_full = REPO_ROOT / png_full
        if png_full.exists():
            ocr_detections = _extract_with_ocr(png_full, screen_type)
            if ocr_detections:
                detections = ocr_detections
                final_method = "ocr_real"
            else:
                warnings.append("real_ocr_requested_but_no_metrics_extracted")
        else:
            warnings.append("real_ocr_requested_but_image_missing")
    elif use_real_ocr:
        warnings.append("real_ocr_requested_without_png_path")

    if use_real_ocr and not detections and not _tesseract_available():
        warnings.append("pytesseract_not_available")

    # Fallback to stub if no OCR results
    if not detections:
        detections = _stub_values_for_symbol(symbol, screen_type)
        final_method = "stub"

    return {
        "input_class": "vision_context.coinglass.v1",
        "symbol": symbol,
        "source_id": f"coinglass_headless_bot",
        "capture_id": capture_id,
        "screenshot_ts": captured_at,
        "analysis_ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "freshness_state": "fresh",
        "screen_type": screen_type,
        "coinglass_slug": _coinglass_slug(screen_type),
        "detection_method": final_method,
        "detections": detections,
        "warnings": warnings,
        "refs": {
            "capture_source": source,
            "image_ref": png_path,
            "requested_real_ocr": use_real_ocr,
        },
    }


VALID_COINGLASS_TYPES = {
    "LIQUIDITY_COINGLASS", "FUNDING_COINGLASS",
    "OI_COINGLASS", "LS_RATIO_COINGLASS",
}


def main() -> int:
    ap = argparse.ArgumentParser(description="OCR analyzer for Coinglass screenshots")
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
