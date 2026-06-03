# Normalizer Plan

## Fichiers a creer

### 1. `modules/telegram_screener/schema.py`

Nouveau module contenant `SignalCandidate`.

```python
@dataclass
class SignalCandidate:
    raw_message: str
    source_channel: str
    asset: Optional[str] = None
    symbol: Optional[str] = None
    direction: Optional[str] = None
    entry_min: Optional[float] = None
    entry_max: Optional[float] = None
    tp: list[float] = field(default_factory=list)
    sl: Optional[float] = None
    leverage: Optional[int] = None
    timeframe: Optional[str] = None
    parse_status: str = "UNKNOWN_FORMAT"
    parse_confidence: str = "LOW"
    parse_errors: list[str] = field(default_factory=list)
    message_ref: str = ""
    created_at: str = ""

    def to_dict(self) -> dict: ...
```

### 2. `modules/telegram_screener/normalizer.py`

Nouveau module contenant :

```python
def coinglass_dict_to_candidate(raw: dict) -> SignalCandidate:
    """Convertit le dict output de coinglass_parser en SignalCandidate."""

def screener_signal_to_candidate(signal: ScreenerSignal) -> SignalCandidate:
    """Convertit un ScreenerSignal existant en SignalCandidate."""

def candidate_to_screener_signal(candidate: SignalCandidate, signal_type: SignalType = SignalType.TRADE) -> ScreenerSignal:
    """Convertit un SignalCandidate en ScreenerSignal pour le pipeline."""

def normalize_coinglass_dict(raw: dict) -> ScreenerSignal:
    """Convenience : coinglass dict -> ScreenerSignal en une etape."""
```

### 3. `tests/test_telegram_screener_normalizer.py`

Tests unitaires pour les 4 fonctions du normalizer.

## Flux de donnees

```
coinglass_parser (dict)
    |
    v
coinglass_dict_to_candidate()
    |
    v
SignalCandidate ---- candidate_to_screener_signal() --> ScreenerSignal --> pipeline
    ^
    |
screener_signal_to_candidate()
    |
trade/news/alpha parsers (ScreenerSignal)
```

## Non-fonctionnel

- Aucune modification des parseurs existants.
- Aucune modification des fixtures existantes.
- Les tests utilisent les fixtures existantes et des entrees inline.
- `coinglass_dict_to_candidate` extrait le raw_text du `raw_text_ref` si disponible, sinon chaine vide.
