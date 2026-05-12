---
doc_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01_ALERTING_PLAN
doc_type: alerting_plan
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01
status: draft_for_review
lifecycle_stage: child_alerting
parent_go_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01
topic_keys:
  - opt-trading
  - observability
  - alerting
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/02_ALERTING_PLAN.md
point_de_reprise: "Plan d'alerting unifié pour les surfaces d'automation."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_OBSERVABILITY_PLAN_01/01_HEALTH_CHECK_CONTRACT.md
---

# 02_ALERTING_PLAN

## 1_CANAUX

```text
Primaire   : Telegram (déjà utilisé par PERF/Bot Vision)
Secondaire : log fichier (tmp/alerts.log)
Futur      : ops_menu_hub (affichage dashboard)
```

## 2_SEUILS

```text
CRITICAL :
  - surface down > 5 min
  - perte de données détectée
  - API externe inaccessible > 15 min
  → Telegram immédiat + log

WARNING :
  - surface degraded (partiel)
  - dernière run trop ancienne
  - espace disque faible
  → log + dashboard

INFO :
  - redémarrage réussi
  - run terminé normalement
  → log uniquement
```

## 3_RÈGLES DE SILENCING

```text
- pas plus d'une alerte CRITICAL par surface toutes les 30 min (dedup)
- si une surface est déjà en CRITICAL, ne pas renvoyer tant que l'état n'a pas changé
- les WARNING ne sont pas répétés avant 2 h
- les INFO sont journalières max
```

## 4_ALERTES EXISTANTES À CONSERVER

```text
PERF :
  - no-activity alert (Telegram, configurable)
  - drawdown alert (Telegram, configurable)

Bot Vision :
  - pas d'alerte active aujourd'hui (à ajouter)
  - alerte si inbox vide > 1 h (optionnel)
  - alerte si step2 error

Desk Pro :
  - pas d'alerte active aujourd'hui (à ajouter)
  - alerte si dernier run échoué
```

## 5_CIBLES PRIORITAIRES

```text
Phase 1 : PERF, TradingView, Bot Vision (déjà partiellement outillés)
Phase 2 : Desk Pro, Collectors
Phase 3 : OpenClaw, DeepSeek
Phase 4 : Repo KG, Bitget Bridge, Ops Menu
```
