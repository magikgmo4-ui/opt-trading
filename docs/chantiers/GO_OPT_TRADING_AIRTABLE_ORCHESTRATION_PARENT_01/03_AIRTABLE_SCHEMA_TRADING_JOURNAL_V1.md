---
doc_id: GO_OPT_TRADING_AIRTABLE_SCHEMA_TRADING_JOURNAL_V1
doc_type: schema
repo: opt-trading
project: opt-trading
module: orchestration
go_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
status: ready
lifecycle_stage: design
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
---

# 03_AIRTABLE_SCHEMA_TRADING_JOURNAL_V1

## Tables

### trades
- id
- date
- symbol
- direction
- entry_price
- exit_price
- rr
- result
- setup_id

### setups
- id
- name
- description
- rules

### signals
- id
- source (bot, manual)
- timestamp
- bias
- screenshot_url

### reviews
- id
- trade_id
- comment
- rating

## Relations

- trades → setups
- trades → signals
- trades → reviews

## Objectif

Journal complet + review + stats simple

