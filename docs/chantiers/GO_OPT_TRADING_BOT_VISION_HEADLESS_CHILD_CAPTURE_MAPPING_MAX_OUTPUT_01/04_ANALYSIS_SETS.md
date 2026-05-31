---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01_ANALYSIS
doc_type: analysis_sets
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
---

# 04_ANALYSIS_SETS.md

Analyse par type d'écran : champs de sortie, confiance, format.

## 1_CHART_TECHNICAL

Analyseur : `bot_vision_step2` (single mode) — existant.

| Champ | Type | Description |
|-------|------|-------------|
| trend_direction | string | bullish / bearish / neutral |
| market_structure | string | HH/HL, LH/LL, range, consolidation |
| support_resistance | number[] | Niveaux S/R détectés |
| breakout_breakdown | boolean | Breakout ou breakdown en cours |
| volatility_state | string | contraction / expansion / normale |
| momentum_state | string | rising / falling / weakening |
| volume_confirmation | boolean | Volume confirme le mouvement |
| invalidations | string[] | Scénarios invalides |

## 2_DASHBOARD_MACRO

Analyseur : `bot_vision_step2` (quad mode) — existant.

| Champ | Type | Description |
|-------|------|-------------|
| risk_on_risk_off | string | risk_on / risk_off / neutral |
| dxy_pressure | string | Impact DXY sur BTC |
| gold_safe_haven_bid | boolean | Or en mode safe haven |
| oil_inflation_pressure | boolean | Pétrole signale inflation |
| btc_correlation_break | boolean | BTC décorrélé du DXY/gold |
| macro_divergence | string[] | Divergences inter-actifs |

## 3_LIQUIDITY_COINGLASS

Analyseur : OCR spécialisé — à créer.

| Champ | Type | Description |
|-------|------|-------------|
| liquidity_zones | number[] | Zones de liquidité |
| long_squeeze_risk | boolean | Risque de squeeze longs |
| short_squeeze_risk | boolean | Risque de squeeze shorts |
| funding_extreme | boolean | Funding anormal |
| oi_expansion_or_flush | string | Expansion ou flush de l'OI |
| crowding_direction | string | long / short / neutral |
| trap_probability | string | low / medium / high |

## 4_SCREENER_STOCKS

Analyseur : analyse texte + LLM — à créer.

| Champ | Type | Description |
|-------|------|-------------|
| sector_rotation | string[] | Secteurs en rotation |
| momentum_clusters | string[] | Clusters de momentum |
| risk_appetite | string | Appétit au risque actions |
| theme_strength | object | Force par thème (AI, defense, etc.) |
| relative_volume_spike | string[] | Tickers avec volume anormal |
| watchlist_candidates | string[] | Candidats à surveiller |

## 5_FORMAT_SORTIE_ANALYSE

Le format de sortie suit le contrat `vision_analysis.v1` (reader DeskPro) :

```json
{
  "input_class": "vision_analysis.v1",
  "capture_id": "cap_20260525_000000_BTCUSDT_15m",
  "symbol": "BTCUSDT",
  "timeframe": "15m",
  "analysis_ts": "2026-05-25T00:00:00Z",
  "source_module": "bot_vision_step2",
  "freshness_state": "fresh",
  "signals": [
    {
      "type": "trend_direction",
      "value": "bullish",
      "confidence": 0.75,
      "note": "higher lows pattern"
    }
  ],
  "raw_analysis": "(OpenAI text output)",
  "image_ref": "data/screenshots/...png"
}
```

## 6_METHODES_D_ANALYSE

| Méthode | Usage | Priorité | Existant |
|---------|-------|----------|----------|
| OpenAI Vision (gpt-4.1-mini) | Analyse chart complète | P0 | ✅ bot_vision_step2 |
| OCR (texte dans l'image) | Lire niveaux, prix, funding | P1 | ❌ à créer |
| Regex parsing | Extraire signaux du texte OpenAI | P0 | ✅ bot_vision_step2 |
| LLM prompt structuré | Analyse screener | P1 | ❌ à créer |

## 7_SCORE_DE_CONFIANCE

| Plage | Interprétation |
|-------|---------------|
| 0.0 – 0.3 | Spéculatif, peu de preuves |
| 0.3 – 0.6 | Possible, preuves partielles |
| 0.6 – 0.8 | Probable, preuves convergentes |
| 0.8 – 1.0 | Confirmé, preuves fortes |
