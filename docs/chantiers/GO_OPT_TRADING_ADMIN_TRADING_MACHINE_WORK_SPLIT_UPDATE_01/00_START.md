---
doc_id: ADMIN_TRADING_MWS_UPDATE_01_START
doc_type: chantier_start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01
parent_go: GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01
status: active
lifecycle_stage: doc_reconciliation
surface: chantier
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01/10_RECONCILIATION.md
---

# 00_START — Update MACHINE_WORK_SPLIT ADMIN_TRADING block

## GO

GO_OPT_TRADING_ADMIN_TRADING_MACHINE_WORK_SPLIT_UPDATE_01

## Parent

GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 (OPEN)

## Branche

N/A — doc-only update sur sot/mainline. Aucun runtime.

## Contexte

Suite directe de `GO_OPT_TRADING_ADMIN_TRADING_BRANCH_DOC_RECONCILIATION_01` (PASS). La réconciliation a montré que le bloc ADMIN_TRADING de `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` couvre 25/54 branches réelles. Ce GO met à jour le bloc pour refléter l'état complet classifié.

## Objectif

- Mettre à jour uniquement le bloc ADMIN_TRADING dans `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- Utiliser la classification de la réconciliation (ACTIVE / REFERENCE / DROP_MERGED / A_VERIFIER)
- Distinguer les sous-blocs pour lisibilité

## Regles

- Ne pas toucher au runtime admin-trading
- Ne pas toucher aux timers/services/systemd
- Ne pas modifier BRANCH_STATE.md, GO_INDEX, ACTIVE_STREAMS, REPRISE
- Une branche seule ne prouve pas un chantier actif
- Ne pas exécuter de cleanup Git

## RISKS

- À qualifier.
