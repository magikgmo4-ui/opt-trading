---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_PROOF_MATRIX_AND_CONSTRAINTS
doc_type: matrix
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 30_PROOF_MATRIX_AND_CONSTRAINTS

## Invariants

- pas d’écriture Sheets automatique (toute écriture est explicitement demandée)
- dry-run par défaut
- aucun secret dans le repo
- pas de write si ADC / sheet_id absent (status BLOCKED)

## Preuves existantes (repo)

| Preuve | Source | Critère |
| --- | --- | --- |
| Daily session sync dry-run | `scripts/sheets/sync_daily_session.py` | imprime preview et log `sync_log.jsonl` |
| Tests sync daily session | `tests/e2e/test_sync_daily_session.py` | pas de write sans `--controlled-write` |
| Scheduler integration | `scripts/schedule/daily_session.sh` | controlled-write flag explicite |

## Preuves requises avant extension (tabs 2-5)

| Preuve | Description | Critère |
| --- | --- | --- |
| Writer transverse dry-run | écrit “row intents” sans API | aucun POST |
| Mapping stable | colonnes figées et versionnées | `schema version: 1` |
| Audit log | log JSONL de chaque tentative | lisible via LocalCMS |

## Ancrage umbrella

- `MASTER_TARGET` : fiabiliser Sheets comme consumer transverse du produit final total
- `Kanban bundle` : reste la carte de navigation principale
- `Prochain item Kanban exact` : `GO_TELEGRAM_LATENCY_BACKTEST_01`
- `Gaps encore ouverts` : audit transverse absent, writer unique absent, controlled-write encore borne au daily session sync
