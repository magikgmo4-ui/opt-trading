# API — Endpoints (résumé)

## Webhook
- `POST /tv` : reçoit alertes TradingView (JSON object + key)
- `GET /dash` : UI dashboard (webhook)
- `GET /api/state` / `/api/events` / `/api/metrics` : données UI

## Performance
- `POST /perf/event` : OPEN/UPDATE/CLOSE
- `GET /perf/summary`
- `GET /perf/equity`
- `GET /perf/open`
- `GET /perf/trades?limit=50&engine=...&status=OPEN|CLOSED&symbol=...`
- `GET /perf/ui`

## Strategy Observation (paper tracking)
- `POST /perf/observation_event` : persiste un ObservationEvent dans `state/observation_events.jsonl`
  - Body : JSON object avec `strategy_id` (flat) ou `strategy.strategy_id` (nested)
  - Retourne : `{ok, event_id, strategy_id, produced_at}`
- `GET /perf/strategy/{strategy_id}/promotion_gate` : évalue la promotion gate via `score_strategy_events()`
  - Retourne : `{strategy_id, sample_size, observation_days, promotion_verdict, promotion_reason, total_events_loaded, ...}`

## Exemples curl
```bash
curl -s http://127.0.0.1:8010/perf/open
curl -s "http://127.0.0.1:8010/perf/trades?limit=5"
curl -s -X POST http://127.0.0.1:8010/perf/observation_event \
  -H 'Content-Type: application/json' \
  -d '{"strategy_id":"SMC_ICT_CHOCH_BOS_RETEST","signal":{"direction":"LONG_WATCH","confidence":0.65}}'
curl -s "http://127.0.0.1:8010/perf/strategy/SMC_ICT_CHOCH_BOS_RETEST/promotion_gate"
```

## RISKS

- À qualifier.
