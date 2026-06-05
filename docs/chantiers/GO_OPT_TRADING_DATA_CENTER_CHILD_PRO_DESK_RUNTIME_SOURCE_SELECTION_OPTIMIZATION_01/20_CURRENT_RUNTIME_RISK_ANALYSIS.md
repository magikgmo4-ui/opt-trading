---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01_CURRENT_RUNTIME_RISK_ANALYSIS
doc_type: risk_analysis
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 20_CURRENT_RUNTIME_RISK_ANALYSIS

## Objet

Identifier les risques si `pro_desk_data_inventory.json` et `source_candidates.json` sont utilises directement dans le runtime entre producers et consumers.

## Risques principaux

| ID | Risque | Impact | Mitigation cible |
|---|---|---|---|
| R01 | Lecture complete des JSON a chaque requete | latence, I/O, CPU | compiled indexes + cache snapshot |
| R02 | Scan lineaire par `data_key` | p95 degrade avec volume | index `by_data_key` |
| R03 | Plusieurs consumers simultanes | contention fichier | snapshot immutable en memoire |
| R04 | Ecriture pendant lecture | JSON partiel ou incoherent | atomic write + version/checksum |
| R05 | Source scoring recalculé trop souvent | CPU inutile | score cache + invalidation controlee |
| R06 | Perte des candidates non selectionnees | audit impossible | `all_candidates` + resolver trace |
| R07 | Score final opaque | confiance artificielle | score vectoriel + reason codes |
| R08 | Freshness globale unique | selection fausse | freshness target par data_key / consumer policy |
| R09 | Units incompatibles | valeur canonique fausse | normalized_value + unit metadata |
| R10 | Consumer contourne Data Center views | divergence | contract tests + path policy |

## Risque critique

Le Data Center peut etre correct conceptuellement mais lent operationnellement si le hot path lit les registries canoniques completes.

## Regle

Les fichiers JSON de production restent la source canonique, mais ne doivent pas etre le format de lookup principal dans le hot path.
