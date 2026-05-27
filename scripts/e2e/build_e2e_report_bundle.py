#!/usr/bin/env python3
"""
E2E Report Bundle Generator — PF_OPENCLAW_ORCHESTRATOR_FULL

Transforms a dry_run_pipeline.py run into a transportable, auditable bundle.

Bundle contents:
  <RUN_ID>/
    manifest.json          GO / PF metadata + run identity
    e2e_report.json        Full pipeline JSON output
    environment_flags.json Flags used/checked during the run
    payload_refs.json      Key identifiers extracted from each step
    summary.md             Human-readable verdict

Usage:
  # Run pipeline inline and bundle:
  ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/build_e2e_report_bundle.py

  # Consume existing pipeline output:
  ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/build_e2e_report_bundle.py \\
    --pipeline-output /path/to/e2e_report.json

  # Custom output dir:
  ALLOW_E2E_LIVE_DRY_RUN=1 DRY_RUN=1 python3 scripts/e2e/build_e2e_report_bundle.py \\
    --output-root /tmp/my_bundles

Output:
  data/e2e_report_bundles/<RUN_ID>/   (default, git-ignored)

Safety:
  Refused if live_trade=True, gate_status != APPROVED_PAPER, or dry_run != true.
  Never writes secrets. Never calls exchange. Never sends real Telegram.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
log = logging.getLogger("build_e2e_report_bundle")

# ── Constants ─────────────────────────────────────────────────────────────────

BUNDLE_VERSION = "1.0"
GO_ID = "GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01"
PF_ID = "PF_OPENCLAW_ORCHESTRATOR_FULL"
PARENT_GO = "GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01"
UPSTREAM_PARENT = "GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01"

DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "data" / "e2e_report_bundles"
_PIPELINE_SCRIPT = PROJECT_ROOT / "scripts" / "e2e" / "dry_run_pipeline.py"

_REQUIRED_ENV = {
    "ALLOW_E2E_LIVE_DRY_RUN": "1",
    "DRY_RUN": "1",
}
_FORBIDDEN_ENV = {
    "ALLOW_LIVE_TRADE": "1",
    "ALLOW_GOOGLE_SHEETS_API_WRITE": "1",
    "ALLOW_TELEGRAM_SEND": "1",
}

_MODULE_STEPS = [
    "signal_router",
    "proposition_engine",
    "validation_gate",
    "trade_executor",
    "result_tracker",
    "datasheet_writer",
    "learning_feeder",
]


# ── Validation ────────────────────────────────────────────────────────────────

class BundleRefused(Exception):
    """Raised when the pipeline output fails safety checks."""


def _validate_env() -> dict:
    """Check environment flags. Returns env_flags dict."""
    flags: dict = {}
    refused: list[str] = []

    for k, expected in _REQUIRED_ENV.items():
        val = os.environ.get(k)
        flags[k] = val
        if val != expected:
            refused.append(f"{k}={expected!r} required but got {val!r}")

    for k, forbidden_val in _FORBIDDEN_ENV.items():
        val = os.environ.get(k)
        flags[k] = val
        if val == forbidden_val:
            refused.append(f"{k}={forbidden_val!r} is forbidden in bundle mode")

    flags["PAPER_MODE"] = os.environ.get("PAPER_MODE", "1")
    flags["REQUIRE_LOCALCMS_E2E"] = os.environ.get("REQUIRE_LOCALCMS_E2E", "0")
    flags["SKIP_LOCALCMS_E2E"] = os.environ.get("SKIP_LOCALCMS_E2E", "0")
    flags["LOCALCMS_URL"] = os.environ.get("LOCALCMS_URL", "http://127.0.0.1:8700")

    if refused:
        raise BundleRefused("Environment preflight failed:\n  " + "\n  ".join(refused))

    return flags


def _validate_report(report: dict) -> None:
    """Validate pipeline report for bundle eligibility. Raises BundleRefused if not safe."""
    pg = report.get("e2e_post_gate_status")
    if pg is None:
        raise BundleRefused(
            "e2e_post_gate_status missing — run must use ALLOW_E2E_LIVE_DRY_RUN=1"
        )

    if pg.get("status") == "BLOCKED":
        raise BundleRefused(
            f"e2e_post_gate_status.status=BLOCKED — {pg.get('reason', 'unknown reason')}"
        )

    if pg.get("live_trade") is True:
        raise BundleRefused(
            "live_trade=True in e2e_post_gate_status — live trades are forbidden in a bundle run"
        )

    if pg.get("gate_status") != "APPROVED_PAPER":
        raise BundleRefused(
            f"gate_status={pg.get('gate_status')!r} — only APPROVED_PAPER runs can be bundled"
        )

    if report.get("dry_run") is not True:
        raise BundleRefused("report.dry_run is not True — bundle requires dry_run mode")


# ── Pipeline execution ────────────────────────────────────────────────────────

def _run_pipeline() -> dict:
    """Run dry_run_pipeline.py as subprocess and return parsed JSON."""
    env = {**os.environ}
    log.info("Running pipeline: %s", _PIPELINE_SCRIPT)
    result = subprocess.run(
        [sys.executable, str(_PIPELINE_SCRIPT)],
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
    )
    if result.returncode != 0:
        # Check if it's a preflight BLOCKED (rc=1 with valid JSON)
        try:
            report = json.loads(result.stdout)
            pg = report.get("e2e_post_gate_status", {})
            if pg.get("status") == "BLOCKED":
                raise BundleRefused(f"Pipeline preflight BLOCKED: {pg.get('reason', '')}")
        except json.JSONDecodeError:
            pass
        raise BundleRefused(
            f"Pipeline exited {result.returncode}: {result.stderr[:300]}"
        )
    return json.loads(result.stdout)


# ── Bundle file builders ──────────────────────────────────────────────────────

def _make_run_id() -> str:
    ts = datetime.now(timezone.utc)
    return ts.strftime("%Y%m%d_%H%M%S")


def _build_manifest(run_id: str, report: dict, env_flags: dict) -> dict:
    pg = report.get("e2e_post_gate_status", {})
    return {
        "bundle_version": BUNDLE_VERSION,
        "run_id": run_id,
        "go_id": GO_ID,
        "pf_id": PF_ID,
        "parent_go": PARENT_GO,
        "upstream_parent": UPSTREAM_PARENT,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "pipeline_started_at": report.get("started_at"),
        "pipeline_completed_at": report.get("completed_at"),
        "duration_s": report.get("duration_s"),
        "verdict": pg.get("status", "UNKNOWN"),
        "gate_status": pg.get("gate_status", "UNKNOWN"),
        "dry_run": report.get("dry_run"),
        "live_trade": pg.get("live_trade"),
        "sheets_mode": pg.get("sheets_mode"),
        "telegram_mode": pg.get("telegram_mode"),
        "localcms_gate": pg.get("localcms_gate"),
        "modules": pg.get("modules", {}),
        "env_summary": {
            "ALLOW_E2E_LIVE_DRY_RUN": env_flags.get("ALLOW_E2E_LIVE_DRY_RUN"),
            "DRY_RUN": env_flags.get("DRY_RUN"),
            "ALLOW_LIVE_TRADE": env_flags.get("ALLOW_LIVE_TRADE"),
            "PAPER_MODE": env_flags.get("PAPER_MODE"),
        },
    }


def _build_payload_refs(report: dict) -> dict:
    steps = {s["step"]: s["result"] for s in report.get("steps", [])}

    sig = steps.get("1_signal_router", {})
    prop = steps.get("2_proposition_engine", {})
    gate = steps.get("3_validation_gate", {})
    trade = steps.get("4_trade_executor", {})
    result = steps.get("5_result_tracker", {})
    writer = steps.get("6_datasheet_writer", {})
    feeder = steps.get("7_learning_feeder", {})

    return {
        "signal": {
            "signal_id": sig.get("signal_id"),
            "ticker": sig.get("ticker"),
            "side": sig.get("side"),
            "price": sig.get("price"),
            "strategy_id": sig.get("strategy_id"),
        },
        "proposition": {
            "request_id": prop.get("request_id"),
            "action": prop.get("action"),
            "confidence": prop.get("confidence"),
        },
        "gate": {
            "request_id": gate.get("request_id"),
            "verdict": gate.get("verdict"),
            "risk_status": gate.get("risk_status"),
        },
        "trade": {
            "trade_id": trade.get("trade_id"),
            "status": trade.get("status"),
            "fill_price": trade.get("fill_price"),
            "fill_qty": trade.get("fill_qty"),
            "dry_run": trade.get("dry_run"),
        },
        "result": {
            "trade_id": result.get("trade_id"),
            "outcome": result.get("outcome"),
            "gross_pnl": result.get("gross_pnl"),
            "net_pnl": result.get("net_pnl"),
            "fees": result.get("fees"),
            "opened_at": result.get("opened_at"),
            "closed_at": result.get("closed_at"),
        },
        "datasheet": {
            "dry_run": writer.get("dry_run"),
            "written": writer.get("written"),
            "jsonl_path": writer.get("jsonl_path") or None,
            "csv_path": writer.get("csv_path") or None,
        },
        "learning": {
            "request_id": feeder.get("request_id"),
            "bridge_status": feeder.get("bridge_status"),
            "brick_stored": feeder.get("brick_stored"),
            "brick_id": feeder.get("brick_id") or None,
        },
    }


def _build_summary_md(run_id: str, manifest: dict, payload_refs: dict) -> str:
    verdict = manifest.get("verdict", "UNKNOWN")
    verdict_icon = "✅" if verdict == "PASS" else "🚫"
    modules = manifest.get("modules", {})

    mod_rows = "\n".join(
        f"| `{mod}` | {'✅ PASS' if status == 'PASS' else '❌ ' + status} |"
        for mod, status in modules.items()
    )
    sig = payload_refs.get("signal", {})
    trade = payload_refs.get("trade", {})
    result = payload_refs.get("result", {})

    return f"""\
