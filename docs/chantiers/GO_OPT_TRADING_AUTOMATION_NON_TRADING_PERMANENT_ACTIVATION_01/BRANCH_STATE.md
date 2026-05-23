# BRANCH_STATE

## Informations

| Champ | Valeur |
|-------|--------|
| Branch | `go/GO_OPT_TRADING_AUTOMATION_NON_TRADING_PERMANENT_ACTIVATION_01` |
| Base | `origin/sot/mainline` (après PR #690 + PR #691) |
| Parent GO | `GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01` |
| Créée | 2026-05-23 |

## État actuel

- Documentation du GO d'activation permanente limitée
- Plan d'activation progressive (3 phases)
- Politique kill switch + ledger
- Plan d'observation J1-J7
- Plan de rollback
- Aucun timer systemd activé
- Aucun write externe

## Protection

- Ne pas pusher vers `sot/mainline` directement
- PR requise pour merge
- HITL obligatoire avant activation timer réelle
- Gmail/Calendar exclus du scope
- Trading interdit
