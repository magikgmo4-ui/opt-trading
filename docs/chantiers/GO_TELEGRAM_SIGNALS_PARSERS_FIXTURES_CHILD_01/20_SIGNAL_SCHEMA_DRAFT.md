# Signal Schema Draft

## Target schema

```json
{
  "schema": "telegram_trade_signal_candidate.v1",
  "source_channel": "coinglass_alerts",
  "message_timestamp": "2026-06-03T04:05:40+00:00",
  "raw_text_ref": "coinglass_alerts:215026",
  "asset": "BTC",
  "symbol": "BTC",
  "direction": "LONG",
  "entry": 66447.4,
  "tp1": null,
  "tp2": null,
  "tp3": null,
  "stop_loss": null,
  "leverage": 25,
  "timeframe": null,
  "exchange_source": "Hyperliquid",
  "confidence": "MEDIUM",
  "parse_status": "PARTIAL",
  "parse_errors": []
}
```

## Status semantics

- `PARSED`: tous les champs critiques du setup sont presents, y compris sorties et stop.
- `PARTIAL`: signal metier exploitable partiellement, mais sorties et/ou stop absents.
- `UNKNOWN_FORMAT`: aucun pattern reconnu.

## Notes

- `raw_text_ref` doit etre stable sans recopier le message complet dans tous les etages suivants.
- `symbol` reste egal a `asset` tant que la paire exacte n'est pas explicite dans le message.
- `confidence` est une confiance de parsing, pas une confiance de trading.
