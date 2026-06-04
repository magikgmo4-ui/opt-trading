# 60_DATA_INVENTORY_AND_ANALYSIS_SYNTHESIS.md

## GO: GO_OPT_TRADING_ANALYSIS_BUNDLES
## Branch: sot/mainline
## Date: 2026-06-04 08:20Z
## Status: GATED SYSTEM — CONTEXT READY, EXECUTION BLOCKED

> **See also**: `70_CANONICAL_DATA_TABLE.md` — complete per-symbol inventory, missing screenshots, 16 consumers, 4 operational modes.

---

## 1. DONNEES INGEREES (6 sources)

| # | Source | Format | Emplacement | Items | Statut | Provenance |
|---|---|---|---|---|---|---|
| 1 | **vision_analysis** | `vision_analysis.v1` | `data/data_center/views/vision_analysis/by_symbol/` | 24 symboles + 508 history | STALE (>6h, cron hourly active) | PROVEN |
| 2 | **coinglass_ocr** | `vision_context.coinglass.v1` | `data/deskpro/inputs/vision_context/coinglass/latest.json` | 1 fichier | STUB (OI 72B, funding 0.0, method=stub) | PROVEN |
| 3 | **market_metrics** | `market_metrics.v1` | `data/data_center/views/market_metrics/` | 8 symboles | SYNTHETIC (prices from vision analysis) | HYPOTHESIS |
| 4 | **telegram_collector** | raw JSON | `modules/collector_telegram/outputs/channel_results/` | 201 messages | NON PARSE (raw messages) | HYPOTHESIS |
| 5 | **telegram_screener** | `telegram_signal.v1` | — | 0 | MISSING (pipeline non active) | MISSING |
| 6 | **runtime_health** | events.jsonl | `data/runtime_health/ledger/events.jsonl` | 53 events | PROVEN | PROVEN |

### Détail vision_analysis — 24 symboles

| Classe | Symboles | Biais | Supports | Resistances | Qualite |
|---|---|---|---|---|---|
| **CRYPTO_MAJOR** | BTCUSDT.P | BULLISH | 62800, 63200 | 64400, 64600 | OK |
| | ETHUSDT.P | BEARISH | 1775 | 1850 | OK |
| **CRYPTO_ALT** | SOLUSDT.P | BEARISH | — | — | OK |
| | XRPUSDT.P | BULLISH | 1.20 | 1.245 | OK |
| | DOGEUSDT.P | BEARISH | 0.0905 | 0.094 | OK |
| **MACRO_CORE** | TVC:DXY | BULLISH | 99.05 | 99.55 | OK |
| | SPY | BULLISH | — | 760.0 | OK |
| | TVC:VIX | BEARISH | 15.8 | 16.3 | OK |
| | OANDA:XAUUSD | BEARISH | 4430 | 4475 | OK (plan=short) |
| | TVC:US10Y | BEARISH | — | — | OK |
| **ENERGY** | NYMEX:CL1! (WTI) | BULLISH | 92.0 | 97.0 | OK |
| | NYMEX:NG1! (NatGas) | BULLISH | 3.15 | 3.25 | OK |
| | NYMEX:RB1! (Gasoline) | BEARISH | 3.06 | 3.18 | OK (plan=vendre) |
| | BITGET:BZUSDT (Brent) | BEARISH | — | — | OK |
| **CRYPTO_MARKET** | CRYPTOCAP:TOTAL | BEARISH | — | — | OK |
| | CRYPTOCAP:TOTAL2 | BULLISH | — | — | OK |
| | CRYPTOCAP:TOTAL3 | BULLISH | — | — | OK |
| | CRYPTOCAP:BTC.D | BEARISH | — | — | OK |
| **ETF** | NASDAQ:IBIT | BEARISH | 36.5 | — | OK |
| | NASDAQ:ARKB | — | — | — | **BLIND (symbole invalide)** |
| | NASDAQ:BITB | — | — | — | **BLIND (symbole invalide)** |
| | NASDAQ:FBTC | — | — | — | **BLIND (symbole invalide)** |
| | OTC:GBTC | — | — | — | **BLIND (symbole invalide)** |
| **MACRO_FX** | FX:EURUSD | BEARISH | 1.16 | 1.163 | OK |

---

## 2. ANALYSES PRODUITES (5 outputs)

| Analyse | Contrat | Emplacement | Contenu |
|---|---|---|---|
| **analysis_verdict** | `analysis_verdict.v1` | `data/deskpro/inputs/analysis_verdict/latest.json` | Signal trading composite: ALIGNED/DIVERGENT, score 0-100, checklist |
| **analysis_report** | `analysis_pipeline_report.v1` | `data/deskpro/inputs/analysis_report/latest.json` | Full pipeline: ingest, 24 tickets, class consensus, actionable, cross-corr, squeeze |
| **data_center_coverage** | `data_center_coverage.v1` | `data/data_center/views/data_center_coverage/latest.json` | Provenance audit: PROVEN/HYPOTHESIS/MISSING par source |
| **cross_correlation** | *(no contract — internal)* | `data/data_center/views/analysis/cross_correlation/latest.json` | 10 paires correlees: BTC-ETH, BTC-GOLD, BTC-DXY, ETH-SOL... |
| **squeeze_alerts** | *(no contract — internal)* | `data/data_center/views/coinglass/squeeze_alerts/latest.json` | Detection squeeze OI/Funding (STUB) |

