---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_03B_RESEAU_SHARE_TRANSFER
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
  - step-03b
  - reseau
  - shared
  - winscp
  - consolidation
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/10_step_03_family_decision_reseau_ssh.md
  - modules/shared/README.md
  - modules/shared_files_sftp/README.md
  - modules/shared_sshfs_permanent/README.md
  - modules/winscp_transfer/README.md
  - modules/reseau_ssh_step2/README.md
---

# Step 03b - evaluation des consolidations possibles

## Statut
Complete.

## Objet
Evaluer les consolidations possibles de la suite élargie `reseau / partage / transfert` après clarification de la lignée `reseau_ssh*`.

## Synthese de suite
- `reseau_ssh_step2` : baseline SSH/WireGuard, inventaire et connectivité
- `shared` : surface canonique inter-machines
- `shared_files_sftp` : couche serveur SFTP de la surface `shared`
- `shared_sshfs_permanent` : montage client Linux de `shared`
- `winscp_transfer` : workflow Windows / inbox-outbox sur la même surface

## Consolidations possibles

### A. Consolidation documentaire de suite
Faible risque, recommandée.
- produire une carte unique `reseau / partage / transfert`
- normaliser les cross-links entre les cinq modules
- harmoniser la terminologie :
  - baseline SSH
  - surface canonique `shared`
  - serveur SFTP
  - montage SSHFS
  - workflow WinSCP

### B. Consolidation contractuelle / wrappers
Risque modéré, possible plus tard.
- aligner les entrées `status`, `path`, `sanity`, `show-*`
- préciser les frontières d'ownership machine :
  - `admin-trading` pour l'exposition SFTP
  - `student` / `db-layer` pour le montage SSHFS
  - Windows pour WinSCP

### C. Consolidation physique
Non recommandée à ce stade.
- ne pas fusionner `winscp_transfer` dans `shared_files_sftp`
- ne pas absorber `shared_sshfs_permanent` dans `reseau_ssh_step2`
- ne pas reclasser `shared` dans la lignée `reseau_ssh*`

## Arbitrage retenu
- oui à une suite fonctionnelle élargie `reseau / partage / transfert`
- non à une fusion physique de modules dans ce lot
- prochaine consolidation utile :
  - carte de suite
  - conventions de wrappers
  - clarification ownership par machine

## Point de reprise
Poursuivre `Step 03` avec `desk_*`, puis basculer en `Step 04` pour les cartes de rôle P1 si besoin.
