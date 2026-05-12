---
doc_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01
status: draft_for_review
lifecycle_stage: child_cadrage
topic_keys:
  - opt-trading
  - automation
  - capability-matrix
  - triggers
  - timers
  - webhooks
  - orchestration
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/00_CADRAGE.md
point_de_reprise: "Cartographier toutes les surfaces d'automation actives, leurs triggers, capabilities, limites et gaps."
updated_at: 2026-05-12
links:
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_HELPERS_CLOSEOUT_SYNC_01/01_GLOBAL_CLOSEOUT.md
---

# 00_CADRAGE — GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01

## 1_MASTER_TARGET

Produire une matrice lisible de toutes les surfaces d'automation actives dans `opt-trading` : ce qui tourne, comment c'est déclenché, quelles sont les capacités réelles, les limites documentées, et les gaps vers l'autonomie complète.

## 2_BESOIN

```text
Le projet a accumulé des couches d'automation sans vue unifiée :
- timers systemd
- webhooks TradingView
- pipelines Desk Pro
- agents OpenClaw
- bots Telegram
- watchers vision
- bridges exchange

Il n'existe pas de carte unique qui permette de répondre :
"Qu'est-ce qui tourne en ce moment ?"
"Qu'est-ce qui pourrait tourner mais ne tourne pas ?"
"Qu'est-ce qui ne doit jamais tourner sans supervision ?"
```

## 3_SURFACES À CARTOGRAPHIER

```text
1. Desk Pro Automation    → pipeline timer + orchestrateur
2. Bot Vision             → capture + analyse + Telegram
3. TradingView Pipeline   → webhook → alerte → exécution
4. OpenClaw Runtime       → agent / orchestration / workers
5. DeepSeek Student       → AI reporting / roadmaps
6. PERF Runtime           → tracking / dashboard / alerts
7. Collectors             → market data (derivatives + spot)
8. Repo KG                → graphe de connaissances
9. Simex Bitget Bridge    → pont exchange
10. Ops Menu Hub           → menu opérateur unifié
```

## 4_DIMENSIONS DE LA MATRICE

```text
Pour chaque surface :
- trigger          : timer | webhook | manual | agent | subprocess | cron
- cadence          : fréquence réelle
- state            : active | partial | planned | paused | forbidden
- dependencies     : services / API / tokens requis
- failure_mode     : que se passe-t-il si ça casse ?
- monitoring       : comment sait-on que ça tourne ?
- human_gate       : validation humaine obligatoire ?
- gaps             : ce qui manque pour l'autonomie complète
- do_not_auto      : ce qui ne doit jamais être automatisé
```

## 5_LIVRABLES

```text
docs/chantiers/GO_OPT_TRADING_AUTOMATION_CAPABILITY_MATRIX_01/
├── 00_CADRAGE.md
├── 01_AUTOMATION_MATRIX.md
├── 02_TRIGGER_MAP.md
├── 03_GAPS_AND_RISKS.md
└── 90_CLOSEOUT.md
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 service change
- 0 secret
- cartographier l'existant, pas le modifier
```

## 17_RESUME_POINT

```text
GO ouvert pour cartographier toutes les surfaces d'automation actives.
Vue unifiée triggers / capabilities / gaps / risques.
Aucune modification runtime.
```
