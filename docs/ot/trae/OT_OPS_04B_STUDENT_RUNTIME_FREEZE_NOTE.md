# OT-OPS-04B — NOTE DE GEL DU RUNTIME STUDENT

**DATE :** 2026-03-12
**STATUT :** FROZEN (GELÉ)
**PORTÉE :** Machine `student` uniquement

## 1. DÉFINITION DE LA VÉRITÉ RUNTIME
Pour éviter toute ambiguïté future, l'état suivant est déclaré **CANONIQUE** et **GELÉ** jusqu'à nouvel ordre :

*   **Runtime Actif (IA/Reporting)** : `scripts/student/`
    *   C'est ici que s'exécutent les routines réelles (`deepseek_student_daily_ai_report.sh`, `deepseek_student_cmd.sh`).
    *   **ACTION : NE PAS TOUCHER / NE PAS SUPPRIMER.**

*   **Module Incomplet** : `modules/deepseek_student/`
    *   Ce module est une structure standard vide ou partielle.
    *   Il ne contient **PAS** la logique métier active.
    *   **ACTION : NE PAS DÉPLOYER EN REMPLACEMENT.**

*   **Runtime Actif (Calcul)** : `modules/probability_engine/`
    *   Ce module est conforme et actif.
    *   **ACTION : STANDARD.**

## 2. INTERDICTIONS STRICTES
1.  **INTERDIT** de migrer `scripts/student/` vers `modules/deepseek_student/` sans un ticket de refactoring dédié et validé (ex: `OT-REFAC-01`).
2.  **INTERDIT** de créer des wrappers distants spéculatifs (ex: `cmd-student-remote`) sur `admin-trading` pour piloter ces scripts locaux. L'accès SSH interactif est la norme actuelle.
3.  **INTERDIT** de supprimer `scripts/student/` sous prétexte de "nettoyage". Cela casserait la prod.

## 3. PROCÉDURE DE DÉGEL
Le dégel ne pourra avoir lieu que si :
1.  Une mission de consolidation est lancée.
2.  Le code de `scripts/student/` est intégralement porté et testé dans `modules/deepseek_student/`.
3.  La bascule est prouvée par un test sur machine réelle.

En attendant, **`scripts/student/` EST LA PROD.**
