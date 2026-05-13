from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
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


def build_desk_pro_dry_run_report(synthesis: dict) -> str:
    """Build a human-readable markdown report from the dry-run synthesis."""
    ev = synthesis.get("signal_event") or {}
    lines = [
        f"# Desk Pro Dry-Run Report",
        f"",
        f"**Status:** {synthesis.get('status', 'UNKNOWN')}",
        f"**Timestamp:** {ev.get('timestamp', 'N/A')}",
        f"**Engine:** {ev.get('engine', 'N/A')}",
        f"**Symbol:** {ev.get('symbol', 'N/A')}",
        f"**Timeframe:** {ev.get('timeframe', 'N/A')}",
        f"**Direction:** {ev.get('direction', 'N/A')}",
        f"**Signal Event Present:** {synthesis['summary']['signal_event_present']}",
        f"**Visual Context Present:** {synthesis['summary']['visual_context_present']}",
        f"**Desk Snapshot Present:** {synthesis['summary']['desk_snapshot_present']}",
        f"",
        f"## Safety Flags",
        f"",
        f"- `no_trade`: {synthesis['no_trade']}",
        f"- `no_telegram`: {synthesis['no_telegram']}",
        f"- `no_webhook`: {synthesis['no_webhook']}",
        f"- `no_systemd`: {synthesis['no_systemd']}",
    ]
    if synthesis.get("errors"):
        lines.append(f"")
        lines.append(f"## Errors")
        for err in synthesis["errors"]:
            lines.append(f"- {err}")
    if synthesis.get("warnings"):
        lines.append(f"")
        lines.append(f"## Warnings")
        for warn in synthesis["warnings"]:
            lines.append(f"- {warn}")
    return "\n".join(lines) + "\n"


def write_desk_pro_dry_run_artifacts(synthesis: dict, output_dir: Path | str) -> dict:
    """Write dry-run artifacts to the output directory.

    Returns:
        dict with written file paths.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = synthesis["signal_event"].get("payload_hash", ts)

    latest_json = out / "latest.json"
    latest_md = out / "latest.md"
    history_jsonl = out / "history.jsonl"

    latest_json.write_text(json.dumps(synthesis, indent=2, default=str), encoding="utf-8")
    latest_md.write_text(build_desk_pro_dry_run_report(synthesis), encoding="utf-8")

    with open(history_jsonl, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(synthesis, default=str) + "\n")

    return {
        "written_files": {
            "latest_json": str(latest_json),
            "latest_md": str(latest_md),
            "history_jsonl": str(history_jsonl),
        },
        "run_id": run_id,
    }


def load_latest_desk_snapshot(
    snapshot_path: Path | str,
    target_symbol: str = "BTCUSDT",
) -> dict | None:
    """Load the best-matching desk snapshot from a snapshot index file.

    The snapshot index is expected to be a JSON dict mapping symbol keys
    to snapshot entries with fields ``symbol``, ``tf``, ``snapshot_ts``, ``path``.
    """
    path = Path(snapshot_path)
    if not path.exists():
        return None
    try:
        index = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    inst_symbol = None
    for key, entry in index.items():
        raw_sym = str(entry.get("symbol", key))
        if raw_sym.startswith(target_symbol) or target_symbol in raw_sym:
            inst_symbol = key
            break

    if inst_symbol is None:
        return None

    entry = index[inst_symbol]
    snapshot_dict = {
        "symbol": entry.get("symbol", inst_symbol),
        "tf": entry.get("tf", "H1"),
        "snapshot_ts": entry.get("snapshot_ts"),
        "path": entry.get("path"),
        "ingested_at": entry.get("ingested_at"),
        "source": entry.get("source"),
    }
    return snapshot_dict


def load_latest_visual_context(
    vc_path: Path | str,
) -> dict | None:
    """Load a visual_context entry from a JSON or JSONL file.

    The file is expected to contain a dict with fields
    ``source``, ``capture_id``, ``symbol``, ``timeframe``,
    ``captured_at``, ``image_ref``, and ``status``.
    """
    path = Path(vc_path)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict):
        return None
    return data
