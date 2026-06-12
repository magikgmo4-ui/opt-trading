---
doc_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01_CONSOLIDATION_MAP
doc_type: consolidation_map
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_consolidation_map
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - collectors
  - map
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01/02_COLLECTORS_CONSOLIDATION_MAP.md
point_de_reprise: "Carte de consolidation documentaire COLLECTORS : canonique, hub, satellites, facade."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01/01_COLLECTORS_CLUSTER_INVENTORY.md
  - docs/COLLECTORS_FAMILY_DOCTRINE_01.md
  - docs/COLLECTORS_MIGRATION_MAP_01.md
---

# 02_COLLECTORS_CONSOLIDATION_MAP

## 1_DECISION DOCUMENTAIRE

```text
Canonique famille      : derivatives_collector
Hub technique partage  : collectors_core
Satellites spot        : collector_coingecko, collector_binance_spot
Facade legere          : marketdata
```

## 2_POURQUOI

```text
1. La doctrine 01 le dit explicitement.
2. La migration map 01 interdit toute migration immediate de derivatives_collector vers collectors_core.
3. Les deux collecteurs spot consomment deja collectors_core proprement.
4. marketdata se decrit lui-meme comme facade et non noyau fonctionnel.
```

## 3_CARTE CIBLE (SANS MIGRATION)

```text
Collecteurs derives
  derivatives_collector
    └── reste separe au runtime

Fondation partagee
  collectors_core
    ├── config
    ├── http
    ├── files
    ├── timeutil
    └── errors

Collecteurs spot
  collector_coingecko
  collector_binance_spot
    └── consomment collectors_core

Facade navigation
  marketdata
    └── reste wrapper tant que la famille n'est pas davantage convergee
```

## 4_CE QUE LE GO CONSOLIDE

```text
- la lecture familiale
- la distinction canonique / hub / satellites / facade
- l'interpretation correcte de marketdata
- le prochain GO utile
```

## 5_CE QUE LE GO NE FAIT PAS

```text
- ne deplace pas derivatives_collector vers packages/
- ne deplace pas collectors_core vers modules/
- ne fusionne pas les schemas spot/derives
- n'ajoute pas de provider #3
- ne retire pas marketdata
```

## 6_NEXT_GO RECOMMANDE

```text
GO_COLLECTORS_BASELINE_INVENTORY_01
```

Mission :

```text
- inventory current derivatives_collector wrappers, config, outputs
- inventory runtime concerns duplicated with collectors_core
- inventory downstream consumers depending on current derivatives outputs
- attacher ce baseline aux phases 1-5 de COLLECTORS_MIGRATION_MAP_01
```

## 7_RISQUES SI ON MIGRE TROP TOT

| Risque | Impact |
|---|---|
| forcer derivatives_collector dans collectors_core | casse downstream derives |
| unifier schema spot/derives trop vite | perte de semantics |
| absorber marketdata sans audit callers | perte surface operateur |
| ajouter provider #3 avant convergence | confusion accrue |

## 17_RESUME_POINT

```text
COLLECTORS se consolide en doctrine, pas en refactor runtime.
derivatives_collector reste canonique.
collectors_core reste hub partage des spot collectors.
marketdata reste facade.
Prochain GO : GO_COLLECTORS_BASELINE_INVENTORY_01.
```

## RISKS

- À qualifier.
