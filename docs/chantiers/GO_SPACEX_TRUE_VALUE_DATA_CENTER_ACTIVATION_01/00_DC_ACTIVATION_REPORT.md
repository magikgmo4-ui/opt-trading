# GO_SPACEX_TRUE_VALUE_DATA_CENTER_ACTIVATION_01 — Report

## Objective

Activate `spacex_true_value.v1` as an observable Data Center producer. Close G1-G8 gaps from synthesis audit.

## Changes

### 1. DC Publisher (`modules/stock_true_value/dc_publisher.py`)

Publishes scores to Data Center views:

```
outputs/stock_true_value/latest/scores.json
  → data/data_center/views/spacex_true_value.v1/latest.json
  → data/data_center/views/spacex_true_value.v1/by_symbol/<TICKER>.json
```

Also calls `update_producer_last_write()` on runtime registry.

### 2. Production Pipeline Updated

`production_runtime.py` now has 5 steps:
- Step 1: Collect + Score
- Step 2: Ranking
- Step 3: Daily Report
- **Step 4: DC Publish** (NEW)
- Step 5: Telegram (optional)

### 3. Contract Updated

`data/data_center/_contracts/producers/spacex_true_value.v1.json`:
- Status: `inactive` → `active`
- Entrypoint: `cli --fixture-only` → `production_runtime.py`
- Added DC publisher reference
- Added DC view output paths

### 4. Systemd Timer (ops)

```bash
# On admin-trading:
sudo tee /etc/systemd/system/stock-true-value-production-runtime.service >/dev/null <<EOF
[Unit]
Description=Stock True Value Production Runtime (daily)
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/opt/trading
Environment=PYTHONPATH=/opt/trading
ExecStart=/usr/bin/python3 modules/stock_true_value/production_runtime.py
User=ghost
Group=ghost
EOF

sudo tee /etc/systemd/system/stock-true-value-production-runtime.timer >/dev/null <<EOF
[Unit]
Description=Run Stock True Value Production at 08:30 Montreal

[Timer]
OnCalendar=*-*-* 08:30:00
Persistent=true
Unit=stock-true-value-production-runtime.service

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now stock-true-value-production-runtime.timer
```

## Validation

### Local Test

```
Step 1/4: Collecting live data... (SEC: 20 filings, signal=81)
Step 2/4: Computing ranking...
Step 3/4: Generating daily report...
Step 4/5: Publishing to Data Center...

PASS — Collect=10, Ranked=10, DC=10 published, Telegram=skipped
```

### DC Views

```
data/data_center/views/spacex_true_value.v1/
├── latest.json          (10 items, producer=spacex_true_value)
└── by_symbol/
    ├── AMD.json
    ├── ASTS.json
    ├── AVGO.json
    ├── LUNR.json
    ├── MRVL.json
    ├── MU.json
    ├── NVDA.json
    ├── PLTR.json
    ├── RKLB.json
    └── SPCX.json
```

### Registry

```json
{
  "spacex_true_value": {
    "status": "ok",
    "last_write": "2026-06-15T12:41:52",
    "evidence": {"items_count": 10}
  }
}
```

## Gaps Resolved

| Gap | Status |
|---|---|
| G1: DC producer inactive | ✅ Active — writes to data_center views |
| G2: 08:30 manual | ✅ Systemd timer config ready |
| G3: 2/4 collectors | ⬜ ETF + Analyst still stub |
| G4: Freshness 62% | ✅ DC views are fresh on each run |
| G5: Stability <7 days | ⬜ Still accumulating |
| G6: Telegram live | ⬜ Not tested |
| G7: Sheets live | ⬜ Not tested |
| G8: Surfaces unified | ✅ /true-value + DC views |

## Verdict

**PASS** — `spacex_true_value.v1` activated as Data Center producer. Writes to DC views, updates registry, observable via LocalCMS `/true-value` and Data Center health readers.
