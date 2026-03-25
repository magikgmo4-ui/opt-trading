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
- `audit/2026-03-20/93_student_phase2_migration.md`
  - rapport de migration Phase 2 `student` — état réel observé, changements appliqués, plan cleanup (`GO_STUDENT_PHASE2_MIGRATION_01`)
- `audit/2026-03-20/94_student_cleanup_duplicates.md`
  - rapport cleanup doublons `student` — classification par risque, caller audit complet, aucun retrait appliqué (`GO_STUDENT_CLEANUP_DUPLICATES_01`)
- `audit/2026-03-20/A0_api_collector_canonical_module.md`
  - fiche canonique module `derivatives_collector` — qualification état réel, runbook minimal, décision classification (`GO_API_COLLECTOR_CANONICAL_MODULE_01`)
- `audit/2026-03-20/A1_runtime_surfaces_canonical_map.md`
  - carte canonique minimale des 3 surfaces runtime (`admin-trading`, `db-layer`, `cursor-ai`) — machine / rôle / repo / état (`GO_RUNTIME_SURFACES_CANONICAL_MAP_01`)
- `audit/2026-03-20/A2_localcms_canon_decision.md`
  - décision canonique `localcms` — statut projet séparé, rôle des 2 branches, règle de lecture/pilotage (`GO_LOCALCMS_CANON_DECISION_01`)
- `audit/2026-03-20/A3_algo_hf_audit.md`
  - audit de qualification `algo_hf` — service runtime prouvé sur db-layer, source code non localisée, workstream séparé de `opt-trading` (`GO_ALGO_HF_AUDIT_01`)
- `audit/2026-03-20/A4_audit_2026_03_20_formal_close.md`
  - **clôture formelle de la passe** — livrables, établi/partiel/différé, chantiers ouverts, point de reprise (`GO_AUDIT_2026_03_20_FORMAL_CLOSE_01`)
- `audit/2026-03-20/95_repo_branch_pm_kanban.md`
  - kanban PM aligné sur la logique `sot/mainline`
- `audit/2026-03-20/96_cross_project_inventory_kanban_archive_first.md`
  - inventaire transversal archive-first + plan opérationnel
- `audit/2026-03-20/99_pm_decision.md`
  - décision PM finale de la passe
- `student/validation/validate_student_live.sh`
  - runner principal de validation live — 5 sections (raccourcis, critique, legacy, entrypoints, structure)
- `student/validation/student_validation_cmd.sh`
  - dispatcher CMD du pack validation student
- `student/validation/student_validation_menu.sh`
  - menu interactif opérateur
- `student/validation/student_validation_sanity_check.sh`
  - sanity check structurel statique
- `student/validation/RUNBOOK.md`
  - runbook opérateur complet
- `student/validation/HANDOFF.md`
  - état de livraison, périmètre couvert/non couvert, points de reprise
- `audit/2026-03-20/student_validation_pack_20260320.zip`
  - archive zip du pack complet (à transférer sur la machine Linux cible où /opt/trading/student est déployé)

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
- `GO_STUDENT_PHASE2_MIGRATION_01` → PARTIEL — livré dans `93_student_phase2_migration.md`
- `GO_STUDENT_CLEANUP_DUPLICATES_01` → LIVRÉ — livré dans `94_student_cleanup_duplicates.md`
- `GO_API_COLLECTOR_CANONICAL_MODULE_01` → LIVRÉ — livré dans `A0_api_collector_canonical_module.md`
- `GO_RUNTIME_SURFACES_CANONICAL_MAP_01` → LIVRÉ — livré dans `A1_runtime_surfaces_canonical_map.md`
- `GO_LOCALCMS_CANON_DECISION_01` → LIVRÉ — livré dans `A2_localcms_canon_decision.md`
- `GO_ALGO_HF_AUDIT_01` → LIVRÉ (passe documentaire) — livré dans `A3_algo_hf_audit.md`
- `GO_AUDIT_2026_03_20_FORMAL_CLOSE_01` → **LIVRÉ — PASSE CLÔTURÉE** — livré dans `A4_audit_2026_03_20_formal_close.md`
- `GO_STUDENT_LIVE_VALIDATION_PACK_01` → **LIVRÉ** — pack `student/validation/` créé (6 fichiers + zip)

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
