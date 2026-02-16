# SCHEMAS — Event → Trade → Perf

## Objectif
Définir un format unique et stable :
- **WebhookEvent** (sources : TradingView / jobs / manuel)
- **PerfEvent** (consommé par `/perf/event`)
- **Trade** (persisté dans SQLite)

## WebhookEvent v1 (résumé)
Champs clés : `schema_version, source, event_type, engine, symbol, side, ts, prices{entry,stop,exit}, qty_hint, meta`.
Voir aussi : `schemas/webhook_event_v1.json`.

## PerfEvent (résumé)
Champs : `type(OPEN|UPDATE|CLOSE), trade_id, engine, symbol, side, ts, entry/stop/exit, qty, risk_usd, meta`.

## Adaptateur
Voir `adapters/webhook_to_perf.py` : fonction `webhook_event_to_perf_event(evt) -> dict | None`.

Règles:
- `SIGNAL` ne va pas dans perf.
- `OPEN/UPDATE` requiert `entry+stop+qty`.
- `CLOSE` requiert `exit`.
