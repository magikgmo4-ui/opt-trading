---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE_POINT

## État au merge

- Branche : `go/GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01`
- Tests : 28 reader + 28 contract + 42 writer + 11 layout = **119 PASS**
- Verdict : ACCEPTED

## Fichiers clés

```text
modules/desk_pro/service/market_metrics_reader.py   ← reader migré
tests/test_desk_pro_market_metrics_reader.py         ← 6 nouveaux tests hierarchy
modules/data_center/registry/consumers.json          ← migration_needed → false
modules/data_center/tests/test_contract_tests.py     ← test_desk_pro_migration_complete
```

## Reprendre depuis ici

La migration Desk Pro est complète. Prochaines étapes possibles :

1. **Migrer les autres consumers `latest_only`** (`telegram_screener`, `google_sheets`) de la même façon : modifier leurs readers pour utiliser `data/data_center/views/market_metrics/latest.json`.
2. **`perf_engine__replay_context`** — accès `full_history/normalized/` — requiert une vue historique dédiée dans `data/data_center/views/market_metrics/history/` (GO futur).
3. **Supprimer le fallback legacy** — une fois que tous les consumers lisent la vue DC depuis suffisamment longtemps, `MARKET_METRICS_LEGACY` peut être retiré (GO de nettoyage).
