# 02 — Results

## Tests

```
tests/test_orchestrator.py ............... 17/17 PASS
tests/test_ocr_coinglass.py .............. 17/17 PASS
tests/test_gaps_fill.py .................. 27/27 PASS
tests/test_vision_pipeline_outputs.py .... 37/37 PASS
──────────────────────────────────────────────────
Total .................................................. 98/98 PASS
```

## Fichiers

### Nouveaux
| Fichier | Description |
|---------|-------------|
| scripts/schedule_orchestrator.py | Orchestrateur central (300+ lignes) |
| scripts/run_orchestrator.sh | Runner shell pour systemd |
| systemd/bot-vision-orchestrator.service | Systemd oneshot service |
| systemd/bot-vision-orchestrator.timer | Timer 10min |
| tests/test_orchestrator.py | 17 tests : scheduling, dispatch, CLI, state, market hours |
| docs/chantiers/.../ | Documentation |

## Capacités de l'orchestrateur

- Lit 3 configs (capture_map, trigger_config, screen_types)
- Charge 4 fichiers de profils (production, coinglass, macro, supplementary)
- Résout le schedule par asset override → screen_type default → fallback
- Applique market hours (délègue au JS capture_headless.js)
- Applique cooldown après N échecs consécutifs
- Dispatche 3 analyseurs (bot_vision_step2, OCR Coinglass, stub)
- Publie vision_analysis.v1 + vision_context.coinglass.v1
- Sauve état persistant (state.json + cooldown.json)
- Compatible systemd timer + CLI interactive
- Mode dry-run / force-all / once / reset-state

## Gaps non couverts (reste)

| Gap | GO futur |
|-----|----------|
| Screener analyzer (A-08) | CHILD_SCREENER_ANALYZER_01 |
| News sentiment (A-09) | CHILD_NEWS_SENTIMENT_01 |
| Essence + 6 screeners | CHILD_PROFILES_EXTENSION_02 |
| Cross-validation, dedup, throttling | CHILD_PIPELINE_QUALITY_01 |
| Data Center registry update | CHILD_DC_REGISTRY_UPDATE_01 |
