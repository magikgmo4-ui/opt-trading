---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: open
lifecycle_stage: parent_opening
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
---

# GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01

## 1_MASTER_TARGET

Transformer le perimetre `NON_TRADING_AUTOMATION_ONLY` en rollout planifie,
gouverne et observable, sans ouvrir de surface signal/trading.

## 2_INITIAL_PROJECT_DOC

Ce parent ouvre la suite du closeout `GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01`.
Il porte uniquement la couche canonique de gouvernance, registre, priorisation
et planification du perimetre non-trading.

## 3_INITIAL_NEED

- Recanoniser le nouveau parent avant merge.
- Reintegrer les jobs repo, docs, gouvernance, workers, scheduler, cockpit,
  bridges et ledger dans un registre unique.
- Separer strictement doc-only vs runtime.

## 4_MASTER_PROJECT_PLAN

1. Etablir le registre canonique des jobs non-trading.
2. Definir le rollout scheduler par phases.
3. Definir les canaries write-gated des apps externes.
4. Verrouiller les politiques ledger, kill switch, HITL et gouvernance.
5. Ouvrir ensuite une PR runtime separee hors perimetre doc-only.

## 5_GO_PLAN

Voir:

- `10_NON_TRADING_JOBS_REGISTER.md`
- `20_SCHEDULER_ROLLOUT_PLAN.md`
- `30_EXTERNAL_APPS_WRITE_GATED_CANARY_PLAN.md`
- `40_RUNTIME_CLONE_SETUP.md`
- `50_KILL_SWITCH_LEDGER_HITL_POLICY.md`
- `60_GOVERNANCE_COMPLIANCE_CHECKLIST.md`

## 6_FINAL_TARGET

Obtenir un parent non-trading mergeable, indexe, conforme gouvernance,
pret a piloter une PR runtime separee et un premier scheduler Phase 01.

## 7_CANONICAL_STATE

```text
NON_TRADING_AUTOMATION_ONLY
= repo jobs + docs jobs + governance jobs + worker jobs
+ scheduler jobs + app bridges + cockpit + ledger
```

Base disponible : PR #678 mergee avec G01-G12, contrats bridges,
ledger, scheduler, cockpit et workers documentes. Les livrables runtime
associes vivent sur une branche separee `go/runtime-non-trading-workers-01`.

## 8_VALIDATED_PLAN

- Parent doc-only sur #676 corrigee.
- Runtime non-trading dans une PR separee.
- Aucune surface signal/trading dans ce parent.

## 11_KEY_DECISIONS

- `signal_dry_run_worker.py` sort du perimetre non-trading.
- `#676` ne doit plus porter de runtime workers ni de mutation LocalCMS.
- `GO_CANVAS.md` reste matiere source, pas document parent suffisant.

## 12_INVARIANTS

- Aucun signal/trading dans ce parent.
- Aucun write autonome.
- Tout write externe passe par gate + rollback.
- Tout scheduler doit rester observable via ledger.

## 13_ESTABLISHED

- Le parent precedent est close cote plan rollout.
- Le nouveau parent etait incomplet et doit etre recanonise.
- La separation doc/runtime est obligatoire avant merge.

## 14_HYPOTHESIS

- Le registre Phase 01 peut etre active sans surfacer de risque trading.
- Les jobs apps externes canary peuvent rester bornes via write-gated.

## 15_REMAINING_GAP

- Finaliser le register detaille.
- Finaliser le scheduler rollout.
- Finaliser la checklist gouvernance.
- Creer la PR runtime separee.

## 16_TODO

1. Valider le registre avec Human Owner.
2. Choisir les jobs Phase 01 a scheduler.
3. Ouvrir la PR runtime depuis `go/runtime-non-trading-workers-01`.
4. Mettre a jour le body de #676 sur le scope doc-only.

## 17_RESUME_POINT

`#676` est bloquee tant que le nouveau parent n'est pas recanonise.
Le runtime est separe. Le signal/trading est retire.
Prochaine etape : merger la couche parent doc-only conforme.
