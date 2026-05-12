---
doc_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01
topic_keys:
  - opt-trading
  - automation
  - observability
  - health-check
  - alerting
  - dashboard
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/00_CADRAGE.md
point_de_reprise: "Planifier l'observabilité unifiée de toutes les surfaces d'automation."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01

## 1_MASTER_TARGET

Produire un plan d'observabilité unifié pour les 10 surfaces d'automation cartographiées dans la matrice de capacité.

## 2_POURQUOI

```text
Aujourd'hui :
- chaque surface a son propre sanity check (inégal)
- pas de dashboard unifié qui dit "tout va bien" ou "ça casse ici"
- pas d'alerting centralisé
- pas de circuit breaker
- pas de runbook de reprise standardisé

Résultat : on découvre les pannes tard, et on répare au cas par cas.
```

## 3_DIMENSIONS DU PLAN

```text
1. HEALTH CHECK STANDARD
   - contrat minimal par surface
   - périodicité
   - format de sortie (JSON lisible machine + humain)

2. ALERTING
   - canaux (Telegram, log, dashboard)
   - seuils (critical, warning, info)
   - règles de silencing / dedup

3. DASHBOARD UNIFIÉ
   - vue synthétique (matrice vert/jaune/rouge)
   - par surface, par trigger, par dépendance

4. CIRCUIT BREAKER
   - quand couper une surface automatiquement
   - quand reprendre

5. RUNBOOK
   - procédure de reprise standard par surface
```

## 4_LIVRABLES

```text
docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/
├── 00_CADRAGE.md
├── 01_HEALTH_CHECK_CONTRACT.md
├── 02_ALERTING_PLAN.md
├── 03_DASHBOARD_SPEC.md
├── 04_CIRCUIT_BREAKER_RULES.md
└── 90_CLOSEOUT.md
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 service change
- plan seulement, pas d'implémentation
```
