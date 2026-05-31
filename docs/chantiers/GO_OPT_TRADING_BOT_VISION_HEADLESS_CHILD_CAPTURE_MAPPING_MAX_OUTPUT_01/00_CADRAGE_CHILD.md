# 00 — Cadrage Child GO

## Parent
**PF_BOT_VISION_HEADLESS** — reste OUVERT (non clos par ce GO).

## GO
```
GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
```

## Nature
**Implementation + résultats** — pas un chantier doc-only.

Le cœur est :
```
captures réelles
→ analyse vision par type d'écran
→ JSON exploitable (vision_analysis.v1)
→ ingestion Data Center
→ sortie DeskPro
→ résumé Telegram filtré
→ preuves de résultats
```

## Périmètre
- Définir les **assets** à capturer (crypto, macro, ETF, commodities, screeners)
- Définir les **screen types** et leur classification
- Définir les **triggers** (fréquences, conditions)
- Définir les **outputs** : capture_metadata, vision_analysis.v1, DeskPro, Data Center, Telegram
- Produire une **pipeline minimale exécutable** réutilisant l'existant (bot_vision_step2, headless_capture, desk_snapshot_ingest)
- Produire des **fixtures, tests, et preuves de résultats**

## Hors périmètre
- Fermeture de PF_BOT_VISION_HEADLESS
- Création d'une pipeline concurrente à bot_vision_step2
- Modification des index globaux (sauf changement global prouvé)
- Implémentation des analyseurs OCR Coinglass (A-07) ou screener (A-08) — ces sujets sont des GOs futurs

## Dépendances
- modules/bot_vision/headless_capture/ (Node.js + Playwright) — capture
- modules/bot_vision_step2/ (Python + OpenAI) — analyse vision
- modules/desk_snapshot_ingest/ — ingestion snapshots DeskPro
- modules/desk_pro/ — readers DeskPro (vision_analysis_reader, vision_context_reader)
- modules/data_center/ — ingestion Data Center
- shared/telegram_notify.py — envoi Telegram

## Réutilisation
Ce GO ne crée **pas** de pipeline concurrente. Il ajoute :
1. Un registre machine des assets/screens (*.json)
2. Un writer vision_analysis.v1 (transforme sortie bot_vision_step2 → contrat DeskPro/DC)
3. Un filtre Telegram (résumé court seulement si signal pertinent)
4. Des fixtures et tests de validation
5. L'intégration dans run_vision_pipeline.py existant
