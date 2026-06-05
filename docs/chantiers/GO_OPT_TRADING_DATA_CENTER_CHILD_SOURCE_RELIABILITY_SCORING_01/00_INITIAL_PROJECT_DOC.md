---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01
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
BUNDLE_TARGET: SOURCE_RELIABILITY_SCORING_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01
TRANSPORT_MODE: patch_only
6_FINAL_TARGET: Definir les schemas source_score.v1, source_evidence.v1, canonical_value.v1, resolver_decision.v1 et la policy best_value_resolver pour arbitrer market_metrics.v1 (bitget vs binance).
topic_keys:
  - opt-trading
  - data_center
  - source_scoring
  - best_value_resolver
  - schema
  - market_metrics
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/30_SOURCE_SCORING_AND_RESOLVER_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_INVENTORY_MAPPING_01/PRO_DESK_DATA_GAP_MATRIX.md
  - modules/data_center/registry/producers.json
  - modules/data_center/registry/consumers.json
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01

## Objet

Definir les schemas et la policy de scoring source + best-value resolver pour le Data Center. Le cas concret d'application est `market_metrics.v1` (bitget vs binance), seul contract multi-source actif.

## 1_MASTER_TARGET

*(herite du parent)* Construire la couverture Data Center pro-grade avec scoring multi-sources et best-value resolver.

Objectif immediat de ce child : specifier les schemas et la policy. Le runtime (implementation en Python) n'est pas fait ici.

## 3_INITIAL_NEED

```text
market_metrics.v1 a 2 producers (bitget + binance) produisant les memes metriques.
Aucun mecanisme de selection de la meilleure valeur n'existe.
Il faut :
  - un schema de score par source
  - un schema d'evidence (pourquoi ce score)
  - un schema de valeur canonique resolue
  - un schema de decision du resolver (traçabilite)
  - une policy explicite de selection
```

## 4_MASTER_PROJECT_PLAN

1. Specifier `source_score.v1.schema.json`.
2. Specifier `source_evidence.v1.schema.json`.
3. Specifier `canonical_value.v1.schema.json`.
4. Specifier `resolver_decision.v1.schema.json`.
5. Rediger `BEST_VALUE_RESOLVER_POLICY.md` (policy de resolution).
6. Appliquer sur le cas concret market_metrics.v1 (bitget vs binance).

## 6_FINAL_TARGET

```text
SOURCE_RELIABILITY_SCORING_V1
```

Livrables :

```text
schemas/source_score.v1.schema.json        — score d'une source pour une donnee
schemas/source_evidence.v1.schema.json     — preuve du score (pourquoi)
schemas/canonical_value.v1.schema.json     — valeur resolue publiee dans la view
schemas/resolver_decision.v1.schema.json   — decision du resolver (traçabilite)
BEST_VALUE_RESOLVER_POLICY.md              — policy de selection
```

## 7_CANONICAL_STATE

Etat canonique herite :

```text
candidate sources → source_score.v1 → source_evidence.v1 → resolver_decision.v1 → canonical_value.v1 → data/data_center/views/<contract_class>/
```

## 8_VALIDATED_PLAN

Roadmap child :

1. Creer les 4 schemas JSON.
2. Rediger la policy resolver.
3. Appliquer au cas market_metrics bitget vs binance.

## 9_SELECTED_SOLUTION

4 schemas JSON + 1 policy markdown. Doc-only, pas de code. Les schemas sont des specifications pretes a etre implementees dans le child `BEST_VALUE_RESOLVER_01`.

## 10_SELECTED_SETUP

```text
schemas/          → 4 JSON Schema files
policy            → 1 markdown file
cas concret       → market_metrics.v1 bitget vs binance
```

## 11_KEY_DECISIONS

- Le scoring est fait par le Data Center, pas par DeskPro.
- Chaque source recoit un score calcule selon la formule du parent.
- La meilleure valeur est selectionnee par le resolver, pas par le consumer.
- La decision du resolver est tracee (resolver_decision.v1).
- La valeur canonique est publiee dans la view neutre.
- DeskPro continue de lire la view, sans savoir quelle source a gagne.
- Les schemas sont des specifications, pas du code executant.

## 12_INVARIANTS

Herites du parent :

- Ne pas doubler DeskPro.
- Ne pas ingerer dans DeskPro.
- Ne pas faire lire DeskPro dans les producers raw.
- Ne pas publier une best value sans `resolver_decision`.
- Ne pas traiter deux sources comme equivalentes sans score.
- Ne pas modifier runtime.
- Ne pas modifier les index globaux sans consigne explicite.
- Aucun appel API, DB, Telegram.
- Aucune modification de code.

## 13_FORMULE_DE_SCORE

Heritee du parent (`30_SOURCE_SCORING_AND_RESOLVER_PLAN.md`) :

```text
final_score =
   0.20 × source_reliability
 + 0.20 × freshness
 + 0.15 × schema_validation
 + 0.15 × completeness
 + 0.10 × cross_source_consistency
 + 0.10 × historical_accuracy
 + 0.05 × latency
 + 0.05 × permission
```

Chaque dimension est evaluee sur [0, 1]. `final_score` ∈ [0, 1].

## 15_REMAINING_GAP

Post-specification :
- Implementation du resolver en Python.
- Integration avec le pipeline market_metrics existant.
- Tests de scoring multi-source.
- Generalisation a d'autres contracts multi-source futurs.

## 16_TODO

1. Creer les 4 schemas.
2. Rediger la policy.
3. Fermer ce child et passer a `BEST_VALUE_RESOLVER_01`.

## 17_RESUME_POINT

Reprendre ici : child scoring ouvert, branche `go/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01`. Schemas a produire puis passer au resolver.
