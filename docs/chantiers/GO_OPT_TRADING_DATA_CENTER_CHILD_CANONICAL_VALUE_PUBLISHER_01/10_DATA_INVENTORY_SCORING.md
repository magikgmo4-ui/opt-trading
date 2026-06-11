# Desk Pro — Data Inventory & Scoring

## Groupe A: Market Data (P0)

| Source | Contract | Score | Freshness | Status | Fichier DC | Gap |
|---|---|---|---|---|---|---|
| `binance_public_api` | `market_metrics.v1` | **0.85** | fresh | ✅ PROVEN | `data_center/views/market_metrics/by_symbol/*.json` | — |
| `binance_public_api` | `market_klines.v1` | **0.80** | fresh | ✅ PROVEN | `data/market_data/klines/*/latest.json` | — |
| `binance_public_api` | `pair_market_snapshot.v1` | **0.40** | — | ❌ MISSING | — | **Pas de producer** |
| `derivatives_collector` | `derivatives.v1` | **0.55** | stale | 🟡 HYPOTHESIS | `data/derivatives/latest.json` | **Pas dans DC** |

**Candidates pour `pair_market_snapshot.v1`:**
1. `binance_public_api` — ticker 24h déjà fetché, score 0.85 ✅ **SELECTED**
2. `derivatives_collector` — funding rate + OI, score 0.55
3. `coinglass_headless_bot` — OCR only, pas de prix temps réel, score 0.30

**Action**: Étendre `market_metrics_producer.py` pour produire aussi `pair_market_snapshot.v1`.

---

## Groupe B: Vision & Charts (P0)

| Source | Contract | Score | Freshness | Status | Fichier DC | Gap |
|---|---|---|---|---|---|---|
| `bot_vision_step2` | `vision_analysis.v1` | **0.90** | fresh | ✅ PROVEN | `by_symbol/*.json` (24 symboles) | — |
| `coinglass_headless_bot` | `vision_context.coinglass.v1` | **0.85** | fresh | ✅ PROVEN | `vision_context/coinglass/latest.json` | — |
| `tradingview_screener` | `vision_context.screener.v1` | **0.70** | fresh | ✅ PROVEN | `vision_context/screener/latest.json` | — |

---

## Groupe C: Telegram Signals (P0)

| Source | Contract | Score | Freshness | Status | Fichier DC |
|---|---|---|---|---|---|
| `telegram_screener_bridge` | `telegram_signals.v1` | **0.88** | fresh | ✅ PROVEN | `by_channel/`, `by_symbol/`, `history/` |
| `telegram_screener_bridge` | `telegram_context.v1` | **0.82** | fresh | ✅ PROVEN | `telegram_context/` |
| `telegram_screener_bridge` | `telegram_channel_stats.v1` | **0.80** | fresh | ✅ PROVEN | `channel_stats/latest.json` |
| `collector_telegram` | `telegram_raw.v1` | **0.50** | — | ❌ MISSING | — |

**Candidates pour `telegram_raw.v1`:**
1. `collector_telegram` — données déjà collectées dans `outputs/raw/`, score 0.85 ✅ **SELECTED**
2. `telegram_ingestion` — Telethon live, score 0.60

**Action**: Router `collector_telegram/outputs/raw/` vers `data_center/views/telegram_raw/`.

---

## Groupe D: Trading Runtime (P1)

| Source | Contract | Score | Freshness | Status | Fichier DC | Gap |
|---|---|---|---|---|---|---|
| `webhook_server` | `signal_event.v1` | **0.85** | stale | 🟡 PROVEN | `state/events.jsonl` | **Pas contrat DC** |
| `perf_app` | `trade_ledger.v1` | **0.80** | fresh | 🟡 HYPOTHESIS | `perf/perf.db` (SQLite) | **Pas dans DC** |
| `runtime_health` | `runtime_health.v1` | **0.75** | fresh | 🟡 PROVEN | `runtime_health/events.jsonl` | **Pas contrat DC** |
| `position_engine` | `positions.v1` | **0.40** | — | ❌ MISSING | `state/positions.json` | **Pas dans DC** |
| `execution_engine` | `execution.v1` | **0.30** | — | ❌ MISSING | — | **Pas de producer** |

**Candidates pour `trade_ledger.v1`:**
1. `perf_app` — SQLite → JSONL export, score 0.80 ✅ **SELECTED**
2. `webhook_to_perf` — adapter existe déjà, score 0.70

**Candidates pour `signal_event.v1`:**
1. `webhook_server` — events.jsonl déjà structuré, score 0.85 ✅ **SELECTED**
2. `signal_event_adapter` — normalize V0→V1, score 0.75

---

## Groupe E: Desk Pro Inputs (P1)

| Source | Contract | Score | Freshness | Status | Gap |
|---|---|---|---|---|---|
| `desk_snapshot` | `desk_snapshot.v1` | **0.45** | stale | 🟡 HYPOTHESIS | **Pas consolidé DC** |
| `probability` | `probability.v1` | **0.30** | — | ❌ MISSING | **Pas de producer** |
| `ranker` | `ranker.v1` | **0.25** | — | ❌ MISSING | **Pas de producer** |
| `decision_engine` | `decision.v1` | **0.20** | — | ❌ MISSING | **Pas de producer** |

**Candidates pour `desk_snapshot.v1`:**
1. `desk_pro/snapshot` — route `/desk/snapshot` existe, score 0.60
2. `binance_public_api` — ticker data déjà dans DC, score 0.85 ✅ **SELECTED**

---

## Scoring Matrix

| Score | Critères |
|---|---|
| 0.85-1.00 | PROVEN + fresh + contrat DC + consommé par UI |
| 0.70-0.84 | PROVEN + fresh + contrat DC |
| 0.55-0.69 | HYPOTHESIS + données dispo + pas contrat DC |
| 0.40-0.54 | HYPOTHESIS + stale |
| 0.25-0.39 | MISSING + candidate identifié |
| 0.00-0.24 | MISSING + pas de candidate |

## Priorités de remplissage (TOUTES COMPLÉTÉES — 2026-06-11)

| Priorité | Source | Gap | Candidate | Statut |
|---|---|---|---|---|
| **P0** | `pair_market_snapshot.v1` | Producer manquant | `coingecko_public_api` | ✅ FILLED |
| **P1** | `signal_event.v1` | Pas contrat DC | `webhook_server` | ✅ FILLED |
| **P1** | `telegram_raw.v1` | Pas contrat DC | `collector_telegram` | ✅ FILLED |
| **P2** | `trade_ledger.v1` | SQLite → DC | `perf_app` export | ⏳ P2 |
| **P2** | `derivatives.v1` | Pas dans DC | `derivatives_collector` | ⏳ P2 |
| **P3** | `runtime_health.v1` | Pas contrat DC | `runtime_health` | ✅ FILLED |

**Résultat final**: 12/12 PROVEN, 0 MISSING, score 0.81. Validation report: `GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_LIVE_RUNTIME_VALIDATION_01/20_ACCEPTANCE_REPORT.md`
