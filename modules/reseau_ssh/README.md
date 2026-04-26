# reseau_ssh — module canonique de la famille

Ce répertoire racine est conservé comme point d'entrée de statut pour la famille `reseau_ssh*`.

## Statut
- rôle : module canonique de famille
- continuité canonique active : oui
- origine immédiate : promotion repo-side de l'ancienne base `modules/reseau_ssh_step2`
- repointage machine-side des alias courts : exécuté sur `db-layer`, `admin-trading`, `student`, `fantome`
- interface publiée finale : `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`

## Référence détaillée
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/README.md`

## Scripts utiles
- `modules/reseau_ssh/scripts/install_canonical_shortcuts.sh` : préparation du repointage machine-side des alias courts
- `modules/reseau_ssh/scripts/capture_shortcuts_snapshot.sh` : capture d'état avant rollback / repointage

## Notes
- les wrappers racine historiques ont déjà été archivés sous `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy/`
- ne pas toucher au runtime live hors lot dédié
- `step1b` est maintenant archivé repo-side sous `_archive/legacy_modules/reseau_ssh_step1b/`
- `step2` suffixé est maintenant retiré comme surface publiée et archivé machine-side

## Frontière de suite
- `reseau_ssh` est maintenant la surface canonique top-level de la lignée `reseau_ssh*`
- l'implémentation nested `reseau_ssh_step2` reste interne à ce module
- `bootstrap`, `ssh-hardening-safe` et `ssh-lockdown` sont maintenant absorbés dans `modules/reseau_ssh/scripts/*`
- les commandes `baseline-*` sont maintenant absorbées dans `modules/reseau_ssh/scripts/*`
- l'ancien runtime `scripts/reseau_ssh/` est maintenant archivé repo-side sous `_archive/legacy_modules/reseau_ssh_runtime_rollback_only/`
- l'ancien prérequis `step1b` est maintenant archivé repo-side sous `_archive/legacy_modules/reseau_ssh_step1b/`
- les alias suffixés `*_reseau_ssh_step2` sont retirés du registre et des machines
- il n'existe plus qu'un module top-level actif et un seul jeu d'alias publiés
- il est adjacent, mais non fusionné, avec :
  - `shared` pour la surface canonique inter-machines
  - `shared_files_sftp` pour l'exposition serveur
  - `shared_sshfs_permanent` pour le montage Linux
  - `winscp_transfer` pour le workflow Windows

## Target
1 module canonique par famille.
