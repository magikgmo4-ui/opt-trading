# 20_BUNDLE_DESIGN_AND_OUTPUT_CONTRACT.md

## GO: GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PIPELINE_01
## Branch: go/GO_VISION_CAPTURE_QUALITY_ROUTING_01
## Status: DESIGN — contrat JSON stabilisé, avant implémentation parser live

---

## 1. Architecture des bundles

```
                          ┌──────────────────────┐
                          │   Inbound Pipeline    │
                          │ (Telegram + Vision +  │
                          │  Coinglass + Market)  │
                          └──────┬───────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
          ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
          │  Parsers     │ │  Normalizers│ │  Routers    │
          │  (per src)   │ │  (to canon) │ │  (to dest)  │
          └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
                 │               │               │
          ┌──────▼───────────────▼───────────────▼──────┐
          │            BUNDLE PRODUCERS                  │
          │  (agrège inputs hétérogènes → contrat JSON)  │
          └──────────────────────┬──────────────────────┘
                                 │
          ┌──────────────────────▼──────────────────────┐
          │           Analysis Consumer                 │
          │  (lit les bundles, produit les biais)       │
          └─────────────────────────────────────────────┘
```

---

## 2. Bundles définis

### 2.1 BTC Core Bundle

| Champ | Valeur |
|---|---|
| `bundle_id` | `btc.core.v1` |
| `producer` | `modules/analysis_bundles/btc_core_producer.py` |
| `cadence` | 15m (alignée sur market_metrics refresh) |

**Inputs requis :**
- `market_metrics.v1` — BTCUSDT spot: price, volume, RSI, volatility (source: `data/data_center/views/market_metrics/latest.json`)
- `vision_context.coinglass.v1` — BTCUSDT 1H: OI, funding, liquidations, long/short (source: Coinglass OCR → `data/deskpro/inputs/vision_context/coinglass/latest.json`)
- `telegram_signal.v1` — BTC-related signals from screener pipeline (source: Telegram screener)

**Assets couverts :** BTCUSDT (PERP), BTC (spot)

**Output contract :**
```json
{
  "contract": "bundle.btc_core.v1",
  "bundle_id": "btc.core.v1",
  "produced_at": "2026-06-04T01:30:00Z",
  "freshness_state": "FRESH",
  "assets": ["BTC", "BTCUSDT"],
  "inputs": {
    "market_metrics": {
      "source": "data_center/market_metrics.v1",
      "freshness": "FRESH",
      "produced_at": "2026-06-04T01:29:45Z"
    },
    "coinglass_vision": {
      "source": "vision_context.coinglass.v1",
      "freshness": "STALE",
      "produced_at": "2026-06-04T01:15:00Z"
    },
    "telegram_signals": {
      "source": "telegram_signal.v1",
      "count": 3,
      "latest_at": "2026-06-04T01:28:12Z"
    }
  },
  "analysis": {
    "timeframe": "1H",
    "bias_short_term": "BULLISH",
    "bias_intraday": "NEUTRAL",
    "regime": "TRENDING",
    "squeeze_or_stress_level": "MEDIUM",
    "invalidation": "BTC < 86000",
    "confidence": "MEDIUM"
  },
  "missing_inputs": ["coinglass_vision: OI_delta not extracted"],
  "source_refs": [
    "data/data_center/views/market_metrics/latest.json",
    "data/deskpro/inputs/vision_context/coinglass/latest.json",
    "data/telegram_screener/signals/latest.json"
  ]
}
```

---

### 2.2 Macro Bundle

| Champ | Valeur |
|---|---|
| `bundle_id` | `macro.v1` |
| `producer` | `modules/analysis_bundles/macro_producer.py` |
| `cadence` | 1H (les données macro bougent lentement) |

**Inputs requis :**
- DXY (USD index) — spot ou proxy via TV feed
- SPX ou ES (SP500 futures)
- VIX (volatilité implicite)
- OR (XAUUSD — gold spot)
- US10Y (taux 10 ans US)

