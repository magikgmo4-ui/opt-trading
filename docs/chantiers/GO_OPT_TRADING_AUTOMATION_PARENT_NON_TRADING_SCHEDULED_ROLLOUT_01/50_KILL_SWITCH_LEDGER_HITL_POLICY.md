---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_KILL_SWITCH_LEDGER_HITL_POLICY
doc_type: policy
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: draft
---

# 50_KILL_SWITCH_LEDGER_HITL_POLICY

## Policy

- Tout job observable doit journaliser dans le ledger.
- Tout write non-local doit etre bloque par defaut.
- Tout write externe exige proposal + approval + verification.
- Le kill switch doit pouvoir stopper tout bouton dangereux cockpit.
- Tout stuck job doit aller en dead-letter ou rollback.

## Non-trading guard

Le perimetre de ce parent exclut toute surface signal/trading, meme en dry-run.
