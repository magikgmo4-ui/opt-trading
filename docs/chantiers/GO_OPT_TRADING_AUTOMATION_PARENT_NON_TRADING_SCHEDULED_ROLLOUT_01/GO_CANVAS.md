---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
doc_type: go_canvas
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: open
lifecycle_stage: parent_opening
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
---

# GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01

## 1_MASTER_TARGET

Passer les jobs hors trading du registre NON_TRADING_JOBS_REGISTER en
automatisation contrôlée par phases, avec scheduler, retry, dead-letter,
HITL, et conformité gouvernance.

## 2_INITIAL_PROJECT_DOC

Voir `00_INITIAL_PROJECT_DOC.md`.

## 7_CANONICAL_STATE

Base disponible : PR #678 mergée avec briques G01-G12.
Le parent précédent GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
a fermé P0-P10 (rollout automation phases), créant les workers, ledger,
HITL gate, bridges sous contrat, scheduler et canary — mais ces livrables
runtime vivent sur une branche séparée `go/runtime-non-trading-workers-01`
et seront mergés via une PR distincte.

Ce parent est DOC-ONLY : il pose le registre des jobs non-trading,
la structure de gouvernance, et le plan de rollout scheduler.

Périmètre :
```
NON_TRADING_AUTOMATION_ONLY
= repo jobs + docs jobs + governance jobs + worker jobs
  + scheduler jobs + app bridges (write-gated) + cockpit (localcms) + ledger
```

Voir `10_NON_TRADING_JOBS_REGISTER.md` pour le registre complet.

## 8_VALIDATED_PLAN

Voir `20_SCHEDULER_ROLLOUT_PLAN.md`.

## 12_INVARIANTS

- Aucune action trading live.
- Aucun write autonome.
- Aucune app externe ne devient source de vérité.
- Tout write passe par HITL (contrat bridge).
- Tout job écrit dans le ledger.
- Tout échec a rollback ou dead-letter.
- Tout bouton cockpit dangereux est bloqué par kill switch / dual confirm.
- Le périmètre NON_TRADING_AUTOMATION_ONLY exclut tout signal/trading.

## 16_TODO

1. Valider `10_NON_TRADING_JOBS_REGISTER.md` avec Human Owner.
2. Choisir Phase 01 jobs pour premier scheduler cycle.
3. Merger PR runtime séparée non-trading workers.
4. Activer premier timer scheduler.

## 17_RESUME_POINT

Parent ouvert, doc-only, registre non-trading défini.
PR #676 (parent précédent closeout) en attente de merge.
PR runtime séparée à créer depuis `go/runtime-non-trading-workers-01`.
Prochaine étape : valider registre + choisir Phase 01.
