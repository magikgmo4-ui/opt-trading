# 20_TEST_PLAN

## Tests unitaires

| Test | Cible |
|---|---|
| `test_trade_parser_valid` | Trade setup bien formé → signal normalisé |
| `test_trade_parser_invalid` | Format invalide → erreur documentée |
| `test_news_parser` | Message news → catégorie + texte |
| `test_alpha_parser` | Message alpha → ticker + message |
| `test_signal_normalizer` | Parser output → format canonique |

## Tests d'échantillons

Utiliser des samples réels (anonymisés) depuis `samples/` pour valider
le parsing sur des messages Telegram authentiques.

## Critères de succès

- 100% des tests passant
- Couverture ≥ 80% du module parser
- Aucune dépendance réseau dans les tests
