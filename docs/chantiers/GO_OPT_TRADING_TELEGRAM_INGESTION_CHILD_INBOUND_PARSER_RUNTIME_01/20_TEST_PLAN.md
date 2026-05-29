# 20_TEST_PLAN

## Tests

| Test | Cible | Type |
|---|---|---|
| `test_raw_message_creation` | RawMessage dataclass fields + defaults | unit |
| `test_inbound_message_creation` | InboundMessage dataclass from RawMessage | unit |
| `test_raw_message_to_inbound` | RawMessage → InboundMessage conversion | unit |
| `test_inbound_client_is_protocol` | InboundClient is a Protocol class | unit |
| `test_mock_client_get_messages` | MockClient.get_messages returns preset list | unit |
| `test_mock_client_get_messages_limit` | MockClient respects limit param | unit |
| `test_mock_client_iter_messages` | MockClient.iter_messages yields messages | unit |
| `test_mock_client_empty` | MockClient returns [] when no messages | unit |
| `test_message_receiver_poll` | MessageReceiver.poll returns messages | unit |
| `test_message_receiver_poll_limit` | MessageReceiver.poll respects limit | unit |
| `test_message_receiver_poll_empty` | MessageReceiver.poll returns [] for empty | unit |
| `test_message_receiver_stream` | MessageReceiver.stream calls handler per message | unit |
| `test_no_network` | Aucune dépendance réseau dans les tests | audit |

## Critères

- 100% tests passant
- 0 appel réseau live
- 0 secret/token/chat_id dans le repo
- 0 dépendance Telethon
