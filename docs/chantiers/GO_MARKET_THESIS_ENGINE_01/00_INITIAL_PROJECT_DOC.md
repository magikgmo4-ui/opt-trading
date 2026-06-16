# GO_MARKET_THESIS_ENGINE_01 — Initial Project Document

> **Status:** PENDING VALIDATION — Ne coder aucun fichier avant validation complète

---

## Table des matières

1. [Audit des producteurs existants](#1-audit-des-producteurs-existants)
2. [Cartographie des datasets disponibles](#2-cartographie-des-datasets-disponibles)
3. [Contrat market_thesis.v1](#3-contrat-market_thesisv1)
4. [Architecture détaillée](#4-architecture-détaillée)
5. [Arborescence fichiers](#5-arborescence-fichiers)
6. [Schémas de données Pydantic](#6-schémas-de-données-pydantic)
7. [Plan d'implémentation détaillé](#7-plan-dimplémentation-détaillé)
8. [Découpage en PRs indépendantes](#8-découpage-en-prs-indépendantes)
9. [Kanban détaillé](#9-kanban-détaillé)
10. [Matrice risques / dépendances](#10-matrice-risques--dépendances)
11. [Plan de tests](#11-plan-de-tests)
12. [Plan de déploiement progressif](#12-plan-de-déploiement-progressif)
13. [Plan de validation](#13-plan-de-validation)
14. [Estimation de complexité](#14-estimation-de-complexité)

---

## 1. Audit des producteurs existants

### 1.1 Collectors (producteurs de données brutes)

| Module | Source | Contrat produit | Symboles | Données clés |
|--------|--------|-----------------|----------|-------------|
| `collector_binance_spot` | Binance REST | `pair_market_snapshot` | BTC, ETH, SOL, XRP, DOGE, BNB, ADA, AVAX, LINK, INJ, APT, OP, PAXG (XAU proxy) | price, change_24h, high/low_24h, volume_24h |
| `collector_coingecko` | CoinGecko API | `market_snapshot` | Idem | price, change_24h, market_cap |
| `collector_telegram` | Telegram messages | structured records | 36 channels × 21 symbols | thesis extraction, asset detection |
| `derivatives_collector` | Binance/Bitget FAPI + Coinglass headless | `market_metrics.v1` | BTCUSDT, ETHUSDT (full), SOLUSDT, XRPUSDT, DOGEUSDT (partial) | OI, funding_rate, volume_futures, L/S ratio, liquidations_long, liquidations_short |
| `bot_vision` (headless) | TradingView/Coinglass screenshots | `vision_analysis.v1`, `vision_context.coinglass.v1` | 24 symbols (BTC/ETH/SOL/XRP/XAU/SPY/VIX/etf/commodities/fx) | support, resistance, trend, OI, liq levels |
| `spacex_super_desk_collector` | DeskPro internal | `spacex_super_desk.v1` | SPCX, NVDA, PLTR, RKLB, ASTS, LUNR, AMD, AVGO, MRVL, MU | price, gap_ipo, momentum, smart_money, risk, trade_ready |

### 1.2 Producers (agrégateurs Data Center)

| Module | Contrat produit | Symboles canoniques |
|--------|-----------------|---------------------|
| `market_metrics_producer` | `market_metrics.v1` + `pair_market_snapshot.v1` | BTC, ETH, SOL, XRP, DOGE, BNB, ADA, AVAX, LINK, INJ, APT, OP, XAU (PAXG proxy) |
| `multitf_analysis_producer` | `multitf_analysis_input.v1` | BTC, ETH, SOL, XAUUSD, SPCX |
| `multitf_setup_scorer` | `multitf_setup_score.v1` | BTC, ETH, SOL, XAUUSD, SPCX |
| `canonical_value_publisher` | `canonical_value.v1` | Résolution cross-source |
| `external_data_producers` | 10 contrats additionnels | (DXY, VIX, SPY, macro, etc.) |

### 1.3 Engines (scoring / décision)

| Module | Rôle | Output clé |
|--------|------|-----------|
| `market_scanner` | Score tendance + momentum + volatilité | `scan_score`, `BUY/SELL/NEUTRAL` |
| `probability_engine` | Probabilité directionnelle (ensemble pondéré) | `probability_long`, `probability_short` |
| `liquidation_analyzer` | Biais liquidation + intensité | `liquidation_bias`, `intensity` |
| `derivatives_analyzer` | Structure marché dérivés | `squeeze_risk`, `crowding_risk`, `directional_bias` |
| `opportunity_ranker` | Score opportunité consolidé | `opportunity_score`, `setup_bias`, `priority` |
| `decision_engine` | Décision GO_LONG/GO_SHORT/WAIT/REJECT | `Signal` (engine, side, reason, entry_zone, invalidation, TPs) |
| `risk_engine` | Position sizing | `risk_usd`, `qty`, `distance` |
| `proposition_engine` | Proposition via LLM (OpenClaw bridge) | `Proposition` (action, size_pct, confidence, rationale) |

### 1.4 Dashboards (consommateurs)

| Module | Point de montage | État actuel |
|--------|-----------------|-------------|
| **DeskPro** | `/desk` sur perf_app:8010 | Snapshot builder + scoring + 4 vision panels. Interface SPCX-first. |
| **Voice Operator** | `/read/*` sur port 8500 | 8 endpoints read-only. Agrège DeskPro + Perf + LocalCMS. Pas de thèse unifiée. |
| **LocalCMS** | `/cms` sur perf_app:8010 | System cockpit read-only. TMUX health, journal, signals. |
| **Perf App** | `/perf/*` sur 8010 | Ledger + equity curve + promotion gates. |

### 1.5 Signaux entrants (flow complet)

```
TradingView alert → POST /tv (webhook_server:8000) → risk_quote() → events.jsonl
                                                              ├→ POST /perf/event
                                                              └→ signal_event.v1 (Data Center)

TradingView CDP → POST /tv/cdp → signal_event.v1 (DC sink, monitor-only)

Telegram message → telegram_ingestion (Telethon) → parser → normalizer → distribution
                → telegram_screener (pipeline) → SignalCandidate → telegram_claim

Derivatives → derivatives_collector → market_metrics.v1 → data_center views

Vision → bot_vision headless → vision_analysis.v1 + vision_context.coinglass.v1
```

### 1.6 Gaps identifiés (aucun module existant ne couvre)

1. **Aucune agrégation cross-source unifiée** — chaque dashboard lit ses propres sources, pas de vue consolidée par symbole
2. **Aucun Context Engine** — le `multitf_analysis_producer` agrège partiellement mais ne produit pas de contexte structuré (contexte/flux/news/risques)
3. **Aucun Thesis Engine** — pas de narrative generator ni de synthèse actionnable par actif
4. **Aucun Confidence Engine** — les scores de confiance existent par engine mais pas de méta-confiance cross-source
5. **Aucun Historical Outcome Engine** — les thèses passées ne sont pas archivées ni mesurées
6. **Voice Operator incomplet** — lit BTC, XAUUSD, SPCX via multitf_reader mais pas ETH, SOL, XRP, NVDA, AVGO, MU
7. **DeskPro limité à SPCX** — le scoring DeskPro est SPCX-centrique, pas multi-actifs

---

## 2. Cartographie des datasets disponibles

### 2.1 Matrice de disponibilité par actif cible

| Actif | Price | OI | Funding | Liq | L/S | S/R Levels | Trend (HTF/LTF) | Setups | Score | VWAP | Macro | Telegram | True Value | Signals CDP | Vision |
|-------|-------|-----|---------|-----|-----|-----------|-----------------|--------|-------|------|------|----------|------------|-------------|--------|
| **BTC** | ✔ P0 | ✔ | ✔ | ✔ | ✔ | ✔ (vision) | ✔ H4/H1/M15 | ✔ A+-C | ✔ 0-100 | ✔ | partial | ✔ 36ch | - | ✔ | ✔ |
| **ETH** | ✔ P0 | ✔ | ✔ | ✔ | ✔ | ✔ (vision) | ✔ H4/H1/M15 | ✔ A+-C | ✔ 0-100 | ✔ | partial | ✔ | - | - | ✔ |
| **SOL** | ✔ P1 | ✔ | ✔ | ✔ | ✔ | ✔ (vision) | ✔ H4/H1/M15 | ✔ A+-C | ✔ 0-100 | ✔ | partial | - | - | - | ✔ |
| **XRP** | ✔ P1 | ✔ | ✔ | ✔ | ✔ | ✔ (vision) | ❌ | ❌ | ❌ | ❌ | ❌ | ✔ | - | - | ✔ |
| **XAU** | ✔ P0(PAXG) | ❌ | ❌ | ❌ | ❌ | ✔ (OANDA) | ✔ H4/H1/M15 | ✔ A+-C | ✔ 0-100 | ✔ | partial | ✔ | - | - | ✔ |
| **SPCX** | ✔ (spacex) | ❌ | ❌ | ❌ | ❌ | ❌ | ✔ (special) | ✔ A+-C | ✔ 0-100 | ✔ | partial | - | ✔ 8 scores | ✔ | ❌ |
| **NVDA** | ✔ (Yahoo) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✔ (VIX/SPY) | - | ✔ true_value | - | ❌ |
| **AVGO** | ✔ (Yahoo) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✔ (VIX/SPY) | - | ✔ true_value | - | ❌ |
| **MU** | ✔ (Yahoo) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✔ (VIX/SPY) | - | ✔ true_value | - | ❌ |

### 2.2 Fichiers DC lus par le Market Thesis Engine

Tous les chemins sont sous `data/data_center/views/`:

```
market_metrics/by_symbol/{SYM}.json              → price, OI, funding, volume, liq
multitf_analysis_input.v1/by_symbol/{SYM}.json   → structure, levels, timeframes, signals, macro, orderflow
multitf_setup_score.v1/by_symbol/{SYM}.json      → bias, setups[], grades, scores, probabilities
vision_analysis/by_symbol/{SYM}.json             → support/resistance, analysis_summary
signal_event.v1/by_symbol/{SYM}/latest.json      → last webhook event
spacex_true_value.v1/by_symbol/{SYM}.json        → true_value scores (NVDA, AVGO, MU, SPCX)
telegram_signals/by_symbol/{SYM}/...             → telegram sentiment (BTC, ETH, XRP, XAU)

data/deskpro/inputs/vision_context/coinglass/latest.json  → OI, liq (via OCR stubs)
data/deskpro/inputs/vision_context/news_sentiment/latest.json → news sentiment
```

### 2.3 Sources de données macro (globales, non par symbole)

```
data/data_center/views/market_metrics/by_symbol/DXY.json   → DXY price
data/data_center/views/market_metrics/by_symbol/SPY.json   → SPY price
data/deskpro/inputs/vision_analysis/by_symbol/TVC:VIX/     → VIX
data/deskpro/inputs/vision_analysis/by_symbol/TVC:US10Y/   → US10Y yield
```

### 2.4 Regroupement par section de thèse

| Section thèse | Sources de données |
|---------------|-------------------|
| **Contexte** (macro, regime) | DXY trend, VIX state, SPY trend, US10Y, BTC dominance, fear_greed, risk_regime |
| **Technique** (structure, levels, setups) | multitf_analysis_input (timeframes, levels, signals), multitf_setup_score (bias, setups, grades), vision_analysis (S/R) |
| **Flux** (funding, OI, liquidations) | market_metrics (OI, funding_rate, volume_futures, long_short_ratio, liquidations), derivatives_analyzer (squeeze, crowding) |
| **News** (sentiment, signaux) | vision_context.news_sentiment, telegram_signals, vision_analysis (analysis_summary), signal_event (latest reason) |
| **Risques** (concentration, squeeze, invalidation) | derivatives_analyzer (squeeze_risk, crowding_risk), liquidation_analyzer (bias, intensity), market_metrics (OI change) |
| **Probabilités** (scoring synthesis) | probability_engine (prob_long/short), opportunity_ranker (opportunity_score), multitf_setup_score (score, confidence), DeskPro scoring |
| **Action** (recommandation, pas d'ordre) | Synthèse de toutes les sections → biais directionnel + conviction + niveaux clés |

---

## 3. Contrat market_thesis.v1

### 3.1 JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://opt-trading/schemas/market_thesis_v1.json",
  "title": "Market Thesis v1",
  "description": "Unified market thesis per asset — read-only, no trade execution",
  "type": "object",
  "required": [
    "schema", "thesis_id", "symbol", "asset_class", "generated_at",
    "context", "technique", "flows", "news", "risks",
    "probabilities", "action", "sources", "freshness", "meta"
  ],
  "properties": {
    "schema": {
      "const": "market_thesis.v1"
    },
    "thesis_id": {
      "type": "string",
      "description": "ULID unique: thesis_<symbol>_<timestamp>"
    },
    "symbol": {
      "type": "string",
      "description": "Canonical symbol: BTC, ETH, SOL, XRP, XAU, SPCX, NVDA, AVGO, MU"
    },
    "asset_class": {
      "type": "string",
      "enum": ["crypto_perp", "forex_cfd", "stock", "ipo", "commodity", "index"]
    },
    "generated_at": {
      "type": "string",
      "format": "date-time"
    },
    "ttl_seconds": {
      "type": "integer",
      "default": 300,
      "description": "Cache TTL. Thesis is valid for 5 min, then must be regenerated."
    },

    "context": {
      "$ref": "#/$defs/ContextSection"
    },
    "technique": {
      "$ref": "#/$defs/TechniqueSection"
    },
    "flows": {
      "$ref": "#/$defs/FlowsSection"
    },
    "news": {
      "$ref": "#/$defs/NewsSection"
    },
    "risks": {
      "$ref": "#/$defs/RisksSection"
    },
    "probabilities": {
      "$ref": "#/$defs/ProbabilitiesSection"
    },
    "action": {
      "$ref": "#/$defs/ActionSection"
    },

    "sources": {
      "$ref": "#/$defs/SourcesSection"
    },
    "freshness": {
      "$ref": "#/$defs/FreshnessSection"
    },
    "meta": {
      "type": "object",
      "description": "Arbitrary metadata",
      "properties": {
        "engine_version": { "type": "string", "const": "1.0.0" },
        "runtime_ms": { "type": "integer" },
        "cache_hit": { "type": "boolean" }
      }
    }
  },

  "$defs": {
    "ContextSection": {
      "type": "object",
      "required": ["macro_regime", "market_phase", "narrative"],
      "properties": {
        "macro_regime": {
          "type": "object",
          "properties": {
            "risk_environment": { "type": "string", "enum": ["risk_on", "risk_off", "neutral", "unknown"] },
            "dxy_trend": { "type": "string", "enum": ["bullish", "bearish", "neutral", "unknown"] },
            "vix_state": { "type": "string", "enum": ["low", "normal", "elevated", "high", "unknown"] },
            "spy_trend": { "type": "string", "enum": ["bullish", "bearish", "neutral", "unknown"] },
            "us10y_trend": { "type": "string", "enum": ["rising", "falling", "flat", "unknown"] },
            "btc_dominance": { "type": "number", "description": "BTC.D percentage" },
            "fear_greed_index": { "type": ["integer", "null"], "minimum": 0, "maximum": 100 }
          }
        },
        "market_phase": {
          "type": "object",
          "properties": {
            "phase": { "type": "string", "enum": ["accumulation", "markup", "distribution", "markdown", "unknown"] },
            "trend_strength": { "type": "string", "enum": ["strong", "moderate", "weak", "ranging"] },
            "volatility_regime": { "type": "string", "enum": ["low", "normal", "high", "extreme"] }
          }
        },
        "narrative": {
          "type": "string",
          "description": "1-2 sentence French narrative of the macro context"
        }
      }
    },

    "TechniqueSection": {
      "type": "object",
      "required": ["htf_bias", "ltf_bias", "alignment", "key_levels", "active_setups", "narrative"],
      "properties": {
        "htf_bias": {
          "type": "object",
          "properties": {
            "direction": { "type": "string", "enum": ["bullish", "bearish", "neutral"] },
            "timeframe": { "type": "string", "description": "W1 or D1" },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "ltf_bias": {
          "type": "object",
          "properties": {
            "direction": { "type": "string", "enum": ["bullish", "bearish", "neutral"] },
            "timeframe": { "type": "string", "description": "H4 or H1" },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "alignment": {
          "type": "string",
          "enum": ["aligned_bullish", "aligned_bearish", "divergent", "neutral"],
          "description": "HTF/LTF alignment"
        },
        "key_levels": {
          "type": "object",
          "properties": {
            "support": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "level": { "type": "number" },
                  "strength": { "type": "string", "enum": ["major", "minor", "micro"] },
                  "source": { "type": "string" }
                }
              }
            },
            "resistance": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "level": { "type": "number" },
                  "strength": { "type": "string", "enum": ["major", "minor", "micro"] },
                  "source": { "type": "string" }
                }
              }
            },
            "vwap": { "type": ["number", "null"] },
            "price_vs_vwap": { "type": "string", "enum": ["above", "below", "at", "unknown"] }
          }
        },
        "active_setups": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "setup_id": { "type": "string" },
              "direction": { "type": "string", "enum": ["long", "short", "monitor_only"] },
              "grade": { "type": "string", "enum": ["A+", "A", "A-", "B+", "B", "B-", "C", "REJECT"] },
              "score": { "type": "integer", "minimum": 0, "maximum": 100 },
              "entry_zone": { "type": "object", "properties": { "low": {"type": "number"}, "high": {"type": "number"} } },
              "invalidation": { "type": "number" },
              "targets": { "type": "array", "items": { "type": "number" } },
              "reason": { "type": "string" }
            }
          }
        },
        "narrative": {
          "type": "string",
          "description": "French narrative: structure, levels, setups summary"
        }
      }
    },

    "FlowsSection": {
      "type": "object",
      "required": ["derivatives", "positioning", "narrative"],
      "properties": {
        "derivatives": {
          "type": "object",
          "properties": {
            "open_interest": { "type": ["number", "null"] },
            "oi_change_24h_pct": { "type": ["number", "null"] },
            "funding_rate": { "type": ["number", "null"] },
            "funding_bias": { "type": "string", "enum": ["positive", "negative", "neutral", "unknown"] },
            "long_short_ratio": { "type": ["number", "null"] },
            "liquidations_long_24h": { "type": ["number", "null"] },
            "liquidations_short_24h": { "type": ["number", "null"] },
            "liquidation_bias": { "type": "string", "enum": ["longs_at_risk", "shorts_at_risk", "balanced", "unknown"] },
            "squeeze_risk": { "type": "string", "enum": ["high", "moderate", "low", "unknown"] },
            "crowding_risk": { "type": "string", "enum": ["high", "moderate", "low", "unknown"] }
          }
        },
        "positioning": {
          "type": "object",
          "properties": {
            "etf_flow": { "type": "string", "enum": ["strong_inflow", "inflow", "flat", "outflow", "strong_outflow", "unknown"] },
            "futures_flow": { "type": "string", "enum": ["in", "out", "flat", "unknown"] },
            "smart_money_signal": { "type": "string", "enum": ["accumulating", "distributing", "neutral", "unknown"] },
            "telegram_sentiment": { "type": "string", "enum": ["bullish", "bearish", "mixed", "silent"] },
            "active_telegram_channels": { "type": "integer" }
          }
        },
        "narrative": {
          "type": "string",
          "description": "French narrative: flows and positioning analysis"
        }
      }
    },

    "NewsSection": {
      "type": "object",
      "required": ["sentiment", "key_drivers", "narrative"],
      "properties": {
        "sentiment": {
          "type": "object",
          "properties": {
            "overall": { "type": "string", "enum": ["positive", "neutral", "negative", "unknown"] },
            "score": { "type": "number", "minimum": -1, "maximum": 1 },
            "article_count": { "type": "integer" },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "key_drivers": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "driver": { "type": "string" },
              "impact": { "type": "string", "enum": ["positive", "negative", "neutral"] },
              "source": { "type": "string" },
              "ts": { "type": "string", "format": "date-time" }
            }
          }
        },
        "recent_signals": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "source": { "type": "string", "enum": ["telegram", "tradingview_cdp", "vision"] },
              "event": { "type": "string" },
              "direction": { "type": "string", "enum": ["buy", "sell", "neutral"] },
              "ts": { "type": "string", "format": "date-time" }
            }
          }
        },
        "narrative": {
          "type": "string",
          "description": "French narrative: news and signals sentiment"
        }
      }
    },

    "RisksSection": {
      "type": "object",
      "required": ["concentration", "technical", "event", "narrative"],
      "properties": {
        "concentration": {
          "type": "object",
          "properties": {
            "overall": { "type": "string", "enum": ["high", "moderate", "low", "unknown"] },
            "factors": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "factor": { "type": "string" },
                  "severity": { "type": "string", "enum": ["high", "moderate", "low"] },
                  "detail": { "type": "string" }
                }
              }
            }
          }
        },
        "technical": {
          "type": "object",
          "properties": {
            "invalidation_level": { "type": ["number", "null"] },
            "max_adverse_excursion_pct": { "type": ["number", "null"] },
            "gap_risk": { "type": "string", "enum": ["high", "moderate", "low", "unknown"] },
            "correlation_risk": { "type": "string", "enum": ["high", "moderate", "low", "unknown"] }
          }
        },
        "event": {
          "type": "object",
          "properties": {
            "macro_event_soon": { "type": "boolean" },
            "earnings_soon": { "type": "boolean" },
            "regulatory_risk": { "type": "string", "enum": ["high", "moderate", "low", "unknown"] }
          }
        },
        "narrative": {
          "type": "string",
          "description": "French narrative: risk synthesis"
        }
      }
    },

    "ProbabilitiesSection": {
      "type": "object",
      "required": ["scores", "consensus", "disagreement", "narrative"],
      "properties": {
        "scores": {
          "type": "object",
          "properties": {
            "probability_long": { "type": ["number", "null"], "minimum": 0, "maximum": 1 },
            "probability_short": { "type": ["number", "null"], "minimum": 0, "maximum": 1 },
            "opportunity_score": { "type": ["number", "null"], "minimum": 0, "maximum": 1 },
            "setup_score": { "type": ["integer", "null"], "minimum": 0, "maximum": 100 },
            "true_value_score": { "type": ["number", "null"], "minimum": 0, "maximum": 100 },
            "deskpro_probability": { "type": ["number", "null"], "minimum": 0, "maximum": 1 }
          }
        },
        "consensus": {
          "type": "object",
          "properties": {
            "direction": { "type": "string", "enum": ["bullish", "bearish", "neutral", "conflicted"] },
            "conviction": { "type": "string", "enum": ["high", "moderate", "low", "none"] },
            "engine_agreement_pct": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "disagreement": {
          "type": "object",
          "properties": {
            "has_disagreement": { "type": "boolean" },
            "details": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "engines": { "type": "array", "items": { "type": "string" } },
                  "conflict": { "type": "string" },
                  "resolution_note": { "type": "string" }
                }
              }
            }
          }
        },
        "narrative": {
          "type": "string",
          "description": "French narrative: probability and confidence synthesis"
        }
      }
    },

    "ActionSection": {
      "type": "object",
      "required": ["bias", "readiness", "key_levels_to_watch", "narrative", "voice_one_liner"],
      "properties": {
        "bias": {
          "type": "object",
          "properties": {
            "direction": { "type": "string", "enum": ["bullish", "bearish", "neutral", "wait"] },
            "confidence": { "type": "string", "enum": ["high", "moderate", "low", "none"] },
            "conviction_score": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        },
        "readiness": {
          "type": "string",
          "enum": ["ready", "monitor_only", "wait_for_trigger", "stand_aside"],
          "description": "Is the asset trade-ready? No auto-execution."
        },
        "key_levels_to_watch": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "level": { "type": "number" },
              "type": { "type": "string", "enum": ["entry", "invalidation", "target", "alert"] },
              "label": { "type": "string" }
            }
          }
        },
        "narrative": {
          "type": "string",
          "description": "French narrative: action recommendation"
        },
        "voice_one_liner": {
          "type": "string",
          "description": "Single-line French summary for voice operator TTS"
        }
      }
    },

    "SourcesSection": {
      "type": "object",
      "required": ["used", "missing", "stale", "confidence"],
      "properties": {
        "used": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Source contracts that contributed data"
        },
        "missing": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Expected sources that had no data"
        },
        "stale": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Sources with stale data (> age threshold)"
        },
        "confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1,
          "description": "Overall source quality score (0-1)"
        }
      }
    },

    "FreshnessSection": {
      "type": "object",
      "required": ["overall", "max_age_minutes", "components"],
      "properties": {
        "overall": {
          "type": "string",
          "enum": ["fresh", "stale", "partial", "expired"]
        },
        "max_age_minutes": {
          "type": "number",
          "description": "Age of the oldest source used"
        },
        "components": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "source": { "type": "string" },
              "age_minutes": { "type": "number" },
              "state": { "type": "string", "enum": ["fresh", "stale", "missing"] }
            }
          }
        }
      }
    }
  }
}
```

### 3.2 Exemple de payload market_thesis.v1 (BTC)

```json
{
  "schema": "market_thesis.v1",
  "thesis_id": "thesis_BTC_20260615T120000Z",
  "symbol": "BTC",
  "asset_class": "crypto_perp",
  "generated_at": "2026-06-15T12:00:00Z",
  "ttl_seconds": 300,

  "context": {
    "macro_regime": {
      "risk_environment": "risk_on",
      "dxy_trend": "bearish",
      "vix_state": "low",
      "spy_trend": "bullish",
      "us10y_trend": "flat",
      "btc_dominance": 58.2,
      "fear_greed_index": 72
    },
    "market_phase": {
      "phase": "markup",
      "trend_strength": "moderate",
      "volatility_regime": "normal"
    },
    "narrative": "Contexte macro favorable : DXY en baisse, VIX bas (<15), SPY haussier. BTC.D à 58% montre un marché crypto dominé par BTC. Fear & Greed à 72 (greed) suggère prudence mais pas d'euphorie extrême."
  },

  "technique": {
    "htf_bias": { "direction": "bullish", "timeframe": "D1", "confidence": 0.75 },
    "ltf_bias": { "direction": "bearish", "timeframe": "H4", "confidence": 0.65 },
    "alignment": "divergent",
    "key_levels": {
      "support": [
        { "level": 65000, "strength": "major", "source": "vision_analysis" },
        { "level": 62000, "strength": "major", "source": "vision_analysis" }
      ],
      "resistance": [
        { "level": 72000, "strength": "major", "source": "vision_analysis" }
      ],
      "vwap": 66450,
      "price_vs_vwap": "below"
    },
    "active_setups": [
      {
        "setup_id": "btc_vwap_reclaim",
        "direction": "long",
        "grade": "B",
        "score": 62,
        "entry_zone": { "low": 66300, "high": 66700 },
        "invalidation": 65000,
        "targets": [68000, 70000],
        "reason": "Reclaim VWAP H4 avec support 65000. HTF D1 haussier mais LTF H4 encore bearish — attente confirmation."
      }
    ],
    "narrative": "Structure D1 haussière mais H4 bearish : divergence HTF/LTF. Prix sous VWAP. Support majeur à 65000, résistance à 72000. Setup VWAP reclaim grade B en attente de confirmation H1."
  },

  "flows": {
    "derivatives": {
      "open_interest": 28500000000,
      "oi_change_24h_pct": 2.1,
      "funding_rate": 0.0035,
      "funding_bias": "positive",
      "long_short_ratio": 1.8,
      "liquidations_long_24h": 45000000,
      "liquidations_short_24h": 12000000,
      "liquidation_bias": "longs_at_risk",
      "squeeze_risk": "moderate",
      "crowding_risk": "high"
    },
    "positioning": {
      "etf_flow": "inflow",
      "futures_flow": "in",
      "smart_money_signal": "accumulating",
      "telegram_sentiment": "bullish",
      "active_telegram_channels": 12
    },
    "narrative": "OI en hausse (+2.1%), funding positif suggère dominance longs. Ratio L/S à 1.8 : sur-foule longs. Liquidations longs 3x shorts — risque de squeeze long. ETF inflows continus. Attention crowding long élevé."
  },

  "news": {
    "sentiment": {
      "overall": "positive",
      "score": 0.45,
      "article_count": 23,
      "confidence": 0.7
    },
    "key_drivers": [
      { "driver": "ETF inflows record", "impact": "positive", "source": "news_sentiment", "ts": "2026-06-15T10:30:00Z" },
      { "driver": "CPI lower than expected", "impact": "positive", "source": "macro_event", "ts": "2026-06-14T14:00:00Z" }
    ],
    "recent_signals": [
      { "source": "telegram", "event": "BTC LONG signal", "direction": "buy", "ts": "2026-06-15T11:00:00Z" },
      { "source": "tradingview_cdp", "event": "vwap_loss", "direction": "sell", "ts": "2026-06-15T10:45:00Z" }
    ],
    "narrative": "Sentiment news globalement positif (score +0.45). ETF inflows et CPI bas soutiennent le biais haussier. Signaux Telegram bullish mais CDP montre vwap_loss H4 récent — divergence court terme."
  },

  "risks": {
    "concentration": {
      "overall": "high",
      "factors": [
        { "factor": "Long crowding (L/S 1.8)", "severity": "high", "detail": "Ratio L/S élevé. Risque de cascade de liquidations si support 65000 casse." },
        { "factor": "Funding rate positif", "severity": "moderate", "detail": "Funding à 0.0035% — coût modéré mais signe de sur-foule." },
        { "factor": "Fear & Greed 72", "severity": "moderate", "detail": "Zone greed pas extrême mais suggère prudence." }
      ]
    },
    "technical": {
      "invalidation_level": 65000,
      "max_adverse_excursion_pct": 2.3,
      "gap_risk": "moderate",
      "correlation_risk": "moderate"
    },
    "event": {
      "macro_event_soon": false,
      "earnings_soon": false,
      "regulatory_risk": "moderate"
    },
    "narrative": "Risque principal : crowding long élevé (L/S 1.8) avec liquidations longs dominantes. Invalidation technique à 65000. Pas d'événement macro imminent. Risque de squeeze long si correction sous support."
  },

  "probabilities": {
    "scores": {
      "probability_long": 0.62,
      "probability_short": 0.38,
      "opportunity_score": 0.55,
      "setup_score": 62,
      "true_value_score": null,
      "deskpro_probability": null
    },
    "consensus": {
      "direction": "bullish",
      "conviction": "moderate",
      "engine_agreement_pct": 0.66
    },
    "disagreement": {
      "has_disagreement": true,
      "details": [
        {
          "engines": ["probability_engine", "derivatives_analyzer"],
          "conflict": "Probabilité LONG 0.62 vs crowding_long élevé",
          "resolution_note": "Crowding long tempère la conviction haussière. Probabilité réduite à 0.55 en adjusted."
        }
      ]
    },
    "narrative": "Probabilité LONG à 62% tirée par contexte macro favorable et structure D1 haussière. Désaccord détecté : le crowding long et le funding positif tempèrent la conviction. Consensus modéré (66% d'accord entre engines)."
  },

  "action": {
    "bias": {
      "direction": "bullish",
      "confidence": "moderate",
      "conviction_score": 0.55
    },
    "readiness": "wait_for_trigger",
    "key_levels_to_watch": [
      { "level": 66450, "type": "entry", "label": "VWAP reclaim H1 confirmé" },
      { "level": 65000, "type": "invalidation", "label": "Support majeur — invalidation si cassé" },
      { "level": 68000, "type": "target", "label": "TP1 — résistance locale" }
    ],
    "narrative": "Biais haussier modéré. Ne pas entrer maintenant : attendre reclaim VWAP H1 confirmé au-dessus de 66450. Invalidation si perte du support 65000. Aucun ordre automatique.",
    "voice_one_liner": "BTC biais haussier modéré, attente confirmation. VWAP à 66450, support à 65000. Contexte macro favorable mais crowding long élevé."
  },

  "sources": {
    "used": [
      "market_metrics.v1",
      "multitf_analysis_input.v1",
      "multitf_setup_score.v1",
      "vision_analysis.v1",
      "vision_context.news_sentiment.v1",
      "telegram_signals.v1",
      "signal_event.v1"
    ],
    "missing": ["vision_context.coinglass.v1", "spacex_true_value.v1"],
    "stale": [],
    "confidence": 0.82
  },

  "freshness": {
    "overall": "fresh",
    "max_age_minutes": 8.5,
    "components": [
      { "source": "market_metrics.v1", "age_minutes": 3.2, "state": "fresh" },
      { "source": "multitf_analysis_input.v1", "age_minutes": 8.5, "state": "fresh" },
      { "source": "multitf_setup_score.v1", "age_minutes": 8.5, "state": "fresh" },
      { "source": "vision_analysis.v1", "age_minutes": 5.1, "state": "fresh" },
      { "source": "telegram_signals.v1", "age_minutes": 2.0, "state": "fresh" }
    ]
  },

  "meta": {
    "engine_version": "1.0.0",
    "runtime_ms": 235,
    "cache_hit": false
  }
}
```

---

## 4. Architecture détaillée

### 4.1 Positionnement dans le pipeline

```
┌──────────────────────────────────────────────────────────────────────┐
│                         DATA COLLECTORS                               │
│  collector_binance_spot  collector_coingecko  collector_telegram      │
│  derivatives_collector   bot_vision (headless)                        │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      DATA CENTER VIEWS                                │
│  market_metrics.v1  multitf_analysis_input.v1  vision_analysis.v1    │
│  multitf_setup_score.v1  signal_event.v1  spacex_true_value.v1       │
│  telegram_signals.v1  vision_context.*.v1                            │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    SCORING / PRIORITY (EXISTANT)                       │
│  market_scanner → probability_engine → liquidation_analyzer           │
│  → opportunity_ranker → decision_engine → risk_engine                 │
│  → priority_engine                                                    │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│               ★ MARKET THESIS ENGINE (NOUVEAU) ★                      │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                     aggregator.py                              │    │
│  │  Lecture de TOUTES les vues DC par symbole                     │    │
│  │  Normalisation → MarketThesisInput                             │    │
│  └──────────────────────────┬───────────────────────────────────┘    │
│                             │                                         │
│                             ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                  context_builder.py                            │    │
│  │  Contexte macro · Phase de marché · Régime volatilité          │    │
│  └──────────────────────────┬───────────────────────────────────┘    │
│                             │                                         │
│                             ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                + thesis_engine.py (orchestrateur)              │    │
│  │  Appelle les 7 builders de section                             │    │
│  │  ┌─ technique_builder    ──► TechniqueSection                 │    │
│  │  ├─ flows_builder        ──► FlowsSection                     │    │
│  │  ├─ news_builder         ──► NewsSection                      │    │
│  │  ├─ risks_builder        ──► RisksSection                     │    │
│  │  ├─ probabilities_builder──► ProbabilitiesSection             │    │
│  │  ├─ action_builder       ──► ActionSection                    │    │
│  │  └─ narrative_builder    ──► textes FR pour chaque section     │    │
│  └──────────────────────────┬───────────────────────────────────┘    │
│                             │                                         │
│                             ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                confidence_engine.py                            │    │
│  │  Méta-confiance · Consensus · Désaccord · Freshness            │    │
│  └──────────────────────────┬───────────────────────────────────┘    │
│                             │                                         │
│                             ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                    OUTPUT                                      │    │
│  │  MarketThesis (Pydantic) → sérialisé en market_thesis.v1       │    │
│  │  Archiver → data/market_thesis/history/{SYM}/{thesis_id}.json  │    │
│  │  Latest → data/market_thesis/by_symbol/{SYM}/latest.json       │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     CONSOMMATEURS                                     │
│                                                                       │
│  DeskPro ──► Card market_thesis dans le dashboard                    │
│  Voice Operator ──► /read/thesis?symbol=BTC (nouvel endpoint)        │
│  LocalCMS ──► Panneau "Market Thesis" dans le cockpit                │
│  API JSON ──► /api/thesis?symbol=BTC (endpoint public)               │
│  Mobile/PWA ──► Vue simplifiée mobile-friendly                       │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.2 Flux de données interne

