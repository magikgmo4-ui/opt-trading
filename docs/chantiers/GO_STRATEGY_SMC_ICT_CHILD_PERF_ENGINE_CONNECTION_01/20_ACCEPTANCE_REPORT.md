---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01_ACCEPTANCE
doc_type: acceptance_report
go_id: GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01
verdict: PASS_PERF_ENGINE_CONNECTED
created_at: 2026-05-30
---

# 20_ACCEPTANCE_REPORT

## Verdict

```
PASS_PERF_ENGINE_CONNECTED
```

## Livrables

| Fichier | Action | Tests |
|---------|--------|-------|
| `perf/perf_app.py` | POST + GET endpoints ajoutés | — |
| `state/observation_events.jsonl` | créé au premier POST (runtime) | — |
| `tests/test_perf_observation_endpoints.py` | 12 tests | 12/12 PASS |
| `docs/API.md` | 2 endpoints documentés | — |

## Validations

```
tests/test_perf_observation_endpoints.py   12 passed in 0.55s
git diff --check                           clean
failures pré-existantes (desk_pro, telethon) = confirmées hors scope
```

## Surface exposée

```
POST /perf/observation_event
  body  : JSON avec strategy_id (flat ou nested sous strategy.strategy_id)
  store : state/observation_events.jsonl (JSONL append-only)
  retour: {ok, event_id, strategy_id, produced_at}

GET /perf/strategy/{strategy_id}/promotion_gate
  lit   : state/observation_events.jsonl
  appel : score_strategy_events(events, strategy_id=...)
  retour: {strategy_id, sample_size, observation_days,
           promotion_gate.verdict, promotion_gate.reason,
           metrics, total_events_loaded}
```

## État post-GO

```
SMC_ICT_CHOCH_BOS_RETEST
  perf_engine_evidence : AVAILABLE (endpoint opérationnel)
  promotion_gate       : BLOCKED_INSUFFICIENT_SAMPLE (0 ObsEvents postés)
  prochain GO          : GO_STRATEGY_SMC_ICT_CHILD_PAPER_CLOSEOUT_01 (gate ≥2026-06-13)
```
