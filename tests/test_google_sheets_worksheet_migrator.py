"""
Tests for WorksheetMigrator — worksheet title alignment tool.

Covers:
- plan() from empty spreadsheet -> 11 creates
- plan() with Sheet1 -> rename daily_sessions + 10 creates
- plan() with French locale "Feuille 1" -> rename daily_sessions + 10 creates
- plan() with all canonical present -> all ok, needs_migration=False
- plan() unknown extra tab -> ignored (not deleted)
- plan() canonical + legacy both present -> ok wins, no double-rename
- apply() dry_run -> ok=True, actions_applied=[]
- apply() fake -> actions_applied = renames+creates
- apply() fake empty client -> all 11 canonical worksheets created
- apply() fake with Sheet1 -> daily_sessions created
- apply() no migration needed -> ok=True, actions_applied=[]
- run() with no client -> dry_run
- run() fake empty -> 11 applied
- real client blocked without flag
- real client blocked without spreadsheet_id
- no Google API calls on import or run
- MigrationPlan properties: renames, creates, already_ok, needs_migration
- MigrationAction.__str__ readable
"""
from __future__ import annotations

import os
import sys
import unittest

GOOGLE_MODULES = frozenset({"google", "gspread", "googleapiclient", "google.auth", "google.oauth2"})


def _google_mods() -> set[str]:
    return {m for m in sys.modules if any(m == g or m.startswith(g + ".") for g in GOOGLE_MODULES)}


def _fake_client():
    from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
    return FakeSheetsClient()


def _migrator(client=None, spreadsheet_id=None, dry_run=True):
    from modules.google_sheets_global_schema.worksheet_migrator import WorksheetMigrator
    return WorksheetMigrator(client=client, spreadsheet_id=spreadsheet_id, dry_run=dry_run)


# ---------------------------------------------------------------------------
# MigrationPlan unit tests
# ---------------------------------------------------------------------------

class TestMigrationPlan(unittest.TestCase):
    def _plan(self, existing):
        return _migrator().plan(existing)

    def test_empty_spreadsheet_plans_11_creates(self):
        plan = self._plan([])
        self.assertEqual(plan.creates, 11)
        self.assertEqual(plan.renames, 0)
        self.assertEqual(plan.already_ok, 0)
        self.assertTrue(plan.needs_migration)

    def test_sheet1_maps_to_daily_sessions_rename(self):
        plan = self._plan(["Sheet1"])
        renames = [a for a in plan.actions if a.action == "rename"]
        self.assertEqual(len(renames), 1)
        self.assertEqual(renames[0].canonical_name, "daily_sessions")
        self.assertEqual(renames[0].current_title, "Sheet1")

    def test_sheet1_reduces_creates_by_1(self):
        plan = self._plan(["Sheet1"])
        self.assertEqual(plan.creates, 10)   # 11 total - 1 rename
        self.assertEqual(plan.renames, 1)

    def test_french_locale_maps_to_daily_sessions(self):
        plan = self._plan(["Feuille 1"])
        renames = [a for a in plan.actions if a.action == "rename"]
        self.assertTrue(any(r.canonical_name == "daily_sessions" for r in renames))

    def test_french_no_space_maps_to_daily_sessions(self):
        plan = self._plan(["Feuille1"])
        renames = [a for a in plan.actions if a.action == "rename"]
        self.assertTrue(any(r.canonical_name == "daily_sessions" for r in renames))

    def test_existing_canonical_is_ok(self):
        plan = self._plan(["daily_sessions"])
        ok_names = [a.canonical_name for a in plan.actions if a.action == "ok"]
        self.assertIn("daily_sessions", ok_names)

    def test_all_canonical_present_is_all_ok(self):
        from modules.google_sheets_global_schema.validator import CANONICAL_TABS
        plan = self._plan(list(CANONICAL_TABS))
        self.assertEqual(plan.renames, 0)
        self.assertEqual(plan.creates, 0)
        self.assertEqual(plan.already_ok, 11)
        self.assertFalse(plan.needs_migration)

    def test_unknown_extra_tab_ignored(self):
        plan = self._plan(["SomeOtherTab", "AnotherExtra"])
        # Unknown tabs are not in LEGACY_TITLE_MAP -> all 11 canonical are creates
        self.assertEqual(plan.creates, 11)

    def test_canonical_and_legacy_both_present_canonical_wins(self):
        # Both "Sheet1" and "daily_sessions" exist -> ok (canonical wins, Sheet1 ignored)
        plan = self._plan(["Sheet1", "daily_sessions"])
        ok_names = [a.canonical_name for a in plan.actions if a.action == "ok"]
        rename_names = [a.canonical_name for a in plan.actions if a.action == "rename"]
        self.assertIn("daily_sessions", ok_names)
        self.assertNotIn("daily_sessions", rename_names)

    def test_plan_covers_all_11_canonical_tabs(self):
        from modules.google_sheets_global_schema.validator import CANONICAL_TABS
        plan = self._plan([])
        canonical_in_plan = {a.canonical_name for a in plan.actions}
        self.assertEqual(canonical_in_plan, CANONICAL_TABS)

    def test_plan_actions_count_is_11(self):
        plan = self._plan([])
        self.assertEqual(len(plan.actions), 11)

    def test_legacy_consumed_only_once(self):
        # "sheet1" lowercase also maps to daily_sessions
        plan = self._plan(["sheet1"])
        renames = [a for a in plan.actions if a.action == "rename"]
        self.assertEqual(len(renames), 1)
        self.assertEqual(renames[0].canonical_name, "daily_sessions")


