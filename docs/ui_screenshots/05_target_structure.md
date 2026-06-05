# UI Screenshots — Target Structure

## Vision cible

### Sur admin-trading
- production continue de snapshots
- stockage working/daily
- génération d’artefacts backend
- possible promotion vers archive

### Sur MSI / db-layer
- surface de lecture/navigation
- filtres par actif / date / run / statut
- accès aux screenshots conservés
- lecture des analyses liées

## Structure logique cible
1. `screenshots_daily`
   - captures temporaires / routine
2. `screenshots_archive`
   - captures retenues avec analyse
3. `screenshots_registry`
   - index lisible des entrées à afficher en UI

## MVP futur de la surface UI
- liste des screenshots archivés
- affichage du chemin / symbole / timestamp
- description courte
- statut analyse associée
- actions de lecture/export

## RISKS

- À qualifier.
