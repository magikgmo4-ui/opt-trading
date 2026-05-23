---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01_BRANCH_STATE
doc_type: branch_state
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01
status: open
created_at: 2026-05-23
---

# BRANCH_STATE

## Branche

```
go/GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01
```

## Base

```
sot/mainline  (après merge de #696, #698, #699, #703, #704)
```

## Fichiers modifiés/créés

```
modules/derivatives_collector/app/bitget_adapter.py             (modifié — +20 lignes)
modules/derivatives_collector/tests/test_bitget_liquidations_patch.py  (nouveau — 10 tests)
docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01/BRANCH_STATE.md
docs/index/inbox/GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01.md
```

## Vérification

```bash
python3 -m unittest modules.derivatives_collector.tests.test_bitget_liquidations_patch -v  # 10 passed
git diff --name-only origin/sot/mainline...HEAD
git status --short
```
