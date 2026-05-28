# 20_TEST_PLAN

## Tests unitaires

| Test | Cible |
|---|---|
| `test_signal_producer_valid` | Signal parsé → screener signal valide |
| `test_signal_producer_empty` | Aucun signal → liste vide |
| `test_desk_pro_adapter` | Screener signal → format Desk Pro |
| `test_signal_schema_validation` | Signal invalide → erreur de validation |

## Critères de succès

- 100% des tests passant
- Format du signal compatible avec Desk Pro
- Aucune dépendance réseau
