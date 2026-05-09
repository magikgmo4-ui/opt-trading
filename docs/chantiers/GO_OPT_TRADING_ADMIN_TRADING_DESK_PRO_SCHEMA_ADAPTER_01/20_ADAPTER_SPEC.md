---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01_ADAPTER_SPEC
doc_type: adapter_spec
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 20_ADAPTER_SPEC - Adapter Specification V0 → V1

## Input contract

Payload V0 (dict) tel que persisté dans `state/events.jsonl` :

```python
{
    "key": None,           # REJECTED (sécurité)
    "engine": str,         # requis
    "signal": str,         # "BUY" | "SELL"
    "symbol": str,         # requis
    "tf": str,             # requis
    "price": float,        # optionnel → meta
    "tp": float,           # optionnel → meta
    "sl": float,           # optionnel → meta
    "reason": str,         # optionnel → meta
    "_ts": str,            # ISO-8601 UTC
    "_ip": str,            # → meta.debug.client_ip
    "qty": float,          # optionnel → risk_context
    "risk_usd": float,     # optionnel → risk_context
    "risk_real_usd": float # optionnel → risk_context
}
```

## Output contract

Signal event V1 (dict) :

```python
{
    "source": "tradingview.webhook",    # DERIVED (constante)
    "event_type": "signal_event",       # DERIVED (constante)
    "engine": str,                      # PASS_THROUGH
    "symbol": str,                      # PASS_THROUGH
    "timeframe": str,                   # PASS_THROUGH (renommé de tf)
    "direction": str,                   # PASS_THROUGH (renommé de signal, upper)
    "timestamp": str,                   # PASS_THROUGH (renommé de _ts)
    "status": "accepted",               # DERIVED
    "payload_hash": str,                # DERIVED (SHA-256)
    "raw_payload_ref": None,            # DEFAULTED
    "meta": dict | None,                # DERIVED (regroupement)
    "risk_context": dict | None,        # DERIVED (regroupement)
    "visual_context_ref": None,         # DEFAULTED
    "desk_snapshot_ref": None,          # DEFAULTED
    "errors": list[str]                 # DERIVED (validation)
}
```

## Erreurs bloquantes (validation)

| Erreur | Impact | Action |
| --- | --- | --- |
| `engine` vide | `is_valid=False` | Rejeté par consumer |
| `symbol` vide | `is_valid=False` | Rejeté par consumer |
| `timeframe` vide | `is_valid=False` | Rejeté par consumer |
| `direction` invalide | `is_valid=False` | Rejeté par consumer |
| `timestamp` manquant | `is_valid=False` | Rejeté par consumer |
| `timestamp` non parseable | `is_valid=False` | Rejeté par consumer |

## Erreurs non bloquantes (warnings)

| Erreur | Impact | Action |
| --- | --- | --- |
| `status` inconnu | `is_valid=True` | Warning dans errors |
| `source` inattendu | `is_valid=True` | Warning dans errors |
| `event_type` inattendu | `is_valid=True` | Warning dans errors |

## Stratégie de defaults

| Champ | Default | Raison |
| --- | --- | --- |
| `source` | `"tradingview.webhook"` | Constacte, seul producteur actuel |
| `event_type` | `"signal_event"` | Constante |
| `status` | `"accepted"` | Seul chemin persisté dans events.jsonl |
| `raw_payload_ref` | `null` | Non produit actuellement |
| `visual_context_ref` | `null` | Futur |
| `desk_snapshot_ref` | `null` | Futur |

## Stratégie de timestamp

- `timestamp` V1 = `_ts` V0 (pass-through, pas de transformation)
- Format: ISO-8601 UTC (déjà dans ce format dans events.jsonl)
- Validation: `datetime.fromisoformat()` avec remplacement `Z` → `+00:00`

## Stratégie de hash/ref

- `payload_hash`: SHA-256 du payload V0 canonique (`json.dumps(sort_keys=True, separators=(",", ":"))`)
- Déterministe: même payload → même hash
- Permet déduplication et intégrité
- `raw_payload_ref`: `null` (non produit, futur pour replay/forensic)

## No-trade semantics

- Les événements `skipped` ne sont **pas** dans `events.jsonl` (le webhook ne les persiste pas)
- Si un événement `skipped` apparaît quand même, l'adapter le traite normalement
- Le consumer ne doit pas déduire l'absence de `skipped` depuis events.jsonl

## Compatibility avec Desk Pro

- L'adapter ne modifie **aucun** fichier existant
- L'adapter est un module Python importable
- `read_events_v1()` retourne une liste de V1 prête à consommer
- `normalize_signal_event_v1()` transforme un seul payload
- `validate_signal_event_v1()` valide un V1 et retourne `(is_valid, errors)`
- `payload_hash()` calcule le hash d'un payload V0

## API publique

```python
from modules.desk_pro.signal_event_adapter import (
    normalize_signal_event_v1,  # V0 dict → V1 dict
    validate_signal_event_v1,   # V1 dict → (bool, list[str])
    read_events_v1,             # path, limit → list[V1]
    payload_hash,               # V0 dict → str (SHA-256)
)
```
