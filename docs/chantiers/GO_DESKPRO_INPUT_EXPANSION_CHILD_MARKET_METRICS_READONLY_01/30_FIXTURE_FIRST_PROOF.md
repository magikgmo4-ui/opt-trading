---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01_FIXTURE_PROOF
doc_type: proof
repo: opt-trading
project: opt-trading
module: desk_pro
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_MARKET_METRICS_READONLY_01
created_at: 2026-05-25
updated_at: 2026-05-25
---

# 30_FIXTURE_FIRST_PROOF

## Fixture canonique

```text
tests/fixtures/admin_trading_contract_smoke/market_metrics_v1_minimal.json
```

Contenu :
- `input_class: market_metrics.v1`
- `provider_id: bitget`
- `symbol: BTCUSDT`
- `freshness_state: fresh`
- `provider_coverage.status: full`
- 6/6 métriques présentes et non-null

## Chaîne de preuve

```text
fixture (JSON) → read_market_metrics(path=fixture_path) → List[Metric] non vide
                                                        ↓
                              run_desk_pro_dry_run(..., market_metrics=metrics)
                                                        ↓
                         result["summary"]["market_metrics_present"] == True
                         "market_metrics missing" absent de result["warnings"]
```

## Tests couvrant la preuve

| Test | Fichier | Preuve |
|---|---|---|
| `test_fixture_file_exists` | `test_desk_pro_market_metrics_reader.py` | fixture présente |
| `test_fixture_is_valid_market_metrics_v1` | idem | contrat valide |
| `test_read_market_metrics_from_fixture_returns_non_empty_list` | idem | reader → liste non vide |
| `test_read_market_metrics_from_fixture_covers_6_metrics` | idem | 6/6 métriques |
| `test_market_metrics_present_sets_summary_flag` | `test_desk_pro_dry_run.py` | synthèse intégrée |
| `test_market_metrics_present_removes_missing_warning` | idem | warning absent si présent |

## Tests warning non bloquant

| Test | Fichier | Preuve |
|---|---|---|
| `test_missing_market_metrics_is_warn_non_blocking` | `test_desk_pro_dry_run.py` | WARN, pas FAIL |
| `test_summary_market_metrics_present_false_when_absent` | idem | flag False si absent |
