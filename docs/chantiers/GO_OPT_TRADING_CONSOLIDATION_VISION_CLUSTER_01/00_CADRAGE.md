---
doc_id: GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - consolidation
  - vision
  - bot-vision
  - desk-pro
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01/00_CADRAGE.md
point_de_reprise: "Consolider la lecture du cluster VISION sans migration executee."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/02_CONSOLIDATION_PLAN.md
  - docs/status/bot_vision_canonique.md
---

# 00_CADRAGE — CONSOLIDATION_VISION_CLUSTER_01

## 1_MASTER_TARGET

Consolider le cluster VISION en fixant :
- la paire operationnelle canonique ;
- la place du legacy `bot_vision` ;
- la place des surfaces de capture annexes ;
- le prochain GO a ouvrir si une migration physique devient utile.

## 2_CONSTAT

```text
Le cluster VISION se repartit en 3 blocs :
  - modules/vision_bot/         → intake capture / inbox-outbox processor
  - modules/bot_vision_step2/   → analyse, artefacts Desk Pro, Telegram
  - modules/bot_vision/         → verticale historique (step1 + headless_capture)

Lecture la plus robuste :
  - paire canonique operationnelle = vision_bot + bot_vision_step2
  - bot_vision = legacy / historique / compatibilite
```

## 3_PERIMETRE

```text
INCLUS :
  - inventaire complet des 3 blocs
  - carte des roles et des flux
  - decision de consolidation documentaire
  - proposition de NEXT_GO si migration utile

EXCLUS :
  - deplacer les services systemd
  - changer les chemins sharex / vision_inbox
  - modifier Telegram / OpenAI Vision
  - fusionner les modules
  - executer du runtime
```

## 4_DECISION CIBLE

```text
Pair operationnelle canonique :
  - modules/vision_bot/
  - modules/bot_vision_step2/

Legacy a conserver en lecture :
  - modules/bot_vision/

Sous-surface utile mais non survivante :
  - modules/bot_vision/headless_capture/
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 migration executee
- 0 changement systemd
- 0 changement sharex/watchdog
- 0 secret
- 0 external connection
```

## 17_RESUME_POINT

```text
VISION_CLUSTER_01 ouvert.
Objectif : clarifier paire canonique, legacy, et NEXT_GO.
Pas de migration executee.
```

## RISKS

- À qualifier.
