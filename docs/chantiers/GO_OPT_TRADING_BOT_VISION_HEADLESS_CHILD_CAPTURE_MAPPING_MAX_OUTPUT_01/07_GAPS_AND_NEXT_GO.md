---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01_GAPS
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
---

# 07_GAPS_AND_NEXT_GO.md

Gaps restants et prochaines actions.

## 1_GAPS_REPERTOIRE

### Input / Capture

| # | Gap | Priorité | Solution |
|---|-----|----------|----------|
| G-01 | URLs TradingView avec paramètres exactes non stabilisées | P0 | Profile Playwright par asset |
| G-02 | Multi-chart 2x2 non couvert par profiles existants | P0 | Créer profile dashboard macro |
| G-03 | Coinglass URLs non stabilisées (sections, filtres) | P0 | Profile Playwright par page Coinglass |
| G-04 | Screen types non normalisés en code | P1 | Implémenter enum screen_type dans bot_vision_step2 |
| G-05 | Layout multi-chart non géré par capture_headless.js | P1 | Ajouter support layout dans le profile |
| G-06 | Screener TV colonnes/filtres non figés | P1 | Documenter la configuration screener |

### Analyse

| # | Gap | Priorité | Solution |
|---|-----|----------|----------|
| G-07 | Analyseur OCR Coinglass non existant | P0 | Nouvel analyseur (OCR texte) |
| G-08 | Analyseur screener stocks non existant | P1 | Nouvel analyseur (table → LLM) |
| G-09 | bot_vision_step2 ne produit pas vision_analysis.v1 | P1 | Adapter sortie bot_vision_step2 |
| G-10 | Score de confiance non calibré | P2 | Calibration sur échantillon |

### Infrastructure

| # | Gap | Priorité | Solution |
|---|-----|----------|----------|
| G-11 | Trigger engine événementiel non existant | P1 | Module séparé ou intégré à bot_vision_step2 |
| G-12 | Data Center ingestion vision non existante | P1 | Endpoint POST + fallback fichier |
| G-13 | Canal DeskPro non branché pour vision_analysis.v1 | P1 | Adapter desk_pro/service/vision_analysis_reader |
| G-14 | desk_snapshot_ingest ne connaît pas les nouveaux screen types | P1 | Étendre le parser de noms de fichiers |
| G-15 | Vision analysis reader non intégré au runtime DeskPro | P2 | Brancher dans desk_pro_runner |

### Télémétrie

| # | Gap | Priorité | Solution |
|---|-----|----------|----------|
| G-16 | Pas de métriques sur le pipeline vision | P2 | Ajouter métriques runtime_health |
| G-17 | Pas d'alerte si capture échoue > N cycles | P2 | Watchdog dans bot_vision_step2 |

## 2_GAPS_RESOLUS

| Gap | Résolution |
|-----|-----------|
| G-CAP-01 (profile BTCUSDT) | ✅ profiles.btcusdt_poc.json créé |
| G-AN-01 (analyseur LLM) | ✅ bot_vision_step2 existant |
| G-DP-01 (vision_analysis DeskPro) | ✅ Stub via run_vision_pipeline.py |
| G-INT-01 (pipeline E2E) | ✅ Validé sur admin-trading |

## 3_PLAN_D_ACTION

| # | Action | Priorité | Dépend de |
|---|--------|----------|-----------|
| A-01 | Créer profile multi-chart 2x2 (BTC, Gold, DXY, Oil) | P0 | — |
| A-02 | Créer profile Coinglass liquidation | P0 | — |
| A-03 | Ajouter screen_type dans les métadonnées de capture | P0 | A-04 |
| A-04 | Implémenter enum screen_type | P1 | — |
| A-05 | Analyser les URLs exactes TV par actif | P0 | — |
| A-06 | Étendre bot_vision_step2 pour produire vision_analysis.v1 | P1 | A-04 |
| A-07 | Créer analyseur OCR Coinglass | P0 | — |
| A-08 | Créer analyseur screener stocks | P1 | — |
| A-09 | Brancher desk_snapshot_ingest pour les nouveaux screen types | P1 | A-04 |

## 4_NEXT_GO_RECOMMANDE

```text
GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PROFILES_AND_SCREENTYPES_01
```

Objectif : stabiliser les profiles Playwright pour tous les assets P0 +
implémenter l'enum screen_type dans les métadonnées de capture.

Livrables :
1. Profiles multi-chart 2x2 (dashboard macro)
2. Profiles Coinglass (liquidation, funding, OI, L/S)
3. Enum screen_type dans capture_headless.js
4. Sidecar JSON avec screen_type
5. Routage screen_type → analyseur dans bot_vision_step2
