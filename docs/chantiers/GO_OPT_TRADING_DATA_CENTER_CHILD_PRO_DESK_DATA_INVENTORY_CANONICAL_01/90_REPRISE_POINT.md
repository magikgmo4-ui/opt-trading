---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 90_REPRISE_POINT

## 7_CANONICAL_STATE

Child ouvert :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
```

Rattachement :

```text
PARENT_GO_ID = GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
PF_ID = PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID = MPP_DATA_CENTER_NORMALIZED_REGISTRY
```

## 1_MASTER_TARGET

Transformer l'inventaire complet des donnees de desks professionnels en registry documentaire P0-P21 pour guider Data Center.

## 4_MASTER_PROJECT_PLAN

1. Conserver P0-P21 comme categories distinctes.
2. Declarer les data classes et candidate contracts.
3. Definir le modele registry documentaire.
4. Definir le modele de champs canonique.
5. Transmettre au prochain child mapping.

## 13_ESTABLISHED

- Le child audit precedent est pris comme input declare par l'utilisateur.
- 0/22 categories sont completement couvertes.
- 7/22 sont partielles.
- 15/22 sont absentes.
- `market_metrics.v1` a deja plusieurs sources mais sans source scoring.
- DeskPro ne doit pas etre double.

## 15_REMAINING_GAP

- Le registry JSON documentaire n'est pas encore materiellement cree dans `modules/data_center/registry/`.
- Le mapping P0-P21 -> existant n'est pas encore produit.
- Les anomalies A/B/C/D/G ne sont pas encore rattachees ligne par ligne aux classes P0-P21.
- `source_score.v1` et `best_value_resolver` restent pour les child suivants.

## 16_TODO

Prochain child :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01
```

## 17_RESUME_POINT

Reprendre par la creation de `PRO_DESK_DATA_GAP_MATRIX.md`, en croisant l'inventaire P0-P21 avec producers, consumers, views, readers, legacy paths et anomalies du child audit.
