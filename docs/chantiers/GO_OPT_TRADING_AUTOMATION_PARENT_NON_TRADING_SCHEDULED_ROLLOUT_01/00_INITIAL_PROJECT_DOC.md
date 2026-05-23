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

- Il faut inclure les jobs repo, pas seulement runtime/ledger/apps.
- Il faut poser la liste maitre hors trading comme base canonique.
- Il faut transformer cette liste en registre exploitable pour choisir Phase 01.

## 4_MASTER_PROJECT_PLAN

1. Etablir le registre canonique des jobs non-trading.
2. Definir le rollout scheduler par phases.
3. Definir les canaries write-gated des apps externes.
4. Verrouiller les politiques ledger, kill switch, HITL et gouvernance.

## 5_GO_PLAN

Voir:

- `10_NON_TRADING_JOBS_REGISTER.md`
- `20_SCHEDULER_ROLLOUT_PLAN.md`
- `30_EXTERNAL_APPS_WRITE_GATED_CANARY_PLAN.md`
- `40_RUNTIME_CLONE_SETUP.md`
- `50_KILL_SWITCH_LEDGER_HITL_POLICY.md`
- `60_GOVERNANCE_COMPLIANCE_CHECKLIST.md`

## 6_FINAL_TARGET

Obtenir un parent non-trading canonique, indexe et exploitable pour
transformer la liste maitre en jobs register puis choisir la Phase 01.

## 7_CANONICAL_STATE

```text
NON_TRADING_AUTOMATION_ONLY
= repo jobs + docs jobs + governance jobs + worker jobs
+ scheduler jobs + app bridges + cockpit + ledger
```

Base disponible : PR #678 mergee avec G01-G12, contrats bridges,
ledger, scheduler, cockpit et workers documentes.

Le perimetre correct est :

```text
NON_TRADING_AUTOMATION_ONLY
= repo jobs + docs jobs + governance jobs + worker jobs + scheduler jobs + app bridges + cockpit + ledger
```

Les apps externes ont des contrats `PASS_WITH_EVIDENCE`, avec
reads/writes/gates/rollback definis.

## 8_VALIDATED_PLAN

- Parent canonique ouvert apres merge de `#676`.
- La liste maitre hors trading sert de base source.
- Prochain livrable : `10_NON_TRADING_JOBS_REGISTER.md` complet.

## 11_KEY_DECISIONS

- Le perimetre non-trading inclut explicitement les jobs repo.
- La liste maitre doit couvrir repo + strict workers + ledger + security + HITL + AI team + LocalCMS + apps externes + scheduler/CI.
- `GO_CANVAS.md` reste matiere source, pas document parent suffisant.

## 12_INVARIANTS

- Aucun signal/trading dans ce parent.
- Aucun write autonome.
- Tout write externe passe par gate + rollback.
- Tout scheduler doit rester observable via ledger.

## 13_ESTABLISHED

- PR #678 fournit la base technique disponible.
- `#676` a ete mergee pour ouvrir le parent doc-only conforme.
- Le register canonique est pose et la shortlist Phase 01 est maintenant selectionnee.

## 14_HYPOTHESIS

- Le registre Phase 01 peut etre active sans surfacer de risque trading.
- Les jobs apps externes canary peuvent rester bornes via write-gated.

## 15_REMAINING_GAP

- Verifier la shortlist `phase_01_selected` avec Human Owner.
- Verrouiller l'ordre d'activation des 13 jobs Phase 01.
- Deriver ensuite les implementions/jobs concrets a scheduler.

## 16_TODO

1. Valider la shortlist `phase_01_selected` avec Human Owner.
2. Verrouiller le scheduler rollout correspondant.
3. Deriver les implementations necessaires depuis le register.
4. Ouvrir le chantier d'execution Phase 01 seulement.

## 17_RESUME_POINT

Les jobs repo sont inclus dans le registre canonique.
La shortlist Phase 01 est selectionnee : 13 jobs read-only/dry-run/local-only.
Prochaine etape : valider cette shortlist puis ouvrir l'execution Phase 01.