```
                    aggregator.py
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    DC Views Reader  Canonical    Source Tracker
    (par symbole)    Resolver     (used/missing/stale)
          │              │              │
          └──────────────┴──────────────┘
                         │
                    MarketThesisInput (modèle unifié)
                         │
          ┌──────────────┼──────────────────────────────┐
          │              │                              │
    context_builder  technique_builder               ...
          │              │                              │
    ContexteSection  TechniqueSection    (×7 builders)
          │              │
          └──────────────┴──────────────┐
                                        │
                              thesis_engine.build()
                                        │
                              confidence_engine.evaluate()
                                        │
                              MarketThesis (Pydantic v2)
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
              JSONL archive        latest.json          API cache
         (history/{SYM}/)     (by_symbol/{SYM}/)    (TTL 300s Redis/in-memory)
```

### 4.3 Mécanisme de cache

- **Cache TTL:** 300 secondes (5 min) par défaut, configurable par symbole
- **Stockage:** In-memory dict `{symbol: (MarketThesis, cached_at)}` dans le process FastAPI
- **Invalidation:** Sur appel à l'API, si `now - cached_at > ttl` → regénération
- **Archive:** Chaque thèse est archivée dans `data/market_thesis/history/{SYM}/{thesis_id}.json` pour l'Historical Outcome Engine (Phase F)

