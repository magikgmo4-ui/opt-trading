---
doc_id: GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01_CONSOLIDATION_MAP
doc_type: consolidation_map
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_consolidation_map
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - vision
  - map
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01/02_VISION_CONSOLIDATION_MAP.md
point_de_reprise: "Carte de consolidation documentaire VISION : paire canonique, compat, legacy, NEXT_GO."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_VISION_CLUSTER_01/01_VISION_CLUSTER_INVENTORY.md
---

# 02_VISION_CONSOLIDATION_MAP

## 1_DECISION DOCUMENTAIRE

```text
Survivant de famille = paire operationnelle, pas module unique :
  - modules/vision_bot/
  - modules/bot_vision_step2/

Legacy conserve en lecture :
  - modules/bot_vision/

Compat capture utile :
  - modules/bot_vision/headless_capture/
```

## 2_POURQUOI

```text
1. vision_bot et bot_vision_step2 se referencent mutuellement comme chaine transitoire valide.
2. bot_vision est explicitement historique dans les README.
3. headless_capture alimente encore la meme inbox, donc reste un composant utile mais non survivant.
4. aucun document ne prouve qu'un module unique a deja remplace les deux etages runtime.
```

## 3_CARTE CIBLE (SANS MIGRATION)

```text
Pair canonique :
  vision_bot          = intake / preprocessing / inbox-outbox
  bot_vision_step2    = analyse / summary / telegram / deskpro

Compat :
  headless_capture    = producer optionnel de captures

Legacy :
  bot_vision_step1    = ancien squelette, a garder en lecture seulement
  bot_vision root     = conteneur historique
```

## 4_CE QUE LE GO CONSOLIDE

```text
- la lecture canonique du cluster
- la paire survivante
- la place du legacy
- la place de headless_capture
```

## 5_CE QUE LE GO NE FAIT PAS

```text
- ne fusionne pas vision_bot et bot_vision_step2
- ne deplace pas headless_capture
- ne touche pas aux unit files
- ne remplace pas ShareX / watchdog
- ne retire pas bot_vision_step1
```

## 6_NEXT_GO RECOMMANDE

```text
GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_PLAN_01
```

Mission :

```text
- evaluer si la paire vision_bot + bot_vision_step2 doit rester paire ou fusionner
- cartographier tous les services, timers et chemins shared_files
- definir si headless_capture reste satellite officiel ou passe archive
- produire rollback plan avant toute migration physique
```

## 7_RISQUES SI ON MIGRE TROP TOT

| Risque | Impact |
|---|---|
| casser vision_inbox / vision_processed | pipeline vision rompu |
| casser timers step2 | perte d'envois Telegram / prune |
| retirer headless_capture trop vite | perte source de capture optionnelle |
| promouvoir bot_vision legacy comme survivant | lecture canonique fausse |

## 17_RESUME_POINT

```text
VISION se consolide autour d'une paire, pas d'un monolithe.
bot_vision = legacy, headless_capture = compat utile.
Tout changement runtime est differe a VISION_RUNTIME_CONSOLIDATION_PLAN_01.
```

## RISKS

- À qualifier.
