---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_DESKPRO_CONSUMER_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_DESKPRO_CONSUMER_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: closed
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_DESKPRO_CONSUMER_01

## Objectif

Implémenter PATCH-A3 : consumer read-only Desk Pro pour `vision_context.coinglass.v1`.

Lire `data/deskpro/inputs/vision_context/coinglass/latest.json` et injecter les métriques de vision dans le Snapshot Desk Pro, indépendamment du flux `market_metrics.v1`.

## Périmètre

- **IN** : `vision_context_reader.py`, wiring dans `aggregator.py`, 14 tests
- **OUT** : headless bot, parser OCR, tout write dans `data/`
- **Invariant fort** : aucun write dans `data/deskpro/inputs/market_metrics/`

## Architecture

`read_vision_context_coinglass(path)` → `List[Metric]`

- `input_class` ≠ `vision_context.coinglass.v1` → liste vide
- `extracted_value = null` → métrique ignorée
- `confidence` → qualité : ≥0.85→0.95, 0.60-0.84→0.70, <0.60→0.30
- Dégradation silencieuse sur fichier absent / JSON malformé

Agrégateur : `_augment_vision_context(snap)` appelé après `_augment_market_metrics`.

## Fichiers modifiés

| Fichier | Action |
|---|---|
| `modules/desk_pro/service/vision_context_reader.py` | créé |
| `modules/desk_pro/service/aggregator.py` | modifié — +import +`_augment_vision_context` |
| `tests/test_desk_pro_vision_context_reader.py` | créé |
