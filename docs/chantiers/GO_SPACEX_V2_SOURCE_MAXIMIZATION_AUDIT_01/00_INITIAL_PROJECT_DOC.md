---
doc_id: GO_SPACEX_V2_SOURCE_MAXIMIZATION_AUDIT_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_SPACEX_V2_SOURCE_MAXIMIZATION_AUDIT_01
parent_go: GO_SPACEX_V2_LIVE_PAPER_TEST_20_SESSIONS_01
status: draft
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-12
links:
  - docs/chantiers/GO_SPACEX_V2_LIVE_PAPER_TEST_20_SESSIONS_01/00_INITIAL_PROJECT_DOC.md
  - modules/spcx_v2/
  - modules/ipo_tracking/
---

# GO_SPACEX_V2_SOURCE_MAXIMIZATION_AUDIT_01

## Audit Results — 2026-06-12 16:43 UTC (12:43 ET)

### P0 — Price Sources

| Source | Status | Price | Confidence | Bars | Volume |
|--------|--------|-------|------------|------|--------|
| **Yahoo chart** | ✅ LIVE | $166.37 | 0.25 | 56 real bars | 1.6M-9.9M/bar |
| **Nasdaq API** | ⚠️ lag | NO_PRICE_AVAILABLE_YET | 0 | 0 | 0 |
| **TradingView webhook** | ❌ no alerts | — | — | 0 SPCX events | 15,159 total events |

**Current state**: `source_count=1`, `price_trust=0.25`, `weighted_trust=0.25`
**Target**: `source_count>=2`, `price_trust>=0.50`

### P1 — Technical / SMC Sources

| Structure | Detected | Source |
|-----------|----------|--------|
| FVG Bullish | ✅ True | enriched smart_money |
| FVG Bearish | ✅ True | enriched smart_money |
| BOS | ✅ True | enriched smart_money |
| CHOCH | ✅ True | enriched smart_money |
| Liquidity Sweep Low | ❌ False | — |
| Liquidity Sweep High | ❌ False | — |

**VWAP**: Available (from Yahoo candle)  
**ORB**: Available (from enriched indicators — opening_range_5m/15m/30m)

### P1 — Context / Halo (available in data center)

| Group | Status | Symbols |
|-------|--------|---------|
| Space basket | ✅ data available | RKLB, ASTS (via bot_vision profiles) |
| Musk halo | ✅ data available | TSLA (via bot_vision profile) |
| AI halo | ✅ data available | NVDA (via bot_vision profile) |
| Crypto risk | ✅ live | BTC, ETH (Coinglass screenshots) |
| Macro | ✅ live | SPY, DXY, VIX, US10Y (production profile) |

### P1 — Coinglass

| Status | What's captured |
|--------|----------------|
| ✅ screenshots | BTC/ETH liquidations, funding, OI, L/S ratio every ~2min |
| ❌ integrated | Not yet wired into SPCX risk_proxy_score |

### P1 — SEC / News

| Source | Status | Detail |
|--------|--------|--------|
| **SEC EDGAR** | ✅ live | 40 filings, company: SPACE EXPLORATION TECHNOLOGIES CORP |
| Latest filing | 🔴 TODAY | 424B4 — IPO Prospectus (2026-06-12) |
| **RSS News** | ❌ empty | 0 headlines (new IPO, expected) |

### P1 — Bot Vision Screenshots

| Metric | Value |
|--------|-------|
| SFTP inbox PNGs | 6,355 |
| SPCX-specific screenshots | **0** (profile added to cron at 12:30, next execution 13:00 ET) |
| Schedule orchestrator | ✅ running (PID active since 12:35) |
| capture_headless.js | ✅ running RIGHT NOW (PID active at 12:43) |

### P1 — Desk / Sheets / Telegram

| Export | Status | Detail |
|--------|--------|--------|
| **Desk Pro** | ✅ ready | `export_desk.py` produces JSON |
| **Google Sheets** | ✅ ready | `export_sheets.py` produces CSV/JSONL |
| **Telegram** | ✅ ready | `export_telegram.py` A+ alerts + EOD summary |
| **Daily Report** | ✅ ready | `daily_summary.py` markdown |

### SPCX V2 Paper Log

| File | Size | Content |
|------|------|---------|
| candidates.jsonl | 2,841B | Multiple candidates logged |
| rejects.jsonl | 771B | Rejected candidates logged |
| summary.json | 333B | Aggregated stats |

### Enriched Pipeline Scores (live at $166.37)

| Score | Value |
|-------|-------|
| momentum | 0.929 |
| volatility | 1.000 |
| trend | 0.750 |
| catalyst | 1.000 |
| trade_ready | 0.417 |
| smart_money | 0.450 |
| risk | 0.387 |
| accumulation | 0.445 |
| liquidity | 0.000 ⚠️ |

### Source Capability Matrix

| Source | Available | Produces Data | Used by Scoring | Used by Export | Gap |
|--------|-----------|---------------|-----------------|----------------|-----|
| Yahoo chart | ✅ | ✅ live price+bars | ✅ | ✅ | volume not mapped to liquidity_score |
| Nasdaq quote | ✅ | ⚠️ lagging | ⚠️ veto only | ❌ | needs to go live |
| TradingView webhook | ✅ infra | ❌ no SPCX alerts | ❌ | ❌ | manual alert creation needed |
| Bot Vision screenshots | ✅ infra | ⏳ first SPCX capture imminent | ❌ | ❌ | needs OCR/analysis pipeline |
| Bot Vision SMC | ✅ | ✅ FVG/BOS/CHOCH via enriched | ❌ not in spcx_v2 | ❌ | wire smart_money → smart_money_score |
| Coinglass | ✅ | ✅ screenshots active | ❌ | ❌ | create risk_proxy_score |
| SEC EDGAR | ✅ | ✅ 40 filings, IPO prospectus | ✅ catalyst | ✅ | working |
| RSS News | ✅ | ❌ 0 items | ❌ | ❌ | expected for new IPO |
| Data Center | ✅ | ✅ 5,943 recent views | ❌ | ❌ | wire market regime |
| Desk Pro | ✅ | ✅ export scripts | ❌ | ✅ | wire spcx_v2 exports |
| Google Sheets | ✅ | ✅ export scripts | ❌ | ✅ | wire spcx_v2 exports |
| Telegram | ✅ | ✅ export scripts | ❌ | ✅ | wire spcx_v2 exports |
| Paper logs | ✅ | ✅ JSONL growing | ✅ | ✅ | working |
| Proxy backtest | ✅ | ✅ CSV replay | ✅ validation | ✅ | working |
| Session tracker | ✅ | ✅ session #2/20 | ✅ | ✅ | working |

### Gaps to Close

| Priority | Gap | Action |
|----------|-----|--------|
| P0 | TV webhook — 0 SPCX alerts | Create TradingView alert for NASDAQ:SPCX → /tv/spacex |
| P0 | Nasdaq live price | Wait for Nasdaq API to exit lag / add fallback |
| P0 | Liquidity score = 0 | Fix enriched_to_snapshot to map volume → liquidity_score |
| P1 | Bot Vision SPCX screenshots | Verify cron captures start at 13:00 ET |
| P1 | SMC structures → setup_detector | Wire enriched smart_money to spcx_v2 scoring |
| P1 | Coinglass → risk_proxy | Create risk_proxy_score from BTC funding/OI/liquidations |
| P2 | Desk/Sheets/Telegram exports | Hook spcx_v2 export scripts to session loop |
| P2 | Sector/halo context | Wire RKLB/ASTS/TSLA/NVDA to market_regime_score |
