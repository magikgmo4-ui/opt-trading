#!/usr/bin/env python3
"""
Pipeline orchestrator: Playwright capture → compose → analysis → DeskPro + DataCenter + Telegram.

Usage:
  python3 scripts/run_vision_pipeline.py --profile profiles.production.json
  python3 scripts/run_vision_pipeline.py --profile profiles.btcusdt_poc.json --dry-run
  python3 scripts/run_vision_pipeline.py --profile profiles.macro_dashboard.json --compose

Screen types:
  - CHART_TECHNICAL / ETF_CRYPTO  → bot_vision_step2 (single mode) + vision_analysis_writer
  - DASHBOARD_MACRO                → compose quad → bot_vision_step2 (quad mode)
  - LIQUIDITY_COINGLASS / FUNDING_* / OI_* / LS_RATIO_* → coinglass_ocr_analyzer + vision_context_writer
  - SCREENER_STOCKS                 → stub (analyzer TBD)

See also:
  modules/bot_vision_step2/          — operational analysis module
  modules/desk_snapshot_ingest/     — per-symbol snapshot ingestion
  modules/desk_pro/service/vision_analysis_reader.py  — DeskPro consumer
  modules/desk_pro/service/vision_context_reader.py   — Coinglass DeskPro consumer
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
HEADLESS_DIR = REPO_ROOT / "modules" / "bot_vision" / "headless_capture"
CAPTURE_SCRIPT = HEADLESS_DIR / "capture_headless.js"
COMPOSE_SCRIPT = HEADLESS_DIR / "scripts" / "compose_quad.py"
VISION_ANALYSIS_WRITER = HEADLESS_DIR / "scripts" / "vision_analysis_writer.py"
TELEGRAM_FILTER_SCRIPT = HEADLESS_DIR / "scripts" / "telegram_filter.py"
TELEGRAM_CLAIM_WRITER = HEADLESS_DIR / "scripts" / "telegram_claim_writer.py"
COINGLASS_OCR_ANALYZER = HEADLESS_DIR / "scripts" / "coinglass_ocr_analyzer.py"
VISION_CONTEXT_WRITER = HEADLESS_DIR / "scripts" / "vision_context_writer.py"
SCREENER_ANALYZER = HEADLESS_DIR / "scripts" / "screener_analyzer.py"
SCREENER_WRITER = HEADLESS_DIR / "scripts" / "screener_writer.py"
NEWS_SENTIMENT_ANALYZER = HEADLESS_DIR / "scripts" / "news_sentiment_analyzer.py"
NEWS_SENTIMENT_WRITER = HEADLESS_DIR / "scripts" / "news_sentiment_writer.py"
SIGNAL_VALIDATOR = HEADLESS_DIR / "scripts" / "signal_validator.py"
VISION_INBOX = Path(os.getenv("BOT_VISION_OUT", str(REPO_ROOT / "data" / "vision_inbox")))

DESKPRO_VISION_ANALYSIS_DIR = REPO_ROOT / "data" / "deskpro" / "inputs" / "vision_analysis"
DESKPRO_VISION_ANALYSIS_PATH = DESKPRO_VISION_ANALYSIS_DIR / "latest.json"

# bot_vision_step2 paths (production module, may not exist in dev env)
BOT_VISION_STEP2_APP = REPO_ROOT / "modules" / "bot_vision_step2" / "app" / "bot_vision_step2.py"
BOT_VISION_STEP2_VENV = Path("/opt/trading/.venvs/bot_vision_step2/bin/python")
BOT_VISION_STEP2_ENV = REPO_ROOT / "modules" / "bot_vision_step2" / "config" / "bot_vision.env"
BOT_VISION_STEP2_ENV_FALLBACK = Path("/opt/trading/modules/bot_vision_step2/config/bot_vision.env")

SCREEN_TYPE_LABELS: dict[str, str] = {
    "CHART_TECHNICAL": "Chart technique",
    "DASHBOARD_MACRO": "Dashboard macro 2x2",
    "LIQUIDITY_COINGLASS": "Liquidations Coinglass",
    "FUNDING_COINGLASS": "Funding rate Coinglass",
    "OI_COINGLASS": "Open interest Coinglass",
    "LS_RATIO_COINGLASS": "Long/Short ratio Coinglass",
    "ETF_CRYPTO": "ETF crypto",
    "SCREENER_STOCKS": "Screener actions",
    "NEWS_SENTIMENT": "News / sentiment",
}

# Coinglass screen types dispatched to coinglass_ocr_analyzer
COINGLASS_TYPES = {"LIQUIDITY_COINGLASS", "FUNDING_COINGLASS", "OI_COINGLASS", "LS_RATIO_COINGLASS"}
SCREENER_TYPES = {"SCREENER_STOCKS"}
NEWS_SENTIMENT_TYPES = {"NEWS_SENTIMENT"}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _capture_id(symbol: str, timeframe: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"cap_{ts}_{symbol}_{timeframe}"


def _read_sidecar(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _read_latest_summary() -> dict[str, Any] | None:
    latest_link = REPO_ROOT / "data" / "deskpro" / "vision" / "latest"
    if latest_link.exists():
        summary_path = latest_link.resolve() / "summary.json"
        if summary_path.exists():
            return _read_sidecar(summary_path)
    fallback = REPO_ROOT / "data" / "deskpro" / "vision" / "latest" / "summary.json"
    if fallback.exists():
        return _read_sidecar(fallback)
    return None


def _latest_run_dir() -> Path | None:
    latest_link = REPO_ROOT / "data" / "deskpro" / "vision" / "latest"
    if latest_link.exists():
        try:
            return latest_link.resolve()
        except Exception:
            return None
    fallback_path = REPO_ROOT / "data" / "deskpro" / "vision" / "latest_path.txt"
    if fallback_path.exists():
        try:
            return Path(fallback_path.read_text(encoding="utf-8").strip())
        except Exception:
            return None
    return None


def _latest_dashboard_path(summary: dict[str, Any] | None) -> Path | None:
    run_dir = _latest_run_dir()
    if run_dir is None or summary is None:
        return None
    rel = (((summary.get("files") or {}).get("dashboard")) or "").strip()
    if not rel:
        return None
    path = run_dir / rel
    return path if path.exists() else None


def _metadata_path_for_meta(meta: dict[str, Any], inbox: Path) -> Path | None:
    output_json = str(meta.get("output_json") or "").strip()
    if output_json:
        path = inbox / output_json
        if path.exists():
            return path
    png_path = str(meta.get("png_path") or "").strip()
    if png_path:
        path = Path(png_path)
        if not path.is_absolute():
            path = inbox / path
        candidate = path.with_suffix(".json")
        if candidate.exists():
            return candidate
    return None


def _fallback_photo_caption(symbol: str, timeframe: str, screen_type: str, reason: str) -> str:
    return f"{symbol} {timeframe} [{screen_type}]\n{reason}"[:900]


def _coinglass_image_path(data: dict[str, Any]) -> Path | None:
    refs = data.get("refs") or {}
    image_ref = str(refs.get("image_ref") or "").strip()
    if not image_ref:
        return None
    path = Path(image_ref)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path if path.exists() else None


def _format_compact_number(value: Any) -> str:
    try:
        num = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    if abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    if abs(num) >= 1_000:
        return f"{num / 1_000:.2f}K"
    return f"{num:.2f}".rstrip("0").rstrip(".")


def _build_coinglass_caption(data: dict[str, Any]) -> str:
    symbol = str(data.get("symbol") or "UNKNOWN")
    screen_type = str(data.get("screen_type") or "COINGLASS")
    detections = data.get("detections") or []
    lines = [f"{symbol} [{screen_type}]"]
    for det in detections[:4]:
        metric = str(det.get("detected_metric_type") or "metric")
        value = _format_compact_number(det.get("extracted_value"))
        unit = str(det.get("unit") or "").strip()
        conf = det.get("confidence")
        conf_txt = f" conf={float(conf):.2f}" if isinstance(conf, (int, float)) else ""
        lines.append(f"- {metric}: {value}{unit and ' ' + unit or ''}{conf_txt}")
    if data.get("warnings"):
        lines.append(f"Warnings: {len(data.get('warnings') or [])}")
    return "\n".join(lines)[:900]


def _build_screener_caption(data: dict[str, Any]) -> str:
    screener = str(data.get("screener_symbol") or "SCREENER")
    avg = data.get("avg_change_pct")
    lines = [f"{screener} [SCREENER_STOCKS]"]
    if isinstance(avg, (int, float)):
        lines.append(f"Avg change: {float(avg):+.2f}%")
    for stock in (data.get("top_gainers") or [])[:3]:
        lines.append(f"+ {stock.get('symbol','?')}: {float(stock.get('change_pct', 0)):+.2f}%")
    for stock in (data.get("top_losers") or [])[:2]:
        lines.append(f"- {stock.get('symbol','?')}: {float(stock.get('change_pct', 0)):+.2f}%")
    return "\n".join(lines)[:900]


def _build_news_caption(data: dict[str, Any]) -> str:
    agg = data.get("aggregate") or {}
    label = str(agg.get("sentiment_label") or "neutral")
    score = agg.get("average_sentiment_score")
    lines = [f"NEWS_SENTIMENT [{label}]"]
    if isinstance(score, (int, float)):
        lines.append(f"Average score: {float(score):+.3f}")
    articles = data.get("articles") or []
    for article in articles[:3]:
        headline = str(article.get("headline") or "").strip()
        if headline:
            lines.append(f"- {headline[:120]}")
    return "\n".join(lines)[:900]


def _load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    env: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def _ensure_telegram_env() -> None:
    if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        return
    loaded = _load_env_file(BOT_VISION_STEP2_ENV)
    if not loaded and BOT_VISION_STEP2_ENV_FALLBACK != BOT_VISION_STEP2_ENV:
        loaded = _load_env_file(BOT_VISION_STEP2_ENV_FALLBACK)
    for key in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
        if not os.getenv(key):
            value = loaded.get(key, "").strip()
            if value and value != "REPLACE_ME":
                os.environ[key] = value


def _processed_candidates(inbox: Path) -> list[Path]:
    candidates: list[Path] = []
    env_path = os.getenv("VISION_PROCESSED") or os.getenv("BOT_VISION_PROCESSED")
    if env_path:
        candidates.append(Path(env_path))
    if inbox.parent:
        candidates.append(inbox.parent / "vision_processed")
    repo_default = REPO_ROOT / "data" / "vision_processed"
    candidates.append(repo_default)

    deduped: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            deduped.append(candidate)
    return deduped


def _resolve_png(meta: dict[str, Any], inbox: Path) -> str | None:
    png_name = meta.get("output_png", "")
    png_path = inbox / png_name if png_name else None
    if png_path and png_path.exists():
        return str(png_path)
    alt = Path(meta.get("png_path", "")) if meta.get("png_path") else None
    if alt and alt.exists():
        return str(alt)
    if png_name:
        for processed_dir in _processed_candidates(inbox):
            candidate = processed_dir / png_name
            if candidate.exists():
                return str(candidate)
    return None


def read_all_captures(inbox: Path) -> list[dict[str, Any]]:
    if not inbox.exists():
        return []
    out = []
    for j in sorted(inbox.glob("screen_*.json"), key=os.path.getmtime, reverse=True):
        meta = _read_sidecar(j)
        if meta is None:
            continue
        png = _resolve_png(meta, inbox)
        if png:
            meta["png_path"] = png
        else:
            meta["png_path"] = None
        out.append(meta)
    return out


def find_latest_capture(inbox: Path) -> dict[str, Any] | None:
    all_captures = read_all_captures(inbox)
    if not all_captures:
        return None
    return all_captures[0]


def group_quad_captures(captures: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for m in captures:
        did = m.get("dashboard_id")
        if did and m.get("layout") == "quad" and m.get("status") == "ready":
            groups[did].append(m)
    return dict(groups)


def compose_quad_group(did: str, members: list[dict[str, Any]], inbox: Path) -> Path | None:
    if len(members) < 4:
        print(f"  SKIP quad group '{did}': only {len(members)}/4 captures ready", file=sys.stderr)
        return None

    slot_map: dict[str, str | None] = {m.get("dashboard_slot"): m.get("png_path") for m in members}
    required = ["top-left", "top-right", "bottom-left", "bottom-right"]
    paths: list[str] = []
    for slot in required:
        p = slot_map.get(slot)
        if not p:
            print(f"  SKIP quad group '{did}': missing slot '{slot}'", file=sys.stderr)
            return None
        paths.append(p)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    composite_name = f"screen_composite_macro_{did}_{ts}.png"
    composite_path = inbox / composite_name

    cmd = [
        sys.executable, str(COMPOSE_SCRIPT),
        "--top-left", paths[0],
        "--top-right", paths[1],
        "--bottom-left", paths[2],
        "--bottom-right", paths[3],
        "--output", str(composite_path),
    ]
    print(f"  COMPOSE quad '{did}': {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.stdout:
        print("  " + result.stdout.strip().replace("\n", "\n  "))
    if result.returncode != 0:
        print(f"  ERROR compose failed (exit {result.returncode})", file=sys.stderr)
        if result.stderr:
            print("  " + result.stderr.strip(), file=sys.stderr)
        return None

    if not composite_path.exists():
        return None

    first = members[0]
    sidecar = {
        "producer": "bot_vision_headless_compose",
        "capture_mode": "compose_quad",
        "screen_type": "DASHBOARD_MACRO",
        "layout": "quad",
        "dashboard_id": did,
        "source": "tradingview",
        "symbol": "DASHBOARD",
        "timeframe": "H1",
        "status": "ready",
        "visual_status": "pass",
        "created_at_utc": _utc_now_iso(),
        "output_png": composite_name,
        "output_json": composite_name.replace(".png", ".json"),
        "png_path": str(composite_path),
        "composed_from": [
            {"slot": s, "src": m.get("png_path")}
            for s, m in zip(required, members)
        ],
    }
    sidecar_path = composite_path.with_suffix(".json")
    sidecar.write_text(json.dumps(sidecar, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  OK: composite sidecar -> {sidecar_path}")
    return composite_path


def run_capture(profile_path: str) -> int:
    if not CAPTURE_SCRIPT.exists():
        print(f"ERROR: {CAPTURE_SCRIPT} not found", file=sys.stderr)
        return 1
    if not os.path.exists(profile_path):
        print(f"ERROR: profile not found: {profile_path}", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env.setdefault("BOT_VISION_TMP", str(REPO_ROOT / "tmp" / "bot_vision"))
    env.setdefault("BOT_VISION_OUT", str(VISION_INBOX))
    cmd = ["node", str(CAPTURE_SCRIPT), "--profile", profile_path, "--once"]
    print(f"RUN: {' '.join(cmd)}")
    result = subprocess.run(cmd, env=env, cwd=str(HEADLESS_DIR), capture_output=True, text=True, timeout=120)
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: capture failed (exit {result.returncode})", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    return result.returncode


def compose_all_quads(inbox: Path) -> list[Path]:
    captures = read_all_captures(inbox)
    groups = group_quad_captures(captures)
    composed: list[Path] = []
    for did, members in groups.items():
        print(f"\nQUAD group '{did}': {len(members)} members")
        out = compose_quad_group(did, members, inbox)
        if out:
            composed.append(out)
    return composed


def delegate_to_bot_vision_step2(meta: dict[str, Any]) -> int:
    """Delegate analysis to bot_vision_step2 analyze_latest (if available)."""
    if not BOT_VISION_STEP2_APP.exists():
        print("SKIP: bot_vision_step2 module not available in this environment", file=sys.stderr)
        return 2
    python = str(BOT_VISION_STEP2_VENV) if BOT_VISION_STEP2_VENV.exists() else "python3"
    env = os.environ.copy()
    env.setdefault("VISION_INBOX", str(VISION_INBOX))
    env.setdefault("VISION_PROCESSED", str(VISION_INBOX))
    env.setdefault("DESKPRO_VISION_DIR", str(REPO_ROOT / "data" / "deskpro" / "vision"))
    env.setdefault("WORKDIR", str(REPO_ROOT / "tmp" / "bot_vision_step2"))
    cmd = [python, str(BOT_VISION_STEP2_APP), "analyze_latest"]
    print(f"RUN: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=180)
        if result.stdout:
            print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
        if result.returncode != 0:
            print(f"WARN: bot_vision_step2 exit {result.returncode}", file=sys.stderr)
            if result.stderr:
                print(result.stderr[-1000:], file=sys.stderr)
        return result.returncode
    except FileNotFoundError:
        print("SKIP: bot_vision_step2 not installed (venv missing)", file=sys.stderr)
        return 2
    except subprocess.TimeoutExpired:
        print("SKIP: bot_vision_step2 timed out", file=sys.stderr)
        return 2


def write_vision_analysis_stub(meta: dict[str, Any]) -> Path:
    """Write a vision_analysis.v1 stub pointing to the capture."""
    screen_type = str(meta.get("screen_type", "CHART_TECHNICAL"))
    symbol = str(meta.get("symbol", "BTCUSDT"))
    timeframe = str(meta.get("timeframe", "15m"))
    cid = _capture_id(symbol, timeframe)
    data = {
        "input_class": "vision_analysis.v1",
        "capture_id": cid,
        "screen_type": screen_type,
        "screen_type_label": SCREEN_TYPE_LABELS.get(screen_type, screen_type),
        "layout": str(meta.get("layout", "single")),
        "symbol": symbol,
        "timeframe": timeframe,
        "analysis_ts": _utc_now_iso(),
        "source_module": "bot_vision_headless_capture",
        "freshness_state": "fresh",
        "capture_status": meta.get("status", "unknown"),
        "signals": [],
        "image_ref": meta.get("png_path") or "",
        "note": _analysis_note(screen_type),
    }
    DESKPRO_VISION_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = DESKPRO_VISION_ANALYSIS_PATH.with_suffix(".json.uploading")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, DESKPRO_VISION_ANALYSIS_PATH)
    print(f"OK: {DESKPRO_VISION_ANALYSIS_PATH}")
    return DESKPRO_VISION_ANALYSIS_PATH


def _analysis_note(screen_type: str) -> str:
    if screen_type == "DASHBOARD_MACRO":
        return "Quad composite ready. Delegate to bot_vision_step2 in CROP_MODE=quad."
    if screen_type in COINGLASS_TYPES:
        return "Coinglass analysis via coinglass_ocr_analyzer (A-07). vision_context.coinglass.v1 published."
    if screen_type == "SCREENER_STOCKS":
        return "Screener analysis via screener_analyzer (A-08). vision_context.screener.v1 published."
    return "Capture complete. Full analysis delegated to bot_vision_step2."


def main() -> int:
    ap = argparse.ArgumentParser(description="Run vision pipeline: capture → compose → analyze → DeskPro")
    ap.add_argument("--profile", default=str(HEADLESS_DIR / "profiles.btcusdt_poc.json"))
    ap.add_argument("--skip-capture", action="store_true", help="Skip capture, analyze latest in inbox")
    ap.add_argument("--dry-run", action="store_true", help="Skip bot_vision_step2, write stub only")
    ap.add_argument("--no-delegate", action="store_true", help="Skip bot_vision_step2 delegation")
    ap.add_argument("--no-telegram", action="store_true", help="Skip Telegram dispatch even if signals pass filter")
    ap.add_argument("--compose", action="store_true", help="Run quad composition after capture")
    ap.add_argument("--telegram-threshold", type=float, default=0.70, help="Telegram confidence threshold (default: 0.70)")
    ap.add_argument("--real-ocr", action="store_true", help="Use real OCR for Coinglass (requires pytesseract)")
    args = ap.parse_args()

    t0 = time.time()

    if not args.skip_capture:
        ret = run_capture(args.profile)
        if ret != 0:
            return ret

    if args.compose:
        composed = compose_all_quads(VISION_INBOX)
        if composed:
            print(f"\nComposed {len(composed)} quad dashboard(s)")

    meta = find_latest_capture(VISION_INBOX)
    if meta is None:
        print("ERROR: no capture found in inbox", file=sys.stderr)
        return 1
    if meta.get("status") != "ready":
        print(f"SKIP: capture status is '{meta.get('status')}'", file=sys.stderr)
        return 1
    if not meta.get("png_path"):
        print("ERROR: no PNG path in capture metadata", file=sys.stderr)
        return 1

    screen_type = str(meta.get("screen_type", "CHART_TECHNICAL"))
    symbol = str(meta.get("symbol", "BTCUSDT"))
    timeframe = str(meta.get("timeframe", "15m"))
    label = SCREEN_TYPE_LABELS.get(screen_type, screen_type)

    print(f"\nCapture ready: {symbol} {timeframe}")
    print(f"  Type: {label} ({screen_type})")
    print(f"  PNG: {meta['png_path']}")

    write_vision_analysis_stub(meta)

    # ── Dispatch Coinglass captures to OCR analyzer ──
    coinglass_ok = False
    coinglass_payload: dict[str, Any] | None = None
    if screen_type in COINGLASS_TYPES and not args.dry_run:
        print(f"\n--- Coinglass OCR analyzer ({screen_type}) ---")
        inbox_sidecar = next(iter(sorted(Path(VISION_INBOX).glob("screen_*.json"), key=os.path.getmtime, reverse=True)), None)
        if inbox_sidecar:
            cg_cmd = [sys.executable or "python3", str(COINGLASS_OCR_ANALYZER), "--sidecar", str(inbox_sidecar)]
            if args.real_ocr:
                cg_cmd.append("--real-ocr")
            try:
                cg_result = subprocess.run(cg_cmd, capture_output=True, text=True, timeout=60)
                if cg_result.returncode == 0 and cg_result.stdout.strip():
                    cg_data = json.loads(cg_result.stdout.strip())
                    coinglass_payload = cg_data
                    det_count = len(cg_data.get("detections", []))
                    print(f"  Detections: {det_count} (method: {cg_data.get('detection_method', 'N/A')})")
                    # Publish to DeskPro + Data Center
                    wc_cmd = [sys.executable or "python3", str(VISION_CONTEXT_WRITER), "--stdin"]
                    wc_result = subprocess.run(wc_cmd, input=cg_result.stdout, capture_output=True, text=True, timeout=15)
                    if wc_result.stdout:
                        print(wc_result.stdout.strip())
                    if wc_result.returncode == 0:
                        coinglass_ok = True
                        print(f"  OK: Coinglass vision_context.coinglass.v1 published")
                    else:
                        print(f"WARN: vision_context_writer exit {wc_result.returncode}", file=sys.stderr)
                else:
                    print(f"WARN: coinglass_ocr_analyzer exit {cg_result.returncode}", file=sys.stderr)
                    if cg_result.stderr:
                        print(cg_result.stderr.strip(), file=sys.stderr)
            except subprocess.TimeoutExpired:
                print("WARN: coinglass_ocr_analyzer timed out", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"WARN: invalid JSON from coinglass_ocr_analyzer: {e}", file=sys.stderr)
        else:
            print("WARN: no Coinglass sidecar found in inbox", file=sys.stderr)

    # ── Dispatch Screener captures to screener analyzer ──
    screener_ok = False
    screener_payload: dict[str, Any] | None = None
    if screen_type in SCREENER_TYPES and not args.dry_run:
        print(f"\n--- Screener analyzer ({symbol}) ---")
        inbox_sidecar = next(iter(sorted(Path(VISION_INBOX).glob("screen_*.json"), key=os.path.getmtime, reverse=True)), None)
        if inbox_sidecar:
            sa_cmd = [sys.executable or "python3", str(SCREENER_ANALYZER), "--sidecar", str(inbox_sidecar)]
            if args.real_ocr:
                sa_cmd.append("--real-ocr")
            try:
                sa_result = subprocess.run(sa_cmd, capture_output=True, text=True, timeout=60)
                if sa_result.returncode == 0 and sa_result.stdout.strip():
                    sa_data = json.loads(sa_result.stdout.strip())
                    screener_payload = sa_data
                    sc = sa_data.get("stock_count", 0)
                    avg_chg = sa_data.get("avg_change_pct", 0)
                    print(f"  Stocks: {sc} (avg change: {avg_chg:+.2f}%, method: {sa_data.get('analysis_method', 'N/A')})")
                    # Publish to DeskPro + Data Center
                    sw_cmd = [sys.executable or "python3", str(SCREENER_WRITER), "--stdin"]
                    sw_result = subprocess.run(sw_cmd, input=sa_result.stdout, capture_output=True, text=True, timeout=15)
                    if sw_result.stdout:
                        print(sw_result.stdout.strip())
                    if sw_result.returncode == 0:
                        screener_ok = True
                        print(f"  OK: Screener vision_context.screener.v1 published")
                    else:
                        print(f"WARN: screener_writer exit {sw_result.returncode}", file=sys.stderr)
                else:
                    print(f"WARN: screener_analyzer exit {sa_result.returncode}", file=sys.stderr)
                    if sa_result.stderr:
                        print(sa_result.stderr.strip(), file=sys.stderr)
            except subprocess.TimeoutExpired:
                print("WARN: screener_analyzer timed out", file=sys.stderr)
            except json.JSONDecodeError as e:
                print(f"WARN: invalid JSON from screener_analyzer: {e}", file=sys.stderr)
        else:
            print("WARN: no screener sidecar found in inbox", file=sys.stderr)

    # ── Dispatch News/Sentiment to news_sentiment_analyzer ──
    news_ok = False
    news_payload: dict[str, Any] | None = None
    if screen_type in NEWS_SENTIMENT_TYPES and not args.dry_run:
        print(f"\n--- News sentiment analyzer ---")
        ns_cmd = [sys.executable or "python3", str(NEWS_SENTIMENT_ANALYZER)]
        try:
            ns_result = subprocess.run(ns_cmd, capture_output=True, text=True, timeout=60)
            if ns_result.returncode == 0 and ns_result.stdout.strip():
                ns_data = json.loads(ns_result.stdout.strip())
                news_payload = ns_data
                ac = ns_data.get("article_count", 0)
                avg_s = ns_data.get("aggregate", {}).get("average_sentiment_score", 0)
                print(f"  Articles: {ac} (avg sentiment: {avg_s:+.3f})")
                nsw_cmd = [sys.executable or "python3", str(NEWS_SENTIMENT_WRITER), "--stdin"]
                nsw_result = subprocess.run(nsw_cmd, input=ns_result.stdout,
                                            capture_output=True, text=True, timeout=15)
                if nsw_result.stdout:
                    print(nsw_result.stdout.strip())
                if nsw_result.returncode == 0:
                    news_ok = True
                    print("  OK: News sentiment vision_context.news_sentiment.v1 published")
                else:
                    print(f"WARN: news_sentiment_writer exit {nsw_result.returncode}", file=sys.stderr)
            else:
                print(f"WARN: news_sentiment_analyzer exit {ns_result.returncode}", file=sys.stderr)
                if ns_result.stderr:
                    print(ns_result.stderr.strip(), file=sys.stderr)
        except subprocess.TimeoutExpired:
            print("WARN: news_sentiment_analyzer timed out", file=sys.stderr)
        except json.JSONDecodeError as e:
            print(f"WARN: invalid JSON from news_sentiment_analyzer: {e}", file=sys.stderr)

    analysis_ok = False
    if not args.dry_run and not args.no_delegate:
        if screen_type in COINGLASS_TYPES:
            print("  (Coinglass dispatched to OCR analyzer)")
        elif screen_type in SCREENER_TYPES:
            print("  (Screener dispatched to screener analyzer)")
        elif screen_type in NEWS_SENTIMENT_TYPES:
            print("  (News sentiment dispatched to news_sentiment_analyzer)")
        else:
            ret = delegate_to_bot_vision_step2(meta)
            if ret == 0:
                print("OK: bot_vision_step2 analysis complete")
                analysis_ok = True
            elif ret == 2:
                print("(non-bot_vision_step2 environment; stub written for manual analysis)")

    # ── Publish vision_analysis.v1 to DeskPro + Data Center ──
    if analysis_ok:
        print("\n--- Publishing vision_analysis.v1 ---")
        va_cmd = [sys.executable or "python3", str(VISION_ANALYSIS_WRITER)]
        if meta:
            inbox_file = _metadata_path_for_meta(meta, Path(VISION_INBOX))
            if inbox_file:
                va_cmd.extend(["--metadata", str(inbox_file)])
        try:
            va_result = subprocess.run(va_cmd, capture_output=True, text=True, timeout=30)
            if va_result.stdout:
                print(va_result.stdout.strip())
            if va_result.returncode != 0:
                print(f"WARN: vision_analysis_writer exit {va_result.returncode}", file=sys.stderr)
                if va_result.stderr:
                    print(va_result.stderr.strip(), file=sys.stderr)
        except subprocess.TimeoutExpired:
            print("WARN: vision_analysis_writer timed out", file=sys.stderr)
        except FileNotFoundError:
            print("WARN: vision_analysis_writer not found, skipping", file=sys.stderr)

        # ── Cross-validation via signal_validator ──
        print("\n--- Signal cross-validation ---")
        validated_summary_input = None
        sv_cmd = [sys.executable or "python3", str(SIGNAL_VALIDATOR), "--symbol", symbol]
        try:
            sv_result = subprocess.run(sv_cmd, capture_output=True, text=True, timeout=15)
            if sv_result.returncode == 0 and sv_result.stdout.strip():
                sv_data = json.loads(sv_result.stdout.strip())
                validated = sv_data.get("validated_signal_count", 0)
                confirmed = sv_data.get("confirmed_count", 0)
                deduped = sv_data.get("deduped_count", 0)
                print(f"  Validated: {validated} signals ({confirmed} confirmed, {deduped} deduplicated)")
                latest_summary = _read_latest_summary()
                if latest_summary is not None:
                    validated_summary_input = dict(latest_summary)
                    validated_summary_input["signals"] = sv_data.get("validated_signals", [])
            elif sv_result.returncode != 0:
                print(f"  SKIP: signal_validator exit {sv_result.returncode}", file=sys.stderr)
        except subprocess.TimeoutExpired:
            print("  SKIP: signal_validator timed out", file=sys.stderr)
        except FileNotFoundError:
            print("  SKIP: signal_validator not found", file=sys.stderr)
        except json.JSONDecodeError:
            print("  SKIP: signal_validator returned invalid JSON", file=sys.stderr)

        # ── Telegram filter + send ──
        print("\n--- Telegram filter ---")
        tg_cmd = [sys.executable or "python3", str(TELEGRAM_FILTER_SCRIPT)]
        tg_cmd.extend(["--confidence", str(args.telegram_threshold)])
        try:
            tg_input = None
            if validated_summary_input is not None:
                tg_cmd.append("--stdin")
                tg_input = json.dumps(validated_summary_input)
            tg_result = subprocess.run(tg_cmd, input=tg_input, capture_output=True, text=True, timeout=30)
            if tg_result.stdout:
                tg_data = json.loads(tg_result.stdout.strip())
                should_send = tg_data.get("send", False) and not args.no_telegram
                reason = tg_data.get("reason", "N/A")
                print(f"  Decision: {'SEND' if should_send else 'SKIP'} ({reason})")
                summary_text = tg_data.get("summary", "")
                run_id = tg_data.get("run_id", "")
                try:
                    _ensure_telegram_env()
                    sys.path.insert(0, str(REPO_ROOT))
                    tags = {"run_id": run_id, "screen_type": screen_type, "symbol": symbol, "timeframe": timeframe}
                    send_result = None
                    if screen_type in {"CHART_TECHNICAL", "ETF_CRYPTO", "DASHBOARD_MACRO"} and not args.no_telegram:
                        from shared.telegram_channels import send_photo_to_channel  # type: ignore
                        dashboard_path = _latest_dashboard_path(latest_summary)
                        if dashboard_path is not None:
                            caption = summary_text[:900] if should_send and summary_text else _fallback_photo_caption(symbol, timeframe, screen_type, reason)
                            send_result = send_photo_to_channel(
                                "push",
                                str(dashboard_path),
                                caption=caption,
                                source="bot_vision",
                                tags=tags,
                            )
                    elif should_send:
                        from shared.telegram_channels import send_to_channel  # type: ignore
                        send_result = send_to_channel(
                            "push",
                            summary_text,
                            source="bot_vision",
                            tags=tags,
                        )

                    if send_result is not None and not send_result.get("ok"):
                        raise RuntimeError(send_result.get("error") or "Telegram send failed")

                    if should_send:
                        tc_cmd = [
                            sys.executable or "python3",
                            str(TELEGRAM_CLAIM_WRITER),
                            "--stdin",
                            "--screen-type", screen_type,
                            "--symbol", symbol,
                            "--timeframe", timeframe,
                        ]
                        channel_id = send_result.get("telegram_chat_id") if send_result else None
                        message_id = send_result.get("telegram_message_id") if send_result else None
                        if channel_id:
                            tc_cmd.extend(["--channel-id", str(channel_id)])
                        if message_id:
                            tc_cmd.extend(["--message-id", str(message_id)])
                        tc_result = subprocess.run(tc_cmd, input=tg_result.stdout, capture_output=True, text=True, timeout=15)
                        if tc_result.stdout:
                            print(tc_result.stdout.strip())
                        if tc_result.returncode != 0:
                            print(f"WARN: telegram_claim_writer exit {tc_result.returncode}", file=sys.stderr)
                        print(f"  OK: Telegram sent (run_id={run_id})")
                    elif send_result is not None:
                        print(f"  OK: Telegram screenshot pushed (run_id={run_id})")
                except subprocess.TimeoutExpired:
                    print("WARN: telegram_claim_writer timed out", file=sys.stderr)
                except ImportError:
                    print("  SKIP: shared/telegram_notify.py not available", file=sys.stderr)
                except Exception as e:
                    print(f"  ERROR: Telegram send failed: {e}", file=sys.stderr)
            if tg_result.returncode not in (0, 2):
                print(f"WARN: telegram_filter exit {tg_result.returncode}", file=sys.stderr)
                if tg_result.stderr:
                    print(tg_result.stderr.strip(), file=sys.stderr)
        except subprocess.TimeoutExpired:
            print("WARN: telegram_filter timed out", file=sys.stderr)
        except FileNotFoundError:
            print("WARN: telegram_filter not found, skipping", file=sys.stderr)
        except json.JSONDecodeError:
            print("WARN: telegram_filter returned invalid JSON", file=sys.stderr)

    if coinglass_ok and coinglass_payload is not None and not args.no_telegram:
        print("\n--- Telegram Coinglass push ---")
        try:
            _ensure_telegram_env()
            sys.path.insert(0, str(REPO_ROOT))
            from shared.telegram_channels import send_photo_to_channel  # type: ignore

            image_path = _coinglass_image_path(coinglass_payload)
            if image_path is None:
                print("WARN: no Coinglass image_ref found for Telegram push", file=sys.stderr)
            else:
                result = send_photo_to_channel(
                    "push",
                    str(image_path),
                    caption=_build_coinglass_caption(coinglass_payload),
                    source="bot_vision_coinglass",
                    tags={"screen_type": screen_type, "symbol": symbol, "timeframe": timeframe},
                )
                if not result.get("ok"):
                    raise RuntimeError(result.get("error") or "Telegram photo send failed")
                print(f"  OK: Coinglass screenshot pushed ({symbol})")
        except Exception as e:
            print(f"WARN: Coinglass Telegram push failed: {e}", file=sys.stderr)

    if screener_ok and screener_payload is not None and not args.no_telegram:
        print("\n--- Telegram Screener push ---")
        try:
            _ensure_telegram_env()
            sys.path.insert(0, str(REPO_ROOT))
            from shared.telegram_channels import send_photo_to_channel  # type: ignore

            image_path = _coinglass_image_path(screener_payload)
            if image_path is None:
                print("WARN: no Screener image_ref found for Telegram push", file=sys.stderr)
            else:
                result = send_photo_to_channel(
                    "push",
                    str(image_path),
                    caption=_build_screener_caption(screener_payload),
                    source="bot_vision_screener",
                    tags={"screen_type": screen_type, "symbol": symbol, "timeframe": timeframe},
                )
                if not result.get("ok"):
                    raise RuntimeError(result.get("error") or "Telegram photo send failed")
                print(f"  OK: Screener screenshot pushed ({symbol})")
        except Exception as e:
            print(f"WARN: Screener Telegram push failed: {e}", file=sys.stderr)

    if news_ok and news_payload is not None and not args.no_telegram:
        print("\n--- Telegram News push ---")
        try:
            _ensure_telegram_env()
            sys.path.insert(0, str(REPO_ROOT))
            from shared.telegram_channels import send_photo_to_channel  # type: ignore

            image_path = _coinglass_image_path(news_payload)
            if image_path is None:
                print("WARN: no News image_ref found for Telegram push", file=sys.stderr)
            else:
                result = send_photo_to_channel(
                    "push",
                    str(image_path),
                    caption=_build_news_caption(news_payload),
                    source="bot_vision_news",
                    tags={"screen_type": screen_type, "symbol": symbol, "timeframe": timeframe},
                )
                if not result.get("ok"):
                    raise RuntimeError(result.get("error") or "Telegram photo send failed")
                print(f"  OK: News screenshot pushed ({symbol})")
        except Exception as e:
            print(f"WARN: News Telegram push failed: {e}", file=sys.stderr)

    elapsed = time.time() - t0
    print(f"\nPipeline complete in {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
