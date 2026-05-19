---
doc_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE3_DASHBOARD_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE3_DASHBOARD_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
topic_keys:
  - opt-trading
  - observability
  - dashboard
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE3_DASHBOARD_01/00_CADRAGE.md
point_de_reprise: "Phase 3: dashboard read-only avec JSON, HTML, texte."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE2_01/90_CLOSEOUT.md
---

# 00_CADRAGE — OBSERVABILITY_IMPL_PHASE3_DASHBOARD_01

## 1_MASTER_TARGET

Ajouter un dashboard read-only au module health : agrégation des health checks en matrice lisible, export JSON et HTML statique.

## 2_LIVRÉ

```text
modules/health/scripts/health-dashboard
```

## 3_SORTIES

```text
bash modules/health/scripts/health-dashboard             # texte (matrice)
bash modules/health/scripts/health-dashboard --json      # JSON machine
bash modules/health/scripts/health-dashboard --html      # HTML statique
```

## 4_MATRICE

```text
Par surface : status, severity, staleneness, last_seen, details.
Lecture seule, aucun runtime modifié.
```
