# RESEAU SSH — RUNTIME STATUS

⚠️ **ATTENTION : CE DOSSIER N'EST PLUS LE POINT D'ENTRÉE CANONIQUE DES ALIAS COURTS.**

## ETAT DU RUNTIME (2026-04-25)
Les scripts contenus dans ce dossier (`scripts/reseau_ssh/`) restent présents comme backend de compatibilité encore utilisé par la façade canonique, plus rollback.

Les alias courts `menu/cmd/sanity-reseau_ssh` ont été repointés vers `modules/reseau_ssh/scripts/*` sur :
- `db-layer`
- `admin-trading`
- `student`
- `fantome`

## RELATION AVEC LE CANONIQUE
Le canonique repo-side n'est plus ce dossier.

Le canonique de famille est maintenant :
- `modules/reseau_ssh/`

Et son implémentation interne est :
- `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/`

Ce dossier runtime reste seulement :
- une surface legacy conservée pour rollback et appel explicite seulement
- une surface de rollback encore disponible
- une surface à sortir progressivement du flux actif

Les anciens wrappers racine historiques ont deja ete sortis du flux actif vers :
- `_archive/legacy_modules/reseau_ssh_root_wrappers_legacy/`

## CONSIGNE
- Pour modifier le canonique repo-side : modifier `modules/reseau_ssh/`.
- Pour observer l'ancien backend de compat : lire `scripts/reseau_ssh/`.
- Ne pas écraser ce dossier ni le re-promouvoir comme survivant canonique de famille.

## Point d'attention
`install_reseau_ssh.sh` est désormais un installeur legacy déprécié.

Quand le canonique `modules/reseau_ssh` est présent, il doit déléguer vers :
- `modules/reseau_ssh/scripts/install_canonical_shortcuts.sh`

## Blocage de sortie
Ce dossier ne peut pas encore passer en archive directe, même si la façade canonique ne l'utilise plus.

Les commandes suivantes relèvent désormais d'un appel legacy explicite seulement :
- `bootstrap`
- `ssh-hardening-safe`
- `ssh-lockdown`
- `wg-server-init`
- `wg-client-init`
- `wg-add-peer`
