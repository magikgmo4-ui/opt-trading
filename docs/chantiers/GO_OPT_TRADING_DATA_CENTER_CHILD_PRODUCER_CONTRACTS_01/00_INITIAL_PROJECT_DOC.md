---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
pf_id: PF_DATA_CENTER
status: open
lifecycle_stage: implementation
surface: modules/data_center
source_kind: canonical
created_at: 2026-05-28
updated_at: 2026-05-28
upstream:
  - GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01/00_INITIAL_PROJECT_DOC.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01 — INITIAL_PROJECT_DOC

## Objectif

Définir et formaliser les contrats producers du Data Center : format, schéma,
validation et règles d'écriture pour chaque producteur de données.

## 1_MASTER_TARGET

```text
collector -> producer contract -> normalized data -> data/data_center/
```

Producteurs identifiés :
- `derivatives_collector` — OI, Funding Rate, Liquidations, Long/Short
- `collector_binance_spot` — Binance public market data
- `collector_coingecko` — Coingecko market data
- Futurs collecteurs Telegram/Vision/Webhook

Contrat de référence : `market_metrics.v1` (défini dans GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01).

## 17_RESUME_POINT

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01
```
