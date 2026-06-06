---
doc_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
GO_STRUCTURAL_ROLE: GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
PF_ID: PF_DATA_CENTER
MASTER_TARGET_ID: MT_DATA_CENTER_PRO_DESK_DATA_COVERAGE
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: null
NEXT_ATTACH_TARGET: null
6_FINAL_TARGET: Canoniser l'inventaire complet des donnees utilisees par les desks professionnels, le croiser avec l'existant Data Center/DeskPro, identifier les gaps, puis preparer ingestion multi-sources, source scoring, best-value resolver et consommation DeskPro via views Data Center.
BUNDLE_TARGET: PRO_DESK_DATA_COVERAGE_FOUNDATION_V1
TRANSPORT_MODE: patch_only
CLOSE_GATE_MASTER_TARGET: pending
topic_keys:
  - opt-trading
  - data_center
  - deskpro
  - pro_desk_data
  - source_scoring
  - best_value_resolver
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/20_TARGET_INPUT_CLASSES.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01/00_INITIAL_PROJECT_DOC.md
  - modules/data_center/registry/producers.json
  - modules/data_center/registry/consumers.json
---

# GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01

## 1_MASTER_TARGET

Construire une couche `PF_DATA_CENTER` pro-grade capable de couvrir les donnees utilisees par des desks professionnels reels, sans doubler DeskPro.

```text
Desk professionnel reel
-> inventaire complet des donnees utiles
-> Data Center opt-trading
-> scoring des sources
-> resolution meilleure donnee
-> views contractuelles
-> DeskPro / Strategy / Perf / Telegram / Sheets / Dashboards
```

## 2_INITIAL_PROJECT_DOC

Ce fichier est le document initial canonique du parent. Il transporte le plan complet valide au demarrage et doit rester stable sauf changement explicite ou implicite du projet.

## 3_INITIAL_NEED

L'utilisateur a valide le besoin suivant :

```text
Valider l'existant, canoniser, ne pas doubler DeskPro, ingerer les donnees dans Data Center, faire utiliser a DeskPro le schema complet comme guide/checklist, permettre plusieurs sources par donnee avec score de fiabilite, selectionner la valeur au meilleur score lors d'une requete Data Center, puis construire la couverture Data Center et les gaps/manquants avant de balancer vers DeskPro.
```

## 4_MASTER_PROJECT_PLAN

1. Auditer l'existant Data Center / DeskPro.
2. Canoniser l'inventaire complet P0-P21 des donnees de desks professionnels.
3. Mapper l'inventaire pro vers les contracts, producers, consumers et views existants.
4. Produire une gap matrix : existant, partiel, absent, legacy, doublon, a migrer.
5. Definir `source_score.v1`, `source_evidence.v1`, `canonical_value.v1`, `resolver_decision.v1`.
6. Definir la policy Data Center `best_value_resolver`.
7. Etendre les views Data Center sans faire lire DeskPro dans les producer paths.
8. Documenter la consumption map DeskPro : required, optional, future.

## 6_FINAL_TARGET

```text
PRO_DESK_DATA_COVERAGE_FOUNDATION_V1
```

Livrable cible du parent : une fondation documentaire permettant d'ouvrir ensuite les child GO d'audit, inventaire canonique, mapping, scoring source, resolver et consumption map DeskPro.

## 7_CANONICAL_STATE

Etat canonique a respecter :

```text
data/data_center/<family>/<producer_id>/ = ecriture producteur / audit
data/data_center/views/<contract_class>/ = lecture consommateur
data/data_center/_registry/ = status / registry / health
```

DeskPro reste consumer. Data Center reste ingestion/resolution. Les donnees multi-sources sont arbitrees par Data Center, pas par DeskPro.

## 8_VALIDATED_PLAN

Roadmap validee :

1. `GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01`
2. `GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01`
3. `GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01`
4. `GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01`
5. `GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01`
6. `GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_PRO_DATA_CONSUMPTION_MAP_01`

## 9_SELECTED_SOLUTION

```text
PRO_DESK_DATA_INVENTORY
-> DATA_CENTER_DATA_CHECKLIST
-> PRODUCERS
-> RAW/AUDIT PRODUCER PATHS
-> SOURCE SCORING
-> BEST_VALUE_RESOLVER
-> DATA_CENTER VIEWS
-> CONSUMERS
-> DESKPRO / STRATEGY / PERF / TELEGRAM / SHEETS / DASHBOARDS
```

## 10_SELECTED_SETUP

Le parent documente la structure. Les child GO produiront les docs et schemas. Aucun runtime n'est modifie dans ce parent.

## 11_KEY_DECISIONS

- L'inventaire pro complet devient une checklist Data Center.
- Data Center ingere, score, resout et publie.
- DeskPro consomme les views Data Center.
- Une donnee peut avoir plusieurs sources.
- Chaque source peut avoir un score different.
- La valeur utilisee est la meilleure valeur resolue, pas une source brute arbitraire.
- La decision du resolver doit etre tracable.
- L'audit existant vient avant les nouveaux schemas.

## 12_INVARIANTS

- Ne pas doubler DeskPro.
- Ne pas ingerer dans DeskPro.
- Ne pas faire lire DeskPro dans les producers raw.
- Ne pas creer de reader fantome.
- Ne pas fusionner les categories P0-P21.
- Ne pas traiter deux sources comme equivalentes sans score.
- Ne pas publier une best value sans `resolver_decision`.
- Ne pas modifier runtime dans ce parent.

## 15_REMAINING_GAP

- Inventaire P0-P21 non encore canonise dans le repo.
- Mapping complet inventaire pro -> existant non encore produit.
- `source_score.v1` absent.
- `best_value_resolver` absent.
- Gap matrix Data Center/DeskPro a produire.

## 16_TODO

Ouvrir le premier child GO :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01
```

## 17_RESUME_POINT

Reprendre ici : parent ouvert, plan valide, prochaine action = audit doc-only de l'existant pour eviter les doublons avant source scoring/resolver.