# E2E Post-Gate Report Bundle

**Run ID**: `{run_id}`
**Verdict**: {verdict_icon} **{verdict}**
**Gate status**: `{manifest.get("gate_status")}`
**Created at**: {manifest.get("created_at")}

## Safety invariants

| Check | Value |
|-------|-------|
| dry_run | `{manifest.get("dry_run")}` |
| live_trade | `{manifest.get("live_trade")}` |
| sheets_mode | `{manifest.get("sheets_mode")}` |
| telegram_mode | `{manifest.get("telegram_mode")}` |
| localcms_gate | `{manifest.get("localcms_gate")}` |

## Modules

| Module | Status |
|--------|--------|
{mod_rows}

## Signal

| Field | Value |
|-------|-------|
| signal_id | `{sig.get("signal_id")}` |
| ticker | `{sig.get("ticker")}` |
| side | `{sig.get("side")}` |
| price | `{sig.get("price")}` |
| strategy_id | `{sig.get("strategy_id")}` |

## Trade result

| Field | Value |
|-------|-------|
| trade_id | `{trade.get("trade_id")}` |
| status | `{trade.get("status")}` |
| outcome | `{result.get("outcome")}` |
| net_pnl | `{result.get("net_pnl")}` |
| gross_pnl | `{result.get("gross_pnl")}` |
| fees | `{result.get("fees")}` |