### 4.4 Contrat avec les systèmes existants

**Le Market Thesis Engine ne modifie AUCUN contrat existant. Il lit uniquement.**

| Système existant | Action du Thesis Engine |
|-----------------|------------------------|
| `webhook_server.py` | **Aucune** — pas d'impact |
| `perf/perf_app.py` | **Aucune** — pas d'impact |
| `modules/risk_engine/` | **Aucune** — pas d'impact |
| `modules/decision_engine/` | **Aucune** — pas d'impact |
| `modules/proposition_engine/` | **Aucune** — pas d'impact |
| `modules/data_center/` | **Ajout** d'un consommateur dans `registry/consumers.json` |
| `modules/desk_pro/` | **Ajout** d'une card + route API (Phase D) |
| `modules/voice_operator/` | **Ajout** endpoint `/read/thesis` (Phase E) |
| `modules/localcms/` | **Ajout** panneau cockpit (Phase G) |
| `schemas/` | **Ajout** `schemas/market_thesis_v1.json` |

---

## 5. Arborescence fichiers

```
modules/market_thesis/
├── __init__.py                    # Module init, version
├── README.md                      # Doc module
│
├── models.py                      # Modèles Pydantic v2
│                                  # MarketThesisInput, MarketThesis,
│                                  # ContextSection, TechniqueSection,
│                                  # FlowsSection, NewsSection,
│                                  # RisksSection, ProbabilitiesSection,
│                                  # ActionSection, SourcesSection,
│                                  # FreshnessSection, ThesisArchive
│
├── aggregator.py                  # Lecture DC views → MarketThesisInput
│   ├── DataCenterReader           # Classe de lecture des vues DC
│   ├── SourceTracker              # Tracking sources used/missing/stale
│   └── aggregate(symbol) → MarketThesisInput
│
├── context_builder.py             # Contexte macro → ContextSection
│   ├── build_macro_regime()       # DXY, VIX, SPY, US10Y, BTC.D, FearGreed
│   ├── build_market_phase()       # Phase, trend strength, vol regime
│   └── build_context() → ContextSection
│
├── builders/
│   ├── __init__.py
│   ├── technique_builder.py       # → TechniqueSection
│   │   ├── build_htf_bias()       # HTF direction + confidence
│   │   ├── build_ltf_bias()       # LTF direction + confidence
│   │   ├── build_key_levels()     # S/R from vision + multitf
│   │   └── build_active_setups()  # Active setups from multitf_setup_score
│   │
│   ├── flows_builder.py           # → FlowsSection
│   │   ├── build_derivatives()    # OI, funding, L/S, liq, squeeze/crowding
│   │   ├── build_positioning()    # ETF, futures, smart money, telegram
│   │   └── build_flows() → FlowsSection
│   │
│   ├── news_builder.py            # → NewsSection
│   │   ├── build_sentiment()      # News sentiment aggregation
│   │   ├── build_key_drivers()    # Key drivers from multiple sources
│   │   └── build_recent_signals() # Recent signals from all sources
│   │
│   ├── risks_builder.py           # → RisksSection
│   │   ├── build_concentration()  # Crowding, L/S, funding risk
│   │   ├── build_technical_risk() # Invalidation, MAE, gap risk
│   │   └── build_event_risk()     # Macro events, earnings, regulatory
│   │
│   ├── probabilities_builder.py   # → ProbabilitiesSection
│   │   ├── collect_all_scores()   # Gather scores from all engines
│   │   ├── compute_consensus()    # Direction + conviction + agreement
│   │   └── detect_disagreement()  # Conflict detection between engines
│   │
│   └── action_builder.py          # → ActionSection
│       ├── determine_bias()       # Bias direction + confidence
│       ├── assess_readiness()     # Ready / monitor_only / wait / stand_aside
│       └── build_key_levels()     # Levels to watch (entry, inval, targets, alerts)
│
├── thesis_engine.py               # Orchestrateur principal
│   ├── ThesisEngine.build(symbol) → MarketThesis
│   ├── ThesisEngine.build_all() → List[MarketThesis]
│   └── ThesisEngine.invalidate_cache(symbol)
│
├── confidence_engine.py           # Méta-confiance
│   ├── evaluate_sources()        # Source quality → confidence score
│   ├── evaluate_consensus()      # Engine agreement → consensus
│   ├── detect_disagreement()     # Cross-engine conflict detection
│   └── evaluate() → confidence_meta
│
├── narrative.py                   # Générateur de textes FR
│   ├── context_narrative()        # → texte macro
│   ├── technique_narrative()      # → texte structure
│   ├── flows_narrative()          # → texte flux
│   ├── news_narrative()           # → texte news
│   ├── risks_narrative()          # → texte risques
│   ├── probabilities_narrative()  # → texte probas
│   ├── action_narrative()         # → texte action
│   └── voice_one_liner()          # → résumé TTS 1 ligne
│
├── risk_engine.py                 # Synthèse risque (pas sizing)
│   ├── concentration_risk()      # Crowding, L/S imbalance
│   ├── technical_risk()          # Invalidation proximity, gap risk
│   ├── event_risk()              # Macro/earnings/regulatory
│   └── synthesize() → RisksSection
│
├── api.py                         # FastAPI router
│   ├── GET /read/thesis           # Query: symbol, TTL param
│   ├── GET /read/thesis/all       # All symbols
│   ├── GET /read/thesis/summary   # Brief summary all symbols
│   └── GET /health
│
├── archive.py                     # Persistance / historique
│   ├── save(thesis)               # → data/market_thesis/history/{SYM}/{id}.json
│   ├── save_latest(thesis)        # → data/market_thesis/by_symbol/{SYM}/latest.json
│   └── load_history(symbol, limit) → List[MarketThesis]
│
└── scripts/
    ├── cmd.sh                     # CLI entry point
    ├── menu.sh                    # Interactive menu
    ├── sanity_check.sh            # Installation validation
    └── install_shortcuts.sh       # Wrappers in /usr/local/bin

schemas/
├── market_thesis_v1.json          # JSON Schema (canonique)
│
data/market_thesis/                # Créé à l'init
├── by_symbol/
│   ├── BTC/latest.json
│   ├── ETH/latest.json
│   ├── SOL/latest.json
│   ├── XRP/latest.json
│   ├── XAU/latest.json
│   ├── SPCX/latest.json
│   ├── NVDA/latest.json
│   ├── AVGO/latest.json
│   └── MU/latest.json
└── history/
    ├── BTC/
    ├── ETH/
    ├── ...
    └── MU/
```

