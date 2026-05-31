# 02 — Results

## Tests

```
tests/test_gaps_fill.py ........................... 27/27 PASS
tests/test_vision_pipeline_outputs.py ............. 37/37 PASS
Total ................................................. 64/64 PASS
```

## Fichiers

### Nouveaux

| Fichier | Lignes | Description |
|---------|--------|-------------|
| profiles.supplementary.json | 142 | 14 profils de capture pour assets manquants |
| tests/test_gaps_fill.py | 182 | 27 tests : profils, market hours, Telegram |

### Modifiés

| Fichier | Changement |
|---------|-----------|
| capture_headless.js | +68 lignes : MARKET_HOURS_ENABLED, MARKET_HOURS_RULES, MARKET_HOURS_MAP, isInMarketHours(), skip + sidecar |
| run_vision_pipeline.py | --no-telegram flag, --telegram-threshold, appel réel à shared/telegram_notify.send_telegram() |
| capture_map.json | Version 1.1.0, timestamp mis à jour |

## Commandes de vérification

```bash
# Tous les tests
python3 -m pytest tests/test_gaps_fill.py tests/test_vision_pipeline_outputs.py -v

# Pipeline avec les nouveaux profils
python3 scripts/run_vision_pipeline.py --profile profiles.supplementary.json --dry-run

# Pipeline complète avec Telegram
python3 scripts/run_vision_pipeline.py --profile profiles.production.json --telegram-threshold 0.80

# Désactiver market hours
BOT_VISION_MARKET_HOURS=0 node capture_headless.js --profile profiles.production.json --once
```

## Gaps restants (non couverts par ce GO)

| Gap | Raison | GO futur |
|-----|--------|----------|
| OCR Coinglass (A-07) | Nécessite implémentation analyseur | CHILD_OCR_COINGLASS_01 |
| Screener analyzer (A-08) | Nécessite implémentation analyseur | CHILD_SCREENER_ANALYZER_01 |
| News sentiment (A-09) | Source non définie | CHILD_NEWS_SENTIMENT_01 |
| Essence (RB1!) | Source non définie | CHILD_PROFILES_EXTENSION_02 |
| 6 autres screeners | Profils restants | CHILD_PROFILES_EXTENSION_02 |
| Orchestrateur central | GO volumineux | CHILD_PIPELINE_ORCHESTRATOR_01 |
| Cross-validation / dedup / throttling | Qualité | CHILD_PIPELINE_QUALITY_01 |
