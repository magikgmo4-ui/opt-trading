# 20_TEST_PLAN

## Tests

| Test | Cible |
|---|---|
| `test_event_tracker_entry` | Entry event → position candidate |
| `test_event_tracker_exit` | Exit event → position closed |
| `test_position_lifecycle_active` | Candidate → active |
| `test_position_lifecycle_closed` | Active → closed with PnL |

## Critères

- 100% tests passant
- Compatible avec schéma webhook_to_perf existant
