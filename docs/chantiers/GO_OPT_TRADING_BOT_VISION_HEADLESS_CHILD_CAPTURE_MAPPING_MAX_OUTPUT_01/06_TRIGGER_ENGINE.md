# 06 — Trigger Engine

## Configuration

Fichier machine : `modules/bot_vision/headless_capture/trigger_config.json`

## Schedules

| Schedule | Intervalle | Usage |
|----------|-----------|-------|
| every_15m | 900s (avec jitter 60s) | BTC/ETH 15m, 1h |
| every_1h | 3600s (avec jitter 120s) | Charts standard 1h |
| every_4h | 14400s (avec jitter 300s) | Dashboard macro, commodities, Coinglass |
| every_6h | 21600s (avec jitter 300s) | News sentiment |
| every_24h | 86400s (avec jitter 600s) | Screeners stocks (08:00 UTC) |

## Règles globales

- `min_capture_interval_seconds` : 300 (5 min entre deux captures d'un même asset)
- `max_consecutive_failures` : 3 (désactiver temporairement après 3 échecs consécutifs)
- `cooldown_after_failure_minutes` : 15

## Market hours

- Crypto : 24/7/365
- ETF / Stocks : NYSE market hours (09:30-16:00 ET)
- Forex : 24h mais fenêtre active 00:00-23:00 UTC

## Telegram triggers

| Trigger | Condition |
|---------|-----------|
| high_confidence_signal | ≥1 signal avec confidence ≥ 0.75 |
| critical_liquidation | Liquidations cumulées ≥ $50M |
| macro_divergence | Divergence cross-asset détectée |

## Exécution

Les captures sont déclenchées par :
1. **systemd timers** : bot-vision-headless-capture.timer (cron-based)
2. **Run manuel** : `python3 scripts/run_vision_pipeline.py --profile profiles.production.json`
3. **Mode watch** : `--watch` flag sur desk_snapshot_ingest (polling continu)

Le `trigger_config.json` sert de registre de référence pour les fréquences, mais l'orchestrateur reste le timer systemd + le scheduler présent dans le pipeline runner.

## Gaps

- Pas d'orchestrateur central qui lit trigger_config.json et planifie les captures
- Les timers systemd actuels ne sont pas paramétrés par le JSON (config manuelle dans .service/.timer)
- `market_hours` défini mais non appliqué (les captures ETF/stocks tournent 24h)
