---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 70_NEXT_GO_DECISION - Next GO Decision

## Recommandation immediate

```
GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01
```

## Motif

- les contrats sont deja valides
- l'adapter existe deja
- le risque principal n'est plus contractuel mais operationnel
- il faut d'abord prouver un runner automatique dry-run avant de specifier un timer actif

## Alternatives

### `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PLAYWRIGHT_SETUP_01`

Utile si la priorite devient la capture native headless plutot que l'automatisation Desk Pro.

### `GO_OPT_TRADING_ADMIN_TRADING_LIVE_RUNTIME_SMOKE_GATED_01`

Utile apres le dry-run, pas avant. Aller en live smoke maintenant court-circuiterait les gates d'automatisation.

## Decision recommandee

1. Dry-run Desk Pro
2. Timer spec
3. Timer impl
4. Observability
5. Live runtime smoke gate

## RISKS

- À qualifier.
