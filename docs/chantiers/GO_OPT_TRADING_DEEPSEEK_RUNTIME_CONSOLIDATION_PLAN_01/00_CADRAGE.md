---
doc_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
topic_keys:
  - opt-trading
  - deepseek
  - runtime
  - consolidation
  - plan
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/00_CADRAGE.md
point_de_reprise: "Planifier la consolidation runtime du cluster DeepSeek avant toute implementation."
updated_at: 2026-05-13
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01/90_CLOSEOUT.md
  - student/README.md
---

# 00_CADRAGE — DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01

## 1_MASTER_TARGET

Produire un plan de consolidation runtime pour le cluster DeepSeek, en documentant l'état existant, la cible, les étapes, les dépendances avec OpenClaw/AI Team/workers, et les gates avant toute implémentation.

## 2_POURQUOI

```text
Le cluster DeepSeek a été consolidé documentairement (PR #252, DEEPSEEK_CLUSTER_01)
mais la consolidation runtime n'a pas été exécutée :
- scripts/student/ = runtime legacy encore actif
- modules/deepseek_student/ = transition incomplete
- modules/deepseek_response/ et thinking/ = satellites de compatibilite
- student/ = workspace canonique declare mais doublons persistants

Le cluster est important car DeepSeek est le moteur IA local du projet,
utilise par OpenClaw, le workflow post_change, et les operateurs.
```

## 3_PERIMETRE

```text
INCLUS :
- etat existant complet
- cible runtime unifiee
- etapes de consolidation
- lien avec OpenClaw / AI Team / workers
- gates de validation
- risques et rollback

EXCLUS :
- implementation runtime
- lancement de modele
- modification de service
- modification /opt/trading
```

## 4_LIVRABLES

```text
docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01/
├── 00_CADRAGE.md
├── 01_EXISTING_STATE.md
├── 02_RUNTIME_CONSOLIDATION_PLAN.md
├── 03_WORKER_AND_AI_TEAM_USAGE.md
├── 04_VALIDATION_GATES.md
└── 90_CLOSEOUT.md
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 service change
- 0 external connection
- 0 secret
```
