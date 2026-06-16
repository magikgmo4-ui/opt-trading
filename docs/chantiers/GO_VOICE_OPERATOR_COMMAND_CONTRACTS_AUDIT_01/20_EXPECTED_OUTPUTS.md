# 20_EXPECTED_OUTPUTS — Contrats de reponse vocale par commande

Chaque commande retourne:

```json
{
  "intent": "...",
  "ok": true,
  "one_line": "...",
  "rich": {
    "spoken_text": "...",
    "cards": [],
    "badges": []
  },
  "freshness": {"state": "fresh|stale|closed|unknown"},
  "source": "...",
  "missing": [],
  "next_action": []
}
```

## Exemples par commande

### Etat systeme

spoken_text: "Systeme OK. Data Center PASS. Pipeline hourly OK. LocalCMS OK. Voice API OK. 0 erreurs critiques."
cards: [{label: "Services", value: "5"}, {label: "DC Contrats", value: "28"}, {label: "Pipeline", value: "healthy"}]
missing: [] ou ["data_center_contracts"] si DC inaccessible

### Rapport marche

spoken_text: "Vue marche. SPCX a 171. BTC trend bullish. Gold trend bearish. 7 symboles suivis."
cards: [{label: "SPCX", value: "$171.0"}, {label: "BTC", value: "BULLISH LIVE"}, ...]
missing: [] ou ["market_metrics", "vision_analysis"] si sources absentes

### Analyse BTC

spoken_text: "BTC. Prix 96500. Tendance bullish. VWAP reclaim. Aucun signal actif. Derives non disponibles."
cards: [{label: "Prix", value: "96500"}, {label: "Tendance", value: "bullish"}, ...]
missing: [] ou ["crypto_derivatives"] si absents

### Analyse Gold

spoken_text: "Gold. 1 trade actif. Trend H4 bullish. Setup GOLD_CFD_LONG. Prix XAUUSD 4320. DXY non disponible."
cards: [{label: "Trades XAU actifs", value: "1"}, {label: "Trend H4", value: "BULLISH"}, {label: "Prix", value: "4320"}, {label: "DXY", value: "non dispo"}]
missing: ["DXY_context"] si absent

### Resume executif

spoken_text: "3 faits: 5 setups actifs, SPCX VWAP bullish, 2 alertes critiques. 1 risque: BTC near invalidation. Prochaine action: verifier setups BTC et Gold."
cards: [{label: "Setups", value: "5"}, {label: "SPCX VWAP", value: "BULLISH"}, {label: "Alertes", value: "2 critiques"}, {label: "Risque", value: "BTC invalidation proche"}]

### Priorites

spoken_text: "Priorites. 1. SPCX — edge 85, setup VWAP reclaim, confiance 90%. 2. BTC — signal VWAP reclaim, fraicheur LIVE. 3. Gold — setup CFD LONG, 1 trade ouvert."
Chaque item avec raison explicite

### Attention

spoken_text: "Attention. 1. BTC — donnee stale 45min. 2. Gold — stop proche SL. 3. SPCX — source quality degraded."
Chaque item avec cause explicite

### Top movers

spoken_text: "Top movers. BTC +2.1%, ETH +1.5%, SOL +3.2%, XAUUSD -0.8%. Source: vision_analysis + market_metrics."
Chaque item avec variation si disponible
