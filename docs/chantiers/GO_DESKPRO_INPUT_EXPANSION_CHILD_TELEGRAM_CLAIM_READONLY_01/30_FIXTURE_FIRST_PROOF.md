---
doc_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_TELEGRAM_CLAIM_READONLY_01_FIXTURE_FIRST_PROOF
doc_type: fixture_proof
repo: opt-trading
go_id: GO_DESKPRO_INPUT_EXPANSION_CHILD_TELEGRAM_CLAIM_READONLY_01
created_at: 2026-05-25
---

# 30_FIXTURE_FIRST_PROOF

## Fixture canonique

**Path** : `tests/fixtures/admin_trading_contract_smoke/telegram_claim_v1_minimal.json`

**Contenu** :
```json
{
  "input_class": "telegram_claim.v1",
  "claim_id": "tg_claim_20260525_000000_BTCUSDT",
  "source": "telegram_screener",
  "channel_id": "fixture_channel",
  "message_id": "fixture_message_001",
  "symbol": "BTCUSDT",
  "timeframe": "H1",
  "claim_ts": "2026-05-25T00:00:00Z",
  "claim_type": "trade_context",
  "text": "BTCUSDT testing resistance near 68500",
  "entities": {"direction": "long", "levels": [65000.0, 68500.0], "confidence": 0.72},
  "refs": {"telegram_message_ref": "fixture://telegram/fixture_channel/fixture_message_001"}
}
```

**Champs prouvés** : `input_class`, `claim_id`, `source`, `channel_id`, `message_id`,
`symbol`, `timeframe`, `claim_ts`, `claim_type`, `text`, `entities`, `refs`

## Chaîne de preuve

```
fixture → read_telegram_claim(path=fixture) → dry_run synthesis → summary.telegram_claim_present = True
```

## Tests exécutés — 77/77 PASS

### `tests/test_desk_pro_telegram_claim_reader.py` — 10 tests

| Test | Vérification |
|------|-------------|
| `test_fixture_file_exists` | fixture présente sur disque |
| `test_fixture_is_valid_telegram_claim_v1` | `input_class`, `claim_id`, `symbol`, `claim_ts`, `source` présents |
| `test_fixture_has_entities` | `entities` est un dict avec `direction` |
| `test_read_telegram_claim_from_fixture_returns_dict` | retourne un dict |
| `test_read_telegram_claim_from_fixture_has_correct_class` | `input_class == "telegram_claim.v1"` |
| `test_read_telegram_claim_from_fixture_has_symbol` | `symbol == "BTCUSDT"` |
| `test_returns_none_if_file_absent` | `None` si fichier inexistant |
| `test_returns_none_if_wrong_input_class` | `None` si `input_class` erroné |
| `test_returns_none_if_malformed_json` | `None` si JSON invalide |
| `test_returns_none_if_not_dict` | `None` si liste JSON |

### `tests/test_desk_pro_dry_run.py` — 4 nouveaux tests telegram_claim

| Test | Vérification |
|------|-------------|
| `test_missing_telegram_claim_is_warn_non_blocking` | `status == "WARN"`, warning présent |
| `test_telegram_claim_present_sets_summary_flag` | `summary.telegram_claim_present == True` |
| `test_telegram_claim_present_removes_missing_warning` | pas de warning `"telegram_claim missing"` |
| `test_summary_telegram_claim_present_false_when_absent` | `summary.telegram_claim_present == False` |

## Verdict

**PASS — fixture-first proof complete.**
