---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01_RESOLVER_IMPLEMENTATION_SPEC
doc_type: implementation_spec
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BEST_VALUE_RESOLVER_01
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
  - modules/data_center/registry/producers.json
---

# RESOLVER_IMPLEMENTATION_SPEC

## Objet

Spec d'implementation concrete du best-value resolver pour `market_metrics.v1`. Cette spec est exploitable directement pour coder `modules/data_center/resolver/best_value_resolver.py`.

## 1. Module cible

```text
modules/data_center/resolver/best_value_resolver.py
```

Fonction principale :

```python
def resolve(
    contract_class: str,
    symbol: str,
    data_key: str,
    *,
    min_score_threshold: float = 0.3,
    max_age_seconds: int = 3600,
) -> dict:  # canonical_value.v1
```

## 2. Pipeline d'appel

```text
resolve("market_metrics.v1", "BTCUSDT", "open_interest")
    │
    ├── 1. _list_candidates(contract_class, symbol, data_key)
    │       └── lit producers.json → filtre par contract_class
    │           lit chaque producer path → verifie donnee dispo
    │
    ├── 2. _score_candidate(producer, symbol, data_key)
    │       └── calcule source_score.v1 (8 dimensions)
    │           produit source_evidence.v1
    │
    ├── 3. _select_best(candidates, min_score_threshold)
    │       └── filtre eligibles
    │           selectionne highest_score > only_eligible > stale_fallback
    │
    ├── 4. _build_decision(candidates, selected, selection_rule)
    │       └── produit resolver_decision.v1
    │
    └── 5. _publish_canonical(contract_class, symbol, data_key, selected, decision)
            └── ecrit canonical_value.v1 dans view path
```

## 3. Donnees d'entree par producer

Pour `market_metrics.v1`, les producers produisent :

```text
derivatives_collector__bitget:
  path: data/data_center/derivatives/derivatives_collector__bitget/latest.json
  contract_class: market_metrics.v1
  collectable_metrics: open_interest, funding_rate, volume_futures, long_short_ratio, liquidations_long, liquidations_short

derivatives_collector__binance:
  path: data/data_center/derivatives/derivatives_collector__binance/latest.json
  contract_class: market_metrics.v1
  collectable_metrics: open_interest, funding_rate, volume_futures, long_short_ratio, liquidations_long, liquidations_short
```

Le resolver lit `data[key]` depuis le champ `metrics` du payload market_metrics.v1.

## 4. Scoring concret

### 4.1 source_reliability (0.20)

```python
def _score_reliability(producer):
    if producer.last_write is None:
        return 0.5   # jamais execute, neutre
    consecutive_failures = _count_consecutive_failures(producer)
    return max(0.1, 1.0 - consecutive_failures / 10)
```

### 4.2 freshness (0.20)

```python
def _score_freshness(payload, max_age_seconds):
    produced_at = parse_iso(payload["produced_at"])
    age_seconds = (utcnow() - produced_at).total_seconds()
    if age_seconds <= max_age_seconds / 2:
        return 1.0
    return max(0.1, 1.0 - age_seconds / max_age_seconds)
```

### 4.3 schema_validation (0.15)

```python
def _score_schema(payload, contract_class):
    errors = validate_against_schema(payload, contract_class)
    if not errors:
        return 1.0
    if all(e.severity == "warning" for e in errors):
        return 0.8
    return 0.0
```

### 4.4 completeness (0.15)

```python
def _score_completeness(payload, producer):
    metrics_present = sum(1 for k in producer.collectable_metrics if k in payload["metrics"] and payload["metrics"][k] is not None)
    return metrics_present / len(producer.collectable_metrics)
```

### 4.5 cross_source_consistency (0.10)

```python
def _score_consistency(value, peer_values, tolerance_pct=5.0):
    if not peer_values:
        return 0.5
    consistent = 0
    for pv in peer_values:
        denom = max(abs(value), abs(pv), 1)
        deviation = abs(value - pv) / denom
        if deviation <= tolerance_pct / 100:
            consistent += 1
    return consistent / (len(peer_values) + 1)
```

### 4.6 historical_accuracy (0.10)

```python
def _score_historical(producer, data_key):
    history = _load_accuracy_history(producer, data_key)
    if not history or history.samples < 5:
        return 0.5  # neutre
    return max(0.0, 1.0 - history.mean_relative_error)
```

### 4.7 latency (0.05)

```python
def _score_latency(payload):
    total_ms = payload.get("collection_duration_ms", 0) + payload.get("pipeline_duration_ms", 0)
    return max(0.1, 1.0 - total_ms / 60000)
```

### 4.8 permission (0.05)

