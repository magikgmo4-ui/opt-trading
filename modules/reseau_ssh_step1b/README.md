# reseau_ssh_step1b — prérequis intermédiaire conservé

Ce répertoire racine est conservé comme point d'entrée de statut pour la famille `reseau_ssh*`.

## Statut
- rôle : prérequis intermédiaire utile
- continuité canonique finale : non
- conservation justifiée pour la préparation hosts / ssh config / key tests

## Référence détaillée
- `modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/README.md`

## Continuité de famille
- legacy / doc pré-step : `modules/reseau_ssh/`
- survivant canonique de la famille : `modules/reseau_ssh_step2/`

## Frontière de suite
- `reseau_ssh_step1b` prépare la baseline SSH
- il ne remplace ni `shared_files_sftp`, ni `shared_sshfs_permanent`, ni `winscp_transfer`