# ---------------------------------------------------------------------------
# MigrationAction str
# ---------------------------------------------------------------------------

class TestMigrationActionStr(unittest.TestCase):
    def test_ok_str(self):
        from modules.google_sheets_global_schema.worksheet_migrator import MigrationAction
        a = MigrationAction("ok", "daily_sessions")
        self.assertIn("daily_sessions", str(a))

    def test_rename_str(self):
        from modules.google_sheets_global_schema.worksheet_migrator import MigrationAction
        a = MigrationAction("rename", "daily_sessions", current_title="Sheet1")
        s = str(a)
        self.assertIn("Sheet1", s)
        self.assertIn("daily_sessions", s)

    def test_create_str(self):
        from modules.google_sheets_global_schema.worksheet_migrator import MigrationAction
        a = MigrationAction("create", "watchlists")
        self.assertIn("watchlists", str(a))


# ---------------------------------------------------------------------------
# Dry-run mode
# ---------------------------------------------------------------------------

class TestMigratorDryRun(unittest.TestCase):
    def test_dry_run_apply_returns_ok_no_actions(self):
        m = _migrator(dry_run=True)
        plan = m.plan(["Sheet1"])
        result = m.apply(plan)
        self.assertTrue(result.ok)
        self.assertEqual(result.mode, "dry_run")
        self.assertEqual(result.actions_applied, [])

    def test_run_with_no_client_is_dry_run(self):
        m = _migrator()
        result = m.run()
        self.assertTrue(result.ok)
        self.assertEqual(result.mode, "dry_run")
        self.assertIsNone(result.error)

    def test_mode_property_no_client(self):
        m = _migrator()
        self.assertEqual(m.mode, "dry_run")


# ---------------------------------------------------------------------------
# Fake client mode
# ---------------------------------------------------------------------------

class TestMigratorFakeClient(unittest.TestCase):
    def test_empty_client_run_applies_11_actions(self):
        client = _fake_client()
        m = _migrator(client=client)
        result = m.run()
        self.assertTrue(result.ok)
        self.assertEqual(result.mode, "fake")
        self.assertEqual(len(result.actions_applied), 11)

    def test_all_actions_are_creates_on_empty_client(self):
        client = _fake_client()
        m = _migrator(client=client)
        result = m.run()
        for action in result.actions_applied:
            self.assertEqual(action.action, "create")

    def test_sheet1_in_fake_produces_rename_action(self):
        client = _fake_client()
        client.add_worksheet(title="Sheet1")
        m = _migrator(client=client)
        result = m.run()
        self.assertTrue(result.ok)
        renames = [a for a in result.actions_applied if a.action == "rename"]
        self.assertEqual(len(renames), 1)
        self.assertEqual(renames[0].canonical_name, "daily_sessions")

    def test_fake_run_creates_canonical_worksheets(self):
        from modules.google_sheets_global_schema.validator import CANONICAL_TABS
        client = _fake_client()
        m = _migrator(client=client)
        m.run()
        created = set(client.worksheets_created)
        self.assertTrue(CANONICAL_TABS.issubset(created))

    def test_no_migration_needed_returns_empty_applied(self):
        from modules.google_sheets_global_schema.validator import CANONICAL_TABS
        client = _fake_client()
        for tab in CANONICAL_TABS:
            client.add_worksheet(title=tab)
        m = _migrator(client=client)
        result = m.run()
        self.assertTrue(result.ok)
        self.assertEqual(result.actions_applied, [])

    def test_audit_from_fake_client(self):
        client = _fake_client()
        client.add_worksheet(title="Sheet1")
        client.add_worksheet(title="daily_sessions")
        m = _migrator(client=client)
        titles = m.audit()
        self.assertIn("Sheet1", titles)
        self.assertIn("daily_sessions", titles)

    def test_mode_property_fake(self):
        client = _fake_client()
        m = _migrator(client=client)
        self.assertEqual(m.mode, "fake")


