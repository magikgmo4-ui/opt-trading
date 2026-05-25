"""
Fixture validation for Google Sheets global schema (V1).

Rules from VALIDATION_RULES.md:
  R1  tab_name must be in CANONICAL_SHEETS
  R2  schema_version = v1 if present
  R3  required columns present and non-null
  R4  enum values in allowed set
  R5  iso_utc_ts format: YYYY-MM-DDTHH:MM:SSZ
  R6  PK columns present and non-null
  R7  no duplicate PK within a fixture
  R8  *_ref must not contain full JSON payload (heuristic)
  R9  write_mode not violated (doc-only → no writer exercise in fixtures)
  R10 validator is deterministic and has no side effects

No Google Sheets API calls. No live data reads. Pure local fixture validation.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any

FIXTURES = Path(__file__).parent / "fixtures" / "google_sheets_global_schema"

CANONICAL_TABS = {
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
}

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
}


def _is_iso_utc(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    return bool(_ISO_UTC_RE.match(value))


def _is_ref_payload(value: Any) -> bool:
    """Heuristic: *_ref must not be a full JSON payload."""
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    return (stripped.startswith("{") or stripped.startswith("[")) and len(stripped) > 50


def validate_fixture(tab_name: str, rows: list[dict]) -> list[tuple[str, str, str]]:
    """Return list of (severity, rule, message). Empty = 0 FAIL."""
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
        row_id = f"row[{i}]"

        # R3 — required columns
        for col in required:
            if col not in row:
                issues.append(("FAIL", "R3", f"{row_id}: required column '{col}' absent"))
            elif row[col] is None or row[col] == "":
                issues.append(("FAIL", "R3", f"{row_id}: required column '{col}' is null/empty"))

        # R4 — enum values
        for col, allowed in enums.items():
            if col in row and row[col] is not None:
                if row[col] not in allowed:
                    issues.append(("FAIL", "R4", f"{row_id}: column '{col}' value '{row[col]}' not in {sorted(allowed)}"))

        # R5 — iso_utc_ts
        for col in timestamps:
            if col in row and row[col] is not None:
                if not _is_iso_utc(row[col]):
                    issues.append(("FAIL", "R5", f"{row_id}: column '{col}' value '{row[col]}' not ISO UTC Z"))

        # R6 — PK columns present and non-null
        pk_values = []
        for col in pk_cols:
            if col not in row or row[col] is None or row[col] == "":
                issues.append(("FAIL", "R6", f"{row_id}: PK column '{col}' absent or null"))
                pk_values = None
                break
            pk_values.append(row[col])

        # R7 — duplicate PK detection
        if pk_values is not None:
            pk_tuple = tuple(pk_values)
            if pk_tuple in seen_pks:
                issues.append(("FAIL", "R7", f"{row_id}: duplicate PK {dict(zip(pk_cols, pk_values))}"))
            seen_pks.add(pk_tuple)

        # R8 — *_ref must not be full JSON payload
        for col in ref_cols:
            if col in row and row[col] is not None:
                if _is_ref_payload(row[col]):
                    issues.append(("FAIL", "R8", f"{row_id}: column '{col}' looks like a full JSON payload"))

    return issues


def load_fixture(tab_name: str) -> list[dict]:
    path = FIXTURES / f"{tab_name}.jsonl"
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


class TestFixtureFilesExist(unittest.TestCase):
    def _check(self, tab: str) -> None:
        assert (FIXTURES / f"{tab}.jsonl").exists(), f"Missing fixture: {tab}.jsonl"

    def test_sheets_registry_exists(self):
        self._check("sheets_registry")

    def test_daily_sessions_exists(self):
        self._check("daily_sessions")

    def test_strategy_events_exists(self):
        self._check("strategy_events")

    def test_strategy_perf_exists(self):
        self._check("strategy_perf")

    def test_strategy_gates_exists(self):
        self._check("strategy_gates")

    def test_registry_candidates_exists(self):
        self._check("registry_candidates")

    def test_market_metrics_exists(self):
        self._check("market_metrics")

    def test_desk_snapshots_exists(self):
        self._check("desk_snapshots")

    def test_visual_context_exists(self):
        self._check("visual_context")

    def test_telegram_claims_exists(self):
        self._check("telegram_claims")

    def test_watchlists_exists(self):
        self._check("watchlists")


class TestFixtureValidation(unittest.TestCase):
    """Each fixture must produce 0 FAIL."""

    def _assert_zero_fail(self, tab: str) -> None:
        rows = load_fixture(tab)
        assert len(rows) >= 1, f"{tab}: fixture is empty"
        issues = validate_fixture(tab, rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertEqual(
            fails, [],
            f"{tab}: {len(fails)} FAIL(s):\n" + "\n".join(f"  [{r}] {msg}" for _, r, msg in fails),
        )

    def test_sheets_registry_zero_fail(self):
        self._assert_zero_fail("sheets_registry")

    def test_daily_sessions_zero_fail(self):
        self._assert_zero_fail("daily_sessions")

    def test_strategy_events_zero_fail(self):
        self._assert_zero_fail("strategy_events")

    def test_strategy_perf_zero_fail(self):
        self._assert_zero_fail("strategy_perf")

    def test_strategy_gates_zero_fail(self):
        self._assert_zero_fail("strategy_gates")

    def test_registry_candidates_zero_fail(self):
        self._assert_zero_fail("registry_candidates")

    def test_market_metrics_zero_fail(self):
        self._assert_zero_fail("market_metrics")

    def test_desk_snapshots_zero_fail(self):
        self._assert_zero_fail("desk_snapshots")

    def test_visual_context_zero_fail(self):
        self._assert_zero_fail("visual_context")

    def test_telegram_claims_zero_fail(self):
        self._assert_zero_fail("telegram_claims")

    def test_watchlists_zero_fail(self):
        self._assert_zero_fail("watchlists")


class TestFixtureMinimumRows(unittest.TestCase):
    def _assert_min_rows(self, tab: str, minimum: int = 2) -> None:
        rows = load_fixture(tab)
        self.assertGreaterEqual(len(rows), minimum, f"{tab}: expected >= {minimum} rows, got {len(rows)}")

    def test_sheets_registry_min_rows(self):
        self._assert_min_rows("sheets_registry", 11)

    def test_daily_sessions_min_rows(self):
        self._assert_min_rows("daily_sessions")

    def test_strategy_events_min_rows(self):
        self._assert_min_rows("strategy_events")

    def test_market_metrics_min_rows(self):
        self._assert_min_rows("market_metrics")

    def test_watchlists_min_rows(self):
        self._assert_min_rows("watchlists")


class TestValidatorEdgeCases(unittest.TestCase):
    """Validator must reject bad payloads (proves R-rules work)."""

    def test_r3_missing_required_column(self):
        bad_rows = [{"tab_name": "sheets_registry"}]
        issues = validate_fixture("sheets_registry", bad_rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("schema_version" in m for _, _, m in fails))

    def test_r3_null_required_column(self):
        bad_rows = [{"tab_name": None, "schema_version": "v1", "owner_pf": "PF_X", "schema_status": "active", "updated_at": "2026-05-25T00:00:00Z"}]
        issues = validate_fixture("sheets_registry", bad_rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("tab_name" in m for _, _, m in fails))

    def test_r4_bad_enum(self):
        bad_rows = [{"tab_name": "x", "schema_version": "v1", "owner_pf": "PF_X", "schema_status": "unknown_status", "updated_at": "2026-05-25T00:00:00Z"}]
        issues = validate_fixture("sheets_registry", bad_rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("schema_status" in m for _, _, m in fails))

    def test_r5_bad_timestamp_format(self):
        bad_rows = [{"run_id": "r1", "started_at": "2026-05-25 08:00:00", "status": "success"}]
        issues = validate_fixture("daily_sessions", bad_rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("started_at" in m for _, _, m in fails))

    def test_r5_timestamp_missing_z(self):
        bad_rows = [{"run_id": "r1", "started_at": "2026-05-25T08:00:00+00:00", "status": "success"}]
        issues = validate_fixture("daily_sessions", bad_rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("started_at" in m for _, _, m in fails))

    def test_r6_pk_null(self):
        bad_rows = [{"run_id": None, "started_at": "2026-05-25T08:00:00Z", "status": "success"}]
        issues = validate_fixture("daily_sessions", bad_rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("run_id" in m for _, _, m in fails))

    def test_r7_duplicate_pk(self):
        rows = [
            {"run_id": "r1", "started_at": "2026-05-25T08:00:00Z", "status": "success"},
            {"run_id": "r1", "started_at": "2026-05-25T09:00:00Z", "status": "fail"},
        ]
        issues = validate_fixture("daily_sessions", rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("R7" in r for _, r, _ in fails))

    def test_r8_ref_is_full_json_payload(self):
        bad_ref = '{"event_id": "x", "data": "very long payload here that definitely exceeds 50 characters threshold"}'
        rows = [{"event_id": "e1", "event_type": "signal_event.v1", "event_ts": "2026-05-25T09:00:00Z", "payload_ref": bad_ref}]
        issues = validate_fixture("strategy_events", rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("R8" in r for _, r, _ in fails))

    def test_r1_unknown_tab(self):
        issues = validate_fixture("nonexistent_tab", [{}])
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("R1" in r for _, r, _ in fails))

    def test_validator_deterministic(self):
        rows = load_fixture("market_metrics")
        result_a = validate_fixture("market_metrics", rows)
        result_b = validate_fixture("market_metrics", rows)
        self.assertEqual(result_a, result_b)

    def test_no_google_api_calls(self):
        import sys
        mods_before = set(sys.modules.keys())
        load_fixture("watchlists")
        new_mods = set(sys.modules.keys()) - mods_before
        google_mods = [m for m in new_mods if "google" in m.lower() or "gspread" in m.lower()]
        self.assertEqual(google_mods, [])

    def test_daily_sessions_enum_fail(self):
        bad_rows = [{"run_id": "r1", "started_at": "2026-05-25T08:00:00Z", "status": "unknown_status"}]
        issues = validate_fixture("daily_sessions", bad_rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("status" in m for _, _, m in fails))

    def test_strategy_gates_enum_fail(self):
        bad_rows = [{"as_of": "2026-05-25T00:00:00Z", "strategy_id": "s1", "gate_name": "g1", "decision": "approve"}]
        issues = validate_fixture("strategy_gates", bad_rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("decision" in m for _, _, m in fails))

    def test_market_metrics_composite_pk_duplicate(self):
        rows = [
            {"as_of": "2026-05-25T09:00:00Z", "symbol": "BTCUSDT", "metric_name": "funding_rate", "value": 0.0001},
            {"as_of": "2026-05-25T09:00:00Z", "symbol": "BTCUSDT", "metric_name": "funding_rate", "value": 0.0002},
        ]
        issues = validate_fixture("market_metrics", rows)
        fails = [i for i in issues if i[0] == "FAIL"]
        self.assertTrue(any("R7" in r for _, r, _ in fails))
