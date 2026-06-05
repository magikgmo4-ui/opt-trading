# UI Next Actions

## Ordre recommandé
1. Versionner cette indexation UI sous `docs/ui_indexation/`
2. Stabiliser une **UI registry MSI-first**
3. Classer chaque surface par : machine / rôle / utilisateur / catégorie / statut
4. Formaliser la catégorie `ui/screenshots_analyses_passees`
5. Formaliser la catégorie `ui/probabilites_trades`
6. Ensuite seulement ouvrir un chantier UI spécifique :
   - `desk_pro_dashboard`
   - `deskpro_toolbox`
   - `perf_ui`

## Premier chantier UI recommandé après registry
Créer une **registry UI lisible** qui affiche :
- nom de surface
- machine cible
- module source
- catégorie
- usage
- actions disponibles
- statut
- priorité

## À ne pas faire tout de suite
- refactor global des modules
- fusionner toutes les UI trop tôt
- déplacer des services entre machines sans map finale

## RISKS

- À qualifier.