### Verdict actuel (live)

```json
{
  "contract": "analysis_verdict.v1",
  "freshness_state": "FRESH",
  "composite": {
    "btc_bias": "BULLISH",
    "macro_regime": "RISK_ON",
    "alignment": "ALIGNED",
    "overall_bias": "BULLISH",
    "confidence": "MEDIUM",
    "score": 95
  },
  "checklist": [
    "BTC bias: OK", "Macro regime: OK",
    "BTC/macro alignment: OK", "Coinglass OI/Funding: N/A",
    "Telegram signal: N/A", "News conflict: N/A"
  ]
}
```

### +Value producers

| Producer | Fonction | Output live |
|---|---|---|
| `multi_tf_consensus` | Score accord 15m × 1h | BTC: consensus BULLISH 100 |
| `cross_correlation` | 10 paires directionnelles | 0% aligned (all stale, waiting fresh data) |
| `coinglass_squeeze` | OI + funding squeeze risk | STUB |
| `asset_selector` | Tickets per-asset (24) | bias + supports + resistances + plan |
| `data_center_router` | Provenance audit | 3 PROVEN, 2 HYPOTHESIS, 1 MISSING |

---

## 3. ARCHITECTURE FLOW

```
┌─────────────────────────────────────────────────────────────┐
│  ADMIN-TRADING (capture hourly via cron, OpenAI on-demand)  │
│  ┌───────────────────────┐  ┌──────────────────────────────┐│
│  │ headless_capture.js   │  │ bot_vision_step2 (OpenAI)    ││
│  │ profiles.production   │  │ analyze_latest → TA chart    ││
│  │ profiles.coinglass     │  │ supports/resistances/bias    ││
│  │ [--no-delegate]       │  │ [ON_DEMAND only]             ││
│  └─────────┬─────────────┘  └──────────────┬───────────────┘│
│            │                                │                │
│            ▼                                ▼                │
│  vision_inbox (PNG+JSON)  ←  vision_analysis.v1 (OpenAI)    │
│  coinglass latest.json    ←  data_center views              │
│  [ALWAYS ON]                  [ON_DEMAND, --skip-capture]    │
└──────────────────────────┬──────────────────────────────────┘
                           │ rsync every 30min
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  LOCAL REPO (~/opt-trading-clean)                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  sync_admin_trading.sh  →  copy vision + coinglass      ││
│  │  market_metrics_writer  →  synthetic market_metrics     ││
│  │  analysis_pipeline     →  ingest → normalize → analyze  ││
│  └───────────────────────┬─────────────────────────────────┘│
│                          │                                   │
│    ┌─────────────────────┼───────────────────────────┐      │
│    │                     ▼                           │      │
│    │  btc_core    macro    multi_tf   cross_corr     │      │
│    │  producer    producer  consensus  correlation   │      │
│    └─────────────────────┬───────────────────────────┘      │
│                          ▼                                   │
│               verdict_consumer                              │
│          BTC × Macro = analytical signal                   │
│          CONTEXT_READY=YES, EXECUTION_READY=NO              │
│                          │                                   │
│    ┌─────────────────────┼───────────────────────────┐      │
│    │                     ▼                           │      │
│    │  DeskPro inputs:    verdict / report / coverage │      │
│    │  Decision engine:   (future consumer)           │      │
│    │  Strategy backtest: 508 history snapshots       │      │
│    └─────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. DATA CENTER VIEWS

```
data/data_center/views/
├── vision_analysis/
│   ├── by_symbol/          (24 JSON, 301+ captures each)
│   └── history/            (508 timestamped snapshots)
├── market_metrics/
│   ├── by_symbol/          (8 JSON: BTC, ETH, DOGE, XRP, DXY, SPY, WTI, XAUUSD)
│   └── latest.json
├── analysis/
│   └── cross_correlation/
│       └── latest.json     (10 pairs, alignment scoring)
├── coinglass/
│   └── squeeze_alerts/
│       └── latest.json     (OI/funding squeeze detection)
└── data_center_coverage/
    └── latest.json         (provenance audit)

