from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

EVENTS_PATH = Path("data/vision/coinglass/events.jsonl")

_MIN_CONFIDENCE = 0.60
_DEFAULT_REQUIRED = 3


@dataclass
class RunResult:
    screenshot_ts: str
    passed: bool
    detection_count: int
    reason: str


@dataclass
class ValidationReport:
    ok: bool
    required: int
    evaluated: int
    results: List[RunResult]
    message: str


def _run_passes(event: dict) -> tuple[bool, int, str]:
    """Return (passed, detection_count, reason) for a single events.jsonl line."""
    detections = event.get("detections", [])
    qualifying = [
        d for d in detections
        if d.get("confidence", 0) >= _MIN_CONFIDENCE and d.get("extracted_value") is not None
    ]
    if not qualifying:
        return False, len(detections), f"{len(detections)} detections, 0 qualify (conf≥{_MIN_CONFIDENCE} + non-null)"
    return True, len(qualifying), f"{len(qualifying)} qualifying detections"


def validate_staging_runs(
    events_path: Path | None = None,
    required_passes: int = _DEFAULT_REQUIRED,
) -> ValidationReport:
    """Check whether the last `required_passes` runs all PASS.

    A run PASS = ≥1 detection with confidence ≥ 0.6 AND non-null extracted_value.
    Returns a ValidationReport. Never raises — returns ok=False with reason on error.
    """
    p = events_path or EVENTS_PATH
    if not p.exists():
        return ValidationReport(
            ok=False, required=required_passes, evaluated=0, results=[],
            message=f"events.jsonl not found: {p}",
        )

    try:
        lines = [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    except Exception as exc:
        return ValidationReport(
            ok=False, required=required_passes, evaluated=0, results=[],
            message=f"failed to read events.jsonl: {exc}",
        )

    if not lines:
        return ValidationReport(
            ok=False, required=required_passes, evaluated=0, results=[],
            message="events.jsonl is empty — no runs recorded",
        )

    last_n = lines[-required_passes:]
    results: List[RunResult] = []
    for line in last_n:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            results.append(RunResult("?", False, 0, "malformed JSON line"))
            continue
        ts = event.get("screenshot_ts", "?")
        passed, count, reason = _run_passes(event)
        results.append(RunResult(ts, passed, count, reason))

    all_pass = all(r.passed for r in results)
    evaluated = len(results)

    if all_pass and evaluated >= required_passes:
        msg = f"PASS — {evaluated}/{required_passes} consecutive runs OK"
    elif evaluated < required_passes:
        msg = f"INSUFFICIENT — only {evaluated} runs recorded, need {required_passes}"
    else:
        failed = [r for r in results if not r.passed]
        msg = f"FAIL — {len(failed)}/{evaluated} runs did not qualify"

    return ValidationReport(
        ok=all_pass and evaluated >= required_passes,
        required=required_passes,
        evaluated=evaluated,
        results=results,
        message=msg,
    )
