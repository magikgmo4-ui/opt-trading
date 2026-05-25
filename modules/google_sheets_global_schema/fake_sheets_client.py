"""
Fake Google Sheets client for testing.

Stores writes in memory. No network calls, no credentials, no API.
Interface mirrors the subset of gspread used by SheetsWriter.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WriteRecord:
    sheet_name: str
    operation: str  # "append_rows" | "clear_and_write" | "update"
    rows: list[list[Any]]


class FakeSheetsWorksheet:
    def __init__(self, title: str, client: "FakeSheetsClient") -> None:
        self.title = title
        self._client = client
        self._data: list[list[Any]] = []

    def append_rows(self, values: list[list[Any]], **kwargs) -> None:
        self._data.extend(values)
        self._client._records.append(WriteRecord(self.title, "append_rows", list(values)))

    def clear(self) -> None:
        self._data.clear()

    def update(self, values: list[list[Any]], **kwargs) -> None:
        self._data = list(values)
        self._client._records.append(WriteRecord(self.title, "update", list(values)))

    def get_all_records(self) -> list[dict]:
        if not self._data:
            return []
        headers = self._data[0]
        return [dict(zip(headers, row)) for row in self._data[1:]]

    def get_all_values(self) -> list[list[Any]]:
        return list(self._data)

    @property
    def row_count(self) -> int:
        return len(self._data)


class FakeSheetsClient:
    """
    In-memory fake for gspread-style client.

    Usage:
        client = FakeSheetsClient()
        ws = client.worksheet("daily_sessions")  # raises if not created
        ws = client.add_worksheet("daily_sessions", rows=100, cols=20)
    """

    def __init__(self) -> None:
        self._worksheets: dict[str, FakeSheetsWorksheet] = {}
        self._records: list[WriteRecord] = []

    def worksheet(self, title: str) -> FakeSheetsWorksheet:
        if title not in self._worksheets:
            raise KeyError(f"Worksheet '{title}' not found — call add_worksheet first")
        return self._worksheets[title]

    def add_worksheet(self, *, title: str, rows: int = 100, cols: int = 20) -> FakeSheetsWorksheet:
        if title not in self._worksheets:
            self._worksheets[title] = FakeSheetsWorksheet(title, self)
        return self._worksheets[title]

    @property
    def worksheets_created(self) -> list[str]:
        return list(self._worksheets.keys())

    @property
    def write_records(self) -> list[WriteRecord]:
        return list(self._records)

    def total_rows_written(self, sheet_name: str) -> int:
        return sum(len(r.rows) for r in self._records if r.sheet_name == sheet_name)

    def reset(self) -> None:
        self._worksheets.clear()
        self._records.clear()
