# reseau_ssh — legacy / doc pré-step

Ce répertoire racine est conservé comme point d'entrée de statut pour la famille `reseau_ssh*`.

## Statut
- rôle : legacy / documentation pré-step
- continuité canonique active : non
- ne pas utiliser ce niveau comme cible de nouvelle consolidation runtime
- ce répertoire occupe encore le nom canonique final visé pour la famille
- sa sortie future doit libérer le nom `modules/reseau_ssh`

## Référence détaillée
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step1/README.md`

## Continuité de famille
- prérequis intermédiaire conservé : `modules/reseau_ssh_step1b/`
- survivant canonique de la famille : `modules/reseau_ssh_step2/`

## Frontière de suite
- ne pas confondre cette lignée `reseau_ssh*` avec la suite adjacente `shared / sftp / sshfs / winscp`
- `reseau_ssh` reste un repère legacy de la baseline SSH, pas la surface de partage inter-machines
