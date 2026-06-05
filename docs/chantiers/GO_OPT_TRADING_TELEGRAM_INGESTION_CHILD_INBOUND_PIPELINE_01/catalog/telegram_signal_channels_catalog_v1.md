# Telegram Signal Channels Catalog v1

## GO: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PIPELINE_01
## Date: 2026-06-05
## Status: DISCOVERY — catalogue candidat, qualification gated

---

## 1. Qualification Rules

| Level | Criteria | Action |
|---|---|---|
| **P0_ACTIVE** | >= 10 complete setups (entry+sl+tp) parsed, historical exploitable | Feed into signal_tracker, backtest |
| **P1_PENDING** | Raw messages collected, <10 complete setups | Collect more, wait for data |
| **P2_DISCOVERY** | Candidate channel, not yet collected | Add to collector config, collect 200 msg |
| **P3_CONTEXT** | News, alerts, TP hits, analysis without entry/sl | Route to context_signals |
| **REJECTED** | Spam, clone, no signal, no structure, TP-only | Filter out |

**Gate**: a channel becomes ACTIVE only when >= 10 complete setups with entry+sl+tp are parsed AND validated.

---

## 2. Channel Catalog by Bucket

### 2.1 XAU / GOLD

| Alias | Status | Signals | Format | Reason | Next Action |
|---|---|---|---|---|---|
| **xauusd** | **P0_ACTIVE** | 8 | BUY/SELL GOLD + Entry + SL + TP | Complete setups parsed | Expand collection, backtest |
| **wallstreetqueenofficial** | **P0_ACTIVE** | 10 | Coin: #XXX + Direction + Entry + SL + Targets | 10 complete across 10 assets | backtest per asset |
| gold_scalping | P1_PENDING | 0 | Expected: GOLD scalping signals | Config deployed, no data yet | Wait for collector |
| gold_intraday | P1_PENDING | 0 | Expected: GOLD intraday signals | Config deployed, no data yet | Wait for collector |
| forexgoldsignals | P1_PENDING | 0 | Expected: Forex + Gold signals | Config deployed, no data yet | Wait for collector |
| fxpremiumsignals | P1_PENDING | 0 | Expected: FX premium signals | Config deployed, no data yet | Wait for collector |
| goldsignals | P3_CONTEXT | 0 | XAUHQ TP hits only | No ENTRY+SL setups | Route to context |
| goldtrading | REJECTED | 0 | Indo marketing | No trade signals | Keep disabled |
| xauusd_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| gold_forex_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| gold_scalper | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| xauusd_scalping | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |

### 2.2 Crypto BTC/ETH

| Alias | Status | Signals | Format | Reason | Next Action |
|---|---|---|---|---|---|
| binancekillers | P3_CONTEXT | 40 | TP hits, COIN + Direction + Targets | No entry/sl | Route to context |
| fatpigsignals | P3_CONTEXT | 2 | TP hits, incomplete | No complete setups | Route to context |
| cryptoquant_official | P3_CONTEXT | 0 | On-chain analysis | No trade setups | Route to context |
| cryptosignals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| btc_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| bitcoin_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| eth_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| binance_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| binance_futures_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| crypto_futures_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |

### 2.3 Altcoins

| Alias | Status | Signals | Format | Reason | Next Action |
|---|---|---|---|---|---|
| altcoin_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| altsignals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| sol_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |

### 2.4 Forex Majors

| Alias | Status | Signals | Format | Reason | Next Action |
|---|---|---|---|---|---|
| forexsignals | P3_CONTEXT | 0 | XAUHQ TP hits only | No ENTRY+SL setups | Route to context |
| forex_signal | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| forex_signals_free | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| fx_signals | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |

### 2.5 Coinglass / OI / Funding / Liquidations

| Alias | Status | Signals | Format | Reason | Next Action |
|---|---|---|---|---|---|
| coinglass_alerts | P3_CONTEXT | 16 | Chinese whale alerts + entry | No SL/TP, context only | Route to context |
| liquidation_alerts | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |
| funding_rate_alerts | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |

### 2.6 News / Context

| Alias | Status | Signals | Format | Reason | Next Action |
|---|---|---|---|---|---|
| whale_alert_io | P3_CONTEXT | 10 | BTC/ETH transfers | No trade setups, context | Route to context |
| glassnode | P3_CONTEXT | 0 | On-chain analytics | No trade setups | Route to context |
| arkhamintelligence | P3_CONTEXT | 0 | Product announcements | No trade setups | Route to context |
| cryptoquant_official | P3_CONTEXT | 0 | On-chain metrics | No trade setups | Route to context |
| lookonchain | P2_DISCOVERY | 0 | Uncatalogued | Discovery | Add to config |

### 2.7 Rejected / TP-only

