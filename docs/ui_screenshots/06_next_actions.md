# UI Screenshots — Next Actions

## Ordre recommandé
1. versionner cette phase d’indexation/pre-fill screenshots
2. créer un module minimal **registry screenshots** ou **ui_screenshots_registry**
3. faire une seed/registry lisible des entrées conservées
4. seulement ensuite définir le mécanisme de promotion Daily -> Archive
5. enfin construire la vraie surface UI MSI de lecture/navigation

## Premier chantier recommandé
Créer une base de registre lisible qui expose :
- screenshot
- symbole
- date/heure
- source
- analyse liée
- statut archive/daily
- description
- priorité

## À ne pas faire tout de suite
- refactor global du cleanup
- migration massive de fichiers
- UI riche définitive
- fusion avec `desk_pro_dashboard`
