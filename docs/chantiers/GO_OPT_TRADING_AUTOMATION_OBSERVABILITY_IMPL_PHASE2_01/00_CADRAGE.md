---
doc_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE2_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE2_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
topic_keys:
  - opt-trading
  - observability
  - alerting
  - telegram
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE2_01/00_CADRAGE.md
point_de_reprise: "Phase 2: health-alert avec Telegram stateful."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE1_01/90_CLOSEOUT.md
---

# 00_CADRAGE — OBSERVABILITY_IMPL_PHASE2_01

## 1_MASTER_TARGET

Ajouter l'alerting Telegram stateful au module health : détection down > 5 min, dedup 30 min, notifications de recovery.

## 2_LIVRÉ

```text
modules/health/scripts/health-alert
modules/health/README.md (mis à jour)
```

## 3_COMPORTEMENT

```text
- run health-check --json
- détecte les surfaces down/degraded
- stocke l'état dans _work/health/{surface}.state
- alerte Telegram si down > 5 min
- dedup : max 1 alerte par surface toutes les 30 min
- alerte recovery quand la surface remonte
- aucun envoi si TELEGRAM_BOT_TOKEN absent
```

## 4_VALIDATION

```text
- syntax OK (bash -n)
- dry-run OK (10 state files créés)
- desk_pro=healthy, perf=down (cohérent avec health-check)
```

## RISKS

- À qualifier.