```python
def _score_permission(producer):
    if not producer.api_key_valid:
        return 0.0
    return 1.0 if producer.entitlement == "full" else 0.5
```

## 5. Selection

```python
def _select_best(candidates, min_score_threshold):
    eligible = [c for c in candidates if c.score >= min_score_threshold and c.permission_ok and c.schema_valid]

    if not eligible:
        return _stale_fallback(candidates)

    if len(eligible) == 1:
        return eligible[0], "only_eligible"

    # highest_score, tie-break by freshness then reliability
    eligible.sort(key=lambda c: (c.score, c.freshness_value, c.reliability_value), reverse=True)
    return eligible[0], "highest_score"
```

## 6. Stockage des artefacts

```text
data/data_center/scores/<producer_id>/<contract_class>/<symbol>/<data_key>/
    source_score.json       # source_score.v1
    source_evidence.json    # source_evidence.v1

data/data_center/resolver/<contract_class>/<symbol>/
    resolver_decision.json  # resolver_decision.v1 (latest)

data/data_center/views/<contract_class>/by_symbol/<symbol>.json  # canonical_value.v1
data/data_center/views/<contract_class>/latest.json               # aggregation multi-symbol
```

## 7. Plan de test

### 7.1 Test unitaire — scoring dimensions

| Test ID | Description | Expected |
|---|---|---|
| T01 | source_reliability avec last_write=null | 0.5 |
| T02 | source_reliability avec 0 failures | >= 0.9 |
| T03 | source_reliability avec 5 failures | 0.5 |
| T04 | freshness age=30s, max_age=3600 | 1.0 |
| T05 | freshness age=2700s, max_age=3600 | ~0.25 |
| T06 | schema valide sans erreur | 1.0 |
| T07 | schema valide avec warnings | 0.8 |
| T08 | schema invalide | 0.0 |
| T09 | completeness 6/6 metriques | 1.0 |
| T10 | completeness 3/6 metriques | 0.5 |
| T11 | consistency 2 sources identiques (±1%) | ~1.0 |
| T12 | consistency 2 sources divergentes (±20%) | ~0.0 |
| T13 | consistency 0 peers | 0.5 |
| T14 | historical_accuracy avec 100 samples, error 2% | 0.98 |
| T15 | historical_accuracy <5 samples | 0.5 |
| T16 | latency 500ms | ~0.99 |
| T17 | latency 30s | 0.5 |
| T18 | latency >60s | 0.1 |
| T19 | permission full | 1.0 |
| T20 | permission expired | 0.0 |

### 7.2 Test integration — scenarios resolver

| Test ID | Scenario | Expected |
|---|---|---|
| I01 | bitget score 0.87, binance score 0.72, both eligible | Selected: bitget, rule: highest_score |
| I02 | bitget eligible, binance score <0.3 (ineligible) | Selected: bitget, rule: only_eligible |
| I03 | bitget last_write=null, binance last_write=null | Selected: None, rule: stale_fallback, stale: true |
| I04 | bitget schema invalide, binance OK | Selected: binance, disqualified: bitget |
| I05 | bitget + binance scores egaux (0.80), bitget plus frais | Selected: bitget (freshness tie-break) |
| I06 | bitget + binance scores + freshness egaux, bitget fiabilite > | Selected: bitget (reliability tie-break) |
| I07 | 0 producteurs pour le contract_class | Empty result, rule: stale_fallback |
| I08 | 1 producteur eligible, pas de peer | Selected: seul candidat, consistency neutre 0.5 |

### 7.3 Test integration — pipeline complet

| Test ID | Description |
|---|---|
| P01 | resolve("market_metrics.v1", "BTCUSDT", "open_interest") → canonical_value.v1 valide |
| P02 | canonical_value.v1 ecrit dans views/market_metrics/by_symbol/BTCUSDT.json |
| P03 | resolver_decision.v1 publie avec session_id |
| P04 | source_score + source_evidence ecrits pour chaque candidat |
| P05 | DeskPro market_metrics_reader lit la canonical_value sans changement |

## 8. Ordre d'implementation

1. `_list_candidates` — lecture producers.json + donnees disque
2. `_score_candidate` — 8 fonctions de scoring
3. `_select_best` — logique de selection + tie-breaks
4. `_build_decision` — production resolver_decision.v1
5. `_publish_canonical` — ecriture dans la view
6. `resolve` — orchestration du pipeline
7. Tests unitaires T01-T20
8. Tests integration I01-I08
9. Tests pipeline P01-P05

## 9. Interdits

- Pas d'appel API externe (Binance, Bitget) depuis le resolver.
- Pas de modification des producers existants.
- Pas de modification des consumers existants.
- Pas de scoring dans DeskPro.
- Pas de lecture directe de producer path par DeskPro.
