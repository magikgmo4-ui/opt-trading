# 20_WEBHOOK_TEMPLATE — Template JSON

## Fichier

`modules/tradingview_observer/templates/alert_webhook_template_v1.json`

## Template d'alerte

```json
{
  "template_version": "v1",
  "description": "TradingView alert webhook template — non-critical, test only",
  "symbol": "BITGET:BTCUSDT.P",
  "timeframe": "15",
  "alert_type": "webhook",
  "condition": {
    "type": "cross",
    "frequency": "once_per_bar",
    "operator": "crossing",
    "series_1": { "type": "plot", "study": "RSI", "value": "70" },
    "series_2": { "type": "value", "value": 70 }
  },
  "webhook": {
    "url": "http://localhost:9999/test-webhook",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json"
    }
  },
  "message_template": "RSI cross > 70 on {{ticker}} @ {{interval}} — price {{close}}",
  "status": "test_only",
  "active": false
}
```

## Exemple de payload webhook recu

Ce payload est ce que TradingView envoie au webhook URL quand l'alerte se declenche.

```json
{
  "ticker": "BITGET:BTCUSDT.P",
  "interval": "15",
  "time": "2026-05-05T00:00:00Z",
  "close": 80719.9,
  "open": 80600.0,
  "high": 80850.0,
  "low": 80550.0,
  "volume": 1500.0,
  "message": "RSI cross > 70 on BITGET:BTCUSDT.P @ 15 — price 80719.9",
  "study": "RSI",
  "condition": "cross > 70"
}
```

## Champs documentes

| Champ | Type | Description |
|-------|------|-------------|
| `ticker` | string | Symbole TradingView |
| `interval` | string | Timeframe |
| `time` | ISO 8601 | Timestamp de la bougie |
| `close` | float | Prix de cloture |
| `open` | float | Prix d'ouverture |
| `high` | float | Plus haut |
| `low` | float | Plus bas |
| `volume` | float | Volume |
| `message` | string | Message personnalise |
| `study` | string | Nom de l'etude/indicateur |
| `condition` | string | Condition de declenchement |

## Limites connues

- Les champs exacts du payload dependent de la configuration Pine Script et de TradingView
- Certains champs (order_id, strategy) ne sont presents que pour les strategies
- Le payload reel peut varier selon la version de TradingView Desktop
- Ce template est une approximation basee sur la documentation TV publique
