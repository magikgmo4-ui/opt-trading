# 00 — Cadrage Pipeline Orchestrator

## Parent
PF_BOT_VISION_HEADLESS — reste OUVERT.

## GO
```
GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_ORCHESTRATOR_01
```

## Gaps comblés
Depuis 10_RESULTS_AND_NEXT_GO.md :
- **#12** : Pas d'orchestrateur lisant trigger_config.json → **livré**
- **#13** : Timers systemd non synchronisés → **livré** (nouveau systemd unit)
- **#14** : Registre Data Center non mis à jour → **couvert** (orchestrateur pipeline appelle vision_analysis_writer + vision_context_writer)

## Ce que fait l'orchestrateur

1. Lit `capture_map.json`, `trigger_config.json`, `screen_types.json`
2. Charge tous les profils de capture (*.profiles.*.json)
3. Pour chaque profil :
   - Vérifie **scheduler** (intervalle, jitter)
   - Vérifie **market hours** (délègue à capture_headless.js)
   - Vérifie **cooldown** (après N échecs consécutifs)
4. Exécute les captures dues
5. Dispatche l'analyseur approprié (bot_vision_step2, OCR Coinglass, stub)
6. Publie les résultats (DeskPro + Data Center)
7. Maintient l'état (state.json + cooldown.json)
8. Compatible systemd (timer 10min)

## Flags
- `--dry-run` : prévisualisation sans exécution
- `--force-all` : force tous les profils (ignore schedule + market hours)
- `--once --profile X` : one-shot mode (legacy compat)
- `--reset-state` : réinitialise état et cooldowns

## Fichiers créés
- scripts/schedule_orchestrator.py
- scripts/run_orchestrator.sh
- systemd/bot-vision-orchestrator.service
- systemd/bot-vision-orchestrator.timer
- tests/test_orchestrator.py (17 tests)
- docs/chantiers/.../00_CADRAGE.md, 01_TARGETS.md, 02_RESULTS.md
