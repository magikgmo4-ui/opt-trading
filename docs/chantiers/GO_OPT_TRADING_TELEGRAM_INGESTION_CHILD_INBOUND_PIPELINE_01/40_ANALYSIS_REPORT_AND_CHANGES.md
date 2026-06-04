# 40_ANALYSIS_REPORT_AND_CHANGES.md

## GO: GO_OPT_TRADING_ANALYSIS_BUNDLES
## Branch: go/GO_VISION_CAPTURE_QUALITY_ROUTING_01
## Date: 2026-06-04 01:30Z

---

## 1. Real Data Analysis Results

### BTC Core Bundle
| Metric | Value |
|---|---|
| Freshness | STALE (market_metrics missing, telegram_signals missing) |
| Bias | **BULLISH** (from vision_analysis: supports 66000/65000) |
| Regime | TRENDING |
| Confidence | MEDIUM |
| Supports | 66000, 65000 |
| Resistances | 67200, 67600 |
| Plan from vision | "Surveiller rebond potentiel sur support 65k-66k, short si resistance invalide" |

### Macro Bundle
| Metric | Value |
|---|---|
| Freshness | **FRESH** |
| Regime | **RISK_ON** |
| Bias | BULLISH |
| Confidence | MEDIUM (3/4 sources fresh) |
| DXY | BULLISH, FRESH |
| GOLD | BULLISH, FRESH |
| SPY | BULLISH, FRESH |
| VIX | BULLISH, FRESH |

### Verdict
| Metric | Value |
|---|---|
| Alignment | **ALIGNED** (BTC BULLISH + Macro RISK_ON) |
| Overall Bias | **BULLISH** |
| Score | **95/100** |
| Confidence | LOW (BTC bundle stale) |
| Warnings | BTC bundle stale |
| Checklist | 4/7 OK, 2 N/A, 1 WARN |

### Asset Summary by Class (24 symbols, all FRESH)

| Class | Count | Bullish | Bearish |
|---|---|---|---|
| ENERGY | 4 | 3 (WTI, NatGas, Gasoline) | 1 (Brent) |
| CRYPTO_MAJOR | 2 | 1 (BTC) | 1 (ETH) |
| MACRO_EQUITY | 1 | 1 (SPY) | 0 |
| MACRO_COMMODITY | 1 | 1 (GOLD) | 0 |
| MACRO_VOL | 1 | 1 (VIX) | 0 |
| MACRO_FX | 2 | 1 (DXY) | 1 (EURUSD) |
| MACRO_RATES | 1 | 0 | 1 (US10Y) |
| CRYPTO_ALT_L1 | 2 | 1 (XRP) | 1 (SOL) |
| CRYPTO_MEME | 1 | 0 | 1 (DOGE) |
| CRYPTO_ETF | 5 | 0 | 1 (GBTC) |
| CRYPTO_MARKET | 4 | 2 | 2 |

### Data Center Coverage
| Source | Status | Items |
|---|---|---|
| vision_analysis | PROVEN | 24 symbols |
| coinglass_ocr | PROVEN | 1 file |
| runtime_health | PROVEN | 1 file |
| telegram_collector | HYPOTHESIS | 171 files |
| market_metrics | MISSING | 0 |
| telegram_screener | MISSING | 0 |

---

## 2. Changes Complete List

### New Module: `modules/analysis_bundles/` (module convention)

```
modules/analysis_bundles/
├── __init__.py                          # Module docstring + invariants
├── README.md                            # Flow, commands, bundles
├── app/
│   ├── __init__.py                      # Re-exports public API
│   ├── __main__.py                      # python -m entry point
│   ├── schema.py                        # BundleOutput, BundleInput, BundleAnalysis
│   ├── contract_validator.py            # validate_bundle() — canonical schema validator
│   ├── btc_core_producer.py             # produce_btc_core() — aggregates 4 inputs
│   ├── macro_producer.py                # produce_macro() — 14 macro/crypto symbols
│   ├── verdict_schema.py                # AnalysisVerdict, VerdictComposite, ChecklistItem
│   ├── verdict_consumer.py              # produce_verdict(), consume_and_write()
│   ├── vision_analysis_reader.py        # read_vision_analysis(), extract_signals()
│   ├── data_center_router.py            # produce_data_center_coverage(), route_to_dc()
│   └── asset_selector.py                # produce_asset_ticket(), summary_by_class()
├── tests/
│   └── __init__.py
└── scripts/
    ├── cmd.sh                           # CLI: sanity, test, validate, btc, macro, verdict, datacenter, tickets
    ├── menu.sh                          # Interactive TUI (9 options)
    ├── sanity_check.sh                  # Structural + import + smoke validation
    └── install_shortcuts.sh             # Symlinks in /usr/local/bin
```

