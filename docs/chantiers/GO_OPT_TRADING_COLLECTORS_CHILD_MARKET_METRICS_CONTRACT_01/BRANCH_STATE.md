---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01_BRANCH_STATE
doc_type: branch_state
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# BRANCH_STATE

## Branche courante

```
go/GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01
```

## Base

```
sot/mainline  (après merge de #663 et #696)
```

## Fichiers créés

```
modules/derivatives_collector/app/market_metrics_v1.py
modules/derivatives_collector/tests/test_market_metrics_v1.py
docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01/BRANCH_STATE.md
docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01.md
```

## Vérification

```bash
python3 -m unittest modules.derivatives_collector.tests.test_market_metrics_v1 -v
git diff --name-only origin/sot/mainline...HEAD
git status --short
```
