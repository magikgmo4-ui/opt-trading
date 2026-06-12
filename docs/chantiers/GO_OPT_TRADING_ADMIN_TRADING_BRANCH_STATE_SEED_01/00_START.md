---
doc_id: ADMIN_TRADING_BRANCH_STATE_SEED_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: doc_reconciliation
surface: chantier
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/index/BRANCH_STATE.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01/
---

# 00_START — Seed BRANCH_STATE.md for admin-trading

## GO

GO_OPT_TRADING_ADMIN_TRADING_BRANCH_STATE_SEED_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Contexte

Suite de MACHINE_WORK_SPLIT_UPDATE_01 (PASS). BRANCH_STATE.md contient 0 entrées pour les 63 branches ADMIN_TRADING. Ce GO seed le tableau canonique avec les données git réelles.

## Objectif

- Ajouter les 57 branches go/GO_OPT_TRADING_ADMIN_TRADING_* et 6 branches go/GO_TMUX_IDE_* dans BRANCH_STATE.md
- Utiliser la classification de MACHINE_WORK_SPLIT (ACTIVE/REFERENCE/DROP_MERGED/A_VERIFIER) convertie en CANON_STATUS
- Avec aide/retard git réel (ahead/behind)
- Aucun cleanup, aucun runtime touché

## Regles

- Doc-only — aucun runtime touché
- Aucune modification des index globaux hors BRANCH_STATE.md
- Aucun cleanup Git
- 2 nouvelles branches non classées (PNL_ALERT_THRESHOLDS, SEQUENCE_PR_MERGE) mises en A_VERIFIER

## RISKS

- À qualifier.
