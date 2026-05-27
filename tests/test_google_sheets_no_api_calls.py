"""
Isolation tests: prove no Google API calls are made by default.

- Importing the module must not load google.* or gspread.
- Using FakeSheetsClient must not touch the network.
- Writing all 11 tabs via fake writer must not call any Google API.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures" / "google_sheets_global_schema"
GOOGLE_MODULES = frozenset({"google", "gspread", "googleapiclient", "google.auth", "google.oauth2"})


def _google_mods_loaded() -> set[str]:
    return {m for m in sys.modules if any(m == g or m.startswith(g + ".") for g in GOOGLE_MODULES)}


def _load_fixture(tab: str) -> list[dict]:
    rows = []
    for line in (FIXTURES / f"{tab}.jsonl").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


class TestNoGoogleModulesLoaded(unittest.TestCase):
    def test_import_validator_no_google(self):
        before = _google_mods_loaded()
        from modules.google_sheets_global_schema import validator  # noqa: F401
        after = _google_mods_loaded()
        self.assertEqual(after - before, set(), f"New Google modules loaded: {after - before}")

    def test_import_fake_client_no_google(self):
        before = _google_mods_loaded()
        from modules.google_sheets_global_schema import fake_sheets_client  # noqa: F401
        after = _google_mods_loaded()
        self.assertEqual(after - before, set())

    def test_import_sheets_writer_no_google(self):
        before = _google_mods_loaded()
        from modules.google_sheets_global_schema import sheets_writer  # noqa: F401
        after = _google_mods_loaded()
        self.assertEqual(after - before, set())


class TestFakeClientNoNetwork(unittest.TestCase):
    def test_write_all_tabs_no_google_api(self):
        from modules.google_sheets_global_schema.fake_sheets_client import FakeSheetsClient
        from modules.google_sheets_global_schema.sheets_writer import SheetsWriter
        from modules.google_sheets_global_schema.validator import CANONICAL_TABS

        before = _google_mods_loaded()
        client = FakeSheetsClient()
        writer = SheetsWriter(client=client)

        for tab in sorted(CANONICAL_TABS):
            rows = _load_fixture(tab)
            result = writer.append_rows(tab, rows)
            self.assertTrue(result.ok, f"{tab}: {result.error}")
            self.assertEqual(result.rows_written, len(rows))

        after = _google_mods_loaded()
        self.assertEqual(after - before, set(), f"Google modules appeared: {after - before}")

    def test_validator_no_google_api(self):
        from modules.google_sheets_global_schema.validator import CANONICAL_TABS, validate_rows

        before = _google_mods_loaded()
        for tab in sorted(CANONICAL_TABS):
            rows = _load_fixture(tab)
            issues = validate_rows(tab, rows)
            fails = [i for i in issues if i[0] == "FAIL"]
            self.assertEqual(fails, [], f"{tab}: {fails}")
        after = _google_mods_loaded()
        self.assertEqual(after - before, set())
