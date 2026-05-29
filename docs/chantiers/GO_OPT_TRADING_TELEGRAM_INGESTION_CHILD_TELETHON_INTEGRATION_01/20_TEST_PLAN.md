# 20_TEST_PLAN

## Tests

| Test | Cible | Type |
|---|---|---|
| `test_import_error_if_not_installed` | Lazy import → ImportError si telethon absent | unit |
| `test_start_calls_telethon_start` | TelethonInboundClient.start() appelle client.start() | unit |
| `test_get_messages_returns_raw_messages` | get_messages mappe Telethon Message → RawMessage | unit |
| `test_get_messages_respects_limit` | limit paramètre transmis à Telethon | unit |
| `test_iter_messages_yields_raw_messages` | iter_messages yield RawMessage pour chaque message | unit |
| `test_iter_messages_empty` | itération vide | unit |
| `test_add_event_handler` | add_event_handler appelé sur client Telethon | unit |
| `test_message_mapping_fields` | Vérifie tous les champs RawMessage mappés | unit |
| `test_message_mapping_null_sender` | sender=None si pas de username | unit |

## Critères

- 100% tests passant
- 0 appel réseau live
- 0 secret / API ID / API hash
- Telethon mocké via unittest.mock