---

## 6. Schémas de données Pydantic

### 6.1 Résumé des modèles

Tous les modèles utilisent Pydantic v2 (compatible avec `shared/pydantic_compat.py`).

**Modèle principal : `MarketThesis`**

| Champ | Type | Description |
|-------|------|-------------|
| `schema` | `Literal["market_thesis.v1"]` | Discriminant |
| `thesis_id` | `str` | ULID format: `thesis_{SYM}_{ts}` |
| `symbol` | `str` | Canonical symbol |
| `asset_class` | `AssetClass` | Enum |
| `generated_at` | `datetime` | UTC |
| `ttl_seconds` | `int` (default 300) | Cache TTL |
| `context` | `ContextSection` | |
| `technique` | `TechniqueSection` | |
| `flows` | `FlowsSection` | |
| `news` | `NewsSection` | |
| `risks` | `RisksSection` | |
| `probabilities` | `ProbabilitiesSection` | |
| `action` | `ActionSection` | |
| `sources` | `SourcesSection` | |
| `freshness` | `FreshnessSection` | |
| `meta` | `ThesisMeta` | Version, runtime_ms, cache_hit |

**Modèle d'entrée : `MarketThesisInput`** — agrégation normalisée de toutes les sources DC avant construction.

| Champ | Type | Source |
|-------|------|--------|
| `symbol` | `str` | Canonical |
| `price` | `float \| None` | market_metrics.price |
| `market_metrics` | `MarketMetricsData \| None` | market_metrics.v1 |
| `multitf_analysis` | `MultiTFAnalysisData \| None` | multitf_analysis_input.v1 |
| `multitf_scores` | `MultiTFSetupScoreData \| None` | multitf_setup_score.v1 |
| `vision_analysis` | `VisionAnalysisData \| None` | vision_analysis.v1 |
| `signal_event` | `SignalEventData \| None` | signal_event.v1 |
| `spacex_true_value` | `SpacexTrueValueData \| None` | spacex_true_value.v1 |
| `telegram_signals` | `TelegramSignalsData \| None` | telegram_signals.v1 |
| `news_sentiment` | `NewsSentimentData \| None` | vision_context.news_sentiment.v1 |
| `coinglass` | `CoinglassContextData \| None` | vision_context.coinglass.v1 |
| `macro` | `MacroContextData \| None` | DXY, SPY, VIX, US10Y |
| `source_status` | `Dict[str, SourceStatus]` | Tracking per source |

