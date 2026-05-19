# OT-OPS-04 — MATRICE DE ROUTINE STUDENT (LOCAL)

Cette matrice recense les routines exécutables **localement** sur la machine `student`.

## 1. ROUTINES MÉTIER (CRITIQUES)

| Routine | Script / Point d'Entrée | Type | Fréquence | Statut |
| :--- | :--- | :--- | :--- | :--- |
| **Daily AI Report** | `scripts/student/deepseek_student_daily_ai_report.sh` | Script Shell | Quotidien | **PROD** (Legacy Path) |
| **DeepSeek Wrapper** | `scripts/student/deepseek_student_cmd.sh` | Wrapper CLI | À la demande | **PROD** (Legacy Path) |
| **Probability Engine** | `modules/probability_engine/scripts/cmd.sh` | Module CLI | Continu | **MODULAIRE** (Clean) |

## 2. ROUTINES DE MAINTENANCE

| Routine | Script / Point d'Entrée | Type | Fréquence | Statut |
| :--- | :--- | :--- | :--- | :--- |
| **Perm Fix** | `modules/perm_fix_student/scripts/cmd.sh` | Module CLI | À la demande | **MODULAIRE** |
| **Log Rotation** | `scripts/student/deepseek_student_run_logged.sh` | Script Interne | Auto | **PROD** (Legacy Path) |

## 3. ROUTINES OBSOLÈTES OU INCOMPLÈTES (À IGNORER)

| Routine | Script / Point d'Entrée | Problème |
| :--- | :--- | :--- |
| **DeepSeek Module Cmd** | `modules/deepseek_student/scripts/deepseek_student_cmd.sh` | Manque les commandes `response`, `daily-ai-report` |
| **DeepSeek Module Menu** | `modules/deepseek_student/scripts/menu.sh` | Menu générique vide |

## 4. CLASSIFICATION D'ACCÈS

- **LOCALE PURE** : Toutes les routines ci-dessus sont conçues pour s'exécuter sur `student`.
- **PILOTABLE À DISTANCE (POTENTIEL)** :
    - `Daily AI Report` pourrait être déclenché par SSH depuis `admin-trading`.
    - `Probability Engine` est un service, donc pilotable via `systemctl` ou API (si existante).
    - **Note** : Aucun wrapper distant n'est *requis* pour l'instant si l'opérateur se connecte en SSH.
