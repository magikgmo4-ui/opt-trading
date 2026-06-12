# Runbook — SpaceX V5

## Apply

```bash
cd /opt/trading
git checkout sot/mainline
git pull --rebase
git checkout -b go/spacex-master-project-v5
git apply /path/to/GO_SPACEX_MASTER_PROJECT_V5.patch
```

## Smoke

```bash
bash scripts/ipo/spacex_smoke_v5.sh
```

## Offline collect

```bash
bash scripts/ipo/spacex_collect_once_v5.sh --offline
```

## Live collect

```bash
bash scripts/ipo/spacex_collect_once_v5.sh
```

## Report

```bash
bash scripts/ipo/spacex_report_daily_v5.sh
```

## Watch loop

```bash
SPACEX_WATCH_INTERVAL_SECONDS=600 bash scripts/ipo/spacex_watch_loop_v5.sh
```

## Backtest ORB

```bash
python3 -m modules.ipo_tracking.cli backtest-orb --csv data/ipo/spacex/ohlcv/spcx_m1.csv --minutes 15
```
