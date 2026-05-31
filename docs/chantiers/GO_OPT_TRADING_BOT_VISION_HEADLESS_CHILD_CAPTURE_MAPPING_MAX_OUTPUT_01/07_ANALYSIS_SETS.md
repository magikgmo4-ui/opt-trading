# 07 — Analysis Sets

## Configuration par screen type

### CHART_TECHNICAL / ETF_CRYPTO

| Paramètre | Valeur |
|-----------|--------|
| Analyzer | bot_vision_step2 analyze_latest |
| Mode | single (1 chart → 1 analyse) |
| Prompt | Français : tendance, structure HH/HL/LH/LL, S/R, scénario, invalidation |
| Modèle | gpt-4.1-mini (configurable via OPENAI_MODEL) |
| Sortie | analysis.txt, analysis.md, summary.json + signals JSON |
| Resume image | 1280x720 JPEG, quality 75 |

### DASHBOARD_MACRO

| Paramètre | Valeur |
|-----------|--------|
| Pre-processing | compose_quad.py (4 captures → 1 image 1920x1080) |
| Analyzer | bot_vision_step2 analyze_latest |
| Mode | quad (CROP_MODE=quad → 4 quadrants analysés) |
| Prompt | Français, spécifique dashboard 2x2 (4 charts décrits) |
| Modèle | gpt-4.1-mini |
| Sortie | analysis.txt/md, summary.json + signals par quadrant |

### Coinglass (LIQUIDITY, FUNDING, OI, LS_RATIO)

| Paramètre | Valeur |
|-----------|--------|
| Analyzer | **Stub** (OCR analyzer A-07 TBD) |
| Comportement actuel | Capture sauvegardée, écriture stub vision_analysis.v1 |
| Sortie actuelle | Stub avec note "OCR Coinglass analyzer not yet implemented" |

### SCREENER_STOCKS

| Paramètre | Valeur |
|-----------|--------|
| Analyzer | **Stub** (screener analyzer A-08 TBD) |
| Comportement actuel | Capture sauvegardée, écriture stub |
| Sortie actuelle | Stub avec note "Screener analyzer not yet implemented" |

### NEWS_SENTIMENT

| Paramètre | Valeur |
|-----------|--------|
| Analyzer | **Stub** (sentiment analyzer A-09 TBD) |
| Comportement actuel | Non implémenté |

## Pipeline d'analyse actuelle

Dans `run_vision_pipeline.py` :
1. Capture → `capture_headless.js` (Node.js/Playwright)
2. (optionnel) Composition quad → `compose_quad.py`
3. Stub vision_analysis → écriture `data/deskpro/inputs/vision_analysis/latest.json`
4. Délégation → `bot_vision_step2 analyze_latest` (si disponible)
5. **Nouveau** : Publication vision_analysis.v1 → `vision_analysis_writer.py`
6. **Nouveau** : Filtre Telegram → `telegram_filter.py`

## Vision analysis writer

`scripts/vision_analysis_writer.py` transforme la sortie de bot_vision_step2 (summary.json) au format `vision_analysis.v1` :
- Extrait les signaux structurés du JSON DeskPro (supports, resistances)
- Fallback sur extraction regex depuis le texte d'analyse
- Publie vers DeskPro et Data Center

## Gaps

- Analyseurs OCR Coinglass, screener, news sentiment : TBD
- Pas de validation croisée des signaux (confirmation multi-timeframe)
- Pas d'agrégation multi-source (même signal issu de plusieurs analyses)
