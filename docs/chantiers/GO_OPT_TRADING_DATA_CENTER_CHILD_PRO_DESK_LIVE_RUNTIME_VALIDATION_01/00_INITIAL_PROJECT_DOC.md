# GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_LIVE_RUNTIME_VALIDATION_01

## Objectif

Valider en conditions admin-trading live que les 12 sources PROVEN écrivent réellement dans data_center, que les views sont fraîches, que LocalCMS expose les pages, et que l'automatisation horaire fonctionne.

## Contexte

- PR #1094: specs/registries (mergée)
- PR #1095: runtime index/cache/source_selector (mergée)
- PR #1098: canonical_value_publisher + 12/12 PROVEN + LocalCMS/backtest (mergée)

## Checklist de validation

### 1. Views data_center écrites
- [ ] `market_metrics` — 13 symboles, CoinGecko
- [ ] `pair_market_snapshot` — 13 symboles
- [ ] `signal_event` — 25+ symboles, 4931 events
- [ ] `telegram_raw` — 165 canaux
- [ ] `runtime_health` — services actifs
- [ ] `telegram_channel_stats` — rafraîchi après bridge

### 2. LocalCMS pages live
- [ ] `/signals` — 259 signaux, 40 canaux
- [ ] `/vision` — Coinglass + screener + screenshots
- [ ] `/backtest/summary` — 39 canaux, 165 trades
- [ ] `/` — perf KPIs proxy + Desk Pro link

### 3. Automatisation horaire
- [ ] `collector-telegram-screener.timer` — actif, 1h
- [ ] Pipeline 6 étapes OK
- [ ] CoinGecko market data frais

### 4. Tests
- [ ] `pytest tests/data_center/ -q` — 113 tests
- [ ] `cmd.sh telegram stats` — fonctionnel
- [ ] `cmd.sh backtest` — fonctionnel

### 5. Couverture Desk Pro
- [ ] 12/12 PROVEN
- [ ] 0 MISSING
- [ ] Score moyen ≥ 0.80

### 6. Services systemd
- [ ] `localcms.service` — actif
- [ ] `collector-telegram-screener.timer` — actif
- [ ] `tv-webhook.service` — actif
- [ ] `tv-perf.service` — actif
