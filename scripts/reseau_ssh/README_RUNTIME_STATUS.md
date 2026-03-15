# RESEAU SSH — RUNTIME STATUS

⚠️ **ATTENTION : CE DOSSIER EST LE RUNTIME ACTIF.**

## ÉTAT DU RUNTIME (2026-03-12)
Les scripts contenus dans ce dossier (`scripts/reseau_ssh/`) sont ceux utilisés en production pour la configuration du réseau et du SSH.

## DIVERGENCE AVEC MODULES/
Le dossier `modules/reseau_ssh/` contient une structure complexe (étapes, sources, archives) qui ne correspond pas directement à l'exécutable déployé ici.

## CONSIGNE
- Pour modifier le comportement réseau actif : Modifier `scripts/reseau_ssh/`.
- Ne pas écraser ce dossier avec le contenu de `modules/reseau_ssh/` sans une procédure de migration validée.
