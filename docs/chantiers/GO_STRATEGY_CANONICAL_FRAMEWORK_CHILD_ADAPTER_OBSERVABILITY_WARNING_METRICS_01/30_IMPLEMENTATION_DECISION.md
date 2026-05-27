# 30 — Implementation Decision

## Option retenue : helper central dans adapter.py

### Pourquoi adapter.py ?

L'adaptateur est déjà le point de vérité pour `validate_strategy_id()`. Centraliser le helper ici garantit que :
- toutes les surfaces utilisent le même format sans coordination supplémentaire
- le logger `strategy.observability` est unique et isolé
- les tests smoke ne dépendent que de l'adaptateur, pas des surfaces

### Pourquoi ne pas utiliser les loggers locaux des surfaces ?

Chaque surface a un logger propre (`signal_router`, `proposition_engine`, etc.). Si le helper émettait via ces loggers, il faudrait passer le logger en paramètre, ce qui couple le helper aux surfaces et complique les tests. Le logger `strategy.observability` est neutre et capturables indépendamment.

### Pourquoi ne pas créer un module dédié ?

Un nouveau module ajouterait une dépendance à importer dans chaque surface. Rester dans `adapter.py` conserve le seul point d'import déjà en place.

### Impact sur les surfaces print-based (event_bridge_v1, runtime_loop_v1)

Ces deux fichiers font un check `validate_strategy_id()` au niveau module. Remplacer le `print` par `log_unknown_strategy_id_warning()` unifie le mécanisme et rend le warning capturable par caplog. La sémantique (warning si l'ID est inconnu, continue dans tous les cas) reste identique.

## Décision finale

- Ajouter `build_unknown_strategy_warning_payload()` et `log_unknown_strategy_id_warning()` dans `adapter.py`
- Remplacer les 6 occurrences de warning direct par `log_unknown_strategy_id_warning()`
- Ajouter les imports nécessaires dans les surfaces
- Aucun autre fichier modifié