## GO / PF

| Field | Value |
|-------|-------|
| go_id | `{manifest.get("go_id")}` |
| pf_id | `{manifest.get("pf_id")}` |
| parent_go | `{manifest.get("parent_go")}` |
| bundle_version | `{manifest.get("bundle_version")}` |
"""


# ── Bundle writer ─────────────────────────────────────────────────────────────

def write_bundle(
    report: dict,
    env_flags: dict,
    output_root: Path,
    run_id: str | None = None,
) -> Path:
    """Write all bundle files. Returns bundle directory path."""
    run_id = run_id or _make_run_id()
    bundle_dir = output_root / run_id
    bundle_dir.mkdir(parents=True, exist_ok=True)

    manifest = _build_manifest(run_id, report, env_flags)
    payload_refs = _build_payload_refs(report)
    summary_md = _build_summary_md(run_id, manifest, payload_refs)

    (bundle_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, default=str), encoding="utf-8"
    )
    (bundle_dir / "e2e_report.json").write_text(
        json.dumps(report, indent=2, default=str), encoding="utf-8"
    )
    (bundle_dir / "environment_flags.json").write_text(
        json.dumps(env_flags, indent=2, default=str), encoding="utf-8"
    )
    (bundle_dir / "payload_refs.json").write_text(
        json.dumps(payload_refs, indent=2, default=str), encoding="utf-8"
    )
    (bundle_dir / "summary.md").write_text(summary_md, encoding="utf-8")

    log.info("Bundle written to %s", bundle_dir)
    return bundle_dir


# ── Main ─────────────────────────────────────────────────────────────────────

def build_bundle(
    pipeline_output_path: str | None = None,
    output_root: Path | None = None,
    run_id: str | None = None,
) -> dict:
    """Main entry point. Returns result dict with bundle_dir and verdict."""
    output_root = output_root or DEFAULT_OUTPUT_ROOT

    try:
        env_flags = _validate_env()
    except BundleRefused as exc:
        log.error("Bundle REFUSED (env): %s", exc)
        return {"status": "REFUSED", "reason": str(exc), "bundle_dir": None}

    try:
        if pipeline_output_path:
            log.info("Loading pipeline output from %s", pipeline_output_path)
            report = json.loads(Path(pipeline_output_path).read_text(encoding="utf-8"))
        else:
            report = _run_pipeline()
    except BundleRefused as exc:
        log.error("Bundle REFUSED (pipeline): %s", exc)
        return {"status": "REFUSED", "reason": str(exc), "bundle_dir": None}
    except Exception as exc:
        log.error("Bundle REFUSED (pipeline error): %s", exc)
        return {"status": "REFUSED", "reason": f"Pipeline error: {exc}", "bundle_dir": None}

    try:
        _validate_report(report)
    except BundleRefused as exc:
        log.error("Bundle REFUSED (report): %s", exc)
        return {"status": "REFUSED", "reason": str(exc), "bundle_dir": None}

    bundle_dir = write_bundle(report, env_flags, output_root, run_id=run_id)
    pg = report.get("e2e_post_gate_status", {})

    return {
        "status": "BUNDLED",
        "bundle_dir": str(bundle_dir),
        "run_id": bundle_dir.name,
        "verdict": pg.get("status"),
        "gate_status": pg.get("gate_status"),
        "dry_run": report.get("dry_run"),
        "live_trade": pg.get("live_trade"),
        "modules": pg.get("modules", {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="E2E Report Bundle Generator")
    parser.add_argument(
        "--pipeline-output",
        metavar="FILE",
        help="Use existing pipeline JSON output instead of running pipeline",
    )
    parser.add_argument(
        "--output-root",
        metavar="DIR",
        default=str(DEFAULT_OUTPUT_ROOT),
        help=f"Bundle output root directory (default: {DEFAULT_OUTPUT_ROOT})",
    )
    parser.add_argument(
        "--run-id",
        metavar="RUN_ID",
        default=None,
        help="Override auto-generated run ID",
    )
    args = parser.parse_args()

    result = build_bundle(
        pipeline_output_path=args.pipeline_output,
        output_root=Path(args.output_root),
        run_id=args.run_id,
    )

    print(json.dumps(result, indent=2, default=str))

    if result["status"] != "BUNDLED":
        sys.exit(1)
    log.info("Bundle complete: %s", result["bundle_dir"])


if __name__ == "__main__":
    main()
