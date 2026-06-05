# GO_OT_DESKPRO_MACHINE_PACK_WRAPPERS_REGISTRY_DECISION_01 — DÉCISION CANONIQUE

Date (America/Montreal) : 2026-04-11

## 1. Objet
Trancher le statut canonique des wrappers machine-specific Desk Pro de `student` et `db-layer` : entrée en `registry/wrappers_registry.yaml` ou exception runtime-layer opposable hors registry.

## 2. Preuves repo-sourcées
- La doctrine wrappers standard vise les modules : `menu-<module>`, `cmd-<module>`, `sanity-<module>` dans `docs/master_pack/00_current_state_and_standards.md`.
- Le repo distingue aussi des exceptions runtime et runtime-layers valides : `scripts/student/` (gelé) et `scripts/db_layer/` (valide).
- `scripts/student/desk_pro_student_install.sh` installe `desk-pro-student`, `menu-desk-pro-student`, `sanity-desk-pro-student`, `desk-pro-student-shared-info`.
- `scripts/db_layer/desk_pro_db_install.sh` installe `desk-pro-db`, `menu-desk-pro-db`, `sanity-desk-pro-db`, `desk-pro-db-shared-info`.
- `scripts/admin_trading/desk_pro_install_admin_trading.sh` a été réaligné vers les entrypoints canoniques globaux déjà portés par la registry, sans conserver de pack global `desk-pro*` admin.
- `registry/wrappers_registry.yaml` porte les surfaces transverses canoniques (`menu-ops_menu_hub`, `cmd-desk_pro_runner`, `cmd-desk_pro_dashboard`) mais aucun wrapper `desk-pro-student*` ou `desk-pro-db*`.
- `docs/student_desk_pro_runbook.md` et `docs/db_layer_desk_pro_runbook.md` décrivent ces packs comme surfaces locales de machine.

## 3. Décision
VERDICT = EXCEPTION RUNTIME-LAYER OPPOSABLE HORS REGISTRY

## 4. Portée de la décision
- Les wrappers `desk-pro-student*` et `desk-pro-db*` ne doivent pas entrer dans `registry/wrappers_registry.yaml` à ce stade.
- Ils sont traités comme wrappers de packs machine installés par des scripts runtime-layer dédiés.
- Ils restent documentés dans leurs runbooks machine et dans la cartographie multi-machine, pas dans la registry des wrappers de modules/surfaces transverses.

## 5. Justification
- Leur forme et leur naming (`desk-pro-student`, `desk-pro-db`) ne suivent pas le standard wrappers de module du repo.
- Leur portée est locale à une machine cible, pas transverse au système.
- Les ajouter à la registry actuelle mélangerait deux classes distinctes :
  - wrappers canoniques de modules / surfaces globales
  - packs runtime-layer spécifiques à une machine
- La doctrine du repo admet déjà des exceptions runtime documentées quand elles sont opposables et clairement bornées.

## 6. Conséquences pratiques
- Aucun patch registry requis dans ce tour.
- Les installateurs `scripts/student/desk_pro_student_install.sh` et `scripts/db_layer/desk_pro_db_install.sh` restent valides repo-side.
- Toute future extension de la registry aux packs machine devra faire l'objet d'une évolution explicite de son périmètre, pas d'un ajout opportuniste.

## 7. Point de reprise
- Suite recommandée : `GO_OT_NEXT_MISSION_SELECTION_01`.

## RISKS

- À qualifier.
