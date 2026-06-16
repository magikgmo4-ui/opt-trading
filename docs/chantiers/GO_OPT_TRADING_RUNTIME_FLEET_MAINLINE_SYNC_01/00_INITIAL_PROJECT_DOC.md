---
doc_id: GO_OPT_TRADING_RUNTIME_FLEET_MAINLINE_SYNC_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_RUNTIME_FLEET_MAINLINE_SYNC_01
GO_STRUCTURAL_ROLE: GO_CHILD
status: open
lifecycle_stage: operations
surface: runtime
source_kind: canonical
updated_at: 2026-06-16
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_GITHUB_ACTIONS_CHILD_RULESET_ENFORCEMENT_PROBE_01/PROBE_EVIDENCE.md
---

# 00_INITIAL_PROJECT_DOC — GO_OPT_TRADING_RUNTIME_FLEET_MAINLINE_SYNC_01

## 3_INITIAL_NEED

Synchroniser toutes les machines du fleet sur `sot/mainline` commit `615d387a` après validation du ruleset enforcement.

## 4_MASTER_PROJECT_PLAN

1. Documenter la procédure de sync par machine.
2. Exécuter sur chaque machine : git fetch, switch, pull --ff-only.
3. Vérifier que chaque machine est sur `615d387a`.

## 6_FINAL_TARGET

Fleet synchronisé : admin-trading, student, db-layer, cursor-ai sur `sot/mainline` à `615d387a`.

## 12_INVARIANTS

- Jamais de `git pull` avec merge commit — `--ff-only` uniquement.
- Jamais de push direct sur `sot/mainline`.
- Chaque machine vérifie `git log -1 --oneline` après sync.
