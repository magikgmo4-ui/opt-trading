---
doc_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01_INBOX_ENTRY
doc_type: index_inbox_entry
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
status: initial_doc_validated
lifecycle_stage: variables_bounds_opening
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
point_de_reprise: "Continuer sur 02_variables_bounds.md : deposer les variables, bornes, domaines, contraintes et garde-fous reels."
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# Inbox — GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01

## Etat

`initial_doc_validated`

## Validation

VERDICT utilisateur : `PASS`.

Le document initial `01_initial_project_doc.md` est accepte comme base canonique du chantier parent.

## Objet

Chantier parent documentaire pour formaliser un moteur mathematique d'accumulation BTC avec :

- DCA spot ;
- marge COIN-M en BTC ;
- shorts COIN-M pour profiter des baisses sans vendre le BTC accumule ;
- variables, bornes, invariants, stress tests ;
- worker calculateur, correcteur et optimiseur a definir apres validation des bornes.

## Reprise

Document principal valide :

`docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md`

Document courant :

`docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md`

Prochaine action : completer et valider les variables, bornes et garde-fous reels.

## Invariants courts

```text
- pas d'execution live
- pas de worker avant validation des variables/bornes
- pas de vente du BTC spot accumule dans le modele strategique normal
- short COIN-M = moteur de profit sur baisse, non hedge principal
- z_short > z_dca reste une contrainte candidate a tester et borner
```
