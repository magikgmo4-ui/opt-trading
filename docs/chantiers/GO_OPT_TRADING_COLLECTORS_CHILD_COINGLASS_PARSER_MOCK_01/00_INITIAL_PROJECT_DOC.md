---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PARSER_MOCK_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PARSER_MOCK_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PARSER_MOCK_01

## Objectif

Implémenter PATCH-A2 : fixtures de test et parser mock pour `vision_context.coinglass.v1`.

Le parser est conçu avec injection de `extraction_fn` — découplé du moteur OCR/AI réel (PATCH-B1). Les tests passent sans dépendance externe.

## Périmètre

- **IN** : fixtures JSON/PNG, `modules/vision/coinglass/parser.py`, 7 tests
- **OUT** : OCR réel, headless bot, Desk Pro consumer
- **OUT** : tout write dans `data/`

## Fixtures créées

```
tests/fixtures/vision/coinglass/
  screenshot_mock_liquidations.png   — PNG synthétique 100x60 (30,30,30)
  vision_coinglass_v1_valid.json     — payload valide 2 détections
  vision_coinglass_v1_low_conf.json  — confidence 0.35 + warning
  vision_coinglass_v1_null_vals.json — extracted_value null, freshness stale
```

## Architecture parser

`parse_screenshot(image_path, screenshot_ts, extraction_fn, confidence_threshold)` retourne `(detections, warnings, freshness_state)`.

- `extraction_fn` injectée — mock en tests, OCR réel en PATCH-B1
- `confidence < 0.6` → `extracted_value = null` + warning
- Screenshot > 4h → `freshness_state = "stale"`
- Fichier absent ou exception → liste vide, dégradation silencieuse

## Fichiers modifiés

| Fichier | Action |
|---|---|
| `modules/vision/coinglass/parser.py` | créé |
| `modules/vision/coinglass/tests/test_parser_mock.py` | créé |
| `tests/fixtures/vision/coinglass/*.png` | créé |
| `tests/fixtures/vision/coinglass/*.json` (×3) | créé |
