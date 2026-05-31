---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01_CADRAGE_CHILD
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01
pf_id: PF_BOT_VISION_HEADLESS
status: open
lifecycle_stage: planning
surface: modules/bot_vision
source_kind: canonical
created_at: 2026-05-29
updated_at: 2026-05-29
links:
  - docs/chantiers/GO_OPT_TRADING_COLLECTORS_BOT_VISION_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01/00_SCOPE_AND_OBJECTIVE.md
---

# GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01

## 7_CANONICAL_STATE

```text
OBJECTIF = screenshots -> analyse vision -> donnees structurees -> Data Center -> Telegram / DeskPro
SURFACE = PF_BOT_VISION_HEADLESS + DeskPro input expansion
STATUS = capture mapping non stabilise
```

## 1_MASTER_TARGET

Construire un systeme de capture visuelle capable de maximiser l'output
exploitable depuis TradingView / Coinglass / screeners / charts / indices /
ETF / commodities vers screenshots normalises, analyse par type d'ecran,
signaux structures, ingestion Data Center, alertes Telegram et exploitation
DeskPro.

## 4_MASTER_PROJECT_PLAN

| Bloc | Role |
|---|---|
| `CAPTURE_MAP` | Definir quoi capturer, ou, quand, avec quel layout |
| `SCREEN_TYPE_SCHEMA` | Definir le type d'ecran : chart, liquidity, screener, ETF, macro, news |
| `ANALYSIS_SET` | Definir quelle analyse appliquer a chaque type d'ecran |
| `TRIGGER_ENGINE` | Declencher les captures selon horaire, variation, signal ou evenement |
| `DATA_CENTER_INGESTION` | Stocker image + metadonnees + analyse JSON |
| `TELEGRAM_OUTPUT` | Envoyer uniquement les sorties utiles, filtrees et resumees |
| `DESKPRO_OUTPUT` | Alimenter l'interface / data center avec les resultats longs |

## 5_GO_PLAN

```text
GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_CAPTURE_MAPPING_MAX_OUTPUT_01
GO_STRUCTURAL_ROLE = GO_CHILD_ATTACHED_TO_PARENT
PARENT = PF_BOT_VISION_HEADLESS
FINAL_TARGET = stabiliser le mapping screenshot + analyse + ingestion
```

## 6_FINAL_TARGET

Un plan executable qui dit :

1. quelles pages capturer
2. quels actifs suivre
3. quels indicateurs afficher
4. quels triggers declenchent une capture
5. quel analyseur traiter chaque screenshot
6. quel JSON envoyer au Data Center
7. quel resume envoyer a Telegram

## 17_RESUME_POINT

```text
Reprise depuis PF_BOT_VISION_HEADLESS.
Creer un child GO dedie au mapping de capture maximaliste.
Objectif : passer de screenshots bruts a un systeme structure :
capture -> analyse -> JSON -> Data Center -> Telegram -> DeskPro.
```
