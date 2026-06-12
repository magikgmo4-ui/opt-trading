---
doc_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - product-usage
  - atlas
  - consolidation
  - collectors
  - marketdata
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01/00_CADRAGE.md
point_de_reprise: "Consolider la lecture du cluster COLLECTORS sans migration runtime."
updated_at: 2026-05-07
links:
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
  - docs/COLLECTORS_MIGRATION_MAP_01.md
  - docs/chantiers/GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01/02_CONSOLIDATION_PLAN.md
---

# 00_CADRAGE — CONSOLIDATION_COLLECTORS_CLUSTER_01

## 1_MASTER_TARGET

Consolider la lecture du cluster COLLECTORS en fixant :
- le survivant canonique de famille ;
- le hub runtime partage ;
- les satellites spot ;
- le statut exact de `marketdata` ;
- le prochain GO utile sans lancer de migration runtime.

## 2_CONSTAT

```text
Le cluster COLLECTORS se compose de :
  - modules/derivatives_collector/
  - modules/collector_coingecko/
  - modules/collector_binance_spot/
  - packages/collectors_core/
  - modules/marketdata/

Doctrine deja gelee :
  - derivatives_collector = module canonique collecteur derives
  - collectors_core = fondation runtime partagee pour les nouveaux collecteurs
  - collector_coingecko + collector_binance_spot = satellites spot valides
  - marketdata = facade legere, statut strategique encore ouvert
```

## 3_PERIMETRE

```text
INCLUS :
  - inventaire des 5 composants
  - carte des roles et des liens runtime
  - decision documentaire sur survivant / hub / satellites / facade
  - proposition du prochain GO utile

EXCLUS :
  - migration de derivatives_collector vers collectors_core
  - unification de schema spot/derives
  - ajout d'un provider #3
  - refactor runtime large
```

## 4_DECISION CIBLE

```text
Survivant canonique famille : derivatives_collector
Hub runtime partage          : packages/collectors_core
Satellites valides           : collector_coingecko, collector_binance_spot
Facade legere               : marketdata
```

## 12_INVARIANTS

```text
- docs only
- 0 runtime
- 0 migration executee
- 0 refactor broad collectors
- 0 changement de schema spot/derives
- 0 provider #3
- 0 secret
- 0 external connection
```

## 17_RESUME_POINT

```text
COLLECTORS_CLUSTER_01 ouvert.
Objectif : clarifier survivant, hub, satellites, facade.
Pas de migration executee dans ce child.
```

## RISKS

- À qualifier.
