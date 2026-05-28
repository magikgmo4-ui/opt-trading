---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: automation_ops
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01
parent_go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: open
lifecycle_stage: in_progress
topic_keys:
  - semiauto_loop
  - go_prompt
  - operator_handoff
  - templates
  - automation_ops
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-28
base_branch: sot/mainline
working_branch: go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01
links:
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01/10_LOOP_PROTOCOL_DETAIL.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01/20_TEMPLATES.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01/30_PILOT_TEST.md
  - docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01/40_ACCEPTANCE_REPORT.md
---

# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01 — INITIAL_PROJECT_DOC

## 1_OBJECTIF

Formaliser et valider la boucle semi-automatisée opérateur ↔ agent ↔ repo ↔ PR.

Ce child GO produit :
- le protocole détaillé de la boucle (avec exemples annotés) ;
- les templates canoniques GO_PROMPT et retour opérateur ;
- une validation sur un GO pilote réel (JOBS_DEDUP_AUDIT_01).

## 2_SCOPE

| Inclus | Exclus |
|---|---|
| Protocole boucle détaillé + exemples | Mutations de code |
| Templates GO_PROMPT / rapport agent / retour screenshot | Modifications de workflow GHA |
| Validation pilote sur GO réel | Suppression de jobs |
| Critères de stop / merge / rollback | Changements d'archi runtime |

## 3_CONTRAINTES

- Doc-only — aucune mutation code, aucune modification de workflow.
- Aucun merge sans instruction opérateur explicite.
- Les templates doivent être compatibles avec les formats déjà définis dans `50_OPERATOR_HANDOFF_FORMAT.md`.
- La validation pilote utilise un GO déjà terminé (JOBS_DEDUP_AUDIT_01) comme référence — pas un GO live.

## 4_LIVRABLES

| Fichier | Contenu |
|---|---|
| `10_LOOP_PROTOCOL_DETAIL.md` | Protocole boucle 7 étapes, conditions, exemples |
| `20_TEMPLATES.md` | Templates GO_PROMPT + rapport agent + retour screenshot avec exemples remplis |
| `30_PILOT_TEST.md` | Replay JOBS_DEDUP_AUDIT_01 en format canonique — validation boucle |
| `40_ACCEPTANCE_REPORT.md` | Verdict PASS_SEMIAUTO_LOOP_PROTOCOL_01 |

## 5_VALIDATIONS

- Chaque template contient un exemple rempli complet.
- Le pilot test replay couvre les 7 étapes de la boucle.
- Les champs obligatoires (LIVRABLES, VALIDATIONS, VERDICT) sont présents dans chaque exemple.
- `bash -n` sur tous les scripts référencés dans les exemples = PASS (aucun script produit).

## 6_SUCCESS_CRITERIA

```text
PASS_SEMIAUTO_LOOP_PROTOCOL_01
→ 3 livrables produits
→ pilot test PASS
→ templates complets avec exemples
NEXT_GO = GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01
```
