---
doc_id: ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: doc_reconciliation
surface: chantier
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/BRANCH_STATE.md
  - docs/index/GO_INDEX.md
---

# 00_START — Admin-Trading Branch Doc Reconciliation

## GO

GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Branche

N/A — doc-only, aucun runtime. Fichiers locaux sur sot/mainline.

## Contexte

La fiche de routage `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` liste 25 branches dans son bloc ADMIN_TRADING. La surface réelle GitHub (remote) contient ~60 branches go/GO_OPT_TRADING_ADMIN_TRADING_* (hors TMUX_IDE). BRANCH_STATE.md contient zéro entrée pour les branches GO_OPT_TRADING_ADMIN_TRADING_*. Écart documentaire constaté.

Le chantier actif le plus important est FIRST_14D_REVIEW_01 (PENDING_OBSERVATION jusqu'au 2026-05-28).

## Objectif

- Recroiser MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md, BRANCH_STATE.md, et les branches GitHub ADMIN_TRADING réelles
- Classer chaque branche : ACTIVE / REFERENCE / DROP_MERGED / A_VERIFIER
- Ne pas toucher au runtime
- Ne pas modifier les index globaux sauf nécessité prouvée et explicitée
- Produire un verdict clair + NEXT_GO recommandé

## Regles

- Doc-only — aucun runtime touché
- Aucune modification de timer/service/systemd
- Aucune modification des index globaux sans preuve
- La branche seule ne prouve pas un chantier actif

## RISKS

- À qualifier.
