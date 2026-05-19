---
doc_id: GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01_FAMILY_PRIORITIZATION
doc_type: chantier_inventory
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01
status: complete
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - modules
  - canonical
  - archive
  - prioritization
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/91_synthese_resultats.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/92_plans_execution_sous_lots.md
---

# Priorisation des familles

## P1 - familles avec variantes actives ou drift historique

### 1. `reseau_ssh*`
Sortie attendue :
- module canonique final vise : `reseau_ssh`
- implementation interne utile : `reseau_ssh_step2`
- `compat` : `reseau_ssh_step1b`
- `compat runtime` : `scripts/reseau_ssh`
- `archive` : `_archive/legacy_modules/reseau_ssh_step1`

### 2. `deepseek*`
Sortie attendue :
- proprietaire canonique a figer entre runtime reel et facade module
- elimination des doublons historiques `response/thinking/student` quand non necessaires

### 3. `vision*`
Sortie attendue :
- survivant ou binome durable
- retrait du legacy `step1`

## P2 - familles avec sous-roles reels mais hygiene encore necessaire

### 4. `shared access / transfer`
Sortie attendue :
- `shared` conserve comme surface canonique
- `shared_files_sftp`, `shared_sshfs_permanent`, `winscp_transfer` gardes comme sous-roles
- zero drift wrappers
- aucun faux doublon actif

### 5. `workflow_post_change*`
Sortie attendue :
- `workflow_post_change_v2` comme seul actif si confirme
- variantes `fix1/fix2/fix3/broken_backup` hors actif et archivees proprement

## P3 - stacks ou suites a ne pas ecraser artificiellement

### 6. `desk_*`
Sortie attendue :
- suite canonique, pas faux module unique

### 7. `openclaw*`
Sortie attendue :
- suite canonique par chaine, pas fusion physique forcee

### 8. `collectors*`
Sortie attendue :
- fondation canonique + satellites distincts si frontiere runtime reelle

## Regle de priorisation
Traiter d'abord :
1. ce qui a des variantes historiques actives
2. ce qui a des wrappers ou callers encore ambigus
3. ensuite seulement les suites legitimes multi-modules

## Target
1 module canonique par famille.
