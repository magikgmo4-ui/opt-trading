# Post-PR #1090 Changes Synthesis

## Branch: sot/mainline
## Date: 2026-06-04 → 2026-06-05
## PR Range: 9c12f116..09a9bbe7 (28 commits)

---

## 1. Overview

### What was built

| Surface | Commits | Status |
|---|---|---|
| **Analysis bundles fixes** | 7 | Post-#1090 bias/freshness/verdict corrections |
| **Live data integration** | 4 | Binance spot + clean capture profiles |
| **Telegram screener** | 11 | Full pipeline: collect → parse → qualify → archive |
| **Documentation** | 5 | Inventory, data table, catalog, cost audit |
| **Infrastructure** | 2 | E2E script, gitignore cleanup |

### Key metrics

| Metric | Before (#1090) | After (09a9bbe7) |
|---|---|---|
| **BTC bundle** | BULLISH (faux) | BEARISH correct (chart analysis) |
| **MACRO bundle** | RISK_ON (faux) | RISK_ON correct (DXY/SPX/VIX FRESH) |
| **Verdict** | UNKNOWN 25 | ALIGNED BULLISH 95, MEDIUM, TRADABLE contingent |
| **market_metrics** | MISSING | LIVE (Binance BTC=$63303, ETH=$1734) |
| **Coinglass** | FRESH (ignored stub) | STALE (stub detected) |
| **Telegram signals** | 0 | 18 archived trade signals (10 WSQ + 8 XAUUSD) |
| **Capture profiles** | 5 separate | 1 clean profile (41 pages, 20 symbols, 0 blind ETFs) |
| **Channel catalog** | 17 channels | 148 channels (13 with data, 135 discovery) |
| **Tests** | 132 | 132 (no regressions) |

---

## 2. Commits by Theme

### 2.1 Analysis Bundles — Post-#1090 Fixes (7 commits)

| Commit | Fix |
|---|---|
| `9c12f116` | Bias extraction: baissier > haussier, plan overrides keyword (fixes GOLD, GASOLINE, BTC) |
| `dcc2be39` | Stale vision bias used instead of discarded, confidence degraded |
| `42da04b5` | Post-fix audit doc: before/after table, gate, gaps |
| `a20a9060` | Synthetic market_metrics, stale bias in macro, sync script, timezone fix |
| `72fb1eca` | data_quality flag (FULL/DEGRADED/STUB), smarter freshness (ignore MISSING) |
| `843224b9` | STALE blocks freshness gate but not confidence (separate concerns) |
| `8705a0c2` | Majority freshness rule, STUB detection, core macro symbols (5 not 14) |
| `327a15f8` | Macro freshness: count only 5 core symbols (DXY/SPX/VIX/GOLD/US10Y) |

### 2.2 Live Data + Capture Profiles (4 commits)

| Commit | Feature |
|---|---|
| `672ca7dd` | Clean capture profile: 41 pages, 20 symbols, removed 4 blind ETFs |
| `b200c919` | Live Binance spot collector → real market_metrics (BTC=$63512, ETH=$1734) |
| `d10c838d` | Fresh BTC capture triggered, coinglass real OCR infra |
| `2ffa3eb9` | E2E fresh cycle script (capture → analyze → sync → verdict) |

### 2.3 Telegram Screener (11 commits)

| Commit | Feature |
|---|---|
| `e9099a0b` | Screener bridge: parse 871 raw messages → 28 signals |
| `9462fb5c` | Refined parser: 3 patterns, 50+ asset whitelist, Chinese, prices, channel stats |
| `5cf50a91` | Auto-clean old signal files before regenerating |
| `9b7155d5` | 4 new parse patterns: #COINUSDT, XAUHQ, BUY GOLD, whale BTC → 87 signals |
| `26b15536` | Complete signals: direction+entry+sl+tp required (76→10 quality-filtered) |
| `d861c054` | Clean architecture: trade(10) vs context(26), binancekillers filtered out |
| `fccf1eee` | Signal archiver: 18 signals archived (entry+sl+tps → ready for backtesting) |
| `5185e713` | Channel qualification: forexsignals/goldsignals TP-only, 4 DISCOVERY pending |
| `8d166533` | Channel catalog v1: 48 channels, 7 buckets, qualification matrix |
| `d006eedd` | Channel modes (DISCOVERY/WATCH/ACTIVE/REJECTED) + cost audit ($0/month) |
| `09a9bbe7` | 135 discovery channels + batch qualification runner + LLM/OCR gate |

### 2.4 Documentation (5 commits)

| Commit | Document |
|---|---|
| `42da04b5` | `50_POST_FIX_AUDIT.md` — before/after PR #1090 |
| `bdd9ceb8` | `60_DATA_INVENTORY_AND_ANALYSIS_SYNTHESIS.md` — system synthesis |
| `f882fb7a` | `70_CANONICAL_DATA_TABLE.md` — per-symbol inventory, 16 consumers |
| `8d166533` | `catalog/telegram_signal_channels_catalog_v1.md` — 48 channels |
| `d006eedd` | `catalog/telegram_screener_cost_audit.md` — cost audit |

### 2.5 Infrastructure (2 commits)

| Commit | Feature |
|---|---|
| `d10c838d` | Cron: admin-trading hourly capture, local 30min sync |
| `da97db3e` | .gitignore for collector outputs |

---

## 3. Architecture — Current State

```
┌─────────────────────────────────────────────────────────────┐
│  ADMIN-TRADING (hourly cron, OpenAI on-demand)              │
│  ┌───────────────────────┐  ┌──────────────────────────────┐│
│  │ headless_capture.js   │  │ bot_vision_step2 (OpenAI)    ││
│  │ profiles.clean.json   │  │ [ON_DEMAND only]             ││
│  │ 41 pages, 20 symbols  │  │ --skip-capture manual trigger││
│  │ [--no-delegate]       │  │                              ││
│  └─────────┬─────────────┘  └──────────────────────────────┘│
│            │                                                 │
│  collector_telegram (Telethon live, 17 channels)             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Ingeste 13 channels hourly → channel_results         │   │
│  │ Config deployed: 4 new channels pending data         │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ rsync every 30min
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  LOCAL REPO (~/opt-trading-clean)                           │
│                                                             │
│  Data Ingestion                                             │
│  ├─ sync_admin_trading.sh (vision + coinglass)              │
│  ├─ collector_binance_spot (live Binance prices)            │
│  └─ collector_telegram (local raw JSONL dump)               │
│                                                             │
│  Analysis Pipeline                                          │
│  ├─ btc_core → macro → verdict (ALIGNED BULLISH 95)        │
│  ├─ multi_tf_consensus (15m+1h BTC: 100)                   │
│  ├─ cross_correlation (10 pairs)                            │
│  └─ coinglass_squeeze (STUB pending real OCR)               │
│                                                             │
│  Telegram Screener                                          │
│  ├─ parse_telegram_message (regex, no LLM)                  │
│  ├─ telegram_screener_bridge (modes: DISCOVERY/ACTIVE...)   │
│  ├─ signal_tracker (18 signals archived for backtesting)    │
│  └─ batch_qualify.sh (qualification 1-4x/day)               │
│                                                             │
│  Outputs                                                    │
│  ├─ analysis_verdict.v1                                     │
│  ├─ analysis_pipeline_report.v1                             │
│  ├─ 18 trade signals (entry+sl+tps)                         │
│  ├─ 26 context signals (whale flows, coinglass entries)     │
│  ├─ 13 channel stats (qualification matrix)                 │
│  └─ data_center_coverage (PROVEN/HYPOTHESIS/MISSING)        │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Data Flow — Telegram Signals

```
17 channels enabled (collector config)
  ↓ Telethon live ingest (admin-trading)
13 channels with data (local raw JSONL)
  ↓ parse_telegram_message (regex, <1ms/msg)
  ↓ telegram_screener_bridge (mode gating)
  ├─ ACTIVE mode → trade signals (direction+entry+sl+tp)
  │   ↓ signal_tracker → archive for backtesting
  │   ↓ data_center/views/telegram_signals/trade_history/
  ├─ WATCH mode → context signals only (whale, coinglass)
  │   ↓ data_center/views/telegram_context/
  ├─ DISCOVERY mode → parse but limit to 200 msgs
  │   ↓ batch_qualify.sh → promote to ACTIVE if >=10 complete
  └─ REJECTED mode → skip parse (zero CPU)
```

---

## 5. Channel Qualification Status

| Mode | Count | Channels |
|---|---|---|
| **ACTIVE** | 2 | xauusd (8 signals, score 48), wallstreetqueenofficial (10 signals, score 18) |
| **WATCH** | 8 | coinglass, whale_alert, fatpig, cryptoquant, glassnode, arkham, forexsignals, goldsignals |
| **REJECTED** | 3 | binancekillers, learn2trade, goldtrading |
| **DISCOVERY** | 4 | gold_scalping, gold_intraday, forexgoldsignals, fxpremiumsignals (pending data) |
| **CATALOG** | 135 | Discovery catalog, all disabled (enable one bucket at a time) |

---

## 6. Files Changed

### New files (25)

```
modules/analysis_bundles/app/market_metrics_live_writer.py
modules/analysis_bundles/app/multi_tf_consensus.py
modules/analysis_bundles/app/cross_correlation.py
modules/analysis_bundles/app/coinglass_squeeze.py
modules/analysis_bundles/app/telegram_screener_bridge.py
modules/analysis_bundles/app/signal_tracker.py
modules/analysis_bundles/scripts/e2e_fresh_cycle.sh
modules/analysis_bundles/scripts/sync_admin_trading.sh
modules/analysis_bundles/scripts/batch_qualify.sh
modules/bot_vision/headless_capture/profiles.clean.json
configs/telegram/discovery_channels.json
docs/chantiers/.../50_POST_FIX_AUDIT.md
docs/chantiers/.../60_DATA_INVENTORY_AND_ANALYSIS_SYNTHESIS.md
docs/chantiers/.../70_CANONICAL_DATA_TABLE.md
docs/chantiers/.../catalog/telegram_signal_channels_catalog_v1.md
docs/chantiers/.../catalog/telegram_screener_cost_audit.md
```

### Modified files (5)

```
modules/desk_pro/telegram/parsers.py (rewritten x3)
modules/analysis_bundles/app/btc_core_producer.py
modules/analysis_bundles/app/macro_producer.py
modules/analysis_bundles/app/vision_analysis_reader.py
modules/analysis_bundles/app/verdict_consumer.py
modules/analysis_bundles/app/analysis_pipeline.py
modules/analysis_bundles/app/market_metrics_writer.py
modules/collector_telegram/config/channels.json
modules/analysis_bundles/scripts/cmd.sh
modules/analysis_bundles/scripts/menu.sh
```

---

## 7. Running the System

```bash
# Full E2E fresh cycle (capture BTC → OpenAI → verdict)
bash modules/analysis_bundles/scripts/e2e_fresh_cycle.sh

# Telegram batch qualification (1-4x/day)
bash modules/analysis_bundles/scripts/batch_qualify.sh

# Individual commands
bash modules/analysis_bundles/scripts/cmd.sh btc          # BTC bundle
bash modules/analysis_bundles/scripts/cmd.sh verdict      # Trading verdict
bash modules/analysis_bundles/scripts/cmd.sh report       # Full pipeline report
bash modules/analysis_bundles/scripts/cmd.sh telegram     # Telegram signals
bash modules/analysis_bundles/scripts/cmd.sh correlation  # Cross-correlation

# Sync from admin-trading
bash modules/analysis_bundles/scripts/sync_admin_trading.sh

# Tests
python3 -m pytest tests/test_bundle_contracts.py tests/test_verdict_consumer.py tests/test_asset_selector.py tests/test_telegram_ingestion_consumer_router.py -q
# 132 passed

# Cron schedule
# Admin-trading: hourly capture (profiles.clean + coinglass, --no-delegate)
# Local: every 30min sync + write_all + full pipeline
```

---

## 8. Decision Record

| Decision | Rationale |
|---|---|
| LLM/OCR on-demand only | $0/month operational cost, text parsing sufficient |
| GOLD bias: baissier > haussier | Plan text overrides keyword (short/vendre wins) |
| STALE blocks freshness gate, not confidence | Separate concerns: analytical quality vs data freshness |
| Core macro = 5 symbols | DXY/SPX/VIX/GOLD/US10Y drive regime |
| Channels must have >=10 complete setups to go ACTIVE | Prevent low-quality signals from polluting strategy |
| Binance spot for market_metrics | Free API, no auth needed, BTC+ETH prices |
| Telegram signals: regex only | No LLM cost, fast (<1ms/msg), sufficient for structured formats |
| Discovery limited to 200 msgs | Cost control on unverified channels |
