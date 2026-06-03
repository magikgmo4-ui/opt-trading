---
inbox_id: GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01
type: go
state: open
parent: GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01
created_at: 2026-06-03
---

# GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01

Normalisation des sorties parseurs en modele commun `SignalCandidate` -> `ScreenerSignal`.

## Fichiers

- `modules/telegram_screener/schema.py` — `SignalCandidate` dataclass
- `modules/telegram_screener/normalizer.py` — fonctions de normalisation
- `tests/test_telegram_screener_normalizer.py` — tests unitaires

## Dependances

- upstream: GO_TELEGRAM_SIGNALS_PARSERS_FIXTURES_CHILD_01
- utilise: `ScreenerSignal`, `Direction`, `Confidence`, `SignalType` (existants)
- fixtures de test existantes dans `tests/fixtures/telegram_screener/`

## Validation

```bash
python3 -m pytest tests/test_telegram_screener_parser.py tests/test_telegram_screener_normalizer.py -q
```
