---
doc_id: DB_LAYER_A_VERIFIER_REVIEW_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01
parent_go: GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01
status: active
lifecycle_stage: review
surface: chantier
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_DB_LAYER_BRANCH_STATE_SEED_01/10_BRANCH_STATE_SEED.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/BRANCH_STATE.md
---

# 00_START - DB_LAYER A_VERIFIER Review

## GO

GO_OPT_TRADING_DB_LAYER_A_VERIFIER_REVIEW_01

## Scope

Revue doc-only des 10 branches `A_VERIFIER` de la surface `db-layer/OpenClaw`.

## Contraintes

- doc-only
- aucun runtime `db-layer/OpenClaw`
- ne pas relancer TMUX
- ne rouvrir aucun child runtime
- ne pas toucher `admin-trading`
- aucune suppression Git
- aucun cleanup
- ne pas modifier `GO_INDEX` / `ACTIVE_STREAMS` / `REPRISE`

## But

Reclassifier chaque branche en `KEEP_ACTIVE`, `KEEP_REFERENCE`, `DROP_MERGED` ou `A_VERIFIER` avec preuve repo/doc.

## RISKS

- À qualifier.
