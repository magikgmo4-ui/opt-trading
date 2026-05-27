---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01_API_WRITE_TARGET
doc_type: target_design
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 20_API_WRITE_TARGET — Design write adapter V1

## Composants livrés

### `modules/google_sheets_global_schema/validator.py`

Extraction du validateur R1-R10 de `tests/test_google_sheets_fixtures.py` (PR #809) en module partagé.

```python
CANONICAL_TABS: frozenset[str]  # 11 tabs
SCHEMA: dict[str, dict]         # required, enums, timestamps, pk, ref_cols par tab

def validate_rows(tab_name: str, rows: list[dict]) -> list[tuple[str, str, str]]:
    """(severity, rule_id, message). Empty list = 0 FAIL."""

def fails(issues: list[tuple]) -> list[str]:
    """Filtre uniquement les messages FAIL."""
```

### `modules/google_sheets_global_schema/fake_sheets_client.py`

Client in-memory mimant l'interface gspread. Aucun réseau, toujours sûr.

```python
@dataclass
class WriteRecord:
    sheet_name: str
    operation: str   # "append_rows" | "clear" | "update"
    rows: list[list[Any]]

class FakeSheetsWorksheet:
    title: str
    def append_rows(self, values, **kwargs): ...
    def clear(self): ...
    def update(self, values, **kwargs): ...
    def get_all_records(self) -> list[dict]: ...
    @property row_count: int

class FakeSheetsClient:
    def worksheet(self, title) -> FakeSheetsWorksheet  # KeyError si absent
    def add_worksheet(self, *, title, rows=100, cols=20) -> FakeSheetsWorksheet
    @property worksheets_created: list[str]
    @property write_records: list[WriteRecord]
    def total_rows_written(self, sheet_name: str) -> int
    def reset(): ...
```

### `modules/google_sheets_global_schema/sheets_writer.py`

```python
REAL_API_FLAG = "ALLOW_GOOGLE_SHEETS_API_WRITE"

@dataclass
class WriteResult:
    ok: bool
    sheet_name: str
    rows_attempted: int
    rows_written: int
    mode: str              # "fake" | "dry_run" | "controlled_write"
    validation_fails: list[str]
    error: str | None

class SheetsWriter:
    def __init__(self, client=None, spreadsheet_id=None, dry_run=True)
    def ensure_worksheet(sheet_name: str) -> dict
    def append_rows(sheet_name, rows, *, validate=True) -> WriteResult
    def write_rows(sheet_name, rows, *, validate=True) -> WriteResult  # alias
    def clear_and_write(sheet_name, rows, *, validate=True) -> WriteResult
```

## Logique de décision write

```
_write(sheet_name, rows, operation, validate)
├── tab non-canonique → WriteResult(ok=False, error="not in CANONICAL_TABS")
├── validate=True → R1-R10 → échec → WriteResult(ok=False, validation_fails=[...])
├── _is_fake → execute write (toujours autorisé)
├── _dry_run=True → WriteResult(ok=True, rows_written=0, mode="dry_run")
├── ALLOW_GOOGLE_SHEETS_API_WRITE != "1" → WriteResult(ok=False, error="Real write blocked")
├── spreadsheet_id manquant → WriteResult(ok=False, error="spreadsheet_id required")
└── execute write → WriteResult(ok=True, rows_written=len(rows), mode="controlled_write")
```

## Contrat de sécurité

- **Dry-run par défaut** (`dry_run=True`) — aucun appel réseau sans action explicite.
- **Flag + spreadsheet_id** requis simultanément pour écriture réelle.
- **Validation R1-R10 avant tout write** — y compris fake.
- **Aucun secret dans les logs** — spreadsheet_id et credentials hors scope code.
- **`ALLOW_GOOGLE_SHEETS_API_WRITE` non défini dans `.env`** — activation manuelle uniquement.

## Isolation Google API

Les trois modules s'importent sans déclencher `google.*` ou `gspread` :

```python
from modules.google_sheets_global_schema import validator         # ok
from modules.google_sheets_global_schema import fake_sheets_client  # ok
from modules.google_sheets_global_schema import sheets_writer        # ok
```

Prouvé par `tests/test_google_sheets_no_api_calls.py` (5 tests).
