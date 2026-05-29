# 10_IMPLEMENTATION_SPEC

## Structure module

```text
modules/telegram_screener/
  registry/
    __init__.py
    loader.py              # charge et valide channels.yaml
    models.py              # Channel dataclass + enums
    channels.yaml          # fichier registry canonique
```

## Schéma YAML (V1, depuis GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01)

```yaml
version: 1
updated_at: "2026-05-28"
channels:
  - alias: "TG_SRC_SIGNALS_01"
    kind: "channel"
    title: "Signals Channel A"
    trust_tier: "C"
    categories: ["signals", "macro"]
    expected_parsers: ["trade_claim", "news"]
    symbols_scope: ["BTCUSDT", "ETHUSDT"]
    timeframes_scope: ["1h", "4h"]
    allow_forwarded: false
    allow_media: true
    enabled: false
    notes: "placeholder"
```

## Models

```python
@dataclass
class Channel:
    alias: str
    kind: str                    # channel | group | supergroup
    title: str
    trust_tier: TrustTier        # A | B | C | D
    categories: list[str]
    expected_parsers: list[str]
    symbols_scope: list[str]
    timeframes_scope: list[str]
    allow_forwarded: bool
    allow_media: bool
    enabled: bool
    notes: str

class TrustTier(str, Enum):
    A = "A"   # validated, production
    B = "B"   # validated, watch-only
    C = "C"   # unverified, watch-only
    D = "D"   # blocked / blacklist
```

## Loader API

```python
def load_channel_registry(path: Optional[Path] = None) -> ChannelRegistry
def get_enabled_channels(registry: ChannelRegistry) -> list[Channel]
def get_channels_by_tier(registry: ChannelRegistry, tier: TrustTier) -> list[Channel]
def get_channels_by_category(registry: ChannelRegistry, category: str) -> list[Channel]
```

## Validation rules

- version must be 1
- alias must match `TG_SRC_[A-Z0-9_]+`
- trust_tier must be A/B/C/D
- enabled=False par défaut (true seulement si override explicite)
- categories non vide
- expected_parsers non vide
