---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01_EXISTING_SURFACE_READ
doc_type: existing_surface_read
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 10_EXISTING_SURFACE_READ — Surfaces existantes

## Surface opérationnelle existante

### `scripts/sheets/sync_daily_session.py`

Writer contrôlé existant pour `daily_sessions` (worksheet "sheet1" today).

Patron établi :
- `--controlled-write` flag requis pour écriture réelle
- ADC via `gcloud auth application-default login`
- `GOOGLE_SHEETS_SYNC_SHEET_ID` env var
- Dry-run par défaut
- gspread + google.auth comme seules dépendances Google

**Ce GO n'est pas en conflit avec ce script.** Le `SheetsWriter` nouveau coexiste et fournit une interface plus générique couvrant les 11 tabs.

## Fixtures validées (parent #809)

```text
tests/fixtures/google_sheets_global_schema/
  sheets_registry.jsonl       # 11 rows — toutes les tabs
  daily_sessions.jsonl        # 3 rows — success, warn, fail
  strategy_events.jsonl       # 3 rows — signal_event.v1 + market_context
  strategy_perf.jsonl         # 3 rows — composite PK 4-col
  strategy_gates.jsonl        # 3 rows — promote, hold
  registry_candidates.jsonl   # 2 rows — composite PK 3-col
  market_metrics.jsonl        # 3 rows — BTCUSDT + ETHUSDT
  desk_snapshots.jsonl        # 2 rows — path_ref uniquement
  visual_context.jsonl        # 2 rows — path_ref uniquement
  telegram_claims.jsonl       # 2 rows — fixtures locales
  watchlists.jsonl            # 3 rows — enabled + disabled
```

Validateur R1-R10 : 41 tests PASS, 0 FAIL.

## Schéma de validation (#809)

Le fichier `tests/test_google_sheets_fixtures.py` contient le validateur inline (fixtures-first). Ce GO extrait la logique dans `modules/google_sheets_global_schema/validator.py` pour réutilisation par le writer.

## Dépendances Google optionnelles

| Package | Requis pour | Status |
|---|---|---|
| `gspread` | Vrai client Google | Optionnel (non installé par défaut) |
| `google.auth` | ADC | Optionnel |
| `google-auth-oauthlib` | OAuth | Optionnel |

Le writer et le fake client s'importent sans ces packages.
