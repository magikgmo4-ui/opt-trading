# 70_CANONICAL_DATA_TABLE.md

## GO: GO_OPT_TRADING_ANALYSIS_BUNDLES
## Branch: sot/mainline
## Date: 2026-06-04
## Source of Truth: Data ingested from admin-trading screenshots + analysis pipeline

---

## 1. CANONICAL DATA-BY-SYMBOL TABLE

### CRYPTO — Core

| Symbol | Class | Screens TF | Missing TF | Data for Analyze | Data for Strategy | Data for DeskPro | Action |
|---|---|---|---|---|---|---|---|
| **BTCUSDT.P** | CRYPTO_MAJOR | 15m, 1h, Coinglass | 4h, 1d | bias, S/R, OI, funding | verdict core, multi-TF | verdict panel, chart | **Add 4h + 1d** |
| **ETHUSDT.P** | CRYPTO_MAJOR | 15m, 1h, Coinglass | 4h | bias, S/R, OI | BTC-ETH correlation | correlation panel | **Add 4h** |
| **SOLUSDT.P** | CRYPTO_ALT_L1 | 15m | 1h, 4h | bias | alt momentum | breadth panel | **Add 1h** |
| **XRPUSDT.P** | CRYPTO_ALT_L1 | 15m | 1h | bias | alt momentum | breadth panel | **Add 1h** |
| **DOGEUSDT.P** | CRYPTO_MEME | 15m | — | bias | risk appetite signal | sentiment indicator | KEEP (low weight) |

### CRYPTO — Market

| Symbol | Class | Screens TF | Missing TF | Data for Analyze | Data for Strategy | Data for DeskPro | Action |
|---|---|---|---|---|---|---|---|
| **CRYPTOCAP:TOTAL** | CRYPTO_MARKET | 1d | 1w | market cap trend | macro crypto trend | market overview | **Add 1w** |
| **CRYPTOCAP:TOTAL2** | CRYPTO_MARKET | 1d | 1w | alt cap trend | alt season signal | breadth indicator | **Add 1w** |
| **CRYPTOCAP:TOTAL3** | CRYPTO_MARKET | 1d | — | small cap trend | extreme greed/fear | breadth indicator | KEEP |
| **CRYPTOCAP:BTC.D** | CRYPTO_MARKET | 1d | 1w | dominance trend | BTC vs alts rotation | dominance chart | **Add 1w** |

### CRYPTO — ETF

| Symbol | Class | Screens TF | Missing TF | Data for Analyze | Data for Strategy | Data for DeskPro | Action |
|---|---|---|---|---|---|---|---|
| **NASDAQ:IBIT** | CRYPTO_ETF | 1h | 1d | bias, flow proxy | institutional BTC confirmation | ETF panel | **Add 1d** |
| **NASDAQ:ARKB** | CRYPTO_ETF | 1h (blind) | — | — | — | — | **REMOVE (blind)** |
| **NASDAQ:BITB** | CRYPTO_ETF | 1h (blind) | — | — | — | — | **REMOVE (blind)** |
| **NASDAQ:FBTC** | CRYPTO_ETF | 1h (blind) | — | — | — | — | **REMOVE (blind)** |
| **OTC:GBTC** | CRYPTO_ETF | 1h (blind) | — | — | — | — | **REMOVE (blind)** |

### MACRO — Core

| Symbol | Class | Screens TF | Missing TF | Data for Analyze | Data for Strategy | Data for DeskPro | Action |
|---|---|---|---|---|---|---|---|
| **SPY** | MACRO_EQUITY | 1h, dashboard | 1d | bias, structure | risk-on/off regime | macro panel | **Add daily** |
| **TVC:DXY** | MACRO_FX | 1h, dashboard | 4h, 1d | bias, S/R | dollar strength filter | macro panel | **Add 4h + 1d** |
| **TVC:VIX** | MACRO_VOL | 1h | 1d | bias | stress/panic filter | macro panel | **Add daily** |
| **TVC:US10Y** | MACRO_RATES | 1h | 1d | bias | rates pressure on BTC | macro panel | **Add daily** |
| **OANDA:XAUUSD** | MACRO_COMMODITY | 1h, dashboard | 4h, 1d | bias, S/R | gold hedge signal | macro panel | **Add 4h + 1d** |
| **FX:EURUSD** | MACRO_FX | 1h | — | bias | DXY confirmation | macro panel | KEEP |

### ENERGY

