# UI Gap Analysis

## Gaps principaux observés

### Gap A — Pas encore de registry UI canonique
ÉTABLI (repo) : une base de registry existe (`registry/ui_surfaces_registry.yaml`, `registry/wrappers_registry.yaml`) et un module lecteur UI est versionné (`modules/ui_registry_msi`).
À CONFIRMER (live) : adoption réelle comme source unique et complétude des surfaces par machine / rôle / catégorie.

### Gap B — `ops_menu_hub` est bon comme hub CLI, pas comme UI finale
Il remplit bien son rôle d’accès opérateur, mais ne remplace pas une UI MSI riche.

### Gap C — `desk_pro_dashboard`, `perf`, `vision_bot` et les moteurs probability/trades ne sont pas encore cartographiés ensemble
Ils existent, mais leur place respective dans la future UX MSI n’est pas encore normalisée.

### Gap D — Catégorie screenshots + analyses passées pas encore structurée comme surface UI
Le besoin métier est clair, mais la vue UI/registre n’est pas encore écrite.

### Gap E — Présence de fichiers non suivis dans certains modules
- `modules/engines/scripts/...`
- `modules/perm_fix_student/scripts/...`
- `modules/shared_sshfs_permanent/scripts/...`
Ces éléments ne doivent pas polluer ce chantier UI tant qu’ils ne sont pas classés.

## Conclusion
Avant toute UI spécifique, maintenir une **UI registry MSI-first** et un **target map** des surfaces, sans sur-interpréter l’état live tant qu’il n’est pas prouvé.

## RISKS

- À qualifier.
