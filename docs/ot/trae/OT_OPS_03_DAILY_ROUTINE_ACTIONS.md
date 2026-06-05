# OT-OPS-03 — ACTIONS RECOMMANDÉES (MINIMALES)

## 1. ACTION CANONIQUE : LIER LES NOUVEAUX OUTILS
Le menu principal `ops_menu_hub` doit être mis à jour pour inclure :
- `menu-validated_prompt_factory` (Group: Maintenance/Tools)
- `menu-trae_module_validator` (Group: Maintenance/Tools)

## 2. ACTION CANONIQUE : NORMALISER STUDENT REPORT
Créer un wrapper `cmd-student_daily_report` pour `scripts/student/deepseek_student_daily_ai_report.sh` et l'enregistrer dans le registry.

## 3. ACTION DE NETTOYAGE (FUTUR)
Supprimer les scripts doublons `desk_pro_menu.sh` une fois que `ops_menu_hub` est confirmé comme remplaçant total.

## 4. DOCUMENTATION
Ajouter ces routines canoniques dans `docs/master_pack/00_current_state_and_standards.md` pour référence future.

## RISKS

- À qualifier.
