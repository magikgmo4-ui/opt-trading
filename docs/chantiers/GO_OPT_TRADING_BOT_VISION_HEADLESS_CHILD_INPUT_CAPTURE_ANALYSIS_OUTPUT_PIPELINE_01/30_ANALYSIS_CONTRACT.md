---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01_ANALYSIS_CONTRACT
doc_type: analysis_contract
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01
---

# 30_ANALYSIS_CONTRACT.md

Analyse par type d'écran : OCR, détection de contenu, extraction de signaux, format de sortie.

## 1_ANALYSIS_CHAIN

```
Capture screenshot
  ↓
Classification du screen_type (déduit ou explicite)
  ↓
Analyseur spécialisé par type
  ↓
Extraction : tendance, niveaux, signaux, risques
  ↓
Génération du JSON d'analyse
  ↓
(optionnel) Résumé texte pour Telegram
  ↓
(optionnel) Données structurées pour Data Center
```

## 2_ANALYSEURS_PAR_TYPE

### 2.1 CHART_TECHNICAL_SCREEN

Objectif : lecture technique pure.

Analyse attendue :

| Champ | Type | Description |
|-------|------|-------------|
| trend_direction | string | haussier / baissier / neutre |
| market_structure | string | HH/HL, LH/LL, range, consolidation |
| support_resistance | number[] | Niveaux S/R détectés |
| breakout_breakdown | boolean | Breakout ou breakdown en cours |
| volatility_state | string | contraction / expansion / normale |
| momentum_state | string | bullish / bearish / weakening / strengthening |
| volume_confirmation | boolean | Volume confirme-t-il le mouvement ? |
| invalidations | string[] | Scénarios invalides |

### 2.2 LIQUIDITY_DERIVATIVES_SCREEN

Objectif : comprendre la pression levier / liquidation.

Analyse attendue :

| Champ | Type | Description |
|-------|------|-------------|
| liquidity_zones | number[] | Zones de liquidité |
| long_squeeze_risk | boolean | Risque de squeeze longs |
| short_squeeze_risk | boolean | Risque de squeeze shorts |
| funding_extreme | boolean | Funding anormal |
| oi_expansion_or_flush | string | Expansion ou flush de l'OI |
| crowding_direction | string | Côté crowding : long / short / neutre |
| trap_probability | string | low / medium / high |

### 2.3 MACRO_CROSS_ASSET_SCREEN

Objectif : relier BTC / gold / oil / DXY / yields.

Analyse attendue :

| Champ | Type | Description |
|-------|------|-------------|
| risk_on_risk_off | string | risk_on / risk_off / neutre |
| dxy_pressure | string | haussier / baissier / neutre sur BTC |
| gold_safe_haven_bid | boolean | Or en mode safe haven |
| oil_inflation_pressure | boolean | Pétrole signale inflation |
| btc_correlation_break | boolean | BTC décorrélé du DXY/gold |
| macro_divergence | string[] | Divergences inter-actifs |

### 2.4 ETF_CRYPTO_SCREEN

Objectif : capter le narratif institutionnel BTC.

Analyse attendue :

| Champ | Type | Description |
|-------|------|-------------|
| etf_relative_strength | string | Force relative des ETF vs spot |
| btc_spot_confirmation | boolean | Spot confirme le mouvement ETF |
| gbtc_pressure | string | Pression GBTC (premium/discount) |
| institutional_bid_proxy | string | Signal institutionnel déduit |
| gap_vs_spot | number | Écart ETF / spot |

### 2.5 STOCK_SCREENER_SCREEN

Objectif : détecter rotation sectorielle et momentum actions.

Analyse attendue :

| Champ | Type | Description |
|-------|------|-------------|
| sector_rotation | string[] | Secteurs en rotation |
| momentum_clusters | string[] | Clusters de momentum |
| risk_appetite | string | Appétit au risque actions |
| theme_strength | object | Force par thème (AI, defense, etc.) |
| relative_volume_spike | string[] | Tickers avec volume anormal |
| watchlist_candidates | string[] | Candidats à surveiller |

### 2.6 NEWS_SENTIMENT_SCREEN

Objectif : relier mouvement prix ↔ catalyseur.

Analyse attendue :

| Champ | Type | Description |
|-------|------|-------------|
| event_type | string | Type d'événement |
| asset_impacted | string | Actif impacté |
| sentiment | string | Positif / négatif / neutre |
| urgency | string | haute / moyenne / faible |
| price_reaction | string | Réaction prix observée |
| confirmed_or_unconfirmed | string | Confirmé / rumeur |

## 3_FORMAT_ANALYSE_GENERIQUE

```json
{
  "capture_id": "uuid",
  "screen_type": "CHART_TECHNICAL_SCREEN",
  "asset": "BTCUSDT",
  "timeframe": "15m",
  "summary": "BTC teste une résistance avec volume en hausse.",
  "signals": [
    {
      "type": "breakout_attempt",
      "direction": "bullish",
      "confidence": 0.68,
      "evidence": ["price above VWAP", "volume increasing", "RSI rising"]
    }
  ],
  "levels": {
    "support": [104000, 102800],
    "resistance": [106500, 108000]
  },
  "risk_flags": ["funding elevated", "liquidity above current price"],
  "next_watch": "confirmation above resistance or rejection back below VWAP",
  "analysis_timestamp_utc": "2026-05-29T00:00:00Z",
  "analysis_version": "v1"
}
```

## 4_METHODES_D_ANALYSE

| Méthode | Usage | Priorité |
|---------|-------|----------|
| OCR (texte dans l'image) | Lire niveaux, prix, indicateurs | P0 |
| Détection de couleur / forme | Identifier bougies, lignes, zones | P1 |
| Classification CNN | Type de pattern (range, trend, volatility) | P2 |
| LLM vision (OpenAI) | Analyse sémantique complète | P0 |

## 5_CONFIDENCE_SCORE

Chaque signal embarque un score de confiance [0.0, 1.0] :

| Plage | Interprétation |
|-------|---------------|
| 0.0 – 0.3 | Spéculatif, peu de preuves |
| 0.3 – 0.6 | Possible, preuves partielles |
| 0.6 – 0.8 | Probable, preuves convergentes |
| 0.8 – 1.0 | Confirmé, preuves fortes |
