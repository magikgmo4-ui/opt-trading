---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_03_RESEAU_SSH
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
  - reseau-ssh
  - family-decision
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/status/reseau_ssh_canonique.md
  - modules/reseau_ssh/README.md
  - modules/reseau_ssh_step1b/README.md
  - modules/reseau_ssh_step2/README.md
  - modules/shared/README.md
  - modules/shared_files_sftp/README.md
  - modules/shared_sshfs_permanent/README.md
  - modules/winscp_transfer/README.md
---

# Step 03 - famille `reseau_ssh*`

## Statut
Complete.

## Objet
Figer la lignée `reseau_ssh*` et la distinguer clairement des modules adjacents de partage et de transfert.

## Verifications utilisees
- lecture de `docs/status/reseau_ssh_canonique.md`
- lecture de `modules/reseau_ssh/README.md`
- lecture de `modules/reseau_ssh_step1b/README.md`
- lecture de `modules/reseau_ssh_step2/README.md`
- lecture des README détaillés sous :
  - `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step1/README.md`
  - `modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/README.md`
  - `modules/reseau_ssh_step2/modules/reseau_ssh/reseau_ssh_step2/README.md`
- recroisement avec les surfaces adjacentes :
  - `modules/shared/README.md`
  - `modules/shared_files_sftp/README.md`
  - `modules/shared_sshfs_permanent/README.md`
  - `modules/winscp_transfer/README.md`

## Decision retenue

### 1. Lignée `reseau_ssh*`
- survivant : `reseau_ssh_step2`
- transition / prérequis : `reseau_ssh_step1b`
- legacy : `reseau_ssh`

### 2. Séparation de rôle avec les surfaces adjacentes
- `reseau_ssh*` porte la baseline SSH, les alias, l'inventaire machine et la trajectoire WireGuard
- `shared` porte la surface canonique inter-machines
- `shared_files_sftp` porte l'exposition serveur SFTP de cette surface
- `shared_sshfs_permanent` porte le montage client Linux de cette surface
- `winscp_transfer` porte le workflow Windows <-> Linux par inbox/outbox

### 3. Conséquence
- `shared*` et `winscp_transfer` ne sont pas reclassés dans la lignée `reseau_ssh*`
- ils relèvent du même domaine opératoire large (`reseau / partage / transfert`), mais pas de la même lignée step-by-step

## Effet documentaire
- la fiche `docs/status/reseau_ssh_canonique.md` est durcie
- les README de la lignée et des surfaces adjacentes sont alignés

## Rollback
- revert doc-only de la fiche `docs/status`
- revert doc-only des `README` ajustés
- revert doc-only de `03_plan_operationnel_step_by_step.md`
- suppression de cette note si le batch est annulé

## Point de reprise
Passer en `Step 03b` pour évaluer les consolidations possibles de la suite élargie `reseau / partage / transfert`, sans move physique.

## RISKS

- À qualifier.