**Nested models** (tous Pydantic `BaseModel`) :
- `ContextSection`, `MacroRegime`, `MarketPhase`
- `TechniqueSection`, `HTFBias`, `LTFBias`, `KeyLevel`, `ActiveSetup`
- `FlowsSection`, `DerivativesState`, `PositioningState`
- `NewsSection`, `SentimentState`, `KeyDriver`, `RecentSignal`
- `RisksSection`, `ConcentrationRisk`, `TechnicalRisk`, `EventRisk`
- `ProbabilitiesSection`, `ScoreSet`, `Consensus`, `Disagreement`
- `ActionSection`, `ActionBias`, `WatchLevel`
- `SourcesSection`, `FreshnessSection`, `FreshnessComponent`, `ThesisMeta`

### 6.2 Enums

```python
class AssetClass(str, Enum):
    CRYPTO_PERP = "crypto_perp"
    FOREX_CFD = "forex_cfd"
    STOCK = "stock"
    IPO = "ipo"
    COMMODITY = "commodity"
    INDEX = "index"

class Direction(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"

class Readiness(str, Enum):
    READY = "ready"                     # Trade-ready: all conditions aligned
    MONITOR_ONLY = "monitor_only"       # Valid setup, monitoring
    WAIT_FOR_TRIGGER = "wait_for_trigger"  # Thesis valid, waiting entry trigger
    STAND_ASIDE = "stand_aside"         # No valid thesis

class Conviction(str, Enum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    NONE = "none"

class RiskLevel(str, Enum):
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    UNKNOWN = "unknown"

class FreshnessState(str, Enum):
    FRESH = "fresh"
    STALE = "stale"
    PARTIAL = "partial"
    EXPIRED = "expired"
```

---

## 7. Plan d'implémentation détaillé

### Phase A — Context Aggregation (SPRINT 1)

**Objectif :** Lire toutes les vues Data Center par symbole et produire un `MarketThesisInput` normalisé.

**Tâches :**
- A1 : Créer le module `modules/market_thesis/` avec structure de base (__init__, README, scripts/)
- A2 : Implémenter `models.py` avec tous les modèles Pydantic (K03)
- A3 : Implémenter `aggregator.py` — `DataCenterReader` qui lit les vues DC
- A4 : Implémenter `SourceTracker` — tracking used/missing/stale
- A5 : Normaliser les symboles (BTCUSDT→BTC, OANDA:XAUUSD→XAU, etc.)
- A6 : Écrire les tests unitaires de l'aggregator (mock DC views)
- A7 : Script `sanity_check.sh`

**Livrables Phase A :** `MarketThesisInput` complet pour BTC, ETH, SOL avec tests verts.

### Phase B — Market Thesis Engine (SPRINT 2)

**Objectif :** Construire le `MarketThesis` complet à partir du `MarketThesisInput`.

**Tâches :**
- B1 : `context_builder.py` — macro regime + market phase
- B2 : `builders/technique_builder.py` — HTF/LTF bias, levels, setups
- B3 : `builders/flows_builder.py` — derivatives + positioning
- B4 : `builders/news_builder.py` — sentiment, drivers, signals
- B5 : `builders/risks_builder.py` — concentration, technical, event
- B6 : `builders/probabilities_builder.py` — scores, consensus, disagreement
- B7 : `builders/action_builder.py` — bias, readiness, levels to watch
- B8 : `thesis_engine.py` — orchestrateur: `ThesisEngine.build(symbol)`
- B9 : `narrative.py` — tous les générateurs de texte FR
- B10 : `archive.py` — persistance history + latest

