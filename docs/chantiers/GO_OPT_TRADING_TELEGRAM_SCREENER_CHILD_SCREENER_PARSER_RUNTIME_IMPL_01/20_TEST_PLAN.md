# 20_TEST_PLAN

## Tests unitaires

| Test | Cible |
|---|---|
| `TestTradeParser::test_valid_trade_setup_basic` | Trade setup simple → signal normalisé |
| `TestTradeParser::test_valid_trade_setup_with_sl_tp` | Trade avec SL+TP → HIGH confidence |
| `TestTradeParser::test_valid_trade_setup_with_size` | Trade avec SIZE |
| `TestTradeParser::test_trade_setup_sl_only_medium_confidence` | SL only → MEDIUM confidence |
| `TestTradeParser::test_invalid_format_returns_none` | Format invalide → None |
| `TestTradeParser::test_empty_string_returns_none` | Chaîne vide → None |
| `TestTradeParser::test_case_insensitive` | Case insensitive pair/direction |
| `TestTradeParser::test_source_channel_propagated` | Source channel conservé |
| `TestTradeParser::test_timestamp_propagated` | Timestamp conservé |
| `TestTradeParser::test_large_price_with_commas` | Prix avec virgules |
| `TestTradeParser::test_to_dict_output` | Conversion to_dict() |
| `TestTradeParser::test_fixture_samples_all_parse` | Tous les samples trade |
| `TestNewsParser::test_valid_news_alert` | News bien formée |
| `TestNewsParser::test_alert_category` | Catégorie ALERT |
| `TestNewsParser::test_economic_category` | Catégorie ECONOMIC |
| `TestNewsParser::test_invalid_format_returns_none` | Format invalide → None |
| `TestNewsParser::test_fixture_samples_all_parse` | Tous les samples news |
| `TestAlphaParser::test_valid_alpha_signal` | Alpha bien formé |
| `TestAlphaParser::test_crypto_ticker` | Ticker crypto |
| `TestAlphaParser::test_invalid_format_returns_none` | Format invalide → None |
| `TestAlphaParser::test_ticker_too_long_returns_none` | Ticker trop long |
| `TestAlphaParser::test_fixture_samples_all_parse` | Tous les samples alpha |
| `TestSignalNormalizer::test_normalize_trade_signal` | Normalisation trade |
| `TestSignalNormalizer::test_normalize_news_signal` | Normalisation news |
| `TestSignalNormalizer::test_normalize_alpha_signal` | Normalisation alpha |
| `TestSignalNormalizer::test_normalized_dict_has_all_expected_keys` | Toutes les clés |
| `TestClassifyRawText::test_classify_trade` | Classification trade |
| `TestClassifyRawText::test_classify_news` | Classification news |
| `TestClassifyRawText::test_classify_alpha` | Classification alpha |
| `TestClassifyRawText::test_classify_unknown` | Texte inconnu → None |

## Tests d'échantillons

Utiliser les fichiers `tests/fixtures/telegram_screener/` pour valider
le parsing sur des messages Telegram représentatifs.

## Critères de succès

- 100% des tests passant
- Aucune dépendance réseau dans les tests