**Assets couverts :** DXY, SPX, VIX, XAUUSD, US10Y

**Output contract :**
```json
{
  "contract": "bundle.macro.v1",
  "bundle_id": "macro.v1",
  "produced_at": "2026-06-04T01:30:00Z",
  "freshness_state": "FRESH",
  "assets": ["DXY", "SPX", "VIX", "XAUUSD", "US10Y"],
  "inputs": {
    "dxy": {
      "source": "market_metrics.v1",
      "freshness": "FRESH",
      "price": 104.32,
      "produced_at": "2026-06-04T01:29:45Z"
    },
    "vix": {
      "source": "market_metrics.v1",
      "freshness": "STALE",
      "price": null,
      "produced_at": null
    },
    "gold": {
      "source": "market_metrics.v1",
      "freshness": "FRESH",
      "price": 3125.50,
      "produced_at": "2026-06-04T01:29:45Z"
    }
  },
  "analysis": {
    "timeframe": "1D",
    "bias_short_term": "RISK_ON",
    "bias_intraday": "NEUTRAL",
    "regime": "RISK_ON_BROADENING",
    "squeeze_or_stress_level": "LOW",
    "invalidation": "VIX > 30",
    "confidence": "MEDIUM"
  },
  "missing_inputs": ["vix: no data source configured"],
  "source_refs": [
    "data/data_center/views/market_metrics/latest.json"
  ]
}
```

---

### 2.3 Telegram Signal Bundle

| Champ | Valeur |
|---|---|
| `bundle_id` | `telegram_signal.v1` |
| `producer` | `modules/telegram_screener/signal/signal_producer.py` (existant) |
| `cadence` | event-driven (chaque nouveau signal) |

**Inputs requis :**
- Messages parsés depuis les canaux Telegram screenés (via `ScreenerPipeline`)
- 3 types de signaux: TRADE, NEWS, ALPHA (enum `SignalType` existant)

**Assets couverts :** Tous les pairs trouvés dans les signaux

**Output contract (version enrichie du ScreenerProducedSignal existant) :**
```json
{
  "contract": "bundle.telegram_signal.v1",
  "bundle_id": "telegram_signal.v1",
  "produced_at": "2026-06-04T01:28:12Z",
  "freshness_state": "LIVE",
  "assets": ["BTC"],
  "signals": [
    {
      "signal_id": "sig-20260604-012812-a1b2",
      "source_channel": "live_xauusd_gold_freesignal",
      "channel_priority": "P0",
      "signal_type": "TRADE",
      "pair": "BTCUSDT",
      "direction": "LONG",
      "entry_price": 92500.0,
      "sl": 91000.0,
      "tp": 96000.0,
      "confidence": "MEDIUM",
      "category": "BREAKOUT",
      "message_ref": "live_xauusd_gold_freesignal:msg_42",
      "raw_text_preview": "BTC LONG Entry: 92500 SL: 91000 TP: 96000"
    }
  ],
  "analysis": {
    "timeframe": "4H",
    "bias_short_term": "BULLISH",
    "bias_intraday": "BULLISH",
    "regime": "BREAKOUT_SIGNAL",
    "squeeze_or_stress_level": "LOW",
    "invalidation": "BTC < 89000",
    "confidence": "LOW",
    "signal_count": {
      "total": 1,
      "trade": 1,
      "news": 0,
      "alpha": 0
    }
  },
  "missing_inputs": [],
  "source_refs": [
    "data/telegram_screener/signals/sig-20260604-012812-a1b2.json"
  ]
}
```

---

### 2.4 Vision / Screenshot Bundle

| Champ | Valeur |
|---|---|
| `bundle_id` | `vision_screenshot.v1` |
| `producer` | `modules/bot_vision_step2/` + `modules/vision/coinglass/` (existants) |
| `cadence` | 30m–1H (headless capture cycle) |

