---
doc_id: GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01_NEXT_GO_CANDIDATES
doc_type: next_candidates
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01
status: final
lifecycle_stage: global_closeout
topic_keys:
  - opt-trading
  - next-go
  - candidates
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01/03_NEXT_GO_CANDIDATES.md
point_de_reprise: "Prochains GO candidats."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_SESSION_CLOSEOUT_MULTI_CHAIN_01/02_INVARIANTS_AND_DEFERRED.md
---

# 03_NEXT_GO_CANDIDATES

## 1_PRIORITE 1

```text
GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01
```

Raison : cluster VISION cartographie en P2 (#253), paire canonique definie,
plan runtime pose (#256), wrapper unifie implemente (#260).
La suite logique est de stabiliser la paire vision_bot + bot_vision_step2.

## 2_PRIORITE 2

```text
GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_EXECUTION_01
```

Raison : chaîne BTC COIN-M restee en attente apres #244 (DATA_PREP).
Les formules sont PAPER_LOCKED, le pipeline de donnees est defini.
Le backtest reel peut etre execute.

## 3_PRIORITE 3

```text
GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_CLOSEOUT_01
```

Raison : chaîne observability livree en 4 phases + README.
Un closeout final peut figer l'etat et proposer les suites (circuit breaker actif, dashboard temps reel).
```

## 4_POINT DE REPRISE CANONIQUE

```text
docs/product/PRODUCT_USAGE_MATRIX.md
```
