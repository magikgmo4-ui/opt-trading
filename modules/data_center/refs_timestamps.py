from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional


def now_utc_z() -> str:
    """Return current UTC time as ISO 8601 string with Z suffix."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def build_refs(
    primary_output: Optional[str] = None,
    latest: Optional[str] = None,
    status: Optional[str] = None,
    **extra: Any,
) -> dict:
    """Build a refs dict from the standard fields.

    Only includes non-None values. Extra keyword args are included as-is.
    Does not overwrite or rename legacy refs fields.
    """
    refs: dict[str, Any] = {}
    if primary_output is not None:
        refs["primary_output"] = primary_output
    if latest is not None:
        refs["latest"] = latest
    if status is not None:
        refs["status"] = status
    refs.update({k: v for k, v in extra.items() if v is not None})
    return refs


def enrich_produced_at(payload: dict, produced_at: Optional[str] = None) -> dict:
    """Add produced_at to a payload dict if not already present.

    Does not overwrite existing produced_at. Returns a new dict (shallow copy).
    Does not modify the original payload.
    """
    if "produced_at" in payload:
        return dict(payload)
    return {**payload, "produced_at": produced_at or now_utc_z()}


def validate_iso_utc(ts: str) -> bool:
    """Return True if ts is a valid ISO 8601 UTC timestamp (Z or +00:00 suffix)."""
    if not isinstance(ts, str):
        return False
    ts = ts.strip()
    if not (ts.endswith("Z") or ts.endswith("+00:00")):
        return False
    try:
        datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def is_compatible_legacy(payload: dict) -> tuple[bool, list[str]]:
    """Check if a payload is compatible with the refs/timestamps standard.

    Checks for presence of at least one recognized timestamp field.
    Returns (ok, warnings) — never raises, never modifies payload.
    Legacy fields (_ts, metrics_ts, analysis_ts, claim_ts, etc.) are ALLOWED.
    """
    ts_candidates = [
        "produced_at", "metrics_ts", "analysis_ts", "claim_ts",
        "generated_at", "captured_at", "snapshot_ts", "ingested_at",
        "written_at", "source_ts", "_ts",
    ]
    found = [k for k in ts_candidates if k in payload]
    warnings = []
    if not found:
        warnings.append("no recognized timestamp field found in payload")
    return len(warnings) == 0, warnings
