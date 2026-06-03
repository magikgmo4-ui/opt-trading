# Fixtures Plan

## Scope

Premier lot de fixtures derive du canal `coinglass_alerts`, car il est deja prouve en collecte locale.

## Files

- `tests/fixtures/telegram_screener/coinglass_alert_samples.json`

## Fixture content rules

- Conserver le texte brut public du message Telegram collecte.
- Associer chaque message a son `message_id`, `source_channel` et `timestamp`.
- Stocker l'expected output minimal du parseur.
- Ne jamais injecter de secret ni de chemin d'env dans les fixtures.

## First batch

- 5 messages reels issus du smoke `coinglass_alerts --limit 5`
- cas `LONG` et `SHORT`
- cas `BTC` et `ETH`
- cas de leverage variables (`25x`, `40x`)
