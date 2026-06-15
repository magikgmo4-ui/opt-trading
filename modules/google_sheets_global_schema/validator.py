"""
Shared validator for Google Sheets global schema V1.

Rules from VALIDATION_RULES.md (R1-R10). Used by sheets_writer before any write.
No Google API calls. Deterministic on inputs.
"""
from __future__ import annotations

import re
from typing import Any

CANONICAL_TABS = frozenset({
    "sheets_registry",
    "daily_sessions",
    "strategy_events",
    "strategy_perf",
    "strategy_gates",
    "registry_candidates",
    "market_metrics",
    "desk_snapshots",
    "visual_context",
    "telegram_claims",
    "watchlists",
    "spacex_super_desk",
    "spacex_true_value",
})

_ISO_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

SCHEMA: dict[str, dict[str, Any]] = {
    "sheets_registry": {
        "required": ["tab_name", "schema_version", "owner_pf", "schema_status", "updated_at"],
        "enums": {"schema_status": {"planned", "active", "deprecated"}},
        "timestamps": ["updated_at"],
        "pk": ["tab_name", "schema_version"],
        "ref_cols": [],
    },
    "daily_sessions": {
        "required": ["run_id", "started_at", "status"],
        "enums": {"status": {"success", "fail", "warn"}},
        "timestamps": ["started_at", "ended_at"],
        "pk": ["run_id"],
        "ref_cols": ["report_ref"],
    },
    "strategy_events": {
        "required": ["event_id", "event_type", "event_ts"],
        "enums": {},
        "timestamps": ["event_ts"],
        "pk": ["event_id"],
        "ref_cols": ["payload_ref"],
    },
    "strategy_perf": {
        "required": ["as_of", "strategy_id", "metric_name", "window", "value"],
        "enums": {},
        "timestamps": ["as_of"],
        "pk": ["as_of", "strategy_id", "metric_name", "window"],
        "ref_cols": [],
    },
    "strategy_gates": {
        "required": ["as_of", "strategy_id", "gate_name", "decision"],
        "enums": {"decision": {"promote", "hold", "retire"}},
        "timestamps": ["as_of"],
        "pk": ["as_of", "strategy_id", "gate_name"],
        "ref_cols": [],
    },
    "registry_candidates": {
        "required": ["as_of", "strategy_id", "candidate_name", "candidate_ref"],
        "enums": {},
        "timestamps": ["as_of"],
        "pk": ["as_of", "strategy_id", "candidate_name"],
        "ref_cols": ["candidate_ref"],
    },
    "market_metrics": {
        "required": ["as_of", "symbol", "metric_name", "value"],
        "enums": {},
        "timestamps": ["as_of"],
        "pk": ["as_of", "symbol", "metric_name"],
        "ref_cols": ["source_ref"],
    },
    "desk_snapshots": {
        "required": ["snapshot_id", "created_at", "snapshot_ref"],
        "enums": {},
        "timestamps": ["created_at"],
        "pk": ["snapshot_id"],
        "ref_cols": ["snapshot_ref"],
    },
    "visual_context": {
        "required": ["context_id", "created_at", "payload_ref"],
        "enums": {},
        "timestamps": ["created_at"],
        "pk": ["context_id"],
        "ref_cols": ["payload_ref"],
    },
    "telegram_claims": {
        "required": ["claim_id", "claim_ts", "claim_type", "payload_ref"],
        "enums": {},
        "timestamps": ["claim_ts"],
        "pk": ["claim_id"],
        "ref_cols": ["payload_ref"],
    },
    "watchlists": {
        "required": ["watchlist_id", "symbol", "timeframe", "enabled"],
        "enums": {},
        "timestamps": [],
        "pk": ["watchlist_id"],
        "ref_cols": [],
    },
    "spacex_super_desk": {
        "required": ["as_of", "symbol", "metric_name", "value"],
        "enums": {},
        "timestamps": ["as_of"],
        "pk": ["as_of", "symbol", "metric_name"],
        "ref_cols": ["source_ref"],
    },
    "spacex_true_value": {
        "required": ["as_of", "ticker", "grade", "true_value_score", "confidence_score"],
        "enums": {},
        "timestamps": ["as_of"],
        "pk": ["as_of", "ticker"],
        "ref_cols": ["source_ref"],
    },
}


def _is_iso_utc(value: Any) -> bool:
    return isinstance(value, str) and bool(_ISO_UTC_RE.match(value))


def _is_ref_payload(value: Any) -> bool:
    """Heuristic: *_ref must not contain a full inlined JSON payload."""
    if not isinstance(value, str):
        return False
    s = value.strip()
    return (s.startswith("{") or s.startswith("[")) and len(s) > 50


def validate_rows(tab_name: str, rows: list[dict]) -> list[tuple[str, str, str]]:
    """
    Validate rows against the V1 schema for *tab_name*.

    Returns list of (severity, rule_id, message).
    severity in: FAIL, WARN, INFO
    Empty list = 0 FAIL (all rules satisfied).
    """
    issues: list[tuple[str, str, str]] = []

    if tab_name not in CANONICAL_TABS:
        issues.append(("FAIL", "R1", f"tab '{tab_name}' not in CANONICAL_TABS"))
        return issues

    schema = SCHEMA[tab_name]
    required = schema["required"]
    enums = schema["enums"]
    timestamps = schema["timestamps"]
    pk_cols = schema["pk"]
    ref_cols = schema["ref_cols"]
    seen_pks: set[tuple] = set()

    for i, row in enumerate(rows):
        label = f"row[{i}]"

        for col in required:
            if col not in row:
                issues.append(("FAIL", "R3", f"{label}: required '{col}' absent"))
            elif row[col] is None or row[col] == "":
                issues.append(("FAIL", "R3", f"{label}: required '{col}' is null/empty"))

        for col, allowed in enums.items():
            if col in row and row[col] is not None and row[col] not in allowed:
                issues.append(("FAIL", "R4", f"{label}: '{col}'='{row[col]}' not in {sorted(allowed)}"))

        for col in timestamps:
            if col in row and row[col] is not None:
                if not _is_iso_utc(row[col]):
                    issues.append(("FAIL", "R5", f"{label}: '{col}'='{row[col]}' not ISO UTC Z"))

        pk_vals: list | None = []
        for col in pk_cols:
            v = row.get(col)
            if v is None or v == "":
                issues.append(("FAIL", "R6", f"{label}: PK col '{col}' absent/null"))
                pk_vals = None
                break
            pk_vals.append(v)

        if pk_vals is not None:
            pk_tuple = tuple(pk_vals)
            if pk_tuple in seen_pks:
                issues.append(("FAIL", "R7", f"{label}: duplicate PK {dict(zip(pk_cols, pk_vals))}"))
            seen_pks.add(pk_tuple)

        for col in ref_cols:
            v = row.get(col)
            if v is not None and _is_ref_payload(v):
                issues.append(("FAIL", "R8", f"{label}: '{col}' contains full JSON payload"))

    return issues


def fails(issues: list[tuple[str, str, str]]) -> list[str]:
    """Return only FAIL messages."""
    return [f"[{r}] {msg}" for sev, r, msg in issues if sev == "FAIL"]
