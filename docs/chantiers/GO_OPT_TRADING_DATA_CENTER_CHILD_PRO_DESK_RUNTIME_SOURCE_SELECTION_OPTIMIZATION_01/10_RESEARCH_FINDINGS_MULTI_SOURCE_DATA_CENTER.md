---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01_RESEARCH_FINDINGS
doc_type: research_findings
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_SOURCE_SELECTION_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
---

# 10_RESEARCH_FINDINGS_MULTI_SOURCE_DATA_CENTER

## Objet

Synthese des patterns connus pour un Data Center avec plusieurs producers, plusieurs consumers, plusieurs sources candidates et scoring.

## Patterns pertinents

### 1. Golden record / survivorship

Plusieurs sources peuvent fournir des valeurs differentes pour un meme objet. La pratique robuste consiste a conserver les candidates, appliquer des regles explicites et publier une valeur canonique avec trace.

Application : `canonical_value.v1` doit garder `selected_source`, `selected_value`, `candidate_values` et `selection_reason`.

### 2. Fiabilite par champ

Une source peut etre bonne pour un champ et faible pour un autre. Le scoring doit donc etre rattache a `source_id + data_key + contract_class`, pas seulement a `source_id`.

### 3. Data contracts

Chaque producer et consumer doit declarer schema, fraicheur attendue, fallback, validation, ownership et breaking-change policy.

Application : `source_candidates.json` doit pointer vers producers connus et contract_class valides.

### 4. Couches raw / normalized / views

Separer les sorties producteur, les valeurs normalisees et les vues consumer-ready.

```text
raw/audit producer output
normalized candidate values
consumer views
```

Application : ne pas faire lire DeskPro dans les chemins producteurs.

### 5. Data quality / lineage

La qualite d'une valeur depend de source, timestamp, fraicheur, schema, unite, transformations et corrections.

Application : `lineage`, `freshness`, `score` et `resolver_decision` doivent accompagner les valeurs selectionnees.

## Problemes courants

- contradiction entre sources ;
- timestamps non alignes ;
- units incompatibles ;
- JSON lourd lu dans le hot path ;
- schema drift ;
- sources stale ;
- fallback silencieux ;
- score opaque ;
- perte des candidates rejetees ;
- decisions non reproductibles ;
- consumers qui contournent les views.

## Solutions a retenir

- conserver toutes les candidates ;
- score vectoriel ;
- policy explicite ;
- compiled indexes ;
- cache snapshot versionne ;
- atomic write ;
- append-only resolver decisions ;
- benchmarks de lookup ;
- separation cold path / hot path.
