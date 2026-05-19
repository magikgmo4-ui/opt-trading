---
doc_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01_INBOX
repo: opt-trading
go_id: GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01
status: open
surface: index_inbox
updated_at: 2026-05-06
topic_keys:
  - botpress
  - openclaw
  - adapter
  - spec
links:
  - docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01/01_ADAPTER_CONTRACT.md
---

# INBOX — GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01

## Objet

Entree courte d indexation pour la specification de l adapter Botpress ↔ OpenClaw.

## Spec

- Contrat API: POST `/api/v1/botpress/intent`
- 5 intents liste blanche: screener, analysis, journal, status, help
- Safety gate: blocage permanent execute_trade, git_push, modify_production
- Error handling: timeout 30s, 1 retry, circuit breaker 3 fails/60s
- Journalisation: Airtable `Botpress_Logs` ou journal local

## Branche

`go/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01`

## Prochain GO

`GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01`