### New Module: `modules/desk_pro/telegram/`

```
modules/desk_pro/telegram/
├── __init__.py                          # Re-exports ParsedTelegramMessage, parse_telegram_message
└── parsers.py                           # ParsedTelegramMessage dataclass + parse_telegram_message()
```

### Modified Files

| File | Change |
|---|---|
| `modules/telegram_ingestion/distribution/consumer_router.py` | ScreenerConsumer: +results, +claims via parse_telegram_message |
| `tests/test_telegram_ingestion_consumer_router.py` | +4 tests: parsed results, claims, tracking |
| `tests/test_bundle_contracts.py` | Updated macro test assertions for new API keys |

### New Test Files

| File | Tests |
|---|---|
| `tests/test_bundle_contracts.py` | 45 tests: schema, validation, producers, enums |
| `tests/test_verdict_consumer.py` | 41 tests: alignment, confidence, score, verdict, parsers |
| `tests/test_asset_selector.py` | 24 tests: reader, router, selector, enriched bundles |
| **Total** | **110 tests** |

### New Design Document

| File | Content |
|---|---|
| `docs/chantiers/.../20_BUNDLE_DESIGN_AND_OUTPUT_CONTRACT.md` | 5 bundles + JSON contract + ESTABLISHED/HYPOTHESIS/TODO/GAP |

### Real Data Copied from admin-trading

```
data/data_center/views/vision_analysis/
├── by_symbol/    (24 JSON files: BTC, ETH, DXY, VIX, Gold, Oil, ETFs...)
└── history/      (timestamped captures)
data/deskpro/inputs/vision_context/coinglass/latest.json
```

### Test Results

```
124 passed in 0.52s
  - 45 test_bundle_contracts
  - 41 test_verdict_consumer (+ desk_pro parsers)
  - 24 test_asset_selector (+ enriched producers)
  - 14 test_telegram_ingestion_consumer_router
```

### Sanity + Verify

- `bash modules/analysis_bundles/scripts/sanity_check.sh` → PASS
- `bash scripts/verify_all.sh` → OK (py_compile PASS)
- No regressions on existing 53 screener tests

---

## 3. Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│  Data Sources (admin-trading → local)                       │
│  ┌──────────────┐ ┌───────────────┐ ┌────────────────────┐ │
│  │ 225 PNG      │ │ vision_analy- │ │ coinglass OCR      │ │
│  │ screenshots  │ │ sis.v1 (24    │ │ latest.json        │ │
│  │ (raw/)       │ │ symbols)      │ │ (funding rate)     │ │
│  └──────┬───────┘ └───────┬───────┘ └─────────┬──────────┘ │
└─────────┼─────────────────┼───────────────────┼────────────┘
          │                 │                   │
    ┌─────▼─────────────────▼───────────────────▼─────────────┐
    │              analysis_bundles                           │
    │                                                         │
    │  vision_analysis_reader.py ← reads per-symbol signals   │
    │         │                                               │
    │    ┌────▼────┐  ┌───────────┐  ┌──────────────────┐    │
    │    │ btc_core│  │ macro     │  │ asset_selector   │    │
    │    │ producer│  │ producer  │  │ (24 tickets)     │    │
    │    └────┬────┘  └─────┬─────┘  └────────┬─────────┘    │
    │         │             │                 │               │
    │    ┌────▼─────────────▼─────────────────▼──────────┐    │
    │    │         verdict_consumer                      │    │
    │    │  BTC bias × Macro regime = AnalysisVerdict    │    │
    │    │  ALIGNED + BULLISH + score 95 + checklist     │    │
    │    └──────────────────────┬────────────────────────┘    │
    │                           │                             │
    │              data_center_router                        │
    │              (prove + route coverage)                   │
    └───────────────────────────┼─────────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Desk Pro / Decision  │
                    │  Engine (next GO)     │
                    └───────────────────────┘
```

---

## 4. Risk Assessment

| Risk | Status |
|---|---|
| market_metrics absent | BTC bundle STALE, verdict confidence LOW |
| telegram_screener absent | pas de signaux Telegram en entree bundle |
| coinglass OCR = stub | detections a 0.0 (pas d'OCR reel) |
| donnees copiees statiques | sans sync periodique, freshness degrade |
| Energy/Oil maintenant ESTABLISHED | 4/4 FRESH, 3/4 BULLISH — prouve |

---

## 5. Next Steps

1. `GO_OPT_TRADING_VERDICT_SIGNAL_CONTEXT_INTEGRATION_01` — brancher le verdict dans decision engine
2. Sync periodique admin-trading → local (cron ou rsync)
3. Activer market_metrics writer sur admin-trading pour que BTC bundle passe FRESH
4. Appliquer le telegram_screener pipeline pour des signaux reels
