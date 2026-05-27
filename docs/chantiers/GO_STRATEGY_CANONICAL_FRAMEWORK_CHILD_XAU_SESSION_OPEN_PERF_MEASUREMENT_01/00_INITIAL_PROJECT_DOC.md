---
doc_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01_INITIAL
doc_type: initial_project_doc
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
pf_id: PF_STRATEGY_FRAMEWORK_REGISTRY
status: IN_PROGRESS
created_at: 2026-05-27
---

# GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_PERF_MEASUREMENT_01

## Objectif

Produire une mesure initiale de performance pour `xau_session_open_v1` afin de réduire le gap `perf_status=UNMEASURED` du parent `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01`.

## Contexte

- `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_ADAPTER_OBSERVABILITY_WARNING_METRICS_01` fermé — PR #860
- `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_REGISTRY_CLOSE_GATE_01` fermé — PR #862
- Registry: 9/9 entrées valides, KNOWN_IDS corrigé 7→9
- Gap restant parent: `perf_status=UNMEASURED` + `telegram_latency_status=UNMEASURED`
- `xau_session_open_v1` raccordée à `trading_realtime_v1` (STRATEGY_ID hardcodé) et `trading_lab_v1` (DEFAULT_STRATEGY_ID)

## Règles

- GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
- Ne pas modifier le live trading
- Ne pas promouvoir lifecycle automatiquement
- Ne pas ajouter de nouvelle stratégie au registry
- Ne pas changer le comportement runtime

## Scope

| Fichier | Rôle |
|---|---|
| `docs/chantiers/GO_.../` | Chantier docs |
| `modules/trading_lab_v1/tests/test_strategy_id_adapter_readonly.py` | Fix pre-existing assertion failure |
| `docs/index/inbox/GO_...md` | Closeout index |