| Symbol | Class | Screens TF | Missing TF | Data for Analyze | Data for Strategy | Data for DeskPro | Action |
|---|---|---|---|---|---|---|---|
| **NYMEX:CL1!** | ENERGY | 1h, 4h | — | bias, S/R | energy regime | energy panel | KEEP |
| **BITGET:BZUSDT** | ENERGY | 1h, 4h | — | bias | Brent proxy | energy panel | VERIFY quality |
| **NYMEX:NG1!** | ENERGY | 1h, 4h | — | bias | energy vol | energy panel | KEEP (low weight) |
| **NYMEX:RB1!** | ENERGY | 1h, 4h | — | bias | refined energy | energy panel | KEEP |

### Coinglass

| Symbol | Pages | Data for Analyze | Data for Strategy | Status | Action |
|---|---|---|---|---|---|
| **BTCUSDT.P** | liquidation, funding, OI, L/S ratio | OI, funding rate, liquidations, long/short | squeeze detection, positioning | STUB | **Enable --real-ocr** |
| **ETHUSDT.P** | liquidation, funding, OI, L/S ratio | OI, funding rate | ETH positioning | STUB | **Enable --real-ocr** |

---

## 2. SCREENSHOTS — MISSING / TO ADD / TO REPLACE

| Priority | Symbol | Timeframe | Type | Reason |
|---|---|---|---|---|
| **P0** | BTCUSDT.P | 4h | CHART_TECHNICAL | Avoid 15m/1h-only decisions |
| **P0** | BTCUSDT.P | 1d | CHART_TECHNICAL | Daily structure confirmation |
| **P0** | OANDA:XAUUSD | 4h + 1d | CHART_TECHNICAL | Gold is #1 macro driver |
| **P0** | TVC:DXY | 4h + 1d | CHART_TECHNICAL | Dollar is #1 inverse BTC driver |
| **P1** | ETHUSDT.P | 4h | CHART_TECHNICAL | BTC confirmation |
| **P1** | SOLUSDT.P | 1h | CHART_TECHNICAL | Alt leader |
| **P1** | SPY | 1d | CHART_TECHNICAL | Weekly equity confirmation |
| **P1** | TVC:VIX | 1d | CHART_TECHNICAL | Weekly stress check |
| **P1** | TVC:US10Y | 1d | CHART_TECHNICAL | Weekly rates check |
| **P1** | CRYPTOCAP:TOTAL | 1w | CHART_TECHNICAL | Long-term trend |
| **P1** | CRYPTOCAP:BTC.D | 1w | CHART_TECHNICAL | BTC dominance cycle |
| **P2** | NASDAQ:IBIT | 1d | ETF_CRYPTO | ETF flow daily |
| **P2** | XRPUSDT.P | 1h | CHART_TECHNICAL | Alt breadth |

### TO REPLACE (blind → valid)

| From | To | Reason |
|---|---|---|
| NASDAQ:ARKB | — | AI returns "symbole invalide" |
| NASDAQ:BITB | — | AI returns "Pas de donnee" |
| NASDAQ:FBTC | — | AI returns "symbole invalide" |
| OTC:GBTC | — | AI returns "donnee indisponible" |

### TO REMOVE (no value)

| Symbol | Reason |
|---|---|
| NASDAQ:ARKB | Blind — no analysis possible |
| NASDAQ:BITB | Blind — no analysis possible |
| NASDAQ:FBTC | Blind — no analysis possible |
| OTC:GBTC | Blind — no analysis possible |

---

## 3. DATA CENTER CONSUMERS — COMPLETE TABLE

