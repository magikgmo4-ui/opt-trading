# UI Screenshots — Surface Map

## Surface cible
### `ui/screenshots_analyses_passees`
But :
- naviguer les screenshots conservés
- voir leur contexte
- voir l’analyse liée
- filtrer par actif / date / run / statut

## Machine cible
### MSI / db-layer
Doit héberger la future surface de lecture/navigation.

## Backend
### admin-trading
Doit rester la source de production :
- snapshots
- runs
- logs
- génération d’artefacts

## Données attendues par la future UI
Pour chaque entrée :
- screenshot path
- symbol
- timestamp
- source run / source snapshot
- analysis status
- short description
- retention class (`daily` / `archive`)
- notes éventuelles

## Ce que cette UI n’est pas
- pas une UI de trading actif
- pas un dashboard perf
- pas un hub CLI
- pas un simple navigateur de fichiers brut
