---
doc_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01_INTEGRATION_ARCHITECTURE
doc_type: architecture
repo: opt-trading
project: opt-trading
module: orchestration
go_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
status: ready
lifecycle_stage: architecture
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
---

# 02_INTEGRATION_ARCHITECTURE

## Architecture cible

[TradingView / Telegram / Bot Vision]
            ↓
    Python opt-trading (core)
            ↓
    Airtable (UI + review + journal)
            ↓
    Export (CSV / JSON / Google Sheets)
            ↓
    DB (Timescale / ClickHouse)

## Rôle Airtable

- Visualisation
- Validation humaine
- Annotation
- Workflow léger

## Flux recommandé

1. Capture → Bot Vision → Python
2. Python → push Airtable (record)
3. Airtable → humain valide / enrichit
4. Export → DB / reporting

## Anti-patterns

- Push tick data
- Boucles API fréquentes
- Dépendance critique

## Sécurité

- API key via `.env`
- Jamais en repo


## RISKS

- À qualifier.
