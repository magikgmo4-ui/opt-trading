---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01_SOURCE_SCHEMA_AUDIT
doc_type: source_schema_audit
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 10_SOURCE_SCHEMA_AUDIT - Source Schema Audit

## Format signal_event V0 (source actuel)

Extrait de `webhook_server.py` ligne 439-454, persisté dans `state/events.jsonl` :

```json
{
  "key": null,
  "engine": "USDTM_LONG",
  "signal": "BUY",
  "symbol": "BTCUSDT",
  "tf": "H1",
  "price": 68000.0,
  "tp": 69000.0,
  "sl": 67500.0,
  "reason": "breakout",
  "_ts": "2026-05-06T02:20:00+00:00",
  "_ip": "127.0.0.1",
  "qty": 0.01,
  "risk_usd": 50.0,
  "risk_real_usd": 50.0
}
```

## Format signal_event V1 (cible)

Défini dans `30_SIGNAL_EVENT_CONTRACT.md` :

```json
{
  "source": "tradingview.webhook",
  "event_type": "signal_event",
  "engine": "USDTM_LONG",
  "symbol": "BTCUSDT",
  "timeframe": "H1",
  "direction": "BUY",
  "timestamp": "2026-05-06T02:20:00+00:00",
  "status": "accepted",
  "payload_hash": "a1b2c3...",
  "raw_payload_ref": null,
  "meta": {"price": 68000.0, "tp": 69000.0, "sl": 67500.0, "reason": "breakout", "debug": {"client_ip": "127.0.0.1"}},
  "risk_context": {"qty": 0.01, "risk_usd": 50.0, "risk_real_usd": 50.0},
  "visual_context_ref": null,
  "desk_snapshot_ref": null,
  "errors": []
}
```

## Classification des champs

| Champ V1 | Source V0 | Classification | Notes |
| --- | --- | --- | --- |
| `source` | constante | **DERIVED** | Toujours `"tradingview.webhook"` |
| `event_type` | constante | **DERIVED** | Toujours `"signal_event"` |
| `engine` | `engine` | **PASS_THROUGH** | Direct |
| `symbol` | `symbol` | **PASS_THROUGH** | Direct |
| `timeframe` | `tf` | **PASS_THROUGH** | Renommage |
| `direction` | `signal` | **PASS_THROUGH** | Renommage + upper() |
| `timestamp` | `_ts` | **PASS_THROUGH** | Renommage |
| `status` | persistance `evt` | **DERIVED** | `"accepted"` si persisté dans events.jsonl |
| `payload_hash` | tout le payload | **DERIVED** | SHA-256 du payload V0 canonique |
| `raw_payload_ref` | — | **DEFAULTED** | `null` (non produit actuellement) |
| `meta` | `price`, `tp`, `sl`, `reason`, `_ip` | **DERIVED** | Regroupement |
| `risk_context` | `qty`, `risk_usd`, `risk_real_usd` | **DERIVED** | Regroupement |
| `visual_context_ref` | — | **DEFAULTED** | `null` (futur) |
| `desk_snapshot_ref` | — | **DEFAULTED** | `null` (futur) |
| `errors` | validation | **DERIVED** | Liste d'erreurs de normalisation |

## Champs V0 non retenus dans V1

| Champ V0 | Raison | Traitement |
| --- | --- | --- |
| `key` | Sécurité, ne doit pas être propagé | **REJECTED** |
| `_ip` | Sensible, déplacé dans `meta.debug.client_ip` | **DERIVED** |

## Point d'entrée Desk Pro actuel

- `desk_pro_orchestrator` → `run_config.example.json` → modules en séquence
- Aucun module ne lit `state/events.jsonl` directement
- `desk_state` agrège `desk/snapshots/latest.json` + `desk/inputs/tv_inputs_latest.json`
- `desk_analyze` lit `desk/snapshots/latest.json` pour OpenAI vision

## Point d'adaptation minimal

L'adapter est un module **isolé** qui :
1. Lit `state/events.jsonl` (V0)
2. Normalise chaque ligne en V1
3. Expose `read_events_v1()` pour les consumers

Il ne modifie **aucun** fichier existant. Il est appelé explicitement par les consumers qui en ont besoin.

## RISKS

- À qualifier.
