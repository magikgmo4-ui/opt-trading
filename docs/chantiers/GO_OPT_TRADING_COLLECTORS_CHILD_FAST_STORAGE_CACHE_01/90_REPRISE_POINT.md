---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: derivatives_collector
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01
status: closed
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE_POINT

## État au merge

- Branche : `go/GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01`
- Tests : 25 writer + 22 reader = 47 PASS
- Verdict : ACCEPTED

## Fichiers clés

```text
modules/derivatives_collector/app/market_metrics_writer.py   ← writer principal
modules/derivatives_collector/tests/test_market_metrics_writer.py
```

## Reprendre depuis ici

Pour intégrer le writer dans le flux lifecycle :

1. Appeler `write_market_metrics_latest(payload, root)` après `build_latest()` dans `lifecycle_compat.py`.
2. Appeler `write_market_metrics_by_symbol(payload, root)` pour chaque symbole collecté.
3. Appeler `publish_market_metrics_for_deskpro(payload, root)` en fin de run.
4. Le payload doit être un `MarketMetricsV1` construit depuis les `DerivativesRow` collectés.

## Absorption dans PF_DATA_CENTER

Ce child GO est **absorbé** dans :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_STORAGE_RECONCILE_01
```

Ne pas merger `GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01` en standalone.

Raison : le storage/cache doit être canonique sous `data/data_center/`, pas seulement `data/collectors/`. Le writer a été étendu avec `write_market_metrics_to_data_center()` et `publish_market_metrics()` dans le child Data Center.

## Prochain GO recommandé

`GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01` — tests smoke de compatibilité contractuelle Data Center.
