# 00 — Cadrage Gaps Fill & Telegram Integration

## Parent
PF_BOT_VISION_HEADLESS — reste OUVERT.

## GO
```
GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_GAPS_FILL_AND_TELEGRAM_INTEGRATION_01
```

## Gaps comblés (depuis 10_RESULTS_AND_NEXT_GO.md)

| # | Gap | Résultat |
|---|-----|----------|
| 4 | Envoi Telegram effectif | Intégré : telegram_filter → shared/telegram_notify.send_telegram() |
| 5 | Market hours | Implémenté dans capture_headless.js (US market, crypto 24/7, forex) |
| 6 | TOTAL / TOTAL2 / TOTAL3 / BTC.D | Profils créés dans profiles.supplementary.json |
| 7 | FBTC, GBTC, BITB, ARKB | Profils créés dans profiles.supplementary.json |
| 8 | BZUSDT (Brent) | Profil créé dans profiles.supplementary.json |
| 9 | Essence (RB1!) | Non couvert (source non définie) |
| 10 | Screeners stocks | Screener biggest_caps créé dans profiles.supplementary.json |
| 11 | NEWS_SENTIMENT | Non couvert (source non définie) |
| 12-14 | Orchestration | Non couvert (GO futur dédié) |
| 15-17 | Qualité (cross-validation, dedup, throttling) | Non couvert (GO futur dédié) |

## Fichiers créés
- profiles.supplementary.json — 14 nouveaux profils de capture
- tests/test_gaps_fill.py — 27 tests
- docs/chantiers/.../00_CADRAGE.md + 01_TARGETS.md + 02_RESULTS.md

## Fichiers modifiés
- capture_headless.js — market hours enforcement (isInMarketHours)
- run_vision_pipeline.py — Telegram effectif (--no-telegram, --telegram-threshold)
- capture_map.json — version bump 1.1.0
