# OT-OPS-03 — MATRICE DE ROUTINE QUOTIDIENNE (CANONIQUE)

## 1. ROUTINES OPÉRATEUR ÉTABLIES
| Routine | Objectif | Machine | Wrapper Canonique | Fréquence | Statut |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gestion Global** | Hub Principal | admin-trading | `menu-ops_menu_hub` | Session | **ÉTABLIE** |
| **Création** | Prompt Factory | admin-trading | `menu-validated_prompt_factory` | Besoin | **ÉTABLIE** (Manque lien Hub) |
| **Validation** | Module Validator | admin-trading | `menu-trae_module_validator` | Besoin | **ÉTABLIE** (Manque lien Hub) |
| **Dashboard** | Visualisation | admin-trading | `cmd-desk_pro_dashboard` | Session | **PARTIELLE** (Beta) |

## 2. ROUTINES SYSTÈME ÉTABLIES
| Routine | Objectif | Machine | Wrapper Canonique | Fréquence | Statut |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Orchestrateur** | Exécution | admin-trading | `cmd-desk_pro_runner` | Continu | **ÉTABLIE** |
| **Calcul** | Probabilités | student | `cmd-probability_engine` | Continu | **ÉTABLIE** |

## 3. ZONES AMBIGUËS / À CONFIRMER
| Routine | Script / Chemin | Machine | Problème |
| :--- | :--- | :--- | :--- |
| **AI Report** | `scripts/student/deepseek_student_daily_ai_report.sh` | student | Pas de wrapper global normalisé |
| **Legacy Menu** | `scripts/desk_pro_menu.sh` | admin-trading | Doublon potentiel avec `ops_menu_hub` |
| **Legacy Sanity** | `scripts/desk_pro_sanity.sh` | admin-trading | Doublon potentiel avec `sanity-ops_menu_hub` |

## RISKS

- À qualifier.