| # | Consumer | Module/File | Reads From | Writes To | Contract | Freshness Rule | Decision Role | Mode |
|---|---|---|---|---|---|---|---|---|
| 1 | **screenshot_registry** | (implicit via profiles) | PNG + sidecar JSON | `vision_inbox/` | — | — | Raw capture | **ALWAYS ON** |
| 2 | **vision_analysis_writer** | `run_vision_pipeline.py` | screenshots + OpenAI | `vision_analysis/by_symbol/` | `vision_analysis.v1` | OpenAI on-demand | Chart TA | **ON_DEMAND** |
| 3 | **data_center_coverage** | `data_center_router.py` | all data paths | `data_center_coverage/latest.json` | `data_center_coverage.v1` | Always | Provenance audit | **ALWAYS ON** |
| 4 | **vision_analysis_reader** | `vision_analysis_reader.py` | `by_symbol/*.json` | — (in-memory) | — | ≤6h = FRESH | Bias/SR extraction | **ALWAYS ON** |
| 5 | **asset_selector** | `asset_selector.py` | vision_analysis | — (in-memory) | `asset_ticket.v1` | — | Per-asset tickets | **ALWAYS ON** |
| 6 | **btc_core_producer** | `btc_core_producer.py` | vision + coinglass + mm + telegram | `btc.core.v1` | `bundle.btc_core.v1` | >50% present FRESH | BTC bias | **ALWAYS ON** |
| 7 | **macro_producer** | `macro_producer.py` | 5 core macro symbols | `macro.v1` | `bundle.macro.v1` | >50% core FRESH | Macro regime | **ALWAYS ON** |
| 8 | **verdict_consumer** | `verdict_consumer.py` | btc_core + macro | `analysis_verdict/latest.json` | `analysis_verdict.v1` | MIN(btc, macro) | Trading gate | **ALWAYS ON** |
| 9 | **cross_correlation** | `cross_correlation.py` | vision_analysis pairs | `cross_correlation/latest.json` | — | Both FRESH | Pair confirmation | **ALWAYS ON** |
| 10 | **coinglass_squeeze** | `coinglass_squeeze.py` | coinglass OCR | `squeeze_alerts/latest.json` | — | Real OCR only | Squeeze risk | **ON_DEMAND** |
| 11 | **multi_tf_consensus** | `multi_tf_consensus.py` | multi-TF vision | — (in-memory) | — | All TF FRESH | TF confirmation | **ALWAYS ON** |
| 12 | **market_metrics_writer** | `market_metrics_writer.py` | vision_analysis + coinglass | `market_metrics/latest.json` | `market_metrics.v1` | Always | Synthetic pricing | **ALWAYS ON** |
| 13 | **sync_admin_trading** | `sync_admin_trading.sh` | admin-trading:/opt/trading | local data/ | — | Every 30min | Data freshness | **ALWAYS ON** |
| 14 | **DeskPro** | `modules/desk_pro/` | all inputs | — (reads only) | all contracts | — | Dashboard | Consumer |
| 15 | **Decision Engine** | (future) | verdict + gates | — | — | TRADABLE only | Execution gate | **FUTURE** |
| 16 | **Strategy Backtest** | (future) | 508 history snapshots | — | — | — | Performance | **FUTURE** |

---

## 4. CONFIG FLAGS

```bash
# On admin-trading (/opt/trading/modules/bot_vision/headless_capture/scripts/cron_capture.sh):
OPENAI_ANALYZE_MODE=on_demand   # default: capture + ingest only, no OpenAI
OPENAI_ANALYZE_MODE=auto        # override: full pipeline with OpenAI analysis

# Equivalent in analysis_bundles (no config needed — reads FRESH <=6h automatically):
# The pipeline always runs. OpenAI analysis is only applied when vision_analysis data is FRESH.
# No config file needed locally — freshness degradation handles it.
```

### How to trigger OpenAI on-demand analysis:

```bash
# On admin-trading:
cd /opt/trading/modules/bot_vision/headless_capture
python3 scripts/run_vision_pipeline.py --profile profiles.production.json --skip-capture
# This captures nothing new, delegates FULL analysis to bot_vision_step2 (OpenAI)
# Use --skip-capture to analyze existing screenshots without re-capturing

# Or for a single symbol:
python3 scripts/run_vision_pipeline.py --profile profiles.btcusdt_poc.json --skip-capture
```

---

## 5. OPERATIONAL MODES

| Mode | Capture | Ingest | OpenAI | Verdict | Use Case |
|---|---|---|---|---|---|
| **DEFAULT** (on_demand) | ON (hourly) | ON (30min) | OFF | Runs on existing/stale data | Normal ops, cost control |
| **FULL** (auto) | ON (hourly) | ON (30min) | ON (hourly) | Runs on fresh AI analysis | Pre-market deep dive |
| **MANUAL** | OFF | ON | ON (manual trigger) | Runs on manually analyzed data | Specific symbol analysis |
| **DRY** | OFF | ON | OFF | Runs on existing data only | Diagnostic, no new data |

---

## 6. VERIFICATION

```bash
# Verify cron is set to on_demand on admin-trading
ssh admin-trading 'grep OPENAI_ANALYZE_MODE /opt/trading/modules/bot_vision/headless_capture/scripts/cron_capture.sh'

# Verify local cron runs sync + pipeline
crontab -l | grep analysis_bundles

# Force a manual sync + pipeline run
cd ~/opt-trading-clean
bash modules/analysis_bundles/scripts/sync_admin_trading.sh
python3 -c "from modules.analysis_bundles.app.market_metrics_writer import write_all_synthetic; write_all_synthetic()"
python3 -m modules.analysis_bundles.app

# Check current verdict
python3 -c "
import json
with open('data/deskpro/inputs/analysis_verdict/latest.json') as f:
    v = json.load(f)
c = v['composite']
print(f'VERDICT: {c[\"overall_bias\"]} {c[\"alignment\"]} score={c[\"score\"]} conf={c[\"confidence\"]} fresh={v[\"freshness_state\"]}')
"

# Run tests
python3 -m pytest tests/test_bundle_contracts.py tests/test_verdict_consumer.py tests/test_asset_selector.py tests/test_telegram_ingestion_consumer_router.py -q
# 132 passed
```
