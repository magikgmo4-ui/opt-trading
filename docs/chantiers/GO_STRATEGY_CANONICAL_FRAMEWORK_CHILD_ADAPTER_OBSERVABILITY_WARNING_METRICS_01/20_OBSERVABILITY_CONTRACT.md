# 20 — Observability Contract

## Format canonique du warning

Tout warning `strategy_id` inconnu doit être émis via le logger `strategy.observability` au niveau `WARNING`, avec le message structuré suivant :

```
event=STRATEGY_ID_UNKNOWN metric=strategy_id.unknown.warning strategy_id=<id> source=<surface> mode=warning_only runtime_action=continue registry_known=false
```

## Champs obligatoires du payload

| Champ | Type | Valeur fixe | Description |
|---|---|---|---|
| `event` | str | `STRATEGY_ID_UNKNOWN` | Type d'événement canonique |
| `metric` | str | `strategy_id.unknown.warning` | Clé métrique |
| `strategy_id` | str | variable | L'ID inconnu reçu |
| `source` | str | variable | Surface émettrice (ex: `signal_router`) |
| `mode` | str | `warning_only` | Indique absence de hard-fail |
| `runtime_action` | str | `continue` | Comportement runtime inchangé |
| `registry_known` | bool | `False` | Résultat de validate_strategy_id |

## Contrats comportementaux

1. `validate_strategy_id()` n'est pas modifié — sa signature et son retour restent identiques
2. Appeler `log_unknown_strategy_id_warning()` ne lève jamais d'exception
3. Appeler `log_unknown_strategy_id_warning()` ne modifie pas la valeur de retour de la fonction appelante
4. Le logger `strategy.observability` est distinct des loggers métier — les surfaces conservent leurs propres loggers

## API publique ajoutée

```python
def build_unknown_strategy_warning_payload(strategy_id: str, source: str) -> dict:
    ...

def log_unknown_strategy_id_warning(strategy_id: str, source: str) -> None:
    ...
```

Ces deux fonctions font partie de `modules.strategy.adapter` et sont importables directement.
