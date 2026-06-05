---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_PRO_DATA_CONSUMPTION_MAP_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_PRO_DATA_CONSUMPTION_MAP_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
BUNDLE_TARGET: DESKPRO_PRO_DATA_CONSUMPTION_MAP_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: null
TRANSPORT_MODE: patch_only
6_FINAL_TARGET: Documenter la map de consommation DeskPro : quelles donnees P0-P21 DeskPro doit consommer depuis les views Data Center, en required / optional / future, avec le statut de chaque reader.
topic_keys:
  - opt-trading
  - data_center
  - deskpro
  - consumption_map
  - pro_desk
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/10_PRO_DESK_DATA_INVENTORY_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/20_EXISTING_DESKPRO_CONSUMERS.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01/PRO_DESK_DATA_GAP_MATRIX.md
  - modules/desk_pro/service/
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_PRO_DATA_CONSUMPTION_MAP_01

## Objet

Documenter la map de consommation DeskPro : quelles donnees P0-P21 DeskPro doit consommer depuis les views Data Center. C'est le dernier child du parent.

## 1_MASTER_TARGET

*(herite du parent)* DeskPro = consumer de views Data Center. Data Center = ingestion + scoring + resolver.

Objectif : formaliser ce que DeskPro consomme (required), pourrait consommer (optional), et consommera (future), pour chaque categorie P0-P21.

## 3_INITIAL_NEED

```text
DeskPro a 6 readers actifs.
4 sont en legacy (non migres vers DC views).
2 sont migres (market_metrics, spot_snapshot).
La gap matrix montre 0/22 categories couvertes, 7 partielles, 15 absentes.
Il faut maintenant dire a DeskPro : voici ce que tu dois lire depuis les views Data Center.
```

## 4_MASTER_PROJECT_PLAN

1. Lister les readers DeskPro existants avec leur statut.
2. Pour chaque categorie P0-P21, qualifier la consommation DeskPro : required / optional / future / absent.
3. Mapper chaque reader vers sa view DC cible.
4. Identifier les migrations encore necessaires.
5. Produire `DESKPRO_PRO_DATA_CONSUMPTION_MAP.md`.

## 6_FINAL_TARGET

```text
DESKPRO_PRO_DATA_CONSUMPTION_MAP_V1
```

Livrable :

```text
DESKPRO_PRO_DATA_CONSUMPTION_MAP.md   — map de consommation DeskPro P0-P21
```

## 7_CANONICAL_STATE

```text
Data Center views → DeskPro readers → DeskPro dashboard
```

DeskPro ne lit que les views Data Center (ou fallback legacy pendant transition). DeskPro ne lit jamais un producer path directement.

## 8_VALIDATED_PLAN

Unique livrable. Dernier child, fermeture du parent ensuite.

## 9_SELECTED_SOLUTION

Une table unique croisant P0-P21 × consommation DeskPro (required/optional/future/absent) × reader × view DC × statut migration.

## 10_SELECTED_SETUP

```text
readers DeskPro    → modules/desk_pro/service/*.py
views DC           → data/data_center/views/
P0-P21 inventory   → parent 10_PRO_DESK_DATA_INVENTORY_PLAN.md
gap matrix         → mapping child PRO_DESK_DATA_GAP_MATRIX.md
```

## 11_KEY_DECISIONS

- Required = donnee indispensable au fonctionnement actuel de DeskPro.
- Optional = donnee utile mais DeskPro fonctionne sans.
- Future = donnee non encore disponible (pas de producer/view) mais ciblee.
- Absent = donnee hors scope DeskPro (ex: compliance, settlement).
- La map est exploitable pour prioriser les migrations et extensions.

## 12_INVARIANTS

- Ne pas modifier runtime.
- DeskPro = consumer only.
- Data Center = source unique pour DeskPro.
- Aucun appel API, DB, Telegram.
- Aucune modification de code.

## 15_REMAINING_GAP

Post consommation map : implementer les migrations identifiees, puis etendre la couverture P0-P21.

## 16_TODO

Produire `DESKPRO_PRO_DATA_CONSUMPTION_MAP.md`. Dernier livrable du parent.

## 17_RESUME_POINT

Reprendre ici : dernier child. Map a produire puis close gate parent.
