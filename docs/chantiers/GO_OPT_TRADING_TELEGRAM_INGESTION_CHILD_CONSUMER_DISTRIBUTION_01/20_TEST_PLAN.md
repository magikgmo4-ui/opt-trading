# 20_TEST_PLAN

## Tests

| Test | Cible | Type |
|---|---|---|
| `test_consumer_protocol` | Stub implémente Consumer protocol | unit |
| `test_router_register_and_route` | ConsumerRouter.route appelle consumer | unit |
| `test_router_channel_routing` | canal A → consumer A, canal B → consumer B | unit |
| `test_router_default_consumer` | canal inconnu → default consumer | unit |
| `test_router_multiple_consumers` | un canal → N consumers | unit |
| `test_router_no_registration` | aucun route → 0 dispatch | unit |
| `test_router_route_count` | retourne le nombre de consumers appelés | unit |
| `test_screener_consumer_collects` | ScreenerConsumer stub collecte messages | unit |

## Critères

- 100% tests passant
- 0 dépendance réseau
- 0 modification de l'inbound parser / normalizer
