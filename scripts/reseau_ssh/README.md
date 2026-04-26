# reseau_ssh — backend compat runtime

## Statut
- module canonique repo-side : `modules/reseau_ssh`
- rôle courant : surface legacy conservée pour rollback et appel explicite seulement
- état machine-side prouvé : les alias courts `menu/cmd/sanity-reseau_ssh` pointent maintenant vers `modules/reseau_ssh/scripts/*` sur `db-layer`, `admin-trading`, `student`, `fantome`
- sortie visée : maintien temporaire en rollback-only, puis archive quand le retrait ne présentera plus de risque opératoire

## Ce que ce dossier contient encore
- `reseau_ssh_menu.sh` : menu runtime historique
- `reseau_ssh_cmd.sh` : CLI runtime historique
- `sanity_reseau_ssh.sh` : sanity runtime historique
- `install_reseau_ssh.sh` : installeur legacy maintenant garde-foue et delegue au canonique quand disponible

## Règle de lecture
- pour la doctrine canonique et la consolidation de famille : lire `modules/reseau_ssh/`
- pour l'état runtime machine-side encore actif : lire `scripts/reseau_ssh/`
- ne pas re-promouvoir ce dossier comme survivant canonique de famille

## Point de bascule
Le lot repo-side est déjà en place :
- `modules/reseau_ssh` = façade canonique
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2` = implémentation interne

Le repointage machine-side est déjà exécuté sur :
- `db-layer`
- `admin-trading`
- `student`
- `fantome`

Le lot restant est repo-side :
- conserver ce dossier hors flux canonique
- éviter toute republication legacy des alias courts
- décider ensuite l'issue finale : `rollback_only` -> `archive_backup`

## Etat des wrappers racine historiques
Les anciens wrappers racine :
- `scripts/reseau_ssh_cmd.sh`
- `scripts/reseau_ssh_menu.sh`

ont ete sortis du flux actif vers :
- `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy/`

## Blocage courant
La façade canonique `modules/reseau_ssh/scripts/*` ne délègue plus ici.

Les commandes suivantes ne sont plus publiées par la façade canonique et ne relèvent plus que d'un usage legacy explicite :
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`
- `wg-server-init`
- `wg-client-init`
- `wg-add-peer`
