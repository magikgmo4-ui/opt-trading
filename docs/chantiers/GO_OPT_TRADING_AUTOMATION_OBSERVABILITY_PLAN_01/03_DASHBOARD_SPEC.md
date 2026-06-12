---
doc_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01_DASHBOARD_SPEC
doc_type: dashboard_spec
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
status: draft_for_review
lifecycle_stage: child_dashboard
parent_go_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01
topic_keys:
  - opt-trading
  - observability
  - dashboard
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/03_DASHBOARD_SPEC.md
point_de_reprise: "Spécification du dashboard d'observabilité unifié."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/01_HEALTH_CHECK_CONTRACT.md
---

# 03_DASHBOARD_SPEC

## 1_VUE SYNTHÉTIQUE

```text
Matrice 10 surfaces × status :
  🟢 healthy
  🟡 degraded
  🔴 down
  ⚪ unknown

Affichage terminal + option JSON/HTML.
```

## 2_FORMAT CIBLE

```text
=== AUTOMATION HEALTH ===
Desk Pro        🟢 healthy   last_run=2026-05-12T08:00Z success
Bot Vision      🟢 healthy   vision_bot=active step2=active
TradingView     🟢 healthy   listener=8010
OpenClaw        🟡 degraded  ping=timeout
DeepSeek        🟢 healthy   last_report=2026-05-12T06:00Z
PERF            🟢 healthy   /perf/summary=OK DB=OK
Collectors      🟢 healthy   derivatives=fresh coingecko=fresh
Repo KG         ⚪ unknown   no recent check
Bitget Bridge   🟢 healthy   sanity=PASS
Ops Menu        🟢 healthy   shortcuts=OK
```

## 3_COMMANDES ENVISAGÉES

```bash
cmd-health          # vue synthétique
cmd-health --json   # sortie JSON machine
cmd-health --html   # sortie HTML dashboard
cmd-health desk_pro # zoom sur une surface
```

## 4_INTÉGRATION AVEC L'EXISTANT

```text
- chaque surface expose déjà un sanity_* ou status endpoint
- le dashboard agrége ces sorties sans les remplacer
- ops_menu_hub peut intégrer la vue health dans son menu
- PERF /perf/ui peut embarquer le dashboard health
```

## RISKS

- À qualifier.
