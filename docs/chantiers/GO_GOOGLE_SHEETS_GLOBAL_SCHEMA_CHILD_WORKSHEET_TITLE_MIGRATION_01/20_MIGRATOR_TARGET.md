---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01_MIGRATOR_TARGET
doc_type: target_design
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_WORKSHEET_TITLE_MIGRATION_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 20_MIGRATOR_TARGET — Design WorksheetMigrator V1

## Composants livrés

### `modules/google_sheets_global_schema/worksheet_migrator.py`

```python
LEGACY_TITLE_MAP: dict[str, str]   # legacy → canonical (Sheet1 → daily_sessions, etc.)

@dataclass
class MigrationAction:
    action: Literal["ok", "rename", "create"]
    canonical_name: str
    current_title: str | None  # set for "rename" only

@dataclass
class MigrationPlan:
    actions: list[MigrationAction]
    @property renames: int
    @property creates: int
    @property already_ok: int
    @property needs_migration: bool

@dataclass
class MigrationResult:
    ok: bool
    mode: str    # "fake" | "dry_run" | "applied"
    plan: MigrationPlan
    actions_applied: list[MigrationAction]
    error: str | None

class WorksheetMigrator:
    def __init__(self, client=None, spreadsheet_id=None, dry_run=True)
    def audit(self) -> list[str]              # current worksheet titles
    def plan(self, existing_titles) -> MigrationPlan
    def apply(self, plan) -> MigrationResult
    def run(self) -> MigrationResult          # audit + plan + apply
```

## Logique de plan

```
Pour chaque canonical_name (sorted) :
  if canonical_name in existing -> action="ok"
  elif LEGACY_TITLE_MAP[legacy] == canonical and legacy in existing (non-consommé) -> action="rename"
  else -> action="create"

Extra worksheets (hors CANONICAL_TABS) : ignorés (pas de delete)
Chaque legacy title consommé au plus une fois (premier canonique matching gagne)
```

## Logique d'apply

```
needs_migration = False -> return ok=True (rien à faire)
_is_fake -> _apply_to_fake() (in-memory, toujours autorisé)
_dry_run=True -> return ok=True, mode="dry_run", actions_applied=[]
ALLOW_GOOGLE_SHEETS_API_WRITE != "1" -> return ok=False, error="blocked"
spreadsheet_id manquant -> return ok=False, error="spreadsheet_id required"
_apply_to_real() : ws.update_title() pour renames, add_worksheet() pour creates
```

## Comportement FakeSheetsClient

Le fake client simule `rename` via `add_worksheet(canonical_name)` — l'ancien titre ("Sheet1") reste dans le fake store mais les tests vérifient le résultat de `actions_applied` et la présence du canonical name, pas l'absence du legacy.

## Contrat de sécurité

- Dry-run par défaut (`dry_run=True`)
- Aucune suppression de worksheets non canoniques
- Flag + spreadsheet_id requis simultanément pour apply réel
- Import sans `google.*` ni `gspread`
