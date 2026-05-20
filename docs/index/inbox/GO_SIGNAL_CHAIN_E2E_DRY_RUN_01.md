---
doc_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_SIGNAL_CHAIN_E2E_DRY_RUN_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - e2e
  - dry_run
  - signal_chain
  - desk_pro
  - telegram
  - sheets
links:
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/10_CURRENT_SURFACES.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/20_E2E_STEPS.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/30_OUTPUT_SCHEMA.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/90_REPRISE_POINT.md
---

# INBOX - GO_SIGNAL_CHAIN_E2E_DRY_RUN_01

## Objet

Prouver la chaîne E2E en mode dry-run, de bout en bout, sans trade live:

- signal → decision → gating → paper execution → tracking → journal
- Desk Pro consumer (synthesis inputs)
- Telegram outbound (preview) + telemetry
- Google Sheets sync (dry-run)
