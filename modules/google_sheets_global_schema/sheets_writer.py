"""
Google Sheets writer adapter — controlled write layer for the global schema V1.

Safety contract:
- Dry-run by default (no write unless explicitly activated).
- Real Google API write requires env ALLOW_GOOGLE_SHEETS_API_WRITE=1 + spreadsheet_id + credentials.
- Validation rules R1-R10 applied before any write attempt.
- No secrets in logs. No credentials in code.
- FakeSheetsClient is always safe (in-memory, no network).

Write modes:
  fake            — FakeSheetsClient (testing, always allowed)
  dry_run         — real client present but write suppressed (default)
  controlled_write — real client + flag + spreadsheet_id (explicit activation)
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from .validator import CANONICAL_TABS, validate_rows, fails as get_fails
from .fake_sheets_client import FakeSheetsClient

REAL_API_FLAG = "ALLOW_GOOGLE_SHEETS_API_WRITE"


@dataclass
class WriteResult:
    ok: bool
    sheet_name: str
    rows_attempted: int
    rows_written: int
    mode: str  # "fake" | "dry_run" | "controlled_write"
    validation_fails: list[str] = field(default_factory=list)
    error: str | None = None


class SheetsWriterError(Exception):
    pass


class SheetsWriter:
    """
    Controlled writer for Google Sheets global schema tabs.

    Parameters
    ----------
    client : FakeSheetsClient or gspread.Spreadsheet, optional
        If FakeSheetsClient → mode="fake" (always allowed).
        If None → dry_run only.
        If real gspread client → controlled_write requires ALLOW_GOOGLE_SHEETS_API_WRITE=1.
    spreadsheet_id : str, optional
        Required for real controlled writes. Not used in fake/dry-run.
    dry_run : bool
        If True and client is real, suppress writes (default True).
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

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

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
        return "controlled_write"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _validate(self, sheet_name: str, rows: list[dict]) -> list[str]:
        issues = validate_rows(sheet_name, rows)
        return get_fails(issues)

    def _get_or_create_worksheet(self, sheet_name: str) -> Any:
        if self._is_fake:
            client: FakeSheetsClient = self._client  # type: ignore[assignment]
            try:
                return client.worksheet(sheet_name)
            except KeyError:
                return client.add_worksheet(title=sheet_name)
        # Real client: delegate to gspread interface
        try:
            return self._client.worksheet(sheet_name)
        except Exception:
            return self._client.add_worksheet(title=sheet_name, rows=1000, cols=26)

    def _rows_to_values(self, rows: list[dict]) -> list[list[Any]]:
        """Convert list of dicts to list of value lists (no header row — writer manages headers separately)."""
        return [[str(v) if v is not None else "" for v in row.values()] for row in rows]

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def ensure_worksheet(self, sheet_name: str) -> dict:
        """
        Ensure the worksheet exists. Returns {"sheet_name": ..., "created": bool, "mode": ...}.
        """
        if sheet_name not in CANONICAL_TABS:
            raise SheetsWriterError(f"Unknown sheet '{sheet_name}' — not in CANONICAL_TABS")
        if self._client is None:
            return {"sheet_name": sheet_name, "created": False, "mode": "no_client"}
        ws = self._get_or_create_worksheet(sheet_name)
        return {"sheet_name": sheet_name, "created": True, "mode": self.mode, "title": getattr(ws, "title", sheet_name)}

    def append_rows(
        self,
        sheet_name: str,
        rows: list[dict],
        *,
        validate: bool = True,
    ) -> WriteResult:
        """Append rows to the worksheet. Validates before write."""
        return self._write(sheet_name, rows, operation="append", validate=validate)

    def write_rows(
        self,
        sheet_name: str,
        rows: list[dict],
        *,
        validate: bool = True,
    ) -> WriteResult:
        """Alias for append_rows (rows are appended, not replacing)."""
        return self.append_rows(sheet_name, rows, validate=validate)

    def clear_and_write(
        self,
        sheet_name: str,
        rows: list[dict],
        *,
        validate: bool = True,
    ) -> WriteResult:
        """Clear worksheet then write all rows. Validates before write."""
        return self._write(sheet_name, rows, operation="clear_and_write", validate=validate)

    # ------------------------------------------------------------------
    # Core write logic
    # ------------------------------------------------------------------

    def _write(
        self,
        sheet_name: str,
        rows: list[dict],
        operation: str,
        validate: bool,
    ) -> WriteResult:
        if sheet_name not in CANONICAL_TABS:
            return WriteResult(
                ok=False,
                sheet_name=sheet_name,
                rows_attempted=len(rows),
                rows_written=0,
                mode=self.mode,
                error=f"Unknown sheet '{sheet_name}' — not in CANONICAL_TABS",
            )

        validation_fails: list[str] = []
        if validate:
            validation_fails = self._validate(sheet_name, rows)
            if validation_fails:
                return WriteResult(
                    ok=False,
                    sheet_name=sheet_name,
                    rows_attempted=len(rows),
                    rows_written=0,
                    mode=self.mode,
                    validation_fails=validation_fails,
                    error=f"{len(validation_fails)} validation FAIL(s) before write",
                )

        # Fake client: always allowed, skip all real-API guards
        if self._is_fake:
            pass  # fall through to execute write

        elif self._dry_run:
            # Explicitly requested dry-run (no client or dry_run=True)
            return WriteResult(
                ok=True,
                sheet_name=sheet_name,
                rows_attempted=len(rows),
                rows_written=0,
                mode="dry_run",
            )

        else:
            # Real client with dry_run=False: requires flag + spreadsheet_id
            if not self._real_write_allowed:
                return WriteResult(
                    ok=False,
                    sheet_name=sheet_name,
                    rows_attempted=len(rows),
                    rows_written=0,
                    mode="dry_run",
                    error=f"Real write blocked — set {REAL_API_FLAG}=1 to enable",
                )
            if not self._spreadsheet_id:
                return WriteResult(
                    ok=False,
                    sheet_name=sheet_name,
                    rows_attempted=len(rows),
                    rows_written=0,
                    mode="dry_run",
                    error="Real write blocked — spreadsheet_id required",
                )

        # Execute write
        try:
            ws = self._get_or_create_worksheet(sheet_name)
            values = self._rows_to_values(rows)
            if operation == "clear_and_write":
                ws.clear()
                ws.update(values)
            else:
                ws.append_rows(values)
            return WriteResult(
                ok=True,
                sheet_name=sheet_name,
                rows_attempted=len(rows),
                rows_written=len(rows),
                mode=self.mode,
            )
        except Exception as exc:
            return WriteResult(
                ok=False,
                sheet_name=sheet_name,
                rows_attempted=len(rows),
                rows_written=0,
                mode=self.mode,
                error=str(exc),
            )