| Alias | Status | Signals | Reason |
|---|---|---|---|
| learn2trade | REJECTED | 0 | Education content only |
| goldtrading | REJECTED | 0 | Indonesian marketing, no signals |

---

## 3. Qualification Matrix

| Channel | Collected | Setups | Complete | TP-only | Parse Rate | Score |
|---|---|---|---|---|---|---|
| wallstreetqueenofficial | 98 | 10 | 10 | 24 | 10.2% | **A (ACTIVE)** |
| xauusd | 91 | 8 | 8 | 0 | 8.8% | **A (ACTIVE)** |
| coinglass_alerts | 20 | 16 | 0 | 0 | 80% | B (context) |
| whale_alert_io | 20 | 0 | 0 | 0 | 50% | B (context) |
| binancekillers | 100 | 40 | 0 | 40 | 40% | C (TP-only) |
| fatpigsignals | 99 | 2 | 0 | 0 | 2% | C (incomplete) |
| forexsignals | 89 | 0 | 0 | 3 | 0% | D (TP-only) |
| goldsignals | 89 | 0 | 0 | 3 | 0% | D (TP-only) |
| gold_scalping | 0 | 0 | 0 | 0 | — | PENDING |
| gold_intraday | 0 | 0 | 0 | 0 | — | PENDING |
| forexgoldsignals | 0 | 0 | 0 | 0 | — | PENDING |
| fxpremiumsignals | 0 | 0 | 0 | 0 | — | PENDING |
| 9 DISCOVERY | 0 | 0 | 0 | 0 | — | DISCOVERY |

---

## 4. Collector Config Update

Copy this to `configs/telegram/discovery_channels.json`:

```json
{
  "version": 1,
  "description": "Discovery channels — collect, parse, qualify before activating as signal sources",
  "discovery_channels": [
    {"alias": "xauusd_signals", "enabled": false, "categories": ["xau", "discovery"]},
    {"alias": "gold_forex_signals", "enabled": false, "categories": ["xau", "discovery"]},
    {"alias": "gold_scalper", "enabled": false, "categories": ["xau", "discovery"]},
    {"alias": "xauusd_scalping", "enabled": false, "categories": ["xau", "discovery"]},
    {"alias": "cryptosignals", "enabled": false, "categories": ["crypto", "discovery"]},
    {"alias": "btc_signals", "enabled": false, "categories": ["crypto", "discovery"]},
    {"alias": "bitcoin_signals", "enabled": false, "categories": ["crypto", "discovery"]},
    {"alias": "eth_signals", "enabled": false, "categories": ["crypto", "discovery"]},
    {"alias": "binance_signals", "enabled": false, "categories": ["crypto", "discovery"]},
    {"alias": "binance_futures_signals", "enabled": false, "categories": ["crypto", "discovery"]},
    {"alias": "crypto_futures_signals", "enabled": false, "categories": ["crypto", "discovery"]},
    {"alias": "altcoin_signals", "enabled": false, "categories": ["alt", "discovery"]},
    {"alias": "altsignals", "enabled": false, "categories": ["alt", "discovery"]},
    {"alias": "sol_signals", "enabled": false, "categories": ["alt", "discovery"]},
    {"alias": "forex_signal", "enabled": false, "categories": ["forex", "discovery"]},
    {"alias": "forex_signals_free", "enabled": false, "categories": ["forex", "discovery"]},
    {"alias": "fx_signals", "enabled": false, "categories": ["forex", "discovery"]},
    {"alias": "liquidation_alerts", "enabled": false, "categories": ["coinglass", "discovery"]},
    {"alias": "funding_rate_alerts", "enabled": false, "categories": ["coinglass", "discovery"]},
    {"alias": "lookonchain", "enabled": false, "categories": ["context", "discovery"]}
  ]
}
```

---

## 5. Activation Flow

```
DISCOVERY catalog (20 channels)
  → Add to collector config (disabled)
  → Enable one at a time
  → Collect 200 messages
  → Parse with existing parsers (WSQ_SETUP, GOLD_SETUP, etc.)
  → Count complete setups (entry+sl+tp)
  → If >= 10 → add to signal_tracker, backtest
  → If < 10 but > 0 → keep PENDING, collect more
  → If 0 → mark REJECTED or CONTEXT_ONLY
  → If TP-only → mark P3_CONTEXT, route to context_signals
```

---

## 6. Commands

```bash
# Re-qualify all channels
python3 -c "from modules.analysis_bundles.app.signal_tracker import archive_all_channels; print(archive_all_channels())"

# Check catalog
cat docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PIPELINE_01/catalog/telegram_signal_channels_catalog_v1.md

# Add discovery channels to collector (manual — update channels.json on admin-trading)
```
