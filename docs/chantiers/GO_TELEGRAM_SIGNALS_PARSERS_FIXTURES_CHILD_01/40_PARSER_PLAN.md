# Parser Plan

## First parser target

- surface: `modules/telegram_screener/parser/coinglass_parser.py`
- input: `RawMessage`
- output: dict structure `telegram_trade_signal_candidate.v1`

## Parsing strategy

1. Detecter le format `Hyperliquid` de `coinglass_alerts`.
2. Extraire `direction`, `asset`, `entry`, `leverage` et `exchange_source`.
3. Deriver `raw_text_ref` depuis `source_channel:message_id`.
4. Marquer `PARTIAL` si TP/SL/timeframe sont absents.

## Non-goals for this first patch

- pas de routing live
- pas d'execution trading
- pas de score de confiance metier
- pas de generalisation multi-canaux prematuree
