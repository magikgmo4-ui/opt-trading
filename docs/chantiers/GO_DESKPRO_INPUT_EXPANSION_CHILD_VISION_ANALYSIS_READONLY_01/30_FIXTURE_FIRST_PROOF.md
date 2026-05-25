---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01_FIXTURE_FIRST_PROOF
doc_type: fixture_proof
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_VISION_ANALYSIS_READONLY_01
created_at: 2026-05-25
---

# 30_FIXTURE_FIRST_PROOF

## Fixture canonique

**Path** : `tests/fixtures/admin_trading_contract_smoke/vision_analysis_v1_minimal.json`

**Contenu** :
```json
{
  "input_class": "vision_analysis.v1",
  "capture_id": "cap_20260525_000000_BTCUSDT_H1",
  "symbol": "BTCUSDT",
  "timeframe": "H1",
  "analysis_ts": "2026-05-25T00:00:00Z",
  "source_module": "bot_vision_step2",
  "freshness_state": "fresh",
  "signals": [
    {"type": "support_level",    "value": 65000.0, "confidence": 0.85, "note": "horizontal support, multiple touches"},
    {"type": "resistance_level", "value": 68500.0, "confidence": 0.80, "note": "prior high resistance"},
    {"type": "trend_direction",  "value": "bullish","confidence": 0.75, "note": "higher lows pattern"}
  ]
}
```

**Champs prouvés** : `input_class`, `capture_id`, `symbol`, `timeframe`, `analysis_ts`, `source_module`, `freshness_state`, `signals` (3 items)

## Chaîne de preuve

```
fixture → read_vision_analysis(path=fixture) → dry_run synthesis → summary.vision_analysis_present = True
```

## Tests exécutés — 63/63 PASS

### `tests/test_desk_pro_vision_analysis_reader.py` — 10 tests

| Test | Vérification |
|------|-------------|
| `test_fixture_file_exists` | fixture présente sur disque |
| `test_fixture_is_valid_vision_analysis_v1` | `input_class`, `capture_id`, `symbol`, `analysis_ts`, `signals` présents |
| `test_fixture_has_signals` | `len(signals) > 0` |
| `test_read_vision_analysis_from_fixture_returns_dict` | retourne un dict |
| `test_read_vision_analysis_from_fixture_has_correct_class` | `input_class == "vision_analysis.v1"` |
| `test_read_vision_analysis_from_fixture_has_signals` | `len(signals) > 0` via reader |
| `test_returns_none_if_file_absent` | `None` si fichier inexistant |
| `test_returns_none_if_wrong_input_class` | `None` si `input_class` erroné |
| `test_returns_none_if_malformed_json` | `None` si JSON invalide |
| `test_returns_none_if_not_dict` | `None` si liste JSON |

### `tests/test_desk_pro_dry_run.py` — 4 nouveaux tests vision_analysis

| Test | Vérification |
|------|-------------|
| `test_missing_vision_analysis_is_warn_non_blocking` | `status == "WARN"`, warning présent |
| `test_vision_analysis_present_sets_summary_flag` | `summary.vision_analysis_present == True` |
| `test_vision_analysis_present_removes_missing_warning` | pas de warning `"vision_analysis missing"` |
| `test_summary_vision_analysis_present_false_when_absent` | `summary.vision_analysis_present == False` |

## Verdict

**PASS — fixture-first proof complete.**
