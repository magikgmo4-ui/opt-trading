---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_VISION_CONTEXT_SCHEMA_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_VISION_CONTEXT_SCHEMA_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_VISION_CONTEXT_SCHEMA_01

## Objectif

Implémenter le schéma Python `vision_context.coinglass.v1` (PATCH-A1) défini dans le contrat headless bot.

Créer :
- `modules/vision/coinglass/vision_context_v1.py` — dataclasses `Detection`, `VisionRefs`, `VisionContextCoinglassV1` avec `validate()` et `to_json()`
- `modules/vision/coinglass/tests/test_vision_context_v1.py` — 11 tests couvrant TC-SCHEMA-01..06

## Périmètre

- **IN** : dataclasses + invariants + sérialisation JSON
- **OUT** : parser réel, headless bot, Desk Pro consumer (PATCH-A2/A3)
- **OUT** : tout write dans `data/`

## Invariants implémentés

1. `contract_version` = `"v1"` — ValueError sinon
2. `input_class` = `"vision_context.coinglass.v1"` — ValueError sinon
3. `confidence < 0.5` → `warnings` non vide requis — ValueError sinon
4. `extracted_value` non-null + `confidence = 0` → BLOCKED — ValueError

## Fichiers modifiés

| Fichier | Action |
|---|---|
| `modules/vision/__init__.py` | créé (vide) |
| `modules/vision/coinglass/__init__.py` | créé (vide) |
| `modules/vision/coinglass/vision_context_v1.py` | créé |
| `modules/vision/coinglass/tests/__init__.py` | créé (vide) |
| `modules/vision/coinglass/tests/test_vision_context_v1.py` | créé |
