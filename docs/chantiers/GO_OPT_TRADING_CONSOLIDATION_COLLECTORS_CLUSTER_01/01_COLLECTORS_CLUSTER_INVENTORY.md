---
doc_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01_INVENTORY
doc_type: cluster_inventory
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_inventory
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - collectors
  - inventory
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01/01_COLLECTORS_CLUSTER_INVENTORY.md
point_de_reprise: "Inventaire des composants collectors et de leurs roles respectifs."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_COLLECTORS_CLUSTER_01/00_CADRAGE.md
---

# 01_COLLECTORS_CLUSTER_INVENTORY

## 1_DERIVATIVES_COLLECTOR — modules/derivatives_collector/

```text
Role : collecteur derives canonique
Fonctions :
  - collecte OI, funding, liquidations, long/short ratios
  - plusieurs adapters (mock, Coinglass, exchange APIs)
  - exports JSON/CSV + lifecycle compatibility artifacts

Structure :
  - app/derivatives_collector.py
  - app/lifecycle_compat.py
  - app/binance_adapter.py
  - app/bitget_adapter.py
  - config/env.example
  - scripts/cmd/menu/sanity/lifecycle_compat
  - tests/

Statut : anchor canonique de famille deja explicite dans la doctrine.
```

## 2_COLLECTORS_CORE — packages/collectors_core/

```text
Role : fondation runtime partagee pour les nouveaux collecteurs
Boundary explicite :
  - config boundary
  - env/secrets resolution
  - HTTP policy
  - retry / rate limit
  - files / status / timestamps / errors

Structure :
  - src/collectors_core/{config,errors,files,http,timeutil}.py
  - tests/README.md

Statut : hub technique partage, mais pas produit collecteur lui-meme.
```

## 3_COLLECTOR_COINGECKO — modules/collector_coingecko/

```text
Role : collecteur spot CoinGecko pilote valide
Construit sur collectors_core.

Structure :
  - src/collector_coingecko/{cli,client,config,normalize,run}.py
  - config/defaults.toml
  - docs/00_module_plan.txt, 01_runbook.txt
  - outputs/raw normalized snapshots
  - tests/

Statut : satellite spot valide.
```

## 4_COLLECTOR_BINANCE_SPOT — modules/collector_binance_spot/

```text
Role : collecteur spot Binance pilote valide
Construit sur collectors_core.

Structure :
  - src/collector_binance_spot/{cli,client,config,normalize,run}.py
  - config/defaults.toml
  - docs/00_module_plan.txt, 01_runbook.txt
  - outputs/raw normalized snapshots
  - tests/

Statut : satellite spot valide.
```

## 5_MARKETDATA — modules/marketdata/

```text
Role : facade minimale de navigation / wrapper autour de la surface market data
Contenu : __init__.py minimal + scripts/cmd/menu/install_shortcuts/sanity
README : dit explicitement
  - pas de noyau Python riche ici
  - facade legere
  - a clarifier plus tard : rester facade ou etre absorbe

Statut : facade, pas centre de gravite fonctionnel.
```

## 6_RELATIONS DE CODE

```text
collector_coingecko       → importe collectors_core
collector_binance_spot    → importe collectors_core
derivatives_collector     → n'importe pas collectors_core aujourd'hui
marketdata                → pas de couplage runtime, seulement references README
```

## 7_MATRICE DE ROLE

| Surface | Role reel | Statut |
|---|---|---|
| `derivatives_collector` | survivant canonique de famille | CANONIQUE |
| `collectors_core` | hub technique partage | HUB |
| `collector_coingecko` | satellite spot valide | SATELLITE |
| `collector_binance_spot` | satellite spot valide | SATELLITE |
| `marketdata` | facade legere / wrapper | FACADE |

## 8_RESUME

```text
Le cluster collectors n'appelle pas une fusion immediate.
Il appelle une lecture de famille a 4 roles : canonique, hub, satellites, facade.
La doctrine et la migration map existantes confirment deja cette lecture.
```

## RISKS

- À qualifier.
