# 20_TEST_PLAN

## Tests

| Test | Cible |
|---|---|
| `test_message_receiver_connect` | Connexion API Telegram |
| `test_message_receiver_poll` | Polling messages |
| `test_message_normalizer_text` | Normalisation message texte |
| `test_message_normalizer_media` | Normalisation message média |
| `test_consumer_router_screener` | Routage vers Screener |

## Critères

- 100% tests passant
- Aucune dépendance réseau live (mock API)
