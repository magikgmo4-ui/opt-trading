# Source Outputs Audit

## Inputs verifies

- `modules/collector_telegram/outputs/status.json`
- `modules/collector_telegram/outputs/channel_results/channel_results_20260603T041014Z-52347c93.json`

## Findings

- `status.json` confirme un run `healthy` et un `run_id` stable.
- `channel_results_20260603T041014Z-52347c93.json` confirme `messages_total = 5` pour `coinglass_alerts`.
- Le fichier `channel_results` est un agregat de canal, pas une source suffisante pour creer des fixtures de parsing message-par-message.
- Les fixtures de parsing doivent donc etre derivees du raw output associe au meme run family: `modules/collector_telegram/outputs/raw/coinglass_alerts.jsonl`.

## Proven message shape

Les 5 messages `coinglass_alerts` observes partagent ce pattern stable:

```text
Hyperliquid whale alert -> leverage -> long/short -> asset -> entry price -> position notional
```

Exemples de champs presents dans le texte brut:

- direction
- asset
- leverage
- entry price
- venue/source (`Hyperliquid`)
- timestamp via metadata du message collecteur

## Missing fields for full trade execution

Les messages `coinglass_alerts` ne fournissent pas encore:

- TP1 / TP2 / TP3
- stop loss
- timeframe explicite

Conclusion:

- un parseur minimal peut produire un signal structure partiel
- le statut de parsing doit rester `PARTIAL` tant que les niveaux de sortie ne sont pas presents
