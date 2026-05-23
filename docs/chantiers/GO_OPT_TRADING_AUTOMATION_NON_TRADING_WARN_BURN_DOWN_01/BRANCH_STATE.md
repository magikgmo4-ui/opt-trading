# BRANCH_STATE

## Informations

| Champ | Valeur |
|-------|--------|
| Branch | `go/GO_OPT_TRADING_AUTOMATION_NON_TRADING_WARN_BURN_DOWN_01` |
| Base | `origin/sot/mainline` (commit `44225ba8`) |
| Parent GO | `GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01` |
| Créée | 2026-05-22 |

## État actuel

- Document structure créée et commitée
- WARN register complété avec statuts pour les 13 WARN
- P0 : `.env` permissions corrigées (chmod 600)
- P1 : `REVIEW_DRAFT` et `CLOSEOUT_DRAFT` ajoutés à `tasks.index.json`
- P1 : Handoff sources déclassifiées (artefacts obsolètes)
- P1 : Gmail/Calendar/Drive reportés (CARRIED_FORWARD)
- P1 : KG index entries déclassifiées (ratio 1:1)
- P2 : FastAPI venv déclassifié (faux positif)
- P2 : Kill switch déclassifié (présent dans l'Automation Cockpit)
- P3 : Strict worker E2E reporté (CARRIED_FORWARD)

## Protection

- Ne pas pusher vers `sot/mainline` directement
- PR requise pour merge
- HITL obligatoire pour tout write externe
