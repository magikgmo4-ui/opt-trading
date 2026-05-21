---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_EXTERNAL_APPS_CANARY_PLAN
doc_type: canary_plan
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: draft
---

# 30_EXTERNAL_APPS_WRITE_GATED_CANARY_PLAN

## Scope

Apps externes autorisees sous contrat:

- Airtable
- ClickUp
- Botpress
- Google Sheets
- Telegram non-trading
- Gmail / Calendar / Drive
- KG Repo via PR-gated sync

## Conditions minimales avant write

1. Snapshot before write si applicable.
2. Proposal packet cree.
3. Approval packet valide.
4. Write execute sur surface test / canary.
5. Readback verification.
6. Rollback / compensation documente.

## Surfaces explicitement exclues

- Toute execution signal/trading.
- Toute emission ordre exchange.
- Toute source externe promue source de verite.
