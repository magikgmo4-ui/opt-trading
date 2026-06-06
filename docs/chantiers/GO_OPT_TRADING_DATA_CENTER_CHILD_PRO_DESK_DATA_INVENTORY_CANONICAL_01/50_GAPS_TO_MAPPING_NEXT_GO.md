---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01_GAPS_TO_MAPPING_NEXT_GO
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 50_GAPS_TO_MAPPING_NEXT_GO

## Reprise du child precedent

Synthese critique fournie pour `GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01` :

```text
0/22 categories P0-P21 couvertes completement
7 categories partielles
15 categories absentes
7 producers, tous last_write:null
4/6 DeskPro consumers en legacy
pair_market_snapshot view absente
4 producers vision violent la convention <family>/<producer_id>/
market_metrics.v1 a 2 sources sans source scoring
```

## Gaps que ce child transforme en structure canonique

| Gap | Traitement dans ce child |
|---|---|
| P0-P21 non canonise | P0-P21 declares comme data classes |
| Categories partielles non qualifiees | status `partial` conserve jusqu'au mapping |
| Categories absentes | status `absent` conserve jusqu'au mapping |
| Multi-source sans score | source_policy `multi_source_scored` prepare |
| DeskPro legacy | non modifie ; a traiter dans mapping/consumption child |
| View absente | non modifie ; a traiter dans mapping/implementation child |
| Producer path violation | non modifie ; a traiter dans mapping/normalization child |
| last_write:null | qualite/fraicheur a integrer dans P21 |

## NEXT_GO

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01
```

## Objectif du prochain child

Croiser :

```text
P0-P21 canonical inventory
vs producers.json
vs consumers.json
vs views Data Center
vs DeskPro readers
vs legacy paths
vs anomalies A/B/C/D/G
```

## Livrable attendu du prochain child

```text
PRO_DESK_DATA_GAP_MATRIX.md
```

Colonnes minimales :

```text
priority
data_class
field_or_contract
current_status
existing_producer
existing_consumer
existing_view
legacy_path
source_count
source_score_ready
resolver_required
deskpro_use
gap_refs
next_action
```
