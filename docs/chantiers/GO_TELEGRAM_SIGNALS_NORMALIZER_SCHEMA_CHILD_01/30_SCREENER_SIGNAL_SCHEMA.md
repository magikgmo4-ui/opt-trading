# ScreenerSignal Schema (cible de normalisation)

## Definition

Cible de normalisation : `ScreenerSignal` dans `modules/telegram_screener/parser/signal_schema.py`.

Le schema est deja implemente et utilise. Ce document verifie qu'il est compatible avec le flux de normalisation.

## Etat actuel

```python
@dataclass
class ScreenerSignal:
    source_channel: str
    signal_type: SignalType          # TRADE | NEWS | ALPHA
    timestamp: str
    parsed_at: str
    raw_text: str
    pair: Optional[str] = None
    direction: Optional[Direction] = None  # LONG | SHORT
    price: Optional[float] = None
    sl: Optional[float] = None
    tp: Optional[float] = None
    size: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[Confidence] = None # HIGH | MEDIUM | LOW
    metadata: dict = field(default_factory=dict)
```

## Mapping SignalCandidate -> ScreenerSignal

| SignalCandidate | ScreenerSignal | Notes |
|---|---|---|
| `raw_message` | `raw_text` | Copie directe |
| `source_channel` | `source_channel` | Copie directe |
| `symbol` | `pair` | Mapping direct |
| `direction` | `direction` | Cast en `Direction` enum |
| `entry_min` | `price` | On utilise entry_min (ou la moyenne si range) |
| `tp` | `tp` | On prend le premier TP si liste non vide |
| `sl` | `sl` | Copie directe |
| - | `signal_type` | Necessite un type par defaut (ex: `TRADE`) |
| - | `timestamp` | Necessite une valeur (cf `created_at`) |
| - | `parsed_at` | Now |
| `parse_confidence` | `confidence` | Cast en `Confidence` enum |
| - | `size` | Non mappe (pas dans SignalCandidate) |
| - | `category` | Non mappe (pas dans SignalCandidate) |
| `parse_errors` | `metadata["parse_errors"]` | Stocke dans metadata |
| `message_ref` | `metadata["message_ref"]` | Stocke dans metadata |
| `leverage` | `metadata["leverage"]` | Stocke dans metadata |
| `timeframe` | `metadata["timeframe"]` | Stocke dans metadata |
| `parse_status` | `metadata["parse_status"]` | Stocke dans metadata |

## Decision

- `ScreenerSignal` est compatible comme cible.
- Les champs additionnels de `SignalCandidate` (`leverage`, `timeframe`, `parse_status`) sont stockes dans `metadata` de `ScreenerSignal`.
- `signal_type` est force a `TRADE` par defaut dans le normalizer (car `SignalCandidate` est agnostique du type de signal).
