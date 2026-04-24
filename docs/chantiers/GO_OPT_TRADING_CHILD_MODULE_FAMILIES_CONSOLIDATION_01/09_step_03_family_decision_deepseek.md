---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_03_DEEPSEEK
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: in_progress
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-03
  - deepseek
  - family-decision
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/status/deepseek_student_canonique.md
  - docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md
  - docs/student_deepseek_runbook.md
  - docs/ot/trae/OT_OPS_04B_STUDENT_RUNTIME_FREEZE_NOTE.md
  - modules/deepseek_hub/README.md
  - modules/deepseek_student/README.md
  - modules/deepseek_response/README.md
  - modules/deepseek_thinking/README.md
---

# Step 03 - famille `deepseek*`

## Statut
In progress.

## Objet
Figer la lecture operatoire de la famille `deepseek*` sans confondre runtime actif, facade module unifiee, compatibilite legacy et cible de consolidation inachevee.

## Verifications utilisees
- lecture de `docs/status/deepseek_student_canonique.md`
- lecture de `docs/product_targets/DEEPSEEK_OLLAMA_TARGET_CANON.md`
- lecture de `docs/student_deepseek_runbook.md`
- lecture de `docs/ot/trae/OT_OPS_04B_STUDENT_RUNTIME_FREEZE_NOTE.md`
- lecture de `modules/deepseek_hub/README.md`
- lecture de `modules/deepseek_student/README.md`
- lecture de `modules/deepseek_response/README.md`
- lecture de `modules/deepseek_thinking/README.md`
- lecture de `modules/deepseek_hub/scripts/deepseek_hub_cmd.sh`
- lecture de `modules/deepseek_hub/scripts/apply_patches.sh`
- lecture de `modules/deepseek_student/scripts/deepseek_student_cmd.sh`

## Decision retenue

### 1. Verite runtime actuelle
- la verite runtime cote `student` reste `scripts/student/`
- ce point reste gele et ne doit pas etre reinterprete comme migre vers `modules/deepseek_student/`

### 2. Candidat module unifie
- `deepseek_hub` est retenu comme facade module unifiee la plus proche d'un survivant cote `modules/`
- il centralise menu, commandes, modeles, logs et ponts vers thinking / response / roadmap

### 3. Compatibilite conservee
- `deepseek_response` et `deepseek_thinking` restent des modules de compatibilite operatoire
- ils demeurent utiles tant que `deepseek_hub` continue de les orchestrer et tant qu'une absorption complete n'est pas prouvee

### 4. Transition clarifiee
- `deepseek_student` reste une cible de consolidation / transition, mais pas la source de verite runtime actuelle
- il ne doit pas etre deploye comme remplacement de `scripts/student/` dans ce lot

## Effet documentaire
- la fiche `docs/status/deepseek_student_canonique.md` est durcie
- les `README` de la famille sont aligns sur la meme lecture

## Rollback
- revert doc-only de la fiche `docs/status`
- revert doc-only des `README` ajustes
- revert doc-only de `03_plan_operationnel_step_by_step.md`
- suppression de cette note si le batch est annule

## Point de reprise
Poursuivre `Step 03` avec `reseau_ssh*`, puis `desk_*`.
