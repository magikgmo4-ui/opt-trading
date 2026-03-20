# AUDIT 2026-03-20 — INDEX MAÎTRE

Date : 2026-03-20
Branche d’audit : `audit/opt-trading-20260320a`

## 1. RÔLE
Ce fichier est le **point d’entrée unique** de la passe d’audit du 2026-03-20.

Il sert à :
- retrouver rapidement les livrables d’audit ;
- comprendre l’ordre logique de lecture ;
- fournir un point de reprise stable ;
- éviter la perte de mémoire entre sessions.

## 2. ORDRE DE LECTURE RECOMMANDÉ
1. `00_audit_master_index.md`
2. `00_audit_plan.md`
3. `01_sot_mainline.md`
4. `90_convergence_matrix.md`
5. `95_repo_branch_pm_kanban.md`
6. `96_cross_project_inventory_kanban_archive_first.md`
7. `99_pm_decision.md`

## 3. FICHIERS PRÉSENTS

### Cadrage
- `audit/2026-03-20/00_audit_plan.md`
  - plan chef de projet de la passe d’audit

### Rapports de branches
- `audit/2026-03-20/01_sot_mainline.md`
  - rapport individuel de référence pour `opt-trading / sot/mainline`

### Synthèse PM
- `audit/2026-03-20/90_convergence_matrix.md`
  - matrice de convergence de toutes les branches auditées
- `audit/2026-03-20/91_cross_topology_canon.md`
  - carte canonique minimale transverse du périmètre (`GO_CROSS_TOPLOGY_CANON_01`)
- `audit/2026-03-20/92_student_canonical_surface.md`
  - fiche canonique `student` comme sous-projet intégré à `opt-trading` (`GO_STUDENT_CANONICAL_SURFACE_01`)
- `audit/2026-03-20/95_repo_branch_pm_kanban.md`
  - kanban PM aligné sur la logique `sot/mainline`
- `audit/2026-03-20/96_cross_project_inventory_kanban_archive_first.md`
  - inventaire transversal archive-first + plan opérationnel
- `audit/2026-03-20/99_pm_decision.md`
  - décision PM finale de la passe

## 4. CE QUE LA PASSE ÉTABLIT
- `opt-trading / sot/mainline` = pivot canonique
- `localcms` = projet séparé, avec socle + surcouche locale
- `Magikgmo` = historique seulement
- les branches `feat/*` auditées = absorbées
- les archives spécialisées sont conservées mais non réactivées
- `student` est traité comme sous-périmètre intégré à `opt-trading`
- `db-layer`, `admin-trading`, `cursor-ai` sont traités comme surfaces runtime documentées
- `openclaw` reste hors bundle pour cette passe

## 5. POINTS DE REPRISE CANONIQUES
- `GO_REPO_BRANCH_PM_NEXT_ACTION_01`
- `GO_CROSS_PROJECT_ARCHIVE_FIRST_PM_01`
- `GO_CROSS_TOPLOGY_CANON_01` → livré dans `91_cross_topology_canon.md`
- `GO_STUDENT_CANONICAL_SURFACE_01` → livré dans `92_student_canonical_surface.md`

## 6. USAGE RECOMMANDÉ
- utiliser cet index comme première lecture en reprise ;
- utiliser `99_pm_decision.md` pour la décision finale ;
- utiliser `95_repo_branch_pm_kanban.md` pour le suivi PM ;
- utiliser `96_cross_project_inventory_kanban_archive_first.md` pour l’inventaire transverse et le plan opérationnel.

## 7. RÉSUMÉ EXÉCUTABLE
Cette passe d’audit est maintenant structurée en bundle documentaire stable :
- plan
- rapport pivot
- matrice
- kanban PM
- inventaire transverse
- décision finale

Point d’entrée recommandé :
- `audit/2026-03-20/00_audit_master_index.md`
