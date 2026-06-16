---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_CHILD_RULESET_ENFORCEMENT_PROBE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_CHILD_RULESET_ENFORCEMENT_PROBE_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
status: open
lifecycle_stage: validation
surface: github_actions
source_kind: canonical
updated_at: 2026-06-16
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
---

# 00_INITIAL_PROJECT_DOC — GO_OPT_TRADING_GITHUB_ACTIONS_CHILD_RULESET_ENFORCEMENT_PROBE_01

## 1_MASTER_TARGET

github_actions_openclaw

## 3_INITIAL_NEED

Valider que le ruleset GitHub importé sur `sot/mainline` bloque réellement les PR non conformes.

## 4_MASTER_PROJECT_PLAN

1. Créer une PR volontairement invalide sans dossier chantier ni FILE_SCOPE.
2. Observer l'échec des gates.
3. Confirmer que le merge est bloqué par required checks.
4. Fermer la PR invalide sans merge.
5. Documenter la preuve dans ce GO valide.

## 6_FINAL_TARGET

Preuve documentée que les required checks bloquent les PR hors standard.

## 12_INVARIANTS

- Aucun bypass du ruleset.
- Aucun merge de PR invalide.
- Aucun changement runtime.
- Aucun changement workflow.
- PR mergée ≠ master target atteint.

## 17_RESUME_POINT

Après merge de cette PR documentaire, considérer le ruleset enforcement comme validé.
