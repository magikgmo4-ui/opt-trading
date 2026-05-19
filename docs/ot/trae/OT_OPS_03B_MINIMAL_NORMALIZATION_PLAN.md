# OT-OPS-03B — PLAN DE NORMALISATION MINIMALE

## 1. ACTION SÛRE : AJOUT DE LIENS DANS HUB
Modifier `modules/ops_menu_hub/scripts/menu.sh` pour ajouter :
- **Development & QA** :
  - `menu-validated_prompt_factory` (Création)
  - `menu-trae_module_validator` (Validation)

## 2. ACTION SÛRE : CRÉATION WRAPPER STUDENT
Créer un wrapper `cmd-student_daily_report` sur `admin-trading` qui fait `ssh student "/opt/trading/scripts/student/deepseek_student_daily_ai_report.sh"`.
L'enregistrer dans `registry/wrappers_registry.yaml`.

## 3. ACTION SÛRE : CLARIFICATION DOCUMENTAIRE
Mettre à jour `docs/master_pack/00_current_state_and_standards.md` pour refléter ces nouvelles routines canoniques.

## 4. ACTIONS NON JUSTIFIÉES (REPORTÉES)
- Suppression des scripts doublons (`desk_pro_menu.sh`).
- Refactoring global du menu.
- Promotion des outils non quotidiens (smoke, etc.).
