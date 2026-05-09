from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Tuple

from modules.desk_pro.signal_event_adapter import (
    normalize_signal_event_v1,
    validate_signal_event_v1,
)


def _is_signal_event_v1(payload: dict) -> bool:
    return isinstance(payload, dict) and (
        "event_type" in payload or "timeframe" in payload or "direction" in payload
    )


def _validate_visual_context(visual_context: dict | None) -> Tuple[bool, List[str]]:
    if visual_context is None:
        return True, ["visual_context missing: snapshot-only synthesis"]
    errors: List[str] = []
    for field in ("source", "capture_id", "symbol", "timeframe", "captured_at", "image_ref", "status"):
        if not visual_context.get(field):
            errors.append(f"visual_context missing {field}")
    return len(errors) == 0, errors


def _validate_desk_snapshot(desk_snapshot: dict | None) -> Tuple[bool, List[str]]:
    if desk_snapshot is None:
        return True, ["desk_snapshot missing: timer-only synthesis"]
    errors: List[str] = []
    for field in ("symbol", "tf", "snapshot_ts", "path"):
        if not desk_snapshot.get(field):
            errors.append(f"desk_snapshot missing {field}")
    return len(errors) == 0, errors


def validate_desk_pro_dry_run_inputs(
    signal_event: dict,
    visual_context: dict | None = None,
    desk_snapshot: dict | None = None,
) -> tuple[bool, list[str]]:
    errors: List[str] = []

    if not isinstance(signal_event, dict):
        return False, ["signal_event payload is not a dict"]

    signal_v1 = signal_event if _is_signal_event_v1(signal_event) else normalize_signal_event_v1(signal_event)
    signal_ok, signal_errors = validate_signal_event_v1(signal_v1)
    if not signal_ok:
        errors.extend(signal_errors)

    snapshot_ok, snapshot_errors = _validate_desk_snapshot(desk_snapshot)
    if not snapshot_ok:
        errors.extend(snapshot_errors)

    visual_ok, visual_errors = _validate_visual_context(visual_context)
    if not visual_ok:
        errors.extend(visual_errors)

    return len(errors) == 0, errors


def build_desk_pro_dry_run_synthesis(
    signal_event: dict,
    visual_context: dict | None = None,
    desk_snapshot: dict | None = None,
) -> dict:
    signal_v1 = deepcopy(signal_event if _is_signal_event_v1(signal_event) else normalize_signal_event_v1(signal_event))

    errors: List[str] = []
    warnings: List[str] = []

    signal_ok, signal_messages = validate_signal_event_v1(signal_v1)
    if not signal_ok:
        errors.extend(signal_messages)
    else:
        warnings.extend([m for m in signal_messages if m])

    snapshot_ok, snapshot_messages = _validate_desk_snapshot(desk_snapshot)
    if desk_snapshot is None:
        warnings.extend(snapshot_messages)
    elif not snapshot_ok:
        errors.extend(snapshot_messages)

    visual_ok, visual_messages = _validate_visual_context(visual_context)
    if visual_context is None:
        warnings.extend(visual_messages)
    elif not visual_ok:
        errors.extend(visual_messages)

    join_checks: Dict[str, Any] = {
        "timeframe_match": None,
        "symbol_match": None,
        "symbol_normalization_needed": None,
        "visual_context_ref_match": None,
    }

    if desk_snapshot is not None:
        join_checks["timeframe_match"] = signal_v1.get("timeframe") == desk_snapshot.get("tf")
        signal_symbol = str(signal_v1.get("symbol") or "")
        snapshot_symbol = str(desk_snapshot.get("symbol") or "")
        join_checks["symbol_match"] = signal_symbol == snapshot_symbol
        join_checks["symbol_normalization_needed"] = bool(
            signal_symbol and snapshot_symbol and signal_symbol != snapshot_symbol and signal_symbol in snapshot_symbol
        )
        if join_checks["symbol_normalization_needed"]:
            warnings.append("symbol normalization needed between signal_event and desk_snapshot")
        if join_checks["timeframe_match"] is False:
            warnings.append("timeframe mismatch between signal_event and desk_snapshot")

    if visual_context is not None:
        join_checks["visual_context_ref_match"] = signal_v1.get("visual_context_ref") in (None, visual_context.get("capture_id"))
        if desk_snapshot is not None and visual_context.get("symbol") != desk_snapshot.get("symbol"):
            warnings.append("visual_context and desk_snapshot symbol mismatch")

    status = "PASS"
    if errors:
        status = "FAIL"
    elif warnings:
        status = "WARN"

    return {
        "mode": "dry_run",
        "status": status,
        "no_trade": True,
        "no_telegram": True,
        "no_webhook": True,
        "no_systemd": True,
        "signal_event": signal_v1,
        "visual_context": deepcopy(visual_context),
        "desk_snapshot": deepcopy(desk_snapshot),
        "join_checks": join_checks,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "signal_event_present": signal_v1 is not None,
            "visual_context_present": visual_context is not None,
            "desk_snapshot_present": desk_snapshot is not None,
        },
    }


def run_desk_pro_dry_run(
    signal_event_payload: dict,
    visual_context: dict | None = None,
    desk_snapshot: dict | None = None,
) -> dict:
    return build_desk_pro_dry_run_synthesis(
        signal_event=signal_event_payload,
        visual_context=visual_context,
        desk_snapshot=desk_snapshot,
    )
