# OT-OPS-04 — AUDIT DES ROUTINES STUDENT

## 1. OBJECTIF
Auditer spécifiquement les routines de la machine `student`, sans préjuger de leur pilotage à distance et sans nettoyage destructif.

## 2. DÉCOUVERTE MAJEURE : LA DUALITÉ DEEPSEEK
L'audit révèle une divergence critique entre l'implémentation "terrain" et la structure modulaire théorique pour le module `deepseek_student`.

### A. L'Implémentation Réelle (Active)
- **Localisation** : `scripts/student/`
- **État** : **PRODUCTION**
- **Composants Clés** :
  - `deepseek_student_cmd.sh` : Wrapper complet (supporte `think`, `response`, `daily-ai-report`, `roadmap`).
  - `deepseek_student_daily_ai_report.sh` : Script critique de rapport quotidien.
  - `deepseek_student_run_logged.sh` : Moteur d'exécution avec logging.
- **Observation** : C'est ici que réside l'intelligence actuelle de la machine student.

### B. Le Module Théorique (Incomplet)
- **Localisation** : `modules/deepseek_student/`
- **État** : **COQUILLE VIDE / BROUILLON**
- **Composants Clés** :
  - `scripts/deepseek_student_cmd.sh` : Version très limitée (manque `response`, `daily-ai-report`).
  - `scripts/menu.sh` : Menu générique sans fonctionnalités métier.
- **Observation** : Ce module ne peut PAS remplacer les scripts actuels en l'état.

## 3. AUTRES ROUTINES IDENTIFIÉES

### A. Probability Engine (Établi)
- **Localisation** : `modules/probability_engine/`
- **Type** : Service de calcul continu.
- **État** : **CONFORME**. Structure modulaire standard respectée.

### B. Perm Fix Student (Maintenance)
- **Localisation** : `modules/perm_fix_student/`
- **Type** : Utilitaire de maintenance.
- **État** : **ACTIF**. Module simple pour corrections de permissions.

## 4. CONCLUSION DE L'AUDIT
La machine `student` fonctionne sur une base "hybride" :
1.  **Code Legacy Vital** (`scripts/student/`) pour l'IA et le Reporting.
2.  **Modules Modernes** (`modules/probability_engine`) pour le calcul.

**Action requise** : Ne surtout pas supprimer `scripts/student/`. La normalisation (migration vers `modules/deepseek_student`) nécessitera un portage complet du code, pas un simple déplacement.

## RISKS

- À qualifier.
