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
point_de_reprise: "Phase 4: circuit breaker dry-run, aucun trip réel."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE3_DASHBOARD_01/90_CLOSEOUT.md
---

# 00_CADRAGE — PHASE4_CIRCUIT_BREAKER_01

## 1_MASTER_TARGET

Implémenter un circuit breaker dry-run : simulation des seuils de déclenchement sans aucune action corrective réelle.

## 2_LIVRÉ

```text
modules/health/scripts/health-breaker
modules/health/README.md (breaker commande)
```

## 3_COMPORTEMENT

```text
- lit health-check --json
- suit compteur d'échecs consécutifs par surface
- seuil 3 → would_trip=true
- surfaces protégées (tradingview, perf, bot_vision) → never_trip
- healthy → reset compteur
- degraded → pas d'incrément
- sortie texte (icônes) + JSON
- état persistant dans _work/health/breaker/
```

## 4_VALIDATION

```text
- python3 health-breaker OK
- JSON valide (json.tool)
- would_trip correct pour surfaces down x3
- protégées marquées would_trip_but_protected
```

## RISKS

- À qualifier.
