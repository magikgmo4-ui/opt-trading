# OT-OPS-03B — REQUALIFICATION DES ROUTINES

## 1. ROUTINES QUOTIDIENNES ÉTABLIES
Ces routines sont utilisées chaque jour par l'opérateur ou le système.

| Routine | Wrapper Canonique | Machine | Fréquence | Preuve |
| :--- | :--- | :--- | :--- | :--- |
| **Navigation** | `menu-ops_menu_hub` | admin-trading | Session | Point d'entrée central |
| **Orchestration** | `cmd-desk_pro_runner` | admin-trading | Continu | Service critique |
| **Calcul** | `cmd-probability_engine` | student | Continu | Service critique |
| **Rapport IA** | `cmd-student_daily_report` (À Créer) | student | Quotidien | Script explicite |

## 2. OUTILS OPÉRATEUR MAJEURS (NON QUOTIDIENS)
Ces outils sont critiques mais utilisés à la demande (maintenance, dev).

| Outil | Wrapper Canonique | Machine | Usage |
| :--- | :--- | :--- | :--- |
| **Création** | `menu-validated_prompt_factory` | admin-trading | Build / Patch |
| **Validation** | `menu-trae_module_validator` | admin-trading | QA / Pre-commit |
| **Dashboard** | `cmd-desk_pro_dashboard` | admin-trading | Monitoring (Beta) |

## 3. ZONES AMBIGUËS
- `scripts/desk_pro_menu.sh` : Doublon historique de `ops_menu_hub`. À supprimer plus tard.
- `scripts/smoke.sh` : Test global utile, mais pas une routine opérateur standard.
