# OT-OPS-04 — ACTIONS RECOMMANDÉES (STUDENT)

Suite à l'audit, voici les actions préconisées pour maintenir la stabilité sans refactor risqué.

## 1. ACTION IMMÉDIATE : SANCTUARISATION
- **Ne PAS supprimer** `scripts/student/`. Ce dossier contient la vérité opérationnelle.
- **Ne PAS basculer** sur `modules/deepseek_student/` tant qu'il n'a pas été mis à niveau.

## 2. ACTION DE NORMALISATION (FUTUR)
Une mission ultérieure (ex: `OT-REFAC-01_STUDENT_CONSOLIDATION`) devra :
1.  Copier le contenu de `scripts/student/` vers `modules/deepseek_student/scripts/`.
2.  Mettre à jour `modules/deepseek_student/scripts/deepseek_student_cmd.sh` pour inclure toutes les commandes (`response`, `daily-ai-report`, etc.).
3.  Tester localement sur `student`.
4.  Une fois validé, supprimer `scripts/student/`.

## 3. ACTION UTILISATEUR (PRÉSENT)
Pour l'instant, l'opérateur sur `student` doit utiliser :
- Pour l'IA : `bash scripts/student/deepseek_student_cmd.sh menu` (ou les commandes directes).
- Pour Probabilités : `cmd-probability_engine` (si alias installé) ou via le chemin du module.

## 4. ACTION WRAPPER DISTANT (NON REQUISE)
- La création de `cmd-student_daily_report` sur `admin-trading` est **reportée sine die**.
- L'accès SSH interactif reste la méthode privilégiée pour l'instant.

## RISKS

- À qualifier.
