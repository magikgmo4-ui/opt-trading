# UI Screenshots — Scope

## Objectif
Construire d’abord une **surface UI de lecture/navigation** pour les screenshots et leurs analyses liées, avant toute migration profonde des flux de rétention.

## Contraintes validées
- Un **daily cleanup** existe déjà.
- Les **screenshots avec analyses utiles** doivent être conservés **hors du nettoyage fréquent**.
- La future surface de lecture doit être **MSI-first**.
- On sépare :
  - captures + analyses à conserver
  - artefacts jetables de routine quotidienne

## Direction
- `admin-trading` reste la machine backend qui produit et stocke.
- `MSI / db-layer` doit héberger la future surface de lecture/navigation.
- On ne refactor pas encore les modules moteurs.
- On ne change pas encore les services de cleanup, mais on prépare une architecture d’archive séparée.

## Priorité actuelle
1. cartographier les zones actuelles de screenshots / snapshots / desk runs
2. définir une politique d’archive/mémoire séparée du daily
3. définir la future surface UI `screenshots_analyses_passees`

## RISKS

- À qualifier.
