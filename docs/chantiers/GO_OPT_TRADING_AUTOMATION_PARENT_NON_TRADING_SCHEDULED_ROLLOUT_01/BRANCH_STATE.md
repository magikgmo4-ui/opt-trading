---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_BRANCH_STATE
doc_type: branch_state
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: active
---

# BRANCH_STATE

## Current state

- `#676` a ete mergee.
- Le parent non-trading est maintenant ouvert et canonique.

## Decision

- La prochaine etape n'est pas une PR runtime.
- La prochaine etape est de completer le register canonique des jobs hors trading.

## Next actions

1. Completer `10_NON_TRADING_JOBS_REGISTER.md`.
2. Valider la priorisation Phase 01/02/03.
3. Deriver ensuite les travaux d'implementation necessaires.
