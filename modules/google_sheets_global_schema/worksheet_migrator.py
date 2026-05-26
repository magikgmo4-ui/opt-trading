"""
Worksheet title migrator — aligns Google Sheets worksheet titles to canonical tab names.

Use case: a real spreadsheet may have "Sheet1" (default locale title) instead of
"daily_sessions". This migrator audits, plans, and optionally applies renames/creates
so every canonical tab exists with the correct title.

Modes:
  fake     — FakeSheetsClient (in-memory, always allowed)
  dry_run  — audit + plan but no writes (default)
  applied  — renames + creates applied (requires ALLOW_GOOGLE_SHEETS_API_WRITE=1
              + spreadsheet_id + credentials)

Real gspread interface expected on client (when not FakeSheetsClient):
  client.worksheets()           -> list of objects with .title attribute
  client.worksheet(title)       -> worksheet object
  worksheet.update_title(title) -> rename
  client.add_worksheet(title, rows, cols) -> create
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Literal

from .fake_sheets_client import FakeSheetsClient
from .validator import CANONICAL_TABS

REAL_API_FLAG = "ALLOW_GOOGLE_SHEETS_API_WRITE"

# Legacy worksheet title -> canonical tab name.
# Only add entries that are well-known default titles produced by Google Sheets
# or by old scripts that pre-date the canonical schema.
LEGACY_TITLE_MAP: dict[str, str] = {
    "Sheet1": "daily_sessions",
    "sheet1": "daily_sessions",
    "Feuille 1": "daily_sessions",   # French locale
    "Feuille1": "daily_sessions",    # French locale (no space variant)
    "Hoja 1": "daily_sessions",      # Spanish locale
    "Tabelle1": "daily_sessions",    # German locale
}


@dataclass
class MigrationAction:
    action: Literal["ok", "rename", "create"]
    canonical_name: str
    current_title: str | None = None  # set only for "rename"

    def __str__(self) -> str:
        if self.action == "ok":
            return f"ok: '{self.canonical_name}'"
        if self.action == "rename":
            return f"rename: '{self.current_title}' -> '{self.canonical_name}'"
        return f"create: '{self.canonical_name}'"


@dataclass
class MigrationPlan:
    actions: list[MigrationAction] = field(default_factory=list)

    @property
    def renames(self) -> int:
        return sum(1 for a in self.actions if a.action == "rename")

    @property
    def creates(self) -> int:
        return sum(1 for a in self.actions if a.action == "create")

    @property
    def already_ok(self) -> int:
        return sum(1 for a in self.actions if a.action == "ok")

    @property
    def needs_migration(self) -> bool:
        return self.renames > 0 or self.creates > 0


@dataclass
class MigrationResult:
    ok: bool
    mode: str  # "fake" | "dry_run" | "applied"
    plan: MigrationPlan
    actions_applied: list[MigrationAction] = field(default_factory=list)
    error: str | None = None


class WorksheetMigrator:
    """
    Audits and aligns worksheet titles in a Google Sheets spreadsheet.

    Parameters
    ----------
    client : FakeSheetsClient or gspread.Spreadsheet, optional
        FakeSheetsClient -> in-memory mode (always allowed).
        None -> dry_run only (no client available).
        Real gspread Spreadsheet -> controlled apply (requires flag + spreadsheet_id).
    spreadsheet_id : str, optional
        Required for real controlled migrations (not used in fake/dry-run).
    dry_run : bool
        If True and client is real, audit + plan but don't apply (default True).
    """

    def __init__(
        self,
        client: Any = None,
        spreadsheet_id: str | None = None,
        dry_run: bool = True,
    ) -> None:
        self._client = client
        self._spreadsheet_id = spreadsheet_id
        self._dry_run = dry_run

    @property
    def _is_fake(self) -> bool:
        return isinstance(self._client, FakeSheetsClient)

    @property
    def _real_write_allowed(self) -> bool:
        return os.environ.get(REAL_API_FLAG) == "1"

    @property
    def mode(self) -> str:
        if self._is_fake:
            return "fake"
        if self._dry_run or not self._real_write_allowed:
            return "dry_run"
        return "applied"

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def audit(self) -> list[str]:
        """Return current worksheet titles from the client.

        Returns [] when client is None (dry-run baseline).
        """
        if self._client is None:
            return []
        if self._is_fake:
            return list(self._client.worksheets_created)
        return [ws.title for ws in self._client.worksheets()]

    def plan(self, existing_titles: list[str]) -> MigrationPlan:
        """Compute which canonical tabs need rename, create, or are already correct.

        Logic per canonical tab (sorted order):
          - already present as-is -> "ok"
          - a LEGACY_TITLE_MAP entry for this canonical exists in existing_titles -> "rename"
          - otherwise -> "create"

        Extra worksheets (not in CANONICAL_TABS) are ignored — never deleted.
        Each legacy title is consumed at most once (first matching canonical wins).
        """
        existing_set = set(existing_titles)
        claimed_legacy: set[str] = set()
        actions: list[MigrationAction] = []

        for canonical in sorted(CANONICAL_TABS):
            if canonical in existing_set:
                actions.append(MigrationAction("ok", canonical))
                continue

            renamed = False
            for legacy, target in LEGACY_TITLE_MAP.items():
                if target == canonical and legacy in existing_set and legacy not in claimed_legacy:
                    actions.append(MigrationAction("rename", canonical, current_title=legacy))
                    claimed_legacy.add(legacy)
                    renamed = True
                    break

            if not renamed:
                actions.append(MigrationAction("create", canonical))

        return MigrationPlan(actions=actions)

    def apply(self, migration_plan: MigrationPlan) -> MigrationResult:
        """Apply the migration plan (renames + creates).

        No-op (ok=True) if plan.needs_migration is False.
        Returns dry_run result when real write is not enabled.
        """
        if not migration_plan.needs_migration:
            return MigrationResult(
                ok=True,
                mode=self.mode,
                plan=migration_plan,
                actions_applied=[],
            )

        if self._is_fake:
            return self._apply_to_fake(migration_plan)

        if self._dry_run:
            return MigrationResult(
                ok=True,
                mode="dry_run",
                plan=migration_plan,
                actions_applied=[],
            )

        if not self._real_write_allowed:
            return MigrationResult(
                ok=False,
                mode="dry_run",
                plan=migration_plan,
                error=f"Migration blocked — set {REAL_API_FLAG}=1 to enable",
            )
        if not self._spreadsheet_id:
            return MigrationResult(
                ok=False,
                mode="dry_run",
                plan=migration_plan,
                error="Migration blocked — spreadsheet_id required",
            )

        return self._apply_to_real(migration_plan)

    def run(self) -> MigrationResult:
        """Shortcut: audit() -> plan() -> apply() in one call."""
        existing = self.audit()
        migration_plan = self.plan(existing)
        return self.apply(migration_plan)

    # ------------------------------------------------------------------
    # Internal apply helpers
    # ------------------------------------------------------------------

    def _apply_to_fake(self, migration_plan: MigrationPlan) -> MigrationResult:
        applied: list[MigrationAction] = []
        try:
            for action in migration_plan.actions:
                if action.action == "ok":
                    continue
                # For fake client: create the canonical worksheet (simulates both rename
                # and create — no literal rename in in-memory store, which is fine for tests).
                canonical = action.canonical_name
                try:
                    self._client.worksheet(canonical)
                except KeyError:
                    self._client.add_worksheet(title=canonical)
                applied.append(action)
        except Exception as exc:
            return MigrationResult(
                ok=False, mode="fake", plan=migration_plan,
                actions_applied=applied, error=str(exc),
            )
        return MigrationResult(ok=True, mode="fake", plan=migration_plan, actions_applied=applied)

    def _apply_to_real(self, migration_plan: MigrationPlan) -> MigrationResult:
        applied: list[MigrationAction] = []
        try:
            for action in migration_plan.actions:
                if action.action == "ok":
                    continue
                if action.action == "rename":
                    ws = self._client.worksheet(action.current_title)
                    ws.update_title(action.canonical_name)
                    applied.append(action)
                elif action.action == "create":
                    self._client.add_worksheet(
                        title=action.canonical_name, rows=1000, cols=26
                    )
                    applied.append(action)
        except Exception as exc:
            return MigrationResult(
                ok=False, mode="applied", plan=migration_plan,
                actions_applied=applied, error=str(exc),
            )
        return MigrationResult(
            ok=True, mode="applied", plan=migration_plan, actions_applied=applied,
        )
