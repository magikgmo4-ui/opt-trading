# reseau_ssh_step1b — prérequis intermédiaire conservé

Ce répertoire racine est conservé comme point d'entrée de statut pour la famille `reseau_ssh*`.

## Statut
- rôle : ancien prérequis désormais absorbé
- continuité canonique finale : non
- conservation justifiée comme trace de transition, plus comme dépendance active

## Référence détaillée
- `modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/README.md`

## Continuité de famille
- legacy / doc pré-step : `_archive/legacy_modules/reseau_ssh_step1`
- module canonique de la famille : `modules/reseau_ssh/`
- statut cible : `compat_temporaire`

## Frontière de suite
- `reseau_ssh_step1b` préparait la baseline SSH
- les commandes `baseline-*` de `modules/reseau_ssh/scripts/cmd.sh` ne délèguent plus ici
- il ne remplace ni `shared_files_sftp`, ni `shared_sshfs_permanent`, ni `winscp_transfer`

## Règle de retrait
- le déclarer `legacy_only` / archival-candidate est maintenant admissible après preuve repo-side
