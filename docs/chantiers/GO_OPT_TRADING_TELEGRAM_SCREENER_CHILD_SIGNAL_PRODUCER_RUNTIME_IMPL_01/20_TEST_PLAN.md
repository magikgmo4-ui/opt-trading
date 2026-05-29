# 20_TEST_PLAN

## Signal producer tests (`TestSignalProducer`)

| Test | Cible |
|---|---|
| `test_produce_from_trade_setup` | Trade parsé → ScreenerProducedSignal valide |
| `test_produce_from_news` | News parsé → signal news |
| `test_produce_from_alpha` | Alpha parsé → signal alpha |
| `test_produce_sets_produced_at` | produced_at est défini |
| `test_produce_generates_uuid` | id est un uuid4 |
| `test_custom_source` | Source configurable |
| `test_produce_batch_empty` | Liste vide → liste vide |
| `test_produce_batch_multiple` | Plusieurs signaux → batch |
| `test_to_dict_output` | Conversion to_dict() |
| `test_produce_trade_no_sl_tp_low_confidence` | Trade sans SL/TP → LOW |

## Desk Pro adapter tests (`TestDeskProAdapter`)

| Test | Cible |
|---|---|
| `test_adapt_trade_to_telegram_claim` | Trade → telegram_claim.v1 |
| `test_adapt_news_to_telegram_claim` | News → news_alert |
| `test_adapt_alpha_to_telegram_claim` | Alpha → alpha_signal |
| `test_adapt_batch` | Batch adaptation |
| `test_claim_id_format` | Format tg_claim_* |
| `test_confidence_mapping` | HIGH→0.85, MEDIUM→0.60, LOW→0.35 |
| `test_refs_format` | Format telegram:// |

## Critères de succès

- 100% des tests passant
- Aucune dépendance réseau
- Compatible avec le format telegram_claim.v1 existant
