---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_03_DESK
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-03
  - desk
  - family-decision
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/status/desk_pro_stack_canonique.md
  - docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md
  - docs/desk_pro_multi_machine_map.md
  - docs/admin_trading_desk_pro_runbook.md
  - modules/desk_pro/README.md
  - modules/desk_common/README.md
  - modules/desk_pro_runner/README.md
  - modules/desk_pro_orchestrator/README.md
  - modules/desk_pro_dashboard/README.md
---

# Step 03 - famille `desk_*`

## Statut
Complete.

## Objet
Figer la lecture de stack de `desk_pro*` et des surfaces `desk_*` adjacentes sans chercher un faux survivant unique.

## Verifications utilisees
- lecture de `docs/status/desk_pro_stack_canonique.md`
- lecture de `docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md`
- lecture de `docs/desk_pro_multi_machine_map.md`
- lecture de `docs/admin_trading_desk_pro_runbook.md`
- lecture de `scripts/admin_trading/desk_pro_cmd.sh`
- lecture des README de :
  - `modules/desk_pro`
  - `modules/desk_common`
  - `modules/desk_pro_runner`
  - `modules/desk_pro_orchestrator`
  - `modules/desk_pro_dashboard`
  - `modules/desk_snapshot_ingest`
  - `modules/desk_capture_inputs`
  - `modules/desk_analyze`
  - `modules/desk_state`
  - `modules/desk_retention`

## Decision retenue

### 1. Pas de survivant unique
- la famille `desk_*` est une stack multi-composants
- aucun module unique n'est promu survivant exclusif dans ce lot

### 2. Rôles de stack figés
- `desk_pro` : centre de gravité partagé API / UI / service
- `desk_pro_runner` : façade opératoire module
- `desk_pro_orchestrator` : pipeline d'exécution et de chaînage
- `desk_pro_dashboard` : visualisation et export de rendu
- `desk_common` : support partagé minimal

### 3. Runtime opératoire hors modules
- le wrapper admin réel reste `scripts/admin_trading/desk_pro_cmd.sh`
- ce wrapper délègue à `desk_pro_runner` et aux helpers admin
- il ne faut donc pas lire `desk_pro_runner` comme seul entrypoint réel de production

### 4. Satellites adjacents
- `desk_snapshot_ingest`
- `desk_capture_inputs`
- `desk_analyze`
- `desk_state`
- `desk_retention`

Ces modules restent adjacents à la stack Desk Pro, sans être des doublons à fusionner immédiatement.

## Effet documentaire
- la fiche `docs/status/desk_pro_stack_canonique.md` est durcie
- les README de stack et de satellites sont alignés sur la même lecture

## Rollback
- revert doc-only de la fiche `docs/status`
- revert doc-only des `README` ajustés
- revert doc-only de `03_plan_operationnel_step_by_step.md`
- suppression de cette note si le batch est annulé

## Point de reprise
`Step 03` est complete. Basculer en `Step 04` pour produire les cartes de rôle P1 :
- `Desk Pro`
- `DeepSeek/student`
- `reseau/share/transfer`

## RISKS

- À qualifier.
