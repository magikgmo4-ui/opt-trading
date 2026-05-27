# 10 — Warning Surface Audit

## Surfaces identifiées

### signal_router/app/router.py — ligne 70

```python
log.warning("unknown strategy_id %r", normalized.strategy_id)
```

- Logger : `signal_router`
- Flux : continue (signal retourné intact)
- Champs : strategy_id seulement

### proposition_engine/app/engine.py — ligne 74

```python
log.warning("unknown strategy_id %r", request.signal.strategy_id)
```

- Logger : `proposition_engine`
- Flux : continue (proposition produite)
- Champs : strategy_id seulement

### notification_dispatcher/app/dispatcher.py — ligne 27

```python
log.warning("unknown strategy_id %r", sid)
```

- Logger : `notification_dispatcher`
- Flux : continue (dispatch ou dry_run)
- Champs : strategy_id seulement

### trading_realtime_v1/app/event_bridge_v1.py — lignes 15-19

```python
if not validate_strategy_id(STRATEGY_ID):
    print(
        f"[WARNING] strategy_id {STRATEGY_ID!r} not found in registry",
        file=sys.stderr,
    )
```

- Mécanisme : `print` stderr (pas `logging`)
- Flux : module-level check, continue
- Champs : strategy_id seulement

### trading_realtime_v1/app/runtime_loop_v1.py — lignes 17-21

```python
if not validate_strategy_id(STRATEGY_ID):
    print(
        f"[WARNING] strategy_id {STRATEGY_ID!r} not found in registry",
        file=sys.stderr,
    )
```

- Mécanisme : `print` stderr (pas `logging`)
- Flux : module-level check, continue
- Champs : strategy_id seulement

### trading_lab_v1/app/trading_lab_v1.py — ligne 154

```python
log.warning("unknown %s strategy_id %r", source, strategy_id)
```

- Logger : `trading_lab_v1`
- Flux : continue (strategy_id retourné intact via `resolve_strategy_id`)
- Champs : strategy_id + source ("fallback" ou "profile")

## Problème

- Loggers hétérogènes → impossible d'agréger les warnings strategy_id inconnus en une seule requête
- Deux surfaces utilisent `print` → non capturables par `caplog` ni par un log aggregator
- Aucun champ `metric` ni `event` canonique → les warnings ne sont pas labelisés pour le monitoring

## Action

Remplacer les 6 appels par `log_unknown_strategy_id_warning(strategy_id, source)` qui émet via le logger dédié `strategy.observability` avec un format canonique fixe.