**Inputs requis :**
- `vision_context.coinglass.v1` — données OCR structurées depuis screenshot Coinglass
- Screenshots bruts (`data/vision/coinglass/raw/`)
- Screenshots normalisées (`data/vision/coinglass/normalized/`)

**Assets couverts :** BTCUSDT, ETHUSDT (selon board capturé)

**Output contract :**
```json
{
  "contract": "bundle.vision_screenshot.v1",
  "bundle_id": "vision_screenshot.v1",
  "produced_at": "2026-06-04T01:30:00Z",
  "freshness_state": "FRESH",
  "assets": ["BTC"],
  "inputs": {
    "coinglass_ocr": {
      "source": "vision_context.coinglass.v1",
      "board": "liquidations",
      "page": "liquidation_heatmap",
      "screenshot_ref": "data/vision/coinglass/raw/20260604_013000.png",
      "detections": [
        {
          "metric": "open_interest",
          "value": 123456789.0,
          "unit": "USD",
          "confidence": 0.85
        },
        {
          "metric": "funding_rate",
          "value": 0.0123,
          "unit": "%",
          "confidence": 0.92
        }
      ]
    }
  },
  "analysis": {
    "timeframe": "1H",
    "bias_short_term": "NEUTRAL",
    "bias_intraday": "NEUTRAL",
    "regime": "OI_FLAT",
    "squeeze_or_stress_level": "LOW",
    "invalidation": "OI drops >20% in 1H",
    "confidence": "MEDIUM"
  },
  "missing_inputs": ["funding_rate: need OCR confidence >0.9 threshold adjustment"],
  "source_refs": [
    "data/deskpro/inputs/vision_context/coinglass/latest.json",
    "data/vision/coinglass/raw/20260604_013000.png"
  ]
}
```

---

### 2.5 Coinglass Derivatives Bundle

| Champ | Valeur |
|---|---|
| `bundle_id` | `coinglass_derivatives.v1` |
| `producer` | `modules/vision/coinglass/runner.py` (existant, à compléter) |
| `cadence` | 30m–1H |

**Inputs requis :**
- Open Interest (OI) — BTC/ETH
- Funding Rate — BTC/ETH (positif = longs payent shorts)
- Liquidations 24h — Long vs Short
- Long/Short Ratio — distribution des positions
- Heatmap de liquidation — niveaux de stress

**Assets couverts :** BTCUSDT, ETHUSDT

**Output contract :**
```json
{
  "contract": "bundle.coinglass_derivatives.v1",
  "bundle_id": "coinglass_derivatives.v1",
  "produced_at": "2026-06-04T01:30:00Z",
  "freshness_state": "FRESH",
  "assets": ["BTC", "ETH"],
  "inputs": {
    "btc": {
      "open_interest": 12.45e9,
      "oi_unit": "USD",
      "funding_rate": 0.0123,
      "funding_unit": "%",
      "liquidations_24h_long": 45.2e6,
      "liquidations_24h_short": 12.8e6,
      "long_short_ratio": 1.42,
      "liquidation_heatmap": {
        "support_zones": [87500, 87000, 86000],
        "resistance_zones": [94500, 96000, 98000]
      },
      "source": "coinglass_ocr"
    },
    "eth": {
      "open_interest": 5.67e9,
      "oi_unit": "USD",
      "funding_rate": 0.0089,
      "funding_unit": "%",
      "liquidations_24h_long": 18.3e6,
      "liquidations_24h_short": 8.1e6,
      "long_short_ratio": 1.15,
      "liquidation_heatmap": {
        "support_zones": [3200, 3150],
        "resistance_zones": [3650, 3800]
      },
      "source": "coinglass_ocr"
    }
  },
  "analysis": {
    "timeframe": "1H",
    "bias_short_term": "BULLISH",
    "bias_intraday": "NEUTRAL",
    "regime": "LONG_SKEWED",
    "squeeze_or_stress_level": "ELEVATED",
    "invalidation": "OI drops >15%, funding flips negative",
    "confidence": "MEDIUM",
    "notes": "OI élevé + funding positif + longs dominent = risque squeeze si prix baisse vers zones de liquidation long"
  },
  "missing_inputs": [
    "liquidations: values are OCR approximations, not API-level precision",
    "heatmap: zones are coarse from visual OCR, need API for exact levels"
  ],
  "source_refs": [
    "data/deskpro/inputs/vision_context/coinglass/latest.json"
  ]
}
```

