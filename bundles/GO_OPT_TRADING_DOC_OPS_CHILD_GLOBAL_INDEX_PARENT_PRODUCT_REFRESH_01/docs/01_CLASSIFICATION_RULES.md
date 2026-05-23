# 01_CLASSIFICATION_RULES

## Classification obligatoire

Chaque entrée rencontrée dans les index globaux doit être classée dans une seule catégorie :

| Code | Sens | Action |
|---|---|---|
| `KEEP_PARENT_PRODUCT` | parent actif avec produit utilisable ou cible produit claire | garder dans les index globaux |
| `MOVE_TO_CLOSED` | chantier terminé / PASS / fermé | déplacer ou vérifier dans `GO_CLOSED_INDEX.md` |
| `KEEP_LOCAL_ONLY` | détail utile mais non global | conserver dans dossier chantier |
| `MOVE_TO_INBOX` | transition, enfant, micro-GO ou entrée atomique | conserver/référencer via `docs/index/inbox/` |
| `DROP_FROM_GLOBAL_INDEX` | bruit, doublon, artefact non produit | retirer des index globaux |
| `NEEDS_REVIEW` | produit ou statut non prouvé | garder hors global ou noter comme gap à vérifier |

## Critère "produit fini utilisable"

Un parent peut rester global si au moins un de ces éléments est vrai :

- il porte une surface produit exécutable, consultable ou opérable ;
- il a un livrable utilisable par une machine, un humain ou un module ;
- il structure un produit clair encore actif avec next target prouvé ;
- il est nécessaire au pilotage courant et non seulement historique.

## Critère d'exclusion

Retirer des index globaux si l'entrée est seulement :

- un enfant de livraison ;
- une étape de patch ;
- une branche ;
- un bundle ;
- un closeout déjà terminé ;
- un artefact support ;
- une référence sans action courante.
