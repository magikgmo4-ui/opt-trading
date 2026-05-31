# 04 — Capture Map

## Définition

Le `capture_map` est un registre machine (JSON) qui définit pour chaque asset :
- Les screen types applicables
- Les timeframes
- La priorité relative
- La source (TradingView, Coinglass, etc.)
- Les slots dashboard (pour DASHBOARD_MACRO)

## Fichier

```
modules/bot_vision/headless_capture/capture_map.json
```

Structure :
```json
{
  "$schema": "capture_map.v1",
  "assets": [
    {
      "symbol": "BTCUSDT.P",
      "category": "crypto_major",
      "screens": [
        { "screen_type": "CHART_TECHNICAL", "timeframes": ["15m","1h","4h","1d"], "priority": 1 }
      ]
    }
  ],
  "dashboards": [
    {
      "dashboard_id": "macro_dashboard_01",
      "slots": [
        { "slot": "top-left", "symbol": "BTCUSDT.P" },
        { "slot": "top-right", "symbol": "OANDA:XAUUSD" }
      ]
    }
  ]
}
```

## Profils de capture associés

Les profils de capture concrets (URLs, timeouts, viewport) sont dans les fichiers `profiles.*.json` existants :
- `profiles.production.json` — charts TradingView individuels (CHART_TECHNICAL, ETF_CRYPTO)
- `profiles.macro_dashboard.json` — dashboard macro 2x2 (DASHBOARD_MACRO)
- `profiles.coinglass.json` — pages Coinglass (LIQUIDITY_COINGLASS, FUNDING_COINGLASS, OI_COINGLASS, LS_RATIO_COINGLASS)

## Gaps

- Screeners stocks : profils de capture non encore créés (pas d'URLs définies pour chaque screener)
- NEWS_SENTIMENT : source non encore définie
- TOTAL / TOTAL2 / TOTAL3 / BTC.D : profils TradingView à ajouter
- Essence (RB1!) : profil à ajouter
- FBTC, GBTC, BITB, ARKB : profils à ajouter