**Livrables Phase B :** `MarketThesis` complet généré pour les 5 symboles canoniques (BTC, ETH, SOL, XAU, SPCX).

### Phase C — Confidence Engine (SPRINT 3)

**Objectif :** Ajouter la couche de méta-confiance (consensus, désaccord, probabilité calibrée).

**Tâches :**
- C1 : `confidence_engine.py` — evaluate_sources(), evaluate_consensus()
- C2 : Détection de désaccord inter-engine (disagreement detector)
- C3 : Calibration des probabilités (ajustement selon crowding/risques)
- C4 : Intégration dans `thesis_engine.py` — appel confidence après build
- C5 : Tests du disagreement detector avec scénarios contradictoires

**Livrables Phase C :** Probabilités calibrées, désaccords détectés, confiance méta-évaluée.

### Phase D — DeskPro Exposure (SPRINT 4)

**Objectif :** Exposer la thèse dans DeskPro (card, detail view, mobile).

**Tâches :**
- D1 : `api.py` — FastAPI router avec endpoints:
  - `GET /read/thesis?symbol=BTC` — thèse complète
  - `GET /read/thesis/all` — toutes les thèses (9 symboles)
  - `GET /read/thesis/summary` — résumé 1-ligne par symbole
- D2 : Monter le router dans `perf/perf_app.py` (route `/thesis/*`)
- D3 : Card DeskPro "Market Thesis" dans `modules/desk_pro/`:
  - Template HTML avec dark theme
  - Affichage: biais + conviction + one-liner + niveaux clés
- D4 : Detail View: thèse complète par section avec toggle expand/collapse
- D5 : Mobile View: version responsive simplifiée
- D6 : Tests d'intégration DeskPro + Thesis

**Livrables Phase D :** Thèse visible dans DeskPro en mode dark theme, responsive.

### Phase E — Voice Operator Integration (SPRINT 5)

**Objectif :** Exposer la thèse via les endpoints Voice Operator existants + nouveaux.

**Tâches :**
- E1 : Nouvel endpoint `GET /read/thesis?symbol=BTC` dans `voice_operator/api/routes.py`
- E2 : Nouvel intent router: `analyse_btc`, `analyse_eth`, `analyse_sol`, `analyse_xrp`, `analyse_gold`, `analyse_spcx`, `analyse_nvda`, `analyse_avgo`, `analyse_mu`
- E3 : `voice_operator/readers/thesis_reader.py` — lit l'API thesis ou le latest.json
- E4 : Schémas Voice pour `ThesisVoice` (voice-friendly format)
- E5 : Tests TTS: chaque one-liner doit être < 200 caractères, prononçable
- E6 : Intégration avec `voice_operator/engine/intent_router.py` (déjà 30+ intents)

**Livrables Phase E :** "Voice analyse BTC" → TTS du one-liner + sections clés.

### Phase F — Historical Validation (SPRINT 6)

**Objectif :** Archiver, mesurer et recalibrer les thèses.

**Tâches :**
- F1 : `modules/market_thesis/historical.py`:
  - `track_outcome(thesis_id, symbol, actual_outcome)` — enregistre le résultat
  - `measure_accuracy(symbol, days=30)` — winrate, calibration
  - `calibrate()` — ajuste les poids de confiance selon l'historique
- F2 : `AccuracyReport` modèle — métriques par symbole, par section, par source
- F3 : Endpoint `GET /read/thesis/accuracy?symbol=BTC&days=30`
- F4 : Endpoint `GET /read/thesis/calibration` — état de calibration actuel
- F5 : Tests avec données historiques mockées

**Livrables Phase F :** Tracking outcomes, rapport d'accuracy, calibration engine.

### Phase G — Executive Intelligence Layer (SPRINT 7)

**Objectif :** Vue exécutive: top opportunités, top risques, top movers, watchlist.

**Tâches :**
- G1 : `executive.py` — `ExecutiveBriefing`:
  - `top_opportunities(limit=3)` — meilleurs setups par conviction
  - `top_risks(limit=3)` — plus hauts risques concentration
  - `top_movers(limit=5)` — plus grands changements de thèse (delta)
  - `priority_watchlist()` — symboles à surveiller en priorité
- G2 : Endpoint `GET /read/thesis/executive`
- G3 : Panneau LocalCMS "Executive Briefing"
- G4 : Intégration Voice Operator: intent "executive_briefing"
- G5 : Tests

**Livrables Phase G :** Vue exécutive complète dans LocalCMS + Voice.

---

## 8. Découpage en PRs indépendantes

Chaque PR est auto-portante, mergeable indépendamment, sans casser les systèmes existants.

| PR # | Titre | Phase | Fichiers | Dépend de | Complexité |
|------|-------|-------|----------|-----------|------------|
| **PR1** | `market_thesis: module skeleton + models + JSON schema` | A | `modules/market_thesis/__init__.py`, `models.py`, `README.md`, `scripts/*`, `schemas/market_thesis_v1.json` | Rien | ⭐ |
| **PR2** | `market_thesis: aggregator + DC reader + source tracker` | A | `aggregator.py`, tests | PR1 | ⭐⭐ |
| **PR3** | `market_thesis: context + technique + flows builders` | B | `context_builder.py`, `builders/technique_builder.py`, `builders/flows_builder.py`, `narrative.py` (partiel), tests | PR2 | ⭐⭐⭐ |
| **PR4** | `market_thesis: news + risks + probabilities builders` | B | `builders/news_builder.py`, `builders/risks_builder.py`, `builders/probabilities_builder.py`, `narrative.py` (partiel), tests | PR3 | ⭐⭐⭐ |
| **PR5** | `market_thesis: action builder + thesis_engine + archive` | B | `builders/action_builder.py`, `thesis_engine.py`, `archive.py`, `narrative.py` (complet), tests | PR4 | ⭐⭐⭐ |
| **PR6** | `market_thesis: confidence engine + disagreement detector` | C | `confidence_engine.py`, intégration dans `thesis_engine.py`, tests | PR5 | ⭐⭐ |
| **PR7** | `market_thesis: API endpoints + FastAPI router` | D1-D2 | `api.py`, mount dans `perf_app.py`, tests | PR6 | ⭐⭐ |
| **PR8** | `desk_pro: market thesis card + detail view + mobile` | D | `modules/desk_pro/` (templates, routes), tests | PR7 | ⭐⭐⭐ |
| **PR9** | `voice_operator: /read/thesis endpoint + thesis reader` | E | `voice_operator/api/routes.py`, `voice_operator/readers/thesis_reader.py`, `voice_operator/api/schemas.py`, tests | PR7 | ⭐⭐ |
| **PR10** | `voice_operator: intent routing for 9 assets` | E | `voice_operator/engine/intent_router.py`, tests | PR9 | ⭐⭐ |
| **PR11** | `market_thesis: historical tracking + accuracy report` | F | `historical.py`, `AccuracyReport`, endpoints, tests | PR7 | ⭐⭐⭐ |
| **PR12** | `market_thesis: executive briefing + top N views` | G | `executive.py`, endpoints, tests | PR7 | ⭐⭐ |
| **PR13** | `localcms: market thesis panel + executive briefing` | G | `modules/localcms/` (templates, routes), tests | PR12 | ⭐⭐ |

**Total: 13 PRs, ~21 étoiles de complexité**

### Ordre de merge recommandé

```
PR1 → PR2 → PR3 → PR4 → PR5 → PR6
                                ├── PR7 ──┬── PR8  (DeskPro)
                                │         ├── PR9 → PR10 (Voice)
                                │         ├── PR11 (Historical)
                                │         └── PR12 → PR13 (Executive + LocalCMS)
                                │
                                (PR6 bloque PR7, le reste est parallélisable)
```

Les PRs 8, 9, 11, 12 peuvent être développées en parallèle après PR7.

---

## 9. Kanban détaillé

### Colonnes : BACKLOG → SPRINT → IN PROGRESS → REVIEW → DONE

### SPRINT 1 — Context Aggregation (Semaine 1)

| ID | Tâche | Priorité | Estimation | Dépend de |
|----|-------|----------|------------|-----------|
| K01 | Création module market_thesis (__init__, README, scripts/) | P0 | 1h | - |
| K02 | Contrat JSON Schema market_thesis.v1 | P0 | 2h | - |
| K03 | Modèles Pydantic v2 (models.py complet) | P0 | 3h | K02 |
| K04 | Documentation architecture (ce document finalisé) | P0 | 2h | - |
| K05 | Context Aggregator: DataCenterReader | P0 | 3h | K03 |
| K06 | Normalisation des symboles (canonical mapping) | P1 | 2h | K05 |
| K07 | SourceTracker: used/missing/stale par source | P1 | 2h | K05 |
| K08 | Tests aggregator (mock DC views, 3 symboles) | P0 | 3h | K06, K07 |
| **Gate A** | **Revue: MarketThesisInput complet pour BTC, ETH, SOL** | | | |

### SPRINT 2 — Market Thesis Engine (Semaine 2)

| ID | Tâche | Priorité | Estimation | Dépend de |
|----|-------|----------|------------|-----------|
| K09 | context_builder.py: macro regime + market phase | P0 | 3h | Gate A |
| K10 | technique_builder.py: HTF/LTF, levels, setups | P0 | 4h | Gate A |
| K11 | flows_builder.py: derivatives + positioning | P0 | 3h | Gate A |
| K12 | news_builder.py: sentiment, drivers, signals | P1 | 3h | Gate A |
| K13 | risks_builder.py: concentration, technical, event | P0 | 3h | Gate A |
| K14 | probabilities_builder.py: scores, consensus, disagreement | P0 | 3h | Gate A |
| K15 | action_builder.py: bias, readiness, watch levels | P0 | 3h | Gate A |
| K16 | narrative.py: tous les générateurs FR (7 fonctions) | P1 | 4h | K09-K15 |
| K17 | thesis_engine.py: orchestrateur principal | P0 | 3h | K09-K16 |
| K18 | archive.py: persistance history + latest | P1 | 2h | K17 |
| K19 | Tests thesis_engine (5 symboles, thèses complètes) | P0 | 4h | K17, K18 |
| **Gate B** | **Revue: MarketThesis complet généré pour BTC,ETH,SOL,XAU,SPCX** | | | |

