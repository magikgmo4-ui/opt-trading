---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01_INBOX
doc_type: inbox_entry
go_id: GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01
parent_go: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01
status: OPEN
created_at: 2026-05-30
---

# GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01

Brancher le Perf Engine sur les ObservationEvents SMC_ICT_CHOCH_BOS_RETEST.

## Pourquoi

Gap G04 du GO parent `GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01` :
`score_strategy_events()` existe dans `perf_engine.py` mais n'est pas branché.
Aucun endpoint POST/GET pour les ObservationEvents. Requis pour la promotion ACTIVE_LIVE.

## Livrables

- `POST /perf/observation_event` — stockage dans `state/observation_events.jsonl`
- `GET /perf/strategy/{strategy_id}/promotion_gate` — appel `score_strategy_events()`
- `tests/test_perf_observation_endpoints.py` — ≥10 tests
- `docs/API.md` — 2 endpoints documentés

## Gate

Aucune date imposée — à livrer pendant la fenêtre paper (avant 2026-06-13) pour
que `perf_engine_evidence` soit disponible au moment du PAPER_CLOSEOUT_01.

## Chantier

`docs/chantiers/GO_STRATEGY_SMC_ICT_CHILD_PERF_ENGINE_CONNECTION_01/`
