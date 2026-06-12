# 10_END_TO_END_PLAN — SpaceX Final Canonical

## Pipeline cible

```text
TradingView / Bot Vision / SEC / Market / News / Institutional / Context
  -> collectors
  -> raw store
  -> normalizers
  -> scoring
  -> Data Center view
  -> Desk/UI
  -> Telegram
  -> Google Sheets
  -> Reports
  -> Backtest Lab
  -> Accumulation Engine
```

## P0 — Installation

```bash
cd /opt/trading
git checkout sot/mainline
git pull --rebase
git checkout -b go/spacex-final-canonical-01
git apply /path/to/GO_SPACEX_FINAL_CANONICAL_01.patch
bash scripts/ipo/spacex_final_smoke.sh
```

## P1 — Validation locale

Vérifier:

- `data/ipo/spacex/scored/latest_snapshot.json`
- `data/data_center/views/spacex_super_desk/latest.json`
- `reports/ipo/spacex/spacex_daily_YYYYMMDD.md`
- `ui/spacex_desk/index.html`

## P2 — TradingView réel

Créer alertes TradingView avec le template livré:

- `tradingview/spacex_alert_template_v5.json`

Événements minimum:

- `SPCX_PRICE_UPDATE`
- `SPCX_ORB_BREAK`
- `SPCX_VWAP_RECLAIM`
- `SPCX_FVG_DETECTED`
- `SPCX_BOS_DETECTED`
- `SPCX_CHOCH_DETECTED`
- `SPCX_VOLUME_SPIKE`

## P3 — Bot Vision réel

Importer ou adapter:

- `modules/bot_vision/headless_capture/profiles.spacex.v5.json`
- `configs/ipo/spacex_bot_vision_profiles.json`

Cadence initiale: 10 minutes.

## P4 — Desk Pro natif

À intégrer en child GO:

- route `/spacex` ou carte native dans `/perf/ui`.
- lecture de `data/data_center/views/spacex_super_desk/latest.json`.

## P5 — Telegram + Sheets

- Telegram: brancher payloads d'alertes sur le dispatcher existant.
- Sheets: brancher snapshots et daily report sur consumer existant.

## P6 — Backtest Lab

Backtests d'abord sur CSV OHLCV:

```bash
python3 -m modules.ipo_tracking.cli backtest-orb --csv data/ipo/spacex/backtest/sample_ohlcv.csv --minutes 15
```

Puis généraliser aux setups catalogués.
