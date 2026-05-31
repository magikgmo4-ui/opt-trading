# 00 — Cadrage OCR Coinglass

## Parent
PF_BOT_VISION_HEADLESS — reste OUVERT.

## GO
```
GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_OCR_COINGLASS_01
```

## Gap comblé
Depuis `10_RESULTS_AND_NEXT_GO.md` gap #1 : **OCR Coinglass (A-07)**.

## Pipeline
```
capture Coinglass (profile.coinglass.json)
→ coinglass_ocr_analyzer.py (extraction métriques)
→ vision_context_writer.py (vision_context.coinglass.v1)
→ DeskPro (vision_context_reader.py existe déjà)
→ Data Center (views/vision_context/)
```

## Screen types couverts
- LIQUIDITY_COINGLASS — liquidations, heatmap levels
- FUNDING_COINGLASS — funding rates
- OI_COINGLASS — open interest
- LS_RATIO_COINGLASS — long/short ratio

## Modes
- **Stub** (défaut) : génère des valeurs réalistes par symbole et screen type — testable sans OCR
- **Real OCR** (`--real-ocr`) : utilise pytesseract si disponible

## Fichiers créés
- scripts/coinglass_ocr_analyzer.py
- scripts/vision_context_writer.py
- tests/test_ocr_coinglass.py (17 tests)
- tests/fixtures/capture_mapping/vision_context_coinglass_v1_sample.json
- docs/chantiers/.../00_CADRAGE.md, 01_TARGETS.md, 02_RESULTS.md

## Fichiers modifiés
- scripts/run_vision_pipeline.py — dispatch Coinglass vers OCR analyzer + writer
