# 80_RUNBOOK

## Install

```bash
cd /opt/trading
git checkout sot/mainline
git pull --rebase
git checkout -b go/spacex-final-canonical-01
git apply /path/to/GO_SPACEX_FINAL_CANONICAL_01.patch
```

## Smoke

```bash
bash scripts/ipo/spacex_final_smoke.sh
```

## Collect once

```bash
python3 -m modules.ipo_tracking.cli collect-once --offline
python3 -m modules.ipo_tracking.cli collect-once
```

## Report

```bash
python3 -m modules.ipo_tracking.cli report
```

## Watch loop

```bash
bash scripts/ipo/spacex_watch_loop_v5.sh
```

## Backtest ORB

```bash
python3 -m modules.ipo_tracking.cli backtest-orb --csv path/to/ohlcv.csv --minutes 15
```

## Commit

```bash
git status --short
git add docs configs schemas modules scripts ui tradingview RUNBOOK_SPACEX_MASTER_PROJECT_V5.md
git commit -m "feat: add SpaceX final canonical super desk"
git push -u origin go/spacex-final-canonical-01
```
