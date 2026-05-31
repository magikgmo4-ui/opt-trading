#!/usr/bin/env python3
"""
SMC/ICT ObservationEvent builder, scorer, and poster.

Builds valid ObservationEvents for SMC_ICT_CHOCH_BOS_RETEST, computes
confidence via the 60_SCORING_INITIAL formula, and POSTs to
POST /perf/observation_event.

No OpenAI dependency — usable from CLI or as a library.
"""
import argparse
import json
import sys
import uuid
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STRATEGY_ID = "SMC_ICT_CHOCH_BOS_RETEST"
STRATEGY_VERSION = "0.1.0"
LIFECYCLE_STATUS = "ACTIVE_PAPER"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def score_confidence(detail: dict) -> float:
    """
    Compute confidence from smc_ict_detail fields.
    Formula: 60_SCORING_INITIAL.md (max 1.0).
    """
    score = 0.0

    # Structure (max 0.50)
    if detail.get("choch_observed"):
        score += 0.20
        if detail.get("mss_observed"):
            score += 0.15
    elif detail.get("bos_observed"):
        score += 0.15

    if detail.get("htf_alignment_confirmed"):
        score += 0.10
        if detail.get("htf_alignment_4h_confirmed"):
            score += 0.05

    # Liquidity / Sweep (max 0.28)
    if detail.get("sweep_observed"):
        sweep_type = str(detail.get("sweep_type") or "").lower()
        if any(k in sweep_type for k in ("pdh", "pdl", "pwh", "pwl")):
            score += 0.15
        elif any(k in sweep_type for k in ("eqh", "eql")):
            score += 0.12
        else:
            score += 0.10
        if detail.get("sweep_htf_confirmed"):
            score += 0.08
        if detail.get("sweep_fast_return"):
            score += 0.05

    # FVG / OB / Premium-Discount (max 0.50)
    if detail.get("fvg_valid"):
        score += 0.10
        if detail.get("fvg_retest_confirmed"):
            score += 0.08
    if detail.get("ob_valid"):
        score += 0.08
    if detail.get("fvg_ob_confluence"):
        score += 0.07
    if detail.get("ote_zone_active"):
        score += 0.07
    if str(detail.get("premium_discount_filter") or "EQ").upper() in ("PREMIUM", "DISCOUNT"):
        score += 0.10

    return round(min(score, 1.0), 4)


def build_obs_event(
    smc_detail: dict,
    direction: str,
    invalidation_rule: str,
    *,
    symbol: str = "BTCUSDT",
    timeframe: str = "15m",
    signal_source: str = "manual",
    evidence: list | None = None,
    run_id: str | None = None,
    produced_at: str | None = None,
) -> dict:
    """Build a validated ObservationEvent dict."""
    if not smc_detail.get("choch_observed") and not smc_detail.get("bos_observed"):
        raise ValueError("choch_observed or bos_observed must be True")
    if not (invalidation_rule or "").strip():
        raise ValueError("invalidation_rule is required")

    confidence = score_confidence(smc_detail)

    return {
        "run_id": run_id or ("OBS_" + uuid.uuid4().hex[:12]),
        "produced_at": produced_at or now_iso(),
        "strategy": {
            "strategy_id": STRATEGY_ID,
            "strategy_version": STRATEGY_VERSION,
            "setup_type": "SWEEP_CHOCH_BOS_FVG_OB_RETEST",
            "lifecycle_status": LIFECYCLE_STATUS,
        },
        "signal": {
            "direction": direction.upper(),
            "symbol": symbol,
            "timeframe": timeframe,
            "context_timeframes": ["1h", "4h"],
            "signal_source": signal_source,
            "confidence": confidence,
        },
        "trade_plan": {
            "entry_zone": {"kind": "fvg_ob_confluence", "fvg_lower": None, "fvg_upper": None},
            "invalidation": {"rule": invalidation_rule.strip(), "level": None},
            "target_zone": {"kind": "prior_liquidity", "level": None},
            "risk_profile": "paper_only",
        },
        "smc_ict_detail": smc_detail,
        "evidence": evidence or [],
        "gates": {
            "observation_status": LIFECYCLE_STATUS,
            "perf_status": "UNMEASURED",
            "promotion_gate": "BLOCKED_INSUFFICIENT_SAMPLE",
            "retirement_gate": "KEEP_OBSERVING",
        },
    }


