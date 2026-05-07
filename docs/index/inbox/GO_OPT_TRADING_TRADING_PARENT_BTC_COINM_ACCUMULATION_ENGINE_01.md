---
doc_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01_INBOX_ENTRY
doc_type: index_inbox_entry
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
status: draft_for_user_validation
lifecycle_stage: parent_opening_draft
topic_keys:
  - opt-trading
  - trading
  - btc
  - coin-m
  - accumulation
  - short-engine
surface: index_inbox
source_kind: atomic_index_entry
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
point_de_reprise: "Valider ou corriger le document parent initial avant tout worker, backtest ou execution."
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# Inbox — GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01

## Etat

`draft_for_user_validation`

## Objet

Chantier parent documentaire pour formaliser un moteur mathematique d'accumulation BTC avec :

- DCA spot ;
- marge COIN-M en BTC ;
- shorts COIN-M pour profiter des baisses sans vendre le BTC accumule ;
- variables, bornes, invariants, stress tests ;
- worker calculateur, correcteur et optimiseur a definir apres validation.

## Reprise

Document principal :

`docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md`

Prochaine action : validation ou correction utilisateur.

## Invariants courts

```text
- pas d'execution live
- pas de worker avant validation
- pas de vente du BTC spot accumule dans le modele strategique normal
- short COIN-M = moteur de profit sur baisse, non hedge principal
```
