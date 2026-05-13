---
doc_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE4_CIRCUIT_BREAKER_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE4_CIRCUIT_BREAKER_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
topic_keys:
  - opt-trading
  - observability
  - circuit-breaker
  - dry-run
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE4_CIRCUIT_BREAKER_01/00_CADRAGE.md
point_de_reprise: "Phase 4: circuit breaker dry-run, aucun trip reel."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE3_DASHBOARD_01/90_CLOSEOUT.md
---

# 00_CADRAGE — PHASE4_CIRCUIT_BREAKER_01

## 1_MASTER_TARGET

Circuit breaker dry-run: simulation des seuils sans action corrective.

## 2_LIVRE

```text
modules/health/scripts/health-breaker
```

## 3_COMPORTEMENT

```text
- compteur d'echecs consecutifs par surface
- seuil 3 -> would_trip
- surfaces protegees -> would_trip_but_protected
- healthy -> reset
- sortie texte + JSON
- etat dans _work/health/breaker/
```
