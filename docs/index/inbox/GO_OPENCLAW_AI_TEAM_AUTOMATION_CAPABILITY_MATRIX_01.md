---
doc_id: GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01_INBOX
doc_type: inbox
repo: opt-trading
project: opt-trading
go_id: GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: impl
surface: index
source_kind: canonical
created_at: 2026-05-21
links:
  - docs/chantiers/GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01/10_CAPABILITY_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/50_PREPARED_MATRIX.md
---

# GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01

## Objet

Matrice consolidée actor × surface × permission × gate (GAP_01 du parent automation gaps).

## Périmètre

- 6 acteurs × 10 surfaces = matrice cible
- Permissions : read, draft, patch_draft, write_gated, forbidden
- Gates : none, dry_run, human_approve, dual_confirm
- 3 scénarios de validation
- 30 lignes pré-remplies dans la matrice

## Prochaine étape

Remplir les evidence_ref, exécuter les scénarios de validation, passer les lignes en PASS_WITH_EVIDENCE.
