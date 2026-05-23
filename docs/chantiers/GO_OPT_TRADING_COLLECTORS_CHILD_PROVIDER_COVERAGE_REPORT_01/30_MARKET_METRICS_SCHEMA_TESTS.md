---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01_MARKET_METRICS_SCHEMA_TESTS
doc_type: schema_test_spec
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 30_MARKET_METRICS_SCHEMA_TESTS

## Objet

Specification des tests de validation du schema `market_metrics.v1` contre les fixtures decrites dans `20_FIXTURE_MATRIX.md`. Ces tests sont des specs documentees — ils n'executent pas de code dans ce child.

---

## Champs requis — criteres de validation

Un payload `market_metrics.v1` est PASS si tous les champs suivants sont presents et valides :

| Champ | Type | Contrainte |
|---|---|---|
| `contract_version` | string | egal a `"v1"` |
| `input_class` | string | egal a `"market_metrics.v1"` |
| `module_id` | string | non vide |
| `provider_id` | string ou null | non vide si present |
| `symbol` | string | non vide |
| `metrics_ts` | string | format ISO 8601 UTC avec Z |
| `freshness_state` | string | `"fresh"`, `"stale"`, ou `"unknown"` |
| `provider_coverage` | object | voir sous-champs |
| `provider_coverage.status` | string | `"full"`, `"partial"`, `"not_proven_runtime_adapter"`, `"spot_only"` |
| `provider_coverage.collectable_metrics` | list | peut etre vide |
| `provider_coverage.missing_metrics` | list | peut etre vide |
| `metrics` | object | voir sous-champs |
| `metrics.open_interest` | float ou null | null si non prouve |
| `metrics.funding_rate` | float ou null | null si non prouve |
| `metrics.volume_futures` | float ou null | null si non prouve |
| `metrics.long_short_ratio` | float ou null | null si non prouve |
| `metrics.liquidations_long` | float ou null | null si non prouve |
| `metrics.liquidations_short` | float ou null | null si non prouve |
| `refs` | object | voir sous-champs |
| `refs.primary_output` | string | chemin relatif |
| `refs.meta_output` | string | chemin relatif |
| `refs.latest` | string | chemin relatif |
| `refs.status` | string | chemin relatif |
| `warnings` | list | peut etre vide |

---

## Invariants schema

1. Si une metrique est dans `missing_metrics`, sa valeur dans `metrics` doit etre `null`.
2. Si une metrique est dans `collectable_metrics`, sa valeur dans `metrics` ne doit pas etre `null`.
3. `provider_coverage.status = "partial"` implique `missing_metrics` non vide.
4. `provider_coverage.status = "not_proven_runtime_adapter"` implique `collectable_metrics = []` et `metrics.*` tous `null`.
5. Aucune valeur dans `metrics` ne doit etre `0` comme substitut de `null` — `0` est une valeur reelle.

---

## Test cases — Bitget (PARTIAL)

### TC-BITGET-01 : payload partial valide

Input : fixture Bitget de `20_FIXTURE_MATRIX.md`

Assertions :
- `contract_version == "v1"` → PASS
- `input_class == "market_metrics.v1"` → PASS
- `provider_id == "bitget"` → PASS
- `provider_coverage.status == "partial"` → PASS
- `collectable_metrics` contient `["open_interest", "funding_rate", "volume_futures"]` → PASS
- `missing_metrics` contient `["long_short_ratio", "liquidations_long", "liquidations_short"]` → PASS
- `metrics.open_interest == 18234.56` (float, non null) → PASS
- `metrics.long_short_ratio == null` → PASS
- `metrics.liquidations_long == null` → PASS
- `warnings` non vide → PASS

### TC-BITGET-02 : rejet si long_short_ratio non null sans preuve

Input : fixture Bitget avec `metrics.long_short_ratio = 1.5` mais `missing_metrics` contient `long_short_ratio`

Assertion : BLOCKED — invariant 1 viole

### TC-BITGET-03 : rejet si funding_rate absent de collectable_metrics mais non null dans metrics

Input : fixture Bitget avec `funding_rate = 0.0001` mais `funding_rate` absent de `collectable_metrics`

Assertion : BLOCKED — invariant 2 viole

---

## Test cases — Binance Derivatives (PARTIAL)

### TC-BINANCE-DERIV-01 : payload partial valide avec long_short_ratio

Input : fixture Binance Derivatives de `20_FIXTURE_MATRIX.md`

Assertions :
- `provider_id == "binance_derivatives"` → PASS
- `provider_coverage.status == "partial"` → PASS
- `collectable_metrics` contient `long_short_ratio` → PASS
- `metrics.long_short_ratio == 1.8234` (float, non null) → PASS
- `metrics.liquidations_long == null` → PASS
- `missing_metrics` contient `["liquidations_long", "liquidations_short"]` → PASS

### TC-BINANCE-DERIV-02 : liquidations toujours null

Input : fixture Binance Derivatives

Assertion : `metrics.liquidations_long == null` et `metrics.liquidations_short == null` → PASS obligatoire

---

## Test cases — Coinglass (NOT_PROVEN_RUNTIME_ADAPTER)

### TC-COINGLASS-01 : pas de fixture runtime disponible

Status : BLOCKED — aucun adapter reel, aucune fixture executable.

Si un payload Coinglass est recu, il doit satisfaire :
- `provider_coverage.status == "not_proven_runtime_adapter"` → PASS
- `collectable_metrics == []` → PASS
- Tous `metrics.*` == null → PASS

### TC-COINGLASS-02 : rejet si liquidations non nulles sans adapter prouve

Input : payload Coinglass avec `liquidations_long = 123.0`

Assertion : BLOCKED — invariant 4 viole ; Coinglass reste not_proven sans adapter reel

---

## Test cases — Invariants globaux

### TC-INVARIANT-01 : metrics.0 vs null

Input : `metrics.open_interest = 0`

Assertion : PASS (zero est une valeur reelle valide, pas un substitut de null)

### TC-INVARIANT-02 : missing_metrics non vide si status partial

Input : `provider_coverage.status = "partial"` et `missing_metrics = []`

Assertion : BLOCKED — invariant 3 viole

### TC-INVARIANT-03 : freshness_state valeur hors enum

Input : `freshness_state = "expired"`

Assertion : BLOCKED — valeur non dans `["fresh", "stale", "unknown"]`

---

## Verdict schema

| Provider | Schema PASS | Notes |
|---|---|---|
| bitget | OUI (fixture valide) | partial coverage documentee |
| binance_derivatives | OUI (fixture valide) | partial coverage avec long_short_ratio |
| coinglass | BLOCKED | pas d'adapter runtime prouve |
| coingecko | HORS SCOPE | spot uniquement |
| binance_spot | HORS SCOPE | spot uniquement |

**Prochain patch recommande** : voir `40_NEXT_PATCHES.md`.
