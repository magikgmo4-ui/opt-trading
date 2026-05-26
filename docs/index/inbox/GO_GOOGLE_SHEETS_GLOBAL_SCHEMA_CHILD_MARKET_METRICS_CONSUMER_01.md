---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01_INDEX
doc_type: inbox_index
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01
parent_go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
pf_id: PF_GOOGLE_SHEETS_CONSUMER
status: open
lifecycle_stage: implementation
source_kind: canonical
created_at: 2026-05-25
updated_at: 2026-05-25
---

# GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01

**Objectif :** Premier consumer Data Center → Google Sheets pour le tab `market_metrics`.

**Surface :** `modules/google_sheets_global_schema/market_metrics_consumer.py`

**Parent :** GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01

**Upstream :** PF_DATA_CENTER

## Livrables

| Fichier | Rôle |
|---|---|
| `modules/google_sheets_global_schema/market_metrics_consumer.py` | Consumer + mapper market_metrics.v1 → Sheets rows |
| `tests/test_google_sheets_market_metrics_consumer.py` | 21 tests (mapping, validation, fake, no-op, dry-run, isolation API) |

## Résultat

21 tests PASS. 103 tests PASS sur la suite complète google_sheets. Source absente = no-op contrôlé. Isolation Google API prouvée.

## Chantier docs

`docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01/`
