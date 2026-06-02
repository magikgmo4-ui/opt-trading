---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: derivatives_collector
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: closed
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 00_INITIAL_PROJECT_DOC — Fast Storage Cache

## Objectif

Implémenter le stockage rapide `market_metrics.v1` via trois fonctions de publication :

- `write_market_metrics_latest` → `data/collectors/derivatives/latest.json`
- `write_market_metrics_by_symbol` → `data/collectors/derivatives/cache/by_symbol/<SYMBOL>.json`
- `publish_market_metrics_for_deskpro` → `data/deskpro/inputs/market_metrics/latest.json` + `by_symbol/`

## Parent

`GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01` — Plan de stockage défini dans `30_STORAGE_AND_INGESTION_PLAN.md`.

## Contraintes

- Aucun appel Binance / Bitget live.
- Aucune écriture DB.
- Aucune écriture Sheets.
- Aucun envoi Telegram.
- Ne pas modifier Coinglass Vision.
- Ne pas toucher aux gros index globaux.
- Ne pas casser les exports legacy JSON/CSV derivatives.
- `not_proven_runtime_adapter` → ne jamais écrire, retourner `None`.

## Fichiers cibles

| Fichier | Rôle |
|---|---|
| `modules/derivatives_collector/app/market_metrics_writer.py` | Trois fonctions de publication |
| `modules/derivatives_collector/tests/test_market_metrics_writer.py` | Suite unittest (25 tests) |

## Chemins de sortie

```text
data/collectors/derivatives/latest.json
data/collectors/derivatives/cache/by_symbol/<SYMBOL>.json
data/deskpro/inputs/market_metrics/latest.json
data/deskpro/inputs/market_metrics/by_symbol/<SYMBOL>.json
```

## Dépendances

- `modules/derivatives_collector/app/market_metrics_v1.py` — contrat `MarketMetricsV1`
- `modules/desk_pro/service/market_metrics_reader.py` — consumer Desk Pro validé en test

## Validation

```bash
python3 -m unittest modules.derivatives_collector.tests.test_market_metrics_writer -v
python3 -m pytest tests/test_desk_pro_market_metrics_reader.py -q
git diff --check
```
