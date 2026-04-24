# reseau_ssh_step2 — survivant canonique de la famille

Ce répertoire racine est conservé comme point d'entrée de statut pour la famille `reseau_ssh*`.

## Statut
- rôle : survivant canonique de la famille `reseau_ssh*`
- cible de continuité : oui
- consolidation minimale : marquage documentaire uniquement dans ce lot

## Référence détaillée
- `modules/reseau_ssh_step2/modules/reseau_ssh/reseau_ssh_step2/README.md`

## Notes
- ne pas fusionner ni supprimer physiquement `step1b` dans ce lot
- ne pas déplacer les wrappers racine dans ce lot
- ne pas toucher au runtime live dans ce lot sans audit dédié

## Frontière de suite
- `reseau_ssh_step2` reste le survivant de la lignée `reseau_ssh*`
- il est adjacent, mais non fusionné, avec :
  - `shared` pour la surface canonique inter-machines
  - `shared_files_sftp` pour l'exposition serveur
  - `shared_sshfs_permanent` pour le montage Linux
  - `winscp_transfer` pour le workflow Windows
