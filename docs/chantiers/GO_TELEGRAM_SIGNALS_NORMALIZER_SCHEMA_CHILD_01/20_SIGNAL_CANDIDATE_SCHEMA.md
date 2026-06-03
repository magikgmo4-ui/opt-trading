# SignalCandidate Schema

## Definition

Modele intermediaire universel representant le resultat normalise de n'importe quel parseur Telegram.

## Champs

```
raw_message: str
    Texte brut original du message Telegram.

source_channel: str
    Nom du canal Telegram source.

asset: Optional[str]
    Actif sous-jacent (ex: "BTC", "ETH").

symbol: Optional[str]
    Symbole de trading (ex: "BTCUSDT", "BTC"). Par defaut = asset.

direction: Optional[str]
    Direction de trading : "LONG" ou "SHORT".

entry_min: Optional[float]
    Prix d'entree minimum (ou prix unique si entry_max est None).

entry_max: Optional[float]
    Prix d'entree maximum (zone d'entree).

tp: list[float]
    Liste des niveaux de take-profit (0 a N).

sl: Optional[float]
    Niveau de stop-loss unique.

leverage: Optional[int]
    Levier (ex: 25 pour 25x).

timeframe: Optional[str]
    Timeframe du signal (ex: "1h", "4h", "1d").

parse_status: str
    Etat du parsing : "PARSED" | "PARTIAL" | "UNKNOWN_FORMAT"

parse_confidence: str
    Confiance dans le parsing : "HIGH" | "MEDIUM" | "LOW"

parse_errors: list[str]
    Liste des erreurs rencontrees pendant le parsing.

message_ref: str
    Reference stable au message original (ex: "coinglass_alerts:215026").

created_at: str
    Timestamp ISO de creation du SignalCandidate.
```

## Semantique `parse_status`

- `PARSED` : tous les champs critiques du setup sont presents (direction, entry, sorties).
- `PARTIAL` : signal exploitable partiellement (direction + entry presents, mais sorties manquantes).
- `UNKNOWN_FORMAT` : aucun pattern reconnu (signal non parse).

## Semantique `tp`

- `tp` est une liste plate, ordonnee du TP le plus proche au plus eloigne.
- Si aucun TP, liste vide `[]`.
- Pas de limite arbitraire (contrairement a l'ancien `tp1/tp2/tp3` du dict coinglass).

## Mapping depuis les parseurs

### Depuis le dict coinglass (`telegram_trade_signal_candidate.v1`)

| Dict coinglass | SignalCandidate |
|---|---|
| `raw_text_ref` | `message_ref` |
| `source_channel` | `source_channel` |
| `asset` | `asset` |
| `symbol` | `symbol` |
| `direction` | `direction` |
| `entry` | `entry_min` = entry, `entry_max` = entry |
| `tp1/tp2/tp3` | `tp` = liste filtree des non-None |
| `stop_loss` | `sl` |
| `leverage` | `leverage` |
| `timeframe` | `timeframe` |
| `parse_status` | `parse_status` |
| `confidence` | `parse_confidence` |
| `parse_errors` | `parse_errors` |
| (pas de champ) | `raw_message` = reconstruit via `message_ref` |
| `message_timestamp` | `created_at` |

### Depuis `ScreenerSignal` (trade/news/alpha)

| ScreenerSignal | SignalCandidate |
|---|---|
| `raw_text` | `raw_message` |
| `source_channel` | `source_channel` |
| `pair` | `symbol`, `asset` = extrait du pair |
| `direction` | `direction` |
| `price` | `entry_min` = price, `entry_max` = price |
| `tp` | `tp` = [tp] si present |
| `sl` | `sl` |
| `confidence` | `parse_confidence` |
| `signal_type` | perdu volontairement (car `SignalCandidate` est agnostique) |
