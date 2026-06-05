---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/BEST_VALUE_RESOLVER_POLICY.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/schemas/source_score.v1.schema.json
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/schemas/source_evidence.v1.schema.json
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/schemas/canonical_value.v1.schema.json
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/schemas/resolver_decision.v1.schema.json
---

# 90_REPRISE_POINT

## 7_CANONICAL_STATE

Child scoring ouvert :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01
```

Role structurel :

```text
GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID = GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
PF_ID = PF_DATA_CENTER
```

## 1_MASTER_TARGET

Schemas et policy de scoring source + best-value resolver specifies et prets a implementer.

## 4_MASTER_PROJECT_PLAN

Termine. Livrables produits :

```text
schemas/source_score.v1.schema.json        — 8 dimensions ponderees
schemas/source_evidence.v1.schema.json     — preuves par dimension
schemas/canonical_value.v1.schema.json     — valeur resolue publiee
schemas/resolver_decision.v1.schema.json   — decision tracee
BEST_VALUE_RESOLVER_POLICY.md              — algorithme 6 etapes + cas concrets
```

## Synthese

```text
SCHEMAS       : 4 JSON Schema (source_score, source_evidence, canonical_value, resolver_decision)
POLICY        : 1 algorithme (6 etapes : identify → score → select → decide → publish → update view)
SEUILS        : 5 parametres (min_score=0.3, max_age=3600s, stale_max_age=86400s, tolerance=5%, decay=0.05)
REGLES        : 8 dimensions de scoring avec formules explicites
CAS CONCRET   : market_metrics.v1 (bitget vs binance) avec 3 scenarios
INTERDITS     : 7 interdits (pas de resolver/scoring dans DeskPro, pas de best value sans decision, etc.)
```

## 12_INVARIANTS

- Aucune modification runtime.
- Aucune modification de code.
- Aucun appel API, DB, Telegram.
- Schemas prets pour implementation dans `BEST_VALUE_RESOLVER_01`.
- Policy exploitable directement par le child suivant.

## 16_TODO

Passer au child suivant :

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01
```

## 17_RESUME_POINT

Reprendre par l'implementation du resolver : appliquer la policy et les schemas pour implementer le best-value resolver sur market_metrics.v1, puis generaliser aux autres contracts multi-source.
