---
doc_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - consolidation
  - deepseek
  - student
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01/00_CADRAGE.md
point_de_reprise: "Consolider la famille DeepSeek autour d'un point d'entree clair sans migration executee."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/02_CONSOLIDATION_PLAN.md
  - student/README.md
  - modules/deepseek_hub/README.md
  - modules/deepseek_student/README.md
---

# 00_CADRAGE — CONSOLIDATION_DEEPSEEK_CLUSTER_01

## 1_MASTER_TARGET

Consolider la lecture du cluster `deepseek*` en fixant :
- le point d'entree canonique ;
- les satellites de compatibilite ;
- les doublons/legacy encore toleres ;
- le prochain GO a ouvrir si une migration physique devient necessaire.

## 2_CONSTAT

```text
Le cluster DEEPSEEK est eclate entre :
  - modules/deepseek_hub/
  - modules/deepseek_student/
  - modules/deepseek_response/
  - modules/deepseek_thinking/
  - scripts/student/
  - student/

Constat cle :
  - deepseek_hub = facade unifiee la plus avancee cote modules/
  - deepseek_student = structure incomplete, pas verite runtime
  - deepseek_response / deepseek_thinking = satellites de compatibilite
  - student/ = workspace canonique declare pour l'operateur student
  - scripts/student/ = legacy runtime encore present comme source de compatibilite
```

## 3_PERIMETRE

```text
INCLUS :
  - inventaire complet du cluster
  - carte des roles, dependances shell, surfaces runtime et compatibilite
  - decision de consolidation documentaire
  - proposition de NEXT_GO separe si migration utile

EXCLUS :
  - deplacer des scripts
  - fusionner des modules
  - changer les raccourcis runtime
  - changer Ollama / workflow / student runtime
  - executer des commandes student
```

## 4_DECISION CIBLE A TESTER DOCUMENTAIREMENT

```text
Point d'entree canonique famille : student/
Facade famille la plus avancee   : deepseek_hub
Satellites compatibilite         : deepseek_response, deepseek_thinking
Transition incomplete            : modules/deepseek_student/
Legacy compatibilite             : scripts/student/
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 migration executee
- 0 deplacement de scripts
- 0 changement de raccourcis
- 0 changement Ollama
- 0 secret
- 0 external connection
```

## 17_RESUME_POINT

```text
DEEPSEEK_CLUSTER_01 ouvert.
Objectif : clarifier survivant, satellites, legacy, et prochain GO.
Pas de migration executee dans ce child.
```