def from_summary_json(
    summary_path: str,
    smc_detail: dict,
    direction: str,
    invalidation_rule: str,
    **kwargs: Any,
) -> dict:
    """Build ObsEvent from a bot_vision_step2 summary.json + SMC/ICT fields."""
    p = Path(summary_path)
    if not p.exists():
        raise FileNotFoundError(f"summary.json not found: {summary_path}")
    summary = json.loads(p.read_text(encoding="utf-8"))
    evidence = [
        {"type": "vision_summary", "path": str(p)},
        {"type": "run_id", "value": summary.get("run_id", "")},
    ]
    return build_obs_event(
        smc_detail,
        direction,
        invalidation_rule,
        signal_source="bot_vision",
        evidence=evidence,
        run_id=summary.get("run_id"),
        **kwargs,
    )


def post_obs_event(event: dict, base_url: str = "http://127.0.0.1:8010") -> dict:
    """POST ObsEvent to /perf/observation_event."""
    url = base_url.rstrip("/") + "/perf/observation_event"
    data = json.dumps(event, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}") from e


# ---- CLI ----

def _bool(v: str) -> bool:
    return v.lower() in ("1", "true", "yes", "oui")


def _add_smc_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--direction", required=True, choices=["LONG_WATCH", "SHORT_WATCH", "WATCH_ONLY"])
    p.add_argument("--invalidation", required=True, help="Invalidation rule (free text)")
    p.add_argument("--choch", default="false", metavar="BOOL")
    p.add_argument("--bos", default="false", metavar="BOOL")
    p.add_argument("--mss", default="false", metavar="BOOL")
    p.add_argument("--sweep", default="false", metavar="BOOL")
    p.add_argument("--sweep-type", default="", metavar="STR")
    p.add_argument("--fvg", default="false", metavar="BOOL")
    p.add_argument("--ob", default="false", metavar="BOOL")
    p.add_argument("--premium-discount", default="EQ", choices=["PREMIUM", "DISCOUNT", "EQ"])
    p.add_argument("--ote", default="false", metavar="BOOL")
    p.add_argument("--htf-alignment", default="false", metavar="BOOL")
    p.add_argument("--symbol", default="BTCUSDT")
    p.add_argument("--base-url", default="http://127.0.0.1:8010")
    p.add_argument("--dry-run", action="store_true", help="Build only, do not POST")


def _detail_from_args(args: argparse.Namespace) -> dict:
    fvg = _bool(args.fvg)
    ob = _bool(args.ob)
    return {
        "choch_observed": _bool(args.choch),
        "bos_observed": _bool(args.bos),
        "mss_observed": _bool(args.mss),
        "sweep_observed": _bool(args.sweep),
        "sweep_type": args.sweep_type,
        "fvg_valid": fvg,
        "ob_valid": ob,
        "fvg_ob_confluence": fvg and ob,
        "premium_discount_filter": args.premium_discount,
        "ote_zone_active": _bool(args.ote),
        "htf_alignment_confirmed": _bool(args.htf_alignment),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="SMC/ICT ObservationEvent builder/poster")
    sub = parser.add_subparsers(dest="cmd")

    p_post = sub.add_parser("post", help="Build and POST an ObservationEvent")
    _add_smc_args(p_post)

    p_from = sub.add_parser("from-summary", help="Build from bot_vision_step2 summary.json")
    p_from.add_argument("summary_path", help="Path to summary.json")
    _add_smc_args(p_from)

    args = parser.parse_args()

    if args.cmd not in ("post", "from-summary"):
        parser.print_help()
        sys.exit(1)

    detail = _detail_from_args(args)

    try:
        if args.cmd == "from-summary":
            event = from_summary_json(args.summary_path, detail, args.direction, args.invalidation, symbol=args.symbol)
        else:
            event = build_obs_event(detail, args.direction, args.invalidation, symbol=args.symbol)
    except (ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(event, indent=2, ensure_ascii=False))

    if not args.dry_run:
        try:
            result = post_obs_event(event, base_url=args.base_url)
            print("\nPOST result:", json.dumps(result, indent=2))
        except RuntimeError as exc:
            print(f"POST failed: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        print("\n[dry-run] Not posted.")


if __name__ == "__main__":
    main()
