---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01
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
BUNDLE_TARGET: BEST_VALUE_RESOLVER_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_PRO_DATA_CONSUMPTION_MAP_01
TRANSPORT_MODE: patch_only
6_FINAL_TARGET: Specifier l'implementation concrete du best-value resolver pour market_metrics.v1 (bitget vs binance), avec plan de test, en utilisant les schemas et la policy definis dans le child scoring.
topic_keys:
  - opt-trading
  - data_center
  - best_value_resolver
  - market_metrics
  - resolver_implementation
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/schemas/source_score.v1.schema.json
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/schemas/source_evidence.v1.schema.json
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/schemas/canonical_value.v1.schema.json
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/schemas/resolver_decision.v1.schema.json
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/BEST_VALUE_RESOLVER_POLICY.md
  - modules/data_center/registry/producers.json
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01

## Objet

Specifier l'implementation concrete du best-value resolver pour `market_metrics.v1` (bitget vs binance), en appliquant la policy et les schemas definis dans le child scoring. Preparer le plan de test avant implementation runtime.

## 1_MASTER_TARGET

*(herite du parent)* Data Center = ingestion + scoring + resolver. DeskPro = consumer de views Data Center.

Objectif immediat : transformer la policy resolver en spec d'implementation exploitable.

## 3_INITIAL_NEED

```text
La policy et les schemas sont definis.
Il faut maintenant specifier comment implementer le resolver :
  - quel module
  - quelle interface
  - quel pipeline d'appel
  - quels tests
  - comment integrer avec les views existantes
```

## 4_MASTER_PROJECT_PLAN

1. Specifier le module `best_value_resolver.py`.
2. Specifier l'interface `resolve(contract_class, symbol, data_key)`.
3. Specifier le pipeline d'appel (collecte → score → select → publish).
4. Specifier le plan de test (scenarios, assertions).
5. Specifier l'integration avec les views existantes.

## 6_FINAL_TARGET

```text
BEST_VALUE_RESOLVER_V1
```

Livrable :

```text
RESOLVER_IMPLEMENTATION_SPEC.md   — spec d'implementation + plan de test
```

## 7_CANONICAL_STATE

```text
candidate sources → source_score.v1 → source_evidence.v1 → resolver_decision.v1 → canonical_value.v1 → data/data_center/views/<contract_class>/
```

## 8_VALIDATED_PLAN

1. Specifier le resolver pour market_metrics.v1.
2. Plan de test pour bitget vs binance.
3. Fermer et passer au dernier child (DeskPro consumption map).

## 9_SELECTED_SOLUTION

Spec doc-only. Pas de code Python execute ici. La spec est prete a etre implementee des que le parent autorise le transport runtime.

## 10_SELECTED_SETUP

```text
module cible        → modules/data_center/resolver/best_value_resolver.py
schemas ref         → child scoring (4 schemas)
policy ref          → child scoring (BEST_VALUE_RESOLVER_POLICY.md)
contract cible      → market_metrics.v1 (bitget + binance)
```

## 11_KEY_DECISIONS

- Le resolver est un module Data Center, pas DeskPro.
- L'interface est `resolve(contract_class, symbol, data_key) → canonical_value.v1`.
- Le resolver utilise les schemas et la policy du child scoring.
- Les scores sont calcules a chaque appel (pas de cache permanent).
- La view canonique est mise a jour atomiquement.
- Les consumers continuent de lire la view, sans changement.

## 12_INVARIANTS

- Ne pas modifier runtime.
- Ne pas modifier les index globaux.
- Aucun appel API, DB, Telegram.
- Aucun code execute.
- Spec prete pour implementation future.

## 15_REMAINING_GAP

- Implementation Python effective.
- Tests unitaires et integration.
- Generalisation a d'autres contracts multi-source.

## 16_TODO

Produire `RESOLVER_IMPLEMENTATION_SPEC.md`.

## 17_RESUME_POINT

Reprendre ici : child resolver ouvert. Spec a produire puis passer a DeskPro consumption map.
