---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_TARGET_ID: MT_DATA_CENTER_PRO_DESK_DATA_COVERAGE
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
NEXT_ATTACH_TARGET: null
6_FINAL_TARGET: Canoniser l'inventaire P0-P21 des donnees utilisees par les desks professionnels en registry documentaire exploitable par Data Center, sans implementation runtime ni doublon DeskPro.
BUNDLE_TARGET: PRO_DESK_DATA_INVENTORY_CANONICAL_V1
TRANSPORT_MODE: patch_only
CLOSE_GATE_MASTER_TARGET: not_applicable
topic_keys:
  - opt-trading
  - data_center
  - pro_desk_data
  - canonical_inventory
  - p0_p21
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/10_PRO_DESK_DATA_INVENTORY_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/50_PRELIMINARY_GAPS.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01

## 1_MASTER_TARGET

Rattache au parent `GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01` : construire une checklist canonique Data Center couvrant les donnees utilisees par des desks professionnels reels.

## 2_INITIAL_PROJECT_DOC

Ce fichier est le document initial canonique du child. Il transporte le cadre de canonisation de l'inventaire P0-P21.

## 3_INITIAL_NEED

Le child precedent a etabli :

```text
- 0/22 categories P0-P21 couvertes completement ;
- 7 categories partielles ;
- 15 categories absentes ;
- 7 producers tous last_write:null ;
- 4/6 DeskPro consumers encore legacy ;
- pair_market_snapshot view absente ;
- 4 producers vision hors convention <family>/<producer_id>/ ;
- market_metrics.v1 a 2 sources sans source scoring.
```

Besoin courant : canoniser l'inventaire P0-P21 pour servir de reference stable avant mapping, scoring source et resolver.

## 4_MASTER_PROJECT_PLAN

1. Declarer les 22 categories P0-P21 sans fusion.
2. Definir pour chaque categorie : `data_class`, `priority`, `role`, `required_for`, `candidate_contracts`, `canonical_fields`, `freshness_target`, `source_policy`, `current_coverage_status`.
3. Produire la structure cible des registries documentaires.
4. Distinguer les donnees utiles a DeskPro, Data Center, Strategy, Perf, Telegram, Sheets et Dashboards.
5. Preparer le child suivant : mapping inventaire canonique -> existant/gaps.

## 6_FINAL_TARGET

```text
PRO_DESK_DATA_INVENTORY_CANONICAL_V1
```

## 7_CANONICAL_STATE

Ce child ne modifie pas runtime, producers, consumers, readers, schemas runtime ou index globaux.

L'inventaire produit est une reference de couverture Data Center, pas une structure DeskPro.

## 8_VALIDATED_PLAN

Livrables du child :

```text
10_CANONICAL_SCOPE_AND_RULES.md
20_PRO_DESK_DATA_CLASSES_P0_P21.md
30_REGISTRY_MODEL.md
40_CANONICAL_FIELD_MODEL.md
50_GAPS_TO_MAPPING_NEXT_GO.md
90_REPRISE_POINT.md
```

## 11_KEY_DECISIONS

- P0-P21 restent des categories distinctes.
- Chaque categorie peut produire plusieurs `contract_class`.
- Une donnee peut avoir plusieurs sources candidates.
- Le scoring source n'est pas implemente dans ce child ; il est prepare par le modele documentaire.
- DeskPro n'est pas double.

## 12_INVARIANTS

- Ne pas creer de reader fantome.
- Ne pas ingerer dans DeskPro.
- Ne pas modifier les registry runtime dans ce child.
- Ne pas considerer deux sources equivalentes sans score.
- Ne pas fermer le parent depuis ce child.

## 16_TODO

Produire les fichiers de canonisation P0-P21 puis transmettre au child mapping :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01
```

## 17_RESUME_POINT

Reprendre ici : child ouvert, objectif = convertir l'inventaire desks pro en registry documentaire stable P0-P21.