### SPRINT 3 — Confidence Engine (Semaine 3)

| ID | Tâche | Priorité | Estimation | Dépend de |
|----|-------|----------|------------|-----------|
| K20 | confidence_engine.py: evaluate_sources() | P0 | 2h | Gate B |
| K21 | confidence_engine.py: evaluate_consensus() | P0 | 2h | Gate B |
| K22 | Disagreement Detector: cross-engine conflict | P0 | 3h | Gate B |
| K23 | Probability Calibration (crowding/risk adjustment) | P1 | 3h | K22 |
| K24 | Intégration confidence dans thesis_engine | P0 | 2h | K20-K23 |
| K25 | Tests confidence + disagreement (scénarios contradictoires) | P0 | 3h | K24 |
| **Gate C** | **Revue: Confiance calibrée, désaccords détectés** | | | |

### SPRINT 4 — API + DeskPro (Semaine 4)

| ID | Tâche | Priorité | Estimation | Dépend de |
|----|-------|----------|------------|-----------|
| K26 | api.py: GET /read/thesis, /all, /summary, /health | P0 | 3h | Gate C |
| K27 | Montage router dans perf_app.py (/thesis/*) | P0 | 1h | K26 |
| K28 | Cache TTL (in-memory, 300s) | P1 | 2h | K26 |
| K29 | DeskPro Card: template HTML dark theme | P0 | 4h | K27 |
| K30 | DeskPro Detail View: thèse par section | P1 | 3h | K29 |
| K31 | DeskPro Mobile View: responsive | P2 | 2h | K29 |
| K32 | Tests API + DeskPro integration | P0 | 3h | K29-K31 |
| **Gate D** | **Revue: Thèse visible dans DeskPro, API fonctionnelle** | | | |

### SPRINT 5 — Voice Operator (Semaine 5)

| ID | Tâche | Priorité | Estimation | Dépend de |
|----|-------|----------|------------|-----------|
| K33 | voice_operator: GET /read/thesis endpoint | P0 | 2h | Gate D |
| K34 | voice_operator: thesis_reader.py | P0 | 2h | K33 |
| K35 | voice_operator: ThesisVoice schemas | P1 | 1h | K33 |
| K36 | Intent router: 9 nouveaux intents (analyse_*) | P0 | 2h | K34 |
| K37 | Tests TTS: one-liner < 200 chars, prononçable | P1 | 2h | K35 |
| K38 | Tests Voice integration (mock TTS) | P0 | 2h | K36 |
| **Gate E** | **Revue: Voice Operator expose la thèse pour les 9 actifs** | | | |

### SPRINT 6 — Historical Validation (Semaine 6)

| ID | Tâche | Priorité | Estimation | Dépend de |
|----|-------|----------|------------|-----------|
| K39 | historical.py: track_outcome() | P0 | 2h | Gate D |
| K40 | historical.py: measure_accuracy() | P0 | 3h | K39 |
| K41 | historical.py: calibrate() | P1 | 3h | K40 |
| K42 | AccuracyReport modèle + endpoint | P0 | 2h | K40 |
| K43 | Endpoint calibration status | P1 | 1h | K41 |
| K44 | Tests historical (données mockées 30 jours) | P0 | 3h | K42 |
| **Gate F** | **Revue: Outcome tracking + accuracy + calibration opérationnels** | | | |

### SPRINT 7 — Executive Intelligence Layer (Semaine 7)

| ID | Tâche | Priorité | Estimation | Dépend de |
|----|-------|----------|------------|-----------|
| K45 | executive.py: top_opportunities() | P0 | 2h | Gate D |
| K46 | executive.py: top_risks(), top_movers() | P0 | 2h | Gate D |
| K47 | executive.py: priority_watchlist() | P1 | 1h | Gate D |
| K48 | ExecutiveBriefing modèle + endpoint | P0 | 2h | K45-K47 |
| K49 | LocalCMS: panneau "Market Thesis" | P1 | 3h | K48 |
| K50 | LocalCMS: panneau "Executive Briefing" | P2 | 2h | K48 |
| K51 | Voice: intent "executive_briefing" | P1 | 1h | K48 |
| K52 | Tests executive + LocalCMS + Voice | P0 | 3h | K49-K51 |
| **Gate G** | **Revue: Vue exécutive complète, LocalCMS + Voice** | | | |

---

## 10. Matrice risques / dépendances

### 10.1 Risques techniques

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|------------|
| **Données DC manquantes pour certains symboles** (XRP, NVDA, AVGO, MU n'ont pas de multitf_analysis) | **Élevée** | Moyen | Le contrat gère les sections partielles. Narrative indique "données insuffisantes". Fallback: thèse basée uniquement sur les sources disponibles. |
| **Changement de format des vues DC** (les vues DC sont produites par d'autres modules) | **Moyenne** | Élevé | L'aggregator utilise des chemins d'accès explicites. Si une vue change, le `SourceTracker` la marque `stale` ou `missing`. Tests d'intégration avec fixtures DC. |
| **Cache invalidation incorrecte** (thèse périmée servie) | **Faible** | Élevé | TTL court (300s). FreshnessSection exposée. Bouton "refresh" dans DeskPro. |
| **Performance: build() trop lent pour 9 symboles** (> 2 secondes) | **Moyenne** | Moyen | Cache par symbole. Build asynchrone possible (chacun est indépendant). Timeout à 5s. |
| **Dépendance circulaire avec proposition_engine** | **Nulle** | — | Le thesis engine est strictement read-only. Il ne modifie aucun autre module. |
| **Conflit de nommage de symboles** (BTCUSDT vs BTC, OANDA:XAUUSD vs XAU) | **Moyenne** | Faible | `normalize_symbol()` dans aggregator avec table de mapping explicite. Tests exhaustifs. |

### 10.2 Risques opérationnels

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|------------|
| **Surcharge cognitive DeskPro** (trop d'info) | **Élevée** | Faible | Card compacte (one-liner + biais). Detail view en expand/collapse. |
| **Voice Operator TTS trop long** | **Moyenne** | Faible | `voice_one_liner` limité à 200 caractères. Tests TTS systématiques. |
| **Archive disque (history/) croît indéfiniment** | **Élevée** | Faible | Rotation: garder 90 jours max. Nettoyage automatique dans `archive.py`. |
| **Désaccord entre engines non résolu** | **Moyenne** | Moyen | Le disagreement detector expose le conflit mais ne force pas de résolution. L'utilisateur décide. |

### 10.3 Matrice de dépendances inter-modules

```
market_thesis
├── LIT (read-only)
│   ├── data/data_center/views/* (toutes les vues DC)
│   ├── data/deskpro/inputs/vision_context/*
│   └── schemas/ (aucune dépendance)
│
├── EST LU PAR (consumers)
│   ├── modules/desk_pro/       (Phase D — ajout card)
│   ├── modules/voice_operator/  (Phase E — ajout endpoint)
│   ├── modules/localcms/        (Phase G — ajout panneau)
│   └── perf/perf_app.py         (montage router)
│
└── NE MODIFIE PAS
    ├── Aucun contrat existant
    ├── Aucun module existant
    ├── Aucun pipeline de trading
    └── Aucun ordre automatique
```

---

## 11. Plan de tests

### 11.1 Tests unitaires (par PR)

| PR | Fichier de test | Tests |
|----|----------------|-------|
| PR1 | `tests/test_market_thesis_models.py` | Validation Pydantic: MarketThesis complet, tous les nested models, sérialisation/désérialisation JSON, invariants (ex: conviction_score ∈ [0,1]) |
| PR2 | `tests/test_market_thesis_aggregator.py` | DataCenterReader avec fixtures DC mockées: 3 symboles, sources manquantes, sources stales, normalisation symboles |
| PR3 | `tests/test_market_thesis_context.py`, `tests/test_market_thesis_technique.py`, `tests/test_market_thesis_flows.py` | Chaque builder avec input mocké: vérifie output correct, narratives FR non vides |
| PR4 | `tests/test_market_thesis_news.py`, `tests/test_market_thesis_risks.py`, `tests/test_market_thesis_probabilities.py` | Idem pour news, risks, probabilities |
| PR5 | `tests/test_market_thesis_engine.py` | `ThesisEngine.build()` 5 symboles, archive save/load, narrative cohérence (pas de phrases vides, pas d'anglais), one-liner < 200 chars |
| PR6 | `tests/test_market_thesis_confidence.py` | Consensus avec 0%, 50%, 100% d'accord. Disagreement: engines en conflit. Calibration: probabilité ajustée. |
| PR7 | `tests/test_market_thesis_api.py` | Tous les endpoints: /read/thesis, /all, /summary, /health. Cache TTL. Timeout. |
| PR8 | `tests/test_market_thesis_deskpro.py` | Card HTML rendering, detail view, mobile view. Dark theme CSS. |
| PR9-10 | `tests/test_market_thesis_voice.py` | Voice endpoints, thesis_reader, intent routing. TTS one-liner length. |
| PR11 | `tests/test_market_thesis_historical.py` | Track outcome, accuracy report, calibration. Données mock 30 jours. |
| PR12-13 | `tests/test_market_thesis_executive.py` | Top N, watchlist, LocalCMS panel, Voice intent. |

### 11.2 Tests d'intégration

```python
# tests/e2e/test_market_thesis_pipeline.py
def test_full_pipeline_btc():
    """Pipeline complet: aggregator → builders → thesis → archive → API"""
    ...

def test_all_nine_symbols():
    """Les 9 symboles cibles produisent une thèse valide"""
    for sym in ["BTC","ETH","SOL","XRP","XAU","SPCX","NVDA","AVGO","MU"]:
        thesis = engine.build(sym)
        assert thesis.schema == "market_thesis.v1"
        assert thesis.action.voice_one_liner  # non vide

def test_partial_data_symbol():
    """Symbole avec données partielles (ex: XRP sans multitf) — thèse dégradée mais valide"""
    ...

def test_no_data_symbol():
    """Symbole sans aucune donnée — thèse vide avec readiness=stand_aside"""
    ...
```

### 11.3 Tests de non-régression

- Tous les tests existants (~1933) doivent rester verts
- `./scripts/verify_all.sh` doit passer
- `./scripts/smoke.sh` doit passer (endpoints existants inchangés)
- Aucun fichier hors `modules/market_thesis/`, `schemas/`, `data/market_thesis/`, `tests/` modifié avant Phase D

### 11.4 Critères DONE par PR

1. Tous les tests passent
2. `verify_all.sh` passe
3. Aucun warning de lint/typecheck
4. Le contrat `market_thesis.v1` est valide contre le JSON Schema
5. Les narratives FR sont en français correct (pas de placeholder, pas d'anglais)
6. Pour PR8+ : DeskPro/Voice affiche la thèse sans erreur

---

## 12. Plan de déploiement progressif

### Étape 1 — Shadow Mode (PR1-PR6 mergées)

- Le module existe, peut être appelé manuellement
- `python -m modules.market_thesis.thesis_engine` génère des thèses en local
- Aucun endpoint exposé
- Vérification: les thèses sont archivées dans `data/market_thesis/`

### Étape 2 — API Read-Only (PR7 mergée)

- L'API est exposée sur `/thesis/*` via `perf_app.py:8010`
- Tests smoke: `curl localhost:8010/thesis/read/thesis?symbol=BTC`
- Aucun consommateur UI ne l'utilise encore

### Étape 3 — DeskPro Beta (PR8 mergée)

- Card "Market Thesis" visible dans DeskPro pour les admins uniquement
- Feature flag: `MARKET_THESIS_BETA=true` dans `.env`
- Feedback collecté pendant 1 semaine

### Étape 4 — Voice Operator (PR9-PR10 mergées)

- Endpoint `/read/thesis` exposé dans Voice Operator
- Intents vocaux activés
- Test TTS avec les one-liners

### Étape 5 — Full Release (PR11-PR13 mergées)

- DeskPro: card visible pour tous (feature flag retiré)
- LocalCMS: panneau Executive Briefing
- Historical tracking actif
- Monitoring: Prometheus metrics sur latence API, cache hit rate

### Rollback

Chaque étape est réversible:
- **API:** dé-monter le router de `perf_app.py`
- **DeskPro:** feature flag `MARKET_THESIS_BETA=false`
- **Voice:** commenter les nouveaux intents
- **Module:** supprimer `modules/market_thesis/` — aucun autre module n'en dépend

---

## 13. Plan de validation

### 13.1 Validation du contrat market_thesis.v1

1. **JSON Schema valide:** `schemas/market_thesis_v1.json` passe la validation JSON Schema Draft 2020-12
2. **Rétro-compatibilité:** Aucun champ obligatoire ne référence un contrat existant modifié
3. **Extensibilité:** `additionalProperties: false` au top-level, mais les objets internes permettent l'extension via `meta`
4. **Exemple canonique:** L'exemple BTC fourni en section 3.2 valide contre le schéma

### 13.2 Validation de l'architecture

1. **Additive uniquement:** Chaque fichier créé est nouveau. Aucun fichier existant modifié avant Phase D.
2. **Aucun ordre automatique:** Le champ `action.readiness` est strictement informatif. Aucun appel à `execution_engine`.
3. **Aucun changement des contrats existants:** Les contrats DC, webhook, perf, risk, proposition restent inchangés.
4. **Signaux bruts conservés:** Toutes les sources sont listées dans `sources.used`. Les données brutes restent accessibles via les vues DC.
5. **Confiance exposée:** Chaque section a un champ `confidence`, `sources.confidence` donne la confiance globale, `freshness` donne l'âge des données.

### 13.3 Validation de la couverture (9 actifs)

Pour chaque actif, vérifier que la thèse produite contient au minimum:
- ✅ `context` (même si partiel: "données macro insuffisantes")
- ✅ `technique` (même si partiel: "pas de données techniques disponibles")
- ✅ `action.voice_one_liner` (toujours présent, maximum informatif)
- ✅ `sources.used` (liste les sources qui ont contribué)
- ✅ `sources.missing` (liste les sources attendues mais absentes)

### 13.4 Validation des narratives FR

- Toutes les narratives sont en français
- Pas de phrases vides (fallback: "Analyse non disponible pour cette section.")
- Pas de placeholder (ex: "TODO", "Lorem ipsum")
- `voice_one_liner` ≤ 200 caractères

### 13.5 Checklist de validation finale

```
[ ] Tous les tests passent (unit + integration + e2e)
[ ] verify_all.sh passe
[ ] smoke.sh passe (endpoints existants)
[ ] JSON Schema market_thesis.v1 valide
[ ] 9 thèses générées pour 9 actifs
[ ] DeskPro affiche la card sans erreur
[ ] Voice Operator TTS < 200 chars par one-liner
[ ] LocalCMS panneau fonctionnel
[ ] Cache TTL respecté
[ ] Archive history/ correcte
[ ] Aucun warning de lint
[ ] Aucune dépendance circulaire
[ ] Aucun ordre automatique déclenché
[ ] Aucun contrat existant modifié
```

---

## 14. Estimation de complexité

| Phase | PRs | Complexité | Durée estimée | Risque principal |
|-------|-----|-----------|---------------|-----------------|
| A — Context Aggregation | PR1, PR2 | ⭐⭐⭐ (3) | 3-4 jours | Données DC manquantes |
| B — Thesis Engine | PR3, PR4, PR5 | ⭐⭐⭐⭐⭐⭐⭐⭐ (9) | 6-8 jours | Cohérence des narratives |
| C — Confidence Engine | PR6 | ⭐⭐ (2) | 2-3 jours | Calibration juste |
| D — API + DeskPro | PR7, PR8 | ⭐⭐⭐⭐⭐ (5) | 4-5 jours | Intégration UI |
| E — Voice Operator | PR9, PR10 | ⭐⭐⭐⭐ (4) | 3-4 jours | TTS length |
| F — Historical | PR11 | ⭐⭐⭐ (3) | 2-3 jours | Données mock |
| G — Executive + LocalCMS | PR12, PR13 | ⭐⭐⭐⭐ (4) | 3-4 jours | Surcharge UI |
| **TOTAL** | **13 PRs** | **⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐ (30)** | **23-31 jours** | |

**Équivalent homme-semaines:** ~5-6 semaines pour 1 développeur full-time.
**Avec 2 développeurs (PRs parallélisables après PR7):** ~4 semaines.

### Points de complexité élevée

1. **Narrative builder (PR3-PR5):** Génération de texte FR cohérent à partir de données structurées. Pas de LLM — règles déterministes + templates. Complexité: logique conditionnelle riche.
2. **Disagreement detector (PR6):** Détecter les contradictions entre engines (ex: prob LONG > 0.6 mais crowding_risk = high). Nécessite une matrice de règles.
3. **DeskPro integration (PR8):** Injection de HTML/CSS dans le template existant sans le casser. Tests de régression visuels nécessaires.
4. **Historical calibration (PR11):** Mesurer la justesse des thèses passées nécessite des données mockées réalistes sur 30+ jours.

---

## Annexe A — Table de normalisation des symboles

| Source | Valeur brute | Canonique |
|--------|-------------|-----------|
| market_metrics.v1 | `BTCUSDT` | `BTC` |
| market_metrics.v1 | `ETHUSDT` | `ETH` |
| market_metrics.v1 | `SOLUSDT` | `SOL` |
| market_metrics.v1 | `XRPUSDT` | `XRP` |
| market_metrics.v1 | `PAXGUSDT` | `XAU` |
| vision_analysis | `BTCUSDT.P` | `BTC` |
| vision_analysis | `OANDA:XAUUSD` | `XAU` |
| spacex_true_value.v1 | `SPCX` | `SPCX` |
| spacex_true_value.v1 | `NVDA` | `NVDA` |
| spacex_true_value.v1 | `AVGO` | `AVGO` |
| spacex_true_value.v1 | `MU` | `MU` |
| multitf_analysis | `XAUUSD` | `XAU` |

## Annexe B — Mapping sources → sections de thèse

| Source DC | Section(s) alimentée(s) |
|-----------|------------------------|
| `market_metrics.v1` | flows.derivatives (OI, funding, volume, L/S, liq), context (price, change_24h) |
| `multitf_analysis_input.v1` | technique (timeframes, levels, signals, macro_context), context (macro_context.dxy) |
| `multitf_setup_score.v1` | technique (setups, grades, bias), probabilities (setup_score) |
| `vision_analysis.v1` | technique (S/R levels, analysis_summary → narrative) |
| `vision_context.coinglass.v1` | flows.derivatives (OI, L/S, liq via OCR) |
| `vision_context.news_sentiment.v1` | news (sentiment, article_count) |
| `signal_event.v1` | news.recent_signals (latest webhook) |
| `spacex_true_value.v1` | probabilities (true_value_score, final_grade) |
| `telegram_signals.v1` | news (sentiment), flows.positioning (telegram_sentiment) |
| DXY/SPY/VIX/US10Y (macro) | context.macro_regime |
| Fear & Greed (si disponible) | context.macro_regime.fear_greed_index |

## Annexe C — Règles de décision pour action.readiness

| Condition | Readiness |
|-----------|-----------|
| Consensus bullish + conviction high + setup A/A+ actif + pas de crowding high | `ready` |
| Consensus bullish/bearish + setup B/B+ actif + crowding moderate | `monitor_only` |
| Thesis valid but no CDP/TV trigger confirmed yet | `wait_for_trigger` |
| Aucune thèse valide OU crowding high + disagreement fort OU données insuffisantes | `stand_aside` |

**Rappel: `readiness` est strictement informatif. Aucun ordre automatique n'est émis.**

---

> **Prochaine étape:** Validation de cette architecture par le mainteneur. Une fois validée, implémentation PR1 → PR2 → ...
>
> **Fichier initié:** 2026-06-15
> **Dernière mise à jour:** 2026-06-15
> **Auteur:** opencode assistant (deepseek-v4-pro)
