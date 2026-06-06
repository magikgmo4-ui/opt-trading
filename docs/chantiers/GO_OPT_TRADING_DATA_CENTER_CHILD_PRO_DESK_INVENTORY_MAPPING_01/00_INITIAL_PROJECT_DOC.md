---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01
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
BUNDLE_TARGET: PRO_DESK_INVENTORY_MAPPING_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01
TRANSPORT_MODE: patch_only
6_FINAL_TARGET: Produire la gap matrix croisant l'inventaire canonique P0-P21 avec l'existant reel (producers, consumers, views, readers, legacy paths) et les anomalies auditees, pour definir precisement les gaps avant scoring source.
topic_keys:
  - opt-trading
  - data_center
  - deskpro
  - pro_desk
  - inventory_mapping
  - gap_matrix
  - P0_P21
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/10_PRO_DESK_DATA_INVENTORY_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/10_EXISTING_DATA_CENTER_SURFACES.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/20_EXISTING_DESKPRO_CONSUMERS.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/30_EXISTING_PRODUCERS_AND_CONTRACTS.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/40_EXISTING_VIEWS_AND_PATHS.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/50_PRELIMINARY_GAPS.md
  - modules/data_center/registry/producers.json
  - modules/data_center/registry/consumers.json
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01

## Objet

Produire la gap matrix canonique croisant l'inventaire P0-P21 (parent) avec tout l'existant audite (child audit). Cette matrix devient la reference unique pour savoir ce qui est couvert, partiel, absent, et quel producer/consumer/view/reader/legacy path est implique par categorie.

## 1_MASTER_TARGET

*(herite du parent)* Construire la couverture Data Center pro-grade des donnees utilisees par des desks professionnels.

Objectif immediat de ce child : mapper l'inventaire canonique P0-P21 sur chaque surface existante pour produire une gap matrix exploitable par les childs suivants (scoring source, resolver, DeskPro consumption map).

## 3_INITIAL_NEED

L'audit a revele 0/22 categories couvertes, 7 partielles, 15 absentes. Le besoin est maintenant de formaliser cette gap matrix de maniere exploitable : chaque categorie P0-P21 doit etre croisee avec les producers, consumers, views, readers, legacy paths et anomalies correspondants.

## 4_MASTER_PROJECT_PLAN

1. Recharger l'inventaire canonique P0-P21 du parent.
2. Recharger l'audit existant (child audit : 10_ a 50_).
3. Pour chaque categorie P0-P21, mapper :
   - Producers existants (producer_id, contract_class)
   - Consumers existants (consumer_id, contract_class, access_pattern)
   - Views DC existantes (path, status)
   - Readers DeskPro (path, migration status)
   - Legacy paths (path, existence)
   - Anomalies associees (IDs A01-G08)
4. Qualifier chaque categorie : COUVERT, PARTIEL, ABSENT.
5. Pour les PARTIEL, lister precisement ce qui manque.
6. Produire `PRO_DESK_DATA_GAP_MATRIX.md`.

## 6_FINAL_TARGET

```text
PRO_DESK_INVENTORY_MAPPING_V1
```

Livrable :

```text
PRO_DESK_DATA_GAP_MATRIX.md   — matrix P0-P21 croisee avec toutes les surfaces
```

## 7_CANONICAL_STATE

Etat canonique herite :

```text
data/data_center/<family>/<producer_id>/ = ecriture producteur / audit
data/data_center/views/<contract_class>/ = lecture consommateur
data/data_center/_registry/ = status / registry / health
```

## 8_VALIDATED_PLAN

1. Charger l'inventaire P0-P21 (parent `10_PRO_DESK_DATA_INVENTORY_PLAN.md`).
2. Charger l'audit (child `10_` a `50_` + anomalies A01-G08).
3. Produire la matrix : P vs producers, consumers, views, readers, legacy, anomalies.
4. Synthetiser les gaps par bloc de remediation.

## 9_SELECTED_SOLUTION

Une matrix unique croisant toutes les dimensions. Chaque ligne = une categorie P0-P21. Chaque colonne = une surface (producer, consumer, view, reader, legacy, anomalies). Chaque cellule = etat qualifie (present/absent/partiel/legacy).

## 10_SELECTED_SETUP

Sources croisees :

```text
P0-P21 inventory        → docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/10_PRO_DESK_DATA_INVENTORY_PLAN.md
Existing surfaces       → child audit 10_EXISTING_DATA_CENTER_SURFACES.md
DeskPro consumers       → child audit 20_EXISTING_DESKPRO_CONSUMERS.md
Producers & contracts   → child audit 30_EXISTING_PRODUCERS_AND_CONTRACTS.md
Views & paths           → child audit 40_EXISTING_VIEWS_AND_PATHS.md
Preliminary gaps        → child audit 50_PRELIMINARY_GAPS.md
Registry                → modules/data_center/registry/producers.json / consumers.json
Readers DeskPro         → modules/desk_pro/service/*.py
```

## 11_KEY_DECISIONS

- P0-P21 restent distinctes, aucune fusion.
- Une categorie est COUVERT si elle a au moins un producer actif ET un consumer actif ET une view DC presente.
- Une categorie est PARTIELLE si elle a un producer ou consumer partiel, ou si le contrat existe mais la view est absente.
- Une categorie est ABSENTE si aucun producer, aucun consumer, aucun contract n'existe.
- Les anomalies auditees sont referencees par ID, pas dupliquees.
- Le scoring source n'est pas implemente ici — il est prepare par cette matrix.
- La matrix est exploitable directement par le child `SOURCE_RELIABILITY_SCORING_01`.

## 12_INVARIANTS

Herites du parent :

- Ne pas doubler DeskPro.
- Ne pas ingerer dans DeskPro.
- Ne pas faire lire DeskPro dans les producers raw.
- Ne pas creer de reader fantome.
- Ne pas modifier runtime.
- Ne pas modifier les index globaux sans consigne explicite.
- Aucun appel API, DB, Telegram.
- Aucune modification de code.

## 15_REMAINING_GAP

Post-mapping, les gaps seront classes par priorite de remediation (infrastructure > migration DeskPro > multi-source scoring > extension P0-P21).

## 16_TODO

Produire `PRO_DESK_DATA_GAP_MATRIX.md` puis fermer ce child et passer au scoring source.

## 17_RESUME_POINT

Reprendre ici : child mapping ouvert, branche `go/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01`. Livrable a produire : `PRO_DESK_DATA_GAP_MATRIX.md`.
