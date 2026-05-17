---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #512  (Paper mode expansion decision — C→A→B→D — merged)
  - PR #513  (Kill switch + Telegram validation — prereq C PASS — merged)
created_at: 2026-05-17
observation_start: 2026-05-16
threshold_runs: 30
threshold_days: 14
eligible_after: 2026-05-30
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01

## Objectif

Observer le pipeline dry-run quotidien jusqu'à atteindre les seuils Phase 1 :
- ≥ 30 runs sans fail
- ≥ 14 jours d'observation calendaires (depuis le 2026-05-16)

Aucune nouvelle feature. Aucun trade live. Aucun ordre Bitget.
Éligibilité multi-signal débloquée uniquement quand les deux seuils sont atteints.

## Seuils et éligibilité

| Critère          | Seuil | Début observation | Éligible après |
| ---------------- | ----- | ----------------- | -------------- |
| Runs sans fail   | ≥ 30  | 2026-05-16        | variable       |
| Jours calendaires| ≥ 14  | 2026-05-16        | 2026-05-30     |

L'éligibilité multi-signal requiert les **deux** seuils simultanément.

## Contraintes

- Aucune nouvelle feature
- Dry-run uniquement (`DRY_RUN=1 PAPER_MODE=1`)
- No live trade / No Bitget order
- No automatic Sheets write
- No secrets
- Controlled-write Sheets manuel uniquement