data/deskpro/inputs/
├── vision_analysis/latest.json    (TA chart signals → DeskPro vision_panel)
├── vision_context/coinglass/      (OI/Funding/Liquidations → DeskPro)
├── analysis_report/latest.json   (Full pipeline → DeskPro dashboard)
├── analysis_verdict/latest.json  (Trading signal → Decision Engine)
└── telegram_claim/               (Telegram signals → DeskPro, futur)
```

---

## 5. CALENDRIER CRON

| Machine | Frequence | Commande | Mode |
|---|---|---|---|
| **admin-trading** | Hourly (0 * * * *) | `cron_capture.sh` → profiles.production + coinglass, `--no-delegate` | Capture+Ingest ON, OpenAI ON_DEMAND |
| **local** | Every 30min (*/30 * * * *) | sync_admin_trading.sh + market_metrics + full pipeline | Always ON |

### How to trigger OpenAI analysis (manual):

```bash
# On admin-trading:
cd /opt/trading/modules/bot_vision/headless_capture
# Analyze existing screenshots without re-capturing:
python3 scripts/run_vision_pipeline.py --profile profiles.production.json --skip-capture
# Or for a single symbol:
python3 scripts/run_vision_pipeline.py --profile profiles.btcusdt_poc.json --skip-capture
```

---

## 6. DECISION GATE

### Context gate (analytical signal — PASS)

| Check | Status |
|---|---|
| BTC vision bias | BULLISH, supports 62800/63200, resistances 64400/64600 |
| Macro core consensus | RISK_ON (DXY/SPX/VIX bullish, GOLD/US10Y bearish) |
| Multi-TF consensus | BTC 15m+1h agree → BULLISH 100 |
| BTC x Macro aligned | ALIGNED BULLISH, score 95 |
| Cross-correlation | 10 pairs tracked (pending fresh data) |

### Execution gate (trading — BLOCKED)

| Check | Status | Blocker |
|---|---|---|
| Coinglass OCR | **STUB** | `detection_method=stub`, OI=72B plausible but unverified |
| market_metrics | **SYNTHETIC** | Prices derived from vision analysis, not live API |
| telegram_screener | **MISSING** | No Telegram signals parsed |
| Vision freshness | **STALE** | All 24 analyses >6h (cron hourly active, will recover) |
| Data quality | **DEGRADED/STUB** | 3/6 sources are STUB, HYPOTHESIS, or MISSING |

### Verdict

```
CONTEXT_READY    = YES  (analytical signal: ALIGNED BULLISH 95)
EXECUTION_READY  = NO   (blocked: coinglass stub + market_metrics synthetic)
AUTO_TRADE       = NO   (never auto-trade without all sources PROVEN + FRESH)
MANUAL_SETUP     = MAYBE (operator review required)
```

### Unblock criteria

| To unblock | Action |
|---|---|
| Coinglass STUB → LIVE | `--real-ocr` flag on admin-trading |
| market_metrics SYNTHETIC → LIVE | Binance/Bitget API writer active |
| telegram_screener MISSING → LIVE | Screener pipeline active on 201 raw messages |
| Vision STALE → FRESH | Hourly cron will recover freshness within 2 cycles |

---

## 7. GAPS RESTANTS

| Gap | Impact | Action | Priority |
|---|---|---|---|
| Coinglass stub | Squeeze alerts inactifs, execution gate bloque | Activer `--real-ocr` sur admin-trading | **P0** |
| market_metrics synthetic | Prix approximes, execution gate bloque | Brancher API exchange reelle (Binance/Bitget) | **P0** |
| telegram_screener MISSING | Zero signaux Telegram en entree | Activer pipeline screener sur 201 raw messages | **P1** |
| 4 ETF blind spots | IBIT seul utilisable | Retirer ARKB/BITB/FBTC/GBTC des profiles | P1 |
| 24 vision STALE | Cron on_demand (no OpenAI analysis) | Prochain cycle → captures OK, mais analyse OpenAI on-demand | P1 |
| 13 screenshots manquants | BTC 4h/1d, GOLD 4h/1d, DXY 4h/1d... | Ajouter aux profiles capture | P2 |

> See `70_CANONICAL_DATA_TABLE.md` for complete per-symbol inventory, missing screenshots, and consumer table.

---

## 8. COMMANDES

```bash
# Run full pipeline (1 command)
python3 -m modules.analysis_bundles.app

# Individual commands
bash modules/analysis_bundles/scripts/cmd.sh btc          # BTC bundle
bash modules/analysis_bundles/scripts/cmd.sh macro        # Macro bundle
bash modules/analysis_bundles/scripts/cmd.sh verdict      # Trading verdict
bash modules/analysis_bundles/scripts/cmd.sh report       # Full pipeline report
bash modules/analysis_bundles/scripts/cmd.sh correlation  # Cross-correlation
bash modules/analysis_bundles/scripts/cmd.sh squeeze      # Squeeze alerts
bash modules/analysis_bundles/scripts/cmd.sh multitf      # Multi-TF consensus
bash modules/analysis_bundles/scripts/cmd.sh datacenter   # Data center coverage
bash modules/analysis_bundles/scripts/cmd.sh tickets      # Asset tickets summary

# Sync from admin-trading
bash modules/analysis_bundles/scripts/sync_admin_trading.sh

# Tests
python3 -m pytest tests/test_bundle_contracts.py tests/test_verdict_consumer.py tests/test_asset_selector.py tests/test_telegram_ingestion_consumer_router.py -q
# 132 passed
```