# ---------------------------------------------------------------------------
# Real client blocked
# ---------------------------------------------------------------------------

class _MockRealClient:
    """Minimal mock that must never be called for writes unless flag is set."""
    def __init__(self, titles: list[str] | None = None):
        self._titles = titles or []

    def worksheets(self):
        class _WS:
            def __init__(self, title):
                self.title = title
        return [_WS(t) for t in self._titles]

    def worksheet(self, title):
        raise AssertionError("Real worksheet() called unexpectedly")

    def add_worksheet(self, title, rows=100, cols=20):
        raise AssertionError("Real add_worksheet() called unexpectedly")


class TestRealClientBlocked(unittest.TestCase):
    def setUp(self):
        os.environ.pop("ALLOW_GOOGLE_SHEETS_API_WRITE", None)

    def tearDown(self):
        os.environ.pop("ALLOW_GOOGLE_SHEETS_API_WRITE", None)

    def test_real_client_blocked_without_flag(self):
        m = _migrator(client=_MockRealClient(), spreadsheet_id="dummy_id", dry_run=False)
        plan = m.plan([])
        result = m.apply(plan)
        self.assertFalse(result.ok)
        self.assertIn("ALLOW_GOOGLE_SHEETS_API_WRITE", result.error or "")

    def test_real_client_blocked_without_spreadsheet_id(self):
        os.environ["ALLOW_GOOGLE_SHEETS_API_WRITE"] = "1"
        m = _migrator(client=_MockRealClient(), spreadsheet_id=None, dry_run=False)
        plan = m.plan([])
        result = m.apply(plan)
        self.assertFalse(result.ok)
        self.assertIn("spreadsheet_id", result.error or "")

    def test_dry_run_true_suppresses_real_write_even_with_flag(self):
        os.environ["ALLOW_GOOGLE_SHEETS_API_WRITE"] = "1"
        m = _migrator(client=_MockRealClient(), spreadsheet_id="dummy_id", dry_run=True)
        plan = m.plan(["Sheet1"])
        result = m.apply(plan)
        self.assertTrue(result.ok)
        self.assertEqual(result.mode, "dry_run")
        self.assertEqual(result.actions_applied, [])

    def test_audit_from_real_client_mock(self):
        m = _migrator(client=_MockRealClient(["Sheet1", "daily_sessions"]), dry_run=True)
        titles = m.audit()
        self.assertIn("Sheet1", titles)
        self.assertIn("daily_sessions", titles)


# ---------------------------------------------------------------------------
# No Google API calls
# ---------------------------------------------------------------------------

class TestNoGoogleApiCalls(unittest.TestCase):
    def test_import_no_google(self):
        before = _google_mods()
        from modules.google_sheets_global_schema import worksheet_migrator  # noqa: F401
        after = _google_mods()
        self.assertEqual(after - before, set(), f"Google modules loaded: {after - before}")

    def test_run_fake_no_google(self):
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.worksheet_migrator import WorksheetMigrator
        before = _google_mods()
        client = FakeSheetsClient()
        WorksheetMigrator(client=client).run()
        after = _google_mods()
        self.assertEqual(after - before, set(), f"Google modules appeared: {after - before}")
