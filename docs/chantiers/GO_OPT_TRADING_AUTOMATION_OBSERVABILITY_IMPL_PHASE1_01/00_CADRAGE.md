---
doc_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE1_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE1_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
topic_keys:
  - opt-trading
  - observability
  - health-check
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_IMPL_PHASE1_01/00_CADRAGE.md
point_de_reprise: "Implémenter Phase 1 : health check contract + cmd-health local."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/90_CLOSEOUT.md
---

# 00_CADRAGE — OBSERVABILITY_IMPL_PHASE1_01

## 1_MASTER_TARGET

Implémenter Phase 1 du plan d'observabilité : contrat JSON de health check, registry des 10 surfaces, cmd-health local.

## 2_LIVRÉ

```text
modules/health/
├── README.md
└── scripts/
    └── health-check
```

## 3_COMPORTEMENT

```bash
bash modules/health/scripts/health-check              # texte (10 surfaces)
bash modules/health/scripts/health-check --json       # JSON machine
bash modules/health/scripts/health-check perf         # filtre surface
```

## 4_REGISTRY

```text
10 surfaces enregistrées avec leur check natif :
desk_pro, bot_vision, tradingview, openclaw, deepseek,
perf, collectors, repo_kg, bitget_bridge, ops_menu
```

## 5_NON INCLUS (Phase 2+)

```text
- alerting Telegram
- dashboard runtime
- circuit breakers
- restart automatique
- modification /opt/trading
```

## RISKS

- À qualifier.
