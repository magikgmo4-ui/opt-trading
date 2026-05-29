# 20_TEST_PLAN

## Tests

| Test | Cible |
|---|---|
| `test_load_registry` | Chargement YAML valide → ChannelRegistry |
| `test_load_missing_file` | Fichier absent → FileNotFoundError |
| `test_load_invalid_yaml` | YAML malformé → erreur |
| `test_load_wrong_version` | Version != 1 → erreur validation |
| `test_load_invalid_tier` | trust_tier invalide → erreur |
| `test_get_enabled_channels` | Filtre enabled=True |
| `test_get_channels_by_tier` | Filtre par trust_tier |
| `test_get_channels_by_category` | Filtre par catégorie |
| `test_enabled_false_by_default` | enabled=False par défaut |
| `test_alias_pattern` | Alias doit matcher TG_SRC_* |
| `test_fixture_yaml` | Fixture YAML représentatif charge correctement |

## Critères de succès

- 100% des tests passant
- Aucune dépendance réseau
- Aucun id/channel réel dans les fixtures