---

### 2.6 Energy / Oil Bundle — HYPOTHESIS

| Champ | Valeur |
|---|---|
| `bundle_id` | `energy_oil.v1` |
| `status` | **HYPOTHESIS** |

**Condition d'activation :**
- Brent (`BRENT`) et WTI (`WTI`) doivent être disponibles dans les flux market_metrics
- Les symboles doivent être vérifiés : `UKOIL` (Brent CFD), `USOIL` (WTI CFD), ou futures `CL`, `BZ`
- La gasoline (`RB`) est un nice-to-have, pas un requis

**Design (placeholder) :**
```json
{
  "contract": "bundle.energy_oil.v1",
  "bundle_id": "energy_oil.v1",
  "status": "HYPOTHESIS",
  "blocking": "brent_wti_symbols_not_validated",
  "required_validation": [
    "Vérifier que BRENT/WTI sont dans market_metrics.v1 collectables",
    "Confirmer les tickers exacts (UKOIL, USOIL, CL, BZ)",
    "Vérifier la fraîcheur des données (liquidité hors US hours)"
  ],
  "assets": ["BRENT", "WTI"],
  "analysis": {
    "timeframe": "1D",
    "bias_short_term": "UNKNOWN",
    "bias_intraday": "UNKNOWN",
    "regime": "UNKNOWN",
    "squeeze_or_stress_level": "UNKNOWN",
    "invalidation": null,
    "confidence": "UNKNOWN"
  },
  "missing_inputs": ["ALL: symbols not validated"],
  "source_refs": []
}
```

---

## 3. Contrat JSON canonique — schéma partagé

Tous les bundles partagent ce squelette minimal :

```json
{
  "contract": "bundle.<name>.v1",
  "bundle_id": "<name>.v1",
  "produced_at": "ISO8601 UTC",
  "freshness_state": "FRESH | STALE | UNKNOWN | HYPOTHESIS",
  "assets": ["SYM1", "SYM2"],
  "inputs": {
    "<input_name>": {
      "source": "schema.name",
      "freshness": "FRESH | STALE | UNKNOWN",
      "produced_at": "ISO8601 | null"
    }
  },
  "analysis": {
    "timeframe": "1m | 5m | 15m | 1H | 4H | 1D",
    "bias_short_term": "BULLISH | BEARISH | NEUTRAL | UNKNOWN",
    "bias_intraday": "BULLISH | BEARISH | NEUTRAL | UNKNOWN",
    "regime": "TRENDING | RANGING | SQUEEZE | VOLATILE | BREAKOUT_SIGNAL | UNKNOWN",
    "squeeze_or_stress_level": "LOW | MEDIUM | ELEVATED | HIGH | UNKNOWN",
    "invalidation": "string | null",
    "confidence": "HIGH | MEDIUM | LOW | UNKNOWN",
    "notes": "string | null"
  },
  "missing_inputs": ["string"],
  "source_refs": ["path/to/source.json"]
}
```

**Règles de contrat :**
- `freshness_state` = `FRESH` si toutes les sources sont < cadence/2
- `freshness_state` = `STALE` si au moins une source > cadence
- `freshness_state` = `HYPOTHESIS` si le bundle n'est pas encore validé
- `confidence` = `HIGH` si toutes les sources sont FRESH et les inputs qualitatifs
- `confidence` = `LOW` si au moins une source est STALE ou en HYPOTHESIS
- `missing_inputs` ne doit jamais être vide si `freshness_state` = `STALE`

---

## 4. Classification

### 4.1 ESTABLISHED

