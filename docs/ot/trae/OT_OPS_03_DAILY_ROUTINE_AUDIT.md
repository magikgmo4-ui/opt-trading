# OT-OPS-03 — AUDIT DES ROUTINES QUOTIDIENNES

## 1. OBJECTIF
Identifier les routines réelles utilisées par les opérateurs et le système.

## 2. DÉCOUVERTES
- **Point Central** : `menu-ops_menu_hub` est le point d'entrée structurant sur `admin-trading`.
- **Manques** : Les nouveaux outils (`validated_prompt_factory`, `trae_module_validator`) ne sont pas encore intégrés dans ce Hub.
- **Chaos Scripts** : Le dossier `scripts/` contient une multitude de scripts orphelins ou redondants (`desk_pro_menu.sh` vs `ops_menu_hub`).

## 3. ROUTINES CRITIQUES (STUDENT)
- Le script `scripts/student/deepseek_student_daily_ai_report.sh` est vital mais n'a pas de wrapper global normalisé.

## 4. CONCLUSION
L'usage quotidien est possible mais fragmenté.
L'opérateur doit connaître plusieurs commandes distinctes (`menu-ops_menu_hub`, `menu-validated_prompt_factory`) au lieu d'une seule.
