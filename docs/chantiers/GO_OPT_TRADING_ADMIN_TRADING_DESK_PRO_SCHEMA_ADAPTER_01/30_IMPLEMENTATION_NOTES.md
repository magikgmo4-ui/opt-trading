---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01_IMPLEMENTATION_NOTES
doc_type: implementation_notes
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 30_IMPLEMENTATION_NOTES - Implementation Notes

## Fichier créé

`modules/desk_pro/signal_event_adapter.py`

### Pourquoi `modules/desk_pro/` ?

- `desk_pro` est le consumer final de `signal_event` V1
- L'adapter fait partie de la couche d'entrée Desk Pro
- `models.py` et le service aggregator sont déjà dans `desk_pro/`
- `desk_analyze` est un consumer séparé (Telegram /analyze), pas le consumer principal

### Choix d'implémentation

1. **Module isolé**: aucun import depuis `webhook_server.py`, `desk_state.py`, ou tout module runtime
2. **Stateless**: pas de lecture de fichier dans `normalize_signal_event_v1()`, pas d'écriture
3. **Pure functions**: entrée dict → sortie dict, pas d'effets de bord
4. **`read_events_v1()`**: seule fonction qui lit un fichier (events.jsonl), en lecture seule

### Fonctions

| Fonction | Signature | Rôle |
| --- | --- | --- |
| `normalize_signal_event_v1` | `dict → dict` | V0 → V1 mapping |
| `validate_signal_event_v1` | `dict → (bool, list[str])` | Validation V1 |
| `read_events_v1` | `path, limit → list[dict]` | Lecture + normalisation batch |
| `payload_hash` | `dict → str` | SHA-256 canonique |

### Tests

`tests/test_signal_event_adapter.py` — 30 tests, tous passent.

| Classe | Tests | Couverture |
| --- | --- | --- |
| `TestNormalize` | 12 | V0→V1: full, minimal, meta, risk, hash, refs, edge cases |
| `TestValidate` | 10 | V1 validation: valid, missing fields, invalid, non-blocking |
| `TestPayloadHash` | 3 | Hash determinism and format |
| `TestRoundTrip` | 4 | V0→V1→validate round-trip |

### Ce qui n'a PAS été modifié

- `webhook_server.py` — aucun changement
- `state/events.jsonl` — aucun changement
- `modules/desk_analyze/` — aucun changement
- `modules/desk_state/` — aucun changement
- Aucun service systemd
- Aucun import runtime

### Utilisation future

```python
from modules.desk_pro.signal_event_adapter import read_events_v1

# Lire les 50 derniers signaux V1
events = read_events_v1("/opt/trading/state/events.jsonl", limit=50)

for evt in events:
    print(f"{evt['direction']} {evt['symbol']} {evt['timeframe']} @ {evt['timestamp']}")
```
