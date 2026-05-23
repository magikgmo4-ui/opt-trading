---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_TELEGRAM_SUMMARY_B2_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_TELEGRAM_SUMMARY_B2_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_TELEGRAM_SUMMARY_B2_01

## Objectif

Implémenter PATCH-B2 : résumé Telegram read-only des données vision Coinglass.

`format_vision_summary()` formate un `VisionContextCoinglassV1` en message HTML Telegram. `load_and_format()` charge `data/vision/coinglass/latest.json` et retourne le message.

## Invariants

1. Seules les valeurs présentes dans `ctx.detections` apparaissent — aucune valeur inventée.
2. `confidence < 0.85` → tag warning explicite (`⚠ conf=XX%`).
3. `confidence < 0.60` → tag `✗ (low)`.
4. `extracted_value = null` → affiché `N/A`.
5. Aucun write — lecture seule.

## Périmètre

- **IN** : `telegram_summary.py`, 12 tests
- **OUT** : send Telegram réel (caller responsable), activation prod

## Fichiers modifiés

| Fichier | Action |
|---|---|
| `modules/vision/coinglass/telegram_summary.py` | créé |
| `modules/vision/coinglass/tests/test_telegram_summary.py` | créé |
