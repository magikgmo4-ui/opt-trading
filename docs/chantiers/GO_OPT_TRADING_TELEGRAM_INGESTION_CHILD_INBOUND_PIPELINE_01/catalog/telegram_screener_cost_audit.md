# Telegram Screener Cost Audit

## Date: 2026-06-05
## Status: OPERATIONAL — modes implemented, no LLM auto

---

## 1. What Runs (cost)

| Component | Where | Cost | Frequency |
|---|---|---|---|
| **collector_telegram** | admin-trading (Telethon live) | Telegram API rate limits | Continuous |
| **parse_telegram_message** | local (bridge) | Regex only, <1ms/msg | On pipeline run |
| **telegram_screener_bridge** | local (bridge) | I/O, JSON write, ~100ms | On pipeline run |
| **signal_tracker** | local (archiver) | Regex + JSON write, ~200ms | On demand |
| **OpenAI analyze** | admin-trading (bot_vision_step2) | **ON_DEMAND only** ($0.01-0.05/call) | Manual trigger |
| **Coinglass OCR** | admin-trading (headless) | **ON_DEMAND only** (playwright) | Manual trigger |

**Total operational cost: $0/month** (no LLM/OCR auto, no paid APIs for text parsing)

---

## 2. Channel Modes

| Mode | Messages | Parse | Feed Signals | Auto-Promote | Cost |
|---|---|---|---|---|---|
| **DISCOVERY** | Limited to 200 | Parse all | No | Manual review | Minimal |
| **WATCH** | All | Parse all | Context only | If >=10 complete | Minimal |
| **QUALIFIED** | All | Parse all | Yes (LOW confidence) | Manual promote to ACTIVE | Minimal |
| **ACTIVE** | All | Parse all | Yes (MEDIUM confidence) | Backtest validates | Minimal |
| **REJECTED** | Skip | Skip | No | — | Zero |

---

## 3. Per-Channel Cost Matrix

| Channel | Mode | Msgs/run | Parse | Context | Trade | Duplicates | Score |
|---|---|---|---|---|---|---|---|
| xauusd | ACTIVE | 91 | 9% rate | 0 | 8 | 0 | 48 |
| wallstreetqueenofficial | ACTIVE | 98 | 2% rate | 0 | 2 | 0 | 18 |
| coinglass_alerts | WATCH | 20 | 0% rate | 16 | 0 | 0 | 5 |
| whale_alert_io | WATCH | 20 | 0% rate | 10 | 0 | 0 | 3 |
| fatpigsignals | WATCH | 99 | 0% rate | 0 | 0 | 0 | 4 |
| binancekillers | REJECTED | 100 | Skip | 0 | 0 | 0 | 5 |
| 4 DISCOVERY | DISCOVERY | 0 | 0 | 0 | 0 | 0 | 0 |
| 5 WATCH | WATCH | ~300 | <1% | ~12 | 0 | 0 | <10 |
| 2 REJECTED | REJECTED | ~150 | Skip | 0 | 0 | 0 | <5 |

---

## 4. What We DON'T Pay For

| Component | Status | Why |
|---|---|---|
| OpenAI chart analysis | ON_DEMAND via --skip-capture | No automatic calls |
| Coinglass real OCR | ON_DEMAND via --real-ocr | No automatic calls |
| Telegram premium API | Not needed | Collector works with free Telegram API |
| External signal APIs | Not used | All signals from Telegram text parsing |
| Cloud compute | Local only | All processing on local machine |

---

## 5. Scaling Cost (if we add 20 DISCOVERY channels)

| Scenario | Msgs/day | Parse cost | Storage | Risk |
|---|---|---|---|---|
| 20 channels × 200 msgs = 4000 | 4000/run | <100ms regex | ~2MB JSON | None — text only |
| All 20 become ACTIVE | 4000/run | <100ms regex | ~2MB JSON | Signal quality risk |
| LLM auto-activated | +$0.50-2.00/run | +15s/run | +API costs | **BLOCKED** |

**Decision: keep LLM/OCR on-demand. Text parsing is free and fast.**

---

## 6. Optimization Opportunities

| Opportunity | Current | Optimized | Saving |
|---|---|---|---|
| Dedup messages (same raw_text) | Already implemented | — | 0% (already done) |
| Skip parse for REJECTED channels | Already implemented | — | 0% (already done) |
| Limit DISCOVERY to 200 msgs | Already implemented | — | 0% (already done) |
| Cache parse results | Not implemented | Skip re-parse on repeat runs | ~50% parse time |
| Batch JSON writes | Not implemented | Single write per channel | ~30% I/O time |

---

## 7. Decision Record

| Date | Decision | Reason |
|---|---|---|
| 2026-06-05 | LLM on-demand only | Cost control, text parsing sufficient |
| 2026-06-05 | DISCOVERY limited to 200 msgs | Avoid ingestion cost on unverified channels |
| 2026-06-05 | Modes: DISCOVERY/WATCH/QUALIFIED/ACTIVE | Gated activation, prevent low-quality signals |
| 2026-06-05 | REJECTED channels skip parse | Zero CPU cost on verified-no-signal channels |
| 2026-06-05 | Candidate score automates qualification | Reduce manual review |