| Composant | Fichier | Preuve |
|---|---|---|
| SignalType enum (TRADE/NEWS/ALPHA) | `modules/telegram_screener/parser/signal_schema.py:8` | 32 tests dans `tests/test_telegram_screener_parser*.py` |
| Direction/Confidence enums | `modules/telegram_screener/parser/signal_schema.py:14,19` | 23 tests dans FilterRouter |
| ScreenerSignal dataclass | `modules/telegram_screener/parser/signal_schema.py:25` | 21 tests pipeline wiring |
| ScreenerProducedSignal | `modules/telegram_screener/signal/signal_schema.py:7` | 18 tests signal_producer |
| SignalCandidate (bridge) | `modules/telegram_screener/schema.py:8` | 30+ tests normalizer |
| VisionContextCoinglassV1 | `modules/vision/coinglass/vision_context_v1.py:27` | `tests/test_vision_context_v1.py` |
| Coinglass OCR pipeline | `modules/vision/coinglass/runner.py` | `tests/test_headless_runner.py`, `test_parser_mock.py` |
| Channel routing map | `configs/telegram/channel_map.yaml` | PR #1081 merged |
| InboundMessage / RawMessage | `modules/telegram_ingestion/parser/message_schema.py` | `tests/test_telegram_ingestion_*.py` |
| ConsumerRouter pattern | `modules/telegram_ingestion/distribution/consumer_router.py` | `tests/test_telegram_ingestion_consumer_router.py` |
| ScreenerConsumer wiring | `docs/chantiers/.../patches/001_screener_consumer_wiring.patch` | 4 tests passants (patch non apply encore) |
| Signal context reader | `modules/telegram_screener/service/signal_context_reader.py:12` | lit `market_metrics.v1` depuis `data/data_center/` |
| Coinglass parser (whale alerts) | `modules/telegram_screener/parser/coinglass_parser.py` | 2 regex (alert + transfer) |
| bot_vision_step2.pipeline | `modules/bot_vision_step2/app/bot_vision_step2.py` | capture → inbox → output |

### 4.2 HYPOTHESIS

| Hypothèse | Détail | Bloquant |
|---|---|---|
| Energy/Oil bundle | Brent/WTI symbols non validés dans market_metrics | Oui — pas de bundle sans symbole fiable |
| VIX input pour macro | Pas de source VIX configurée | Oui — `missing_inputs: ["vix: no source"]` |
| SPX input pour macro | SPX ou ES non validés dans market_metrics | Oui — à vérifier vs `collector_binance_spot` coverage |
| US10Y input pour macro | Pas de source taux US | Oui — hors scope spot/crypto |
| Confidence "HIGH" | Aucun bundle n'a encore atteint HIGH | Non — attendu en phase DESIGN |
| Multi-timeframe OCR (ETH, SOL) | Coinglass OCR ne couvre que BTC pour l'instant | Non — extension naturelle |
| Telegram channel P0/P1/bruit | Classification non validée par fixtures | Non — les canaux restent en P0/P1/bruit tant que non prouvés |

### 4.3 TODO

| Action | Priorité | Dépendance |
|---|---|---|
| Créer `modules/analysis_bundles/` (module convention) | P0 | — |
| Implémenter `btc_core_producer.py` (agrège 3 inputs) | P0 | market_metrics stampé + Coinglass OCR FRESH |
| Implémenter `macro_producer.py` | P1 | validation symboles DXY/SPX/VIX/GOLD |
| Appliquer `001_screener_consumer_wiring.patch` | P0 | PR review |
| Créer `20_BUNDLE_DESIGN_AND_OUTPUT_CONTRACT.md` | P0 | **DONE** (ce document) |
| Rédiger `tests/test_bundle_contracts.py` — validation schema JSON | P1 | contrat JSON défini |
| Valider symboles Energy (Brent/WTI) via `collector_binance_spot` | P2 | collector runtime opérationnel |
| Documenter les fixtures de canaux Telegram (P0/P1/bruit) | P2 | 5+ messages parsés par canal |
| Intégrer Coinglass API directe (si dispo) pour précision vs OCR | P3 | `coinglass=NOT_PROVEN_RUNTIME_ADAPTER` |

### 4.4 REMAINING_GAP

| Gap | Impact | Mitigation |
|---|---|---|
| Pas de parser live pour les canaux Telegram hors Coinglass | Le bundle Telegram signal n'a que des fixtures | Appliquer `001_screener_consumer_wiring.patch` |
| Coinglass = OCR only, pas d'API directe | Précision des metrics limitée | OCR confidence threshold à 0.7 minimum |
| VIX / SPX / US10Y absents des market_metrics | Macro bundle incomplet | Macro bundle démarre en mode DEGRADED (gold + DXY only) |
| Pas de module `analysis_bundles/` | Les bundles n'ont pas de producer concret | Créer le module avec convention (scripts/cmd.sh, menu.sh, sanity_check.sh) |
| Pas de consumer pour les bundles (qui les lit?) | Les bundles sortent en fichier mais personne ne les consomme | Définir un Analysis Consumer dans un child GO séparé |
| Energy/Oil = HYPOTHESIS pure | Pas de donnée, pas de contrat | Documenter, ne pas bloquer les 5 autres bundles |

---

## 5. Résumé des changements

| Fichier | Action | Statut |
|---|---|---|
| `docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PIPELINE_01/20_BUNDLE_DESIGN_AND_OUTPUT_CONTRACT.md` | Créé | **NEW** |
| Aucun fichier source modifié | — | Design-only |

## 6. Risques

1. **Coinglass OCR precision** — les métriques extraites par OCR ne sont pas API-level. Le contrat JSON gère ceci via `confidence` et `missing_inputs`.
2. **Coverage macro incomplet** — VIX/SPX/US10Y absents. Le bundle macro commence en mode dégradé (gold + DXY only).
3. **Energy bundle prématuré** — tant que les symboles ne sont pas validés, le bundle reste HYPOTHESIS.
4. **Pas de consumer côté analyse** — les bundles seront produits mais personne ne les lit. Nécessite un child GO `analysis_consumer`.

## 7. Next GO recommandé

`GO_OPT_TRADING_ANALYSIS_BUNDLES_PRODUCER_V1_01` — Implémenter `modules/analysis_bundles/` avec :
- Module convention (cmd.sh, menu.sh, sanity_check.sh)
- `btc_core_producer.py` (combine market_metrics + coinglass_vision + telegram_signals)
- `macro_producer.py` (mode dégradé: DXY + gold)
- `contract_validator.py` (valide chaque bundle contre le schéma canonique)
- Tests: `tests/test_bundle_contracts.py`

## 8. Commandes de validation

```bash
# Vérifier que le document est lisible et valide
python3 -c "
import json, sys
from pathlib import Path
p = Path('docs/chantiers/GO_OPT_TRADING_TELEGRAM_INGESTION_CHILD_INBOUND_PIPELINE_01/20_BUNDLE_DESIGN_AND_OUTPUT_CONTRACT.md')
print(f'OK: {p.stat().st_size} bytes')
"

# Vérifier que les modules référencés existent
for m in \
  modules/telegram_screener/parser/signal_schema.py \
  modules/telegram_screener/signal/signal_schema.py \
  modules/telegram_screener/schema.py \
  modules/vision/coinglass/vision_context_v1.py \
  modules/vision/coinglass/runner.py \
  configs/telegram/channel_map.yaml; do
  [ -f "$m" ] && echo "OK: $m" || echo "MISSING: $m"
done

# Vérifier que les tests existent pour les modules référencés
python3 -m pytest tests/test_telegram_screener_parser.py -q --tb=no 2>/dev/null | tail -1
python3 -m pytest tests/test_telegram_screener_signal_producer.py -q --tb=no 2>/dev/null | tail -1
```
