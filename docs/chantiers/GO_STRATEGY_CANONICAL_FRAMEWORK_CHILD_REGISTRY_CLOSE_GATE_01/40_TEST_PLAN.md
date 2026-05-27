# 40 — Test Plan

## Action unique

Corriger la constante `KNOWN_IDS` dans `tests/test_strategy_adapter.py` pour refléter les 9 IDs actuels du registry.

## Changement

```python
# Avant (7 IDs)
KNOWN_IDS = {
    "SMC_ICT_CHOCH_BOS_RETEST",
    "xau_session_open_v1",
    "COINM_SHORT",
    "USDTM_LONG",
    "GOLD_CFD_LONG",
    "range_strategy_v1",
    "btc_coinm_accumulation",
}

# Après (9 IDs)
KNOWN_IDS = {
    "SMC_ICT_CHOCH_BOS_RETEST",
    "xau_session_open_v1",
    "COINM_SHORT",
    "USDTM_LONG",
    "GOLD_CFD_LONG",
    "range_strategy_v1",
    "btc_coinm_accumulation",
    "DCA_ON_FEAR_SOLID_STOCKS",
    "e2e_dry_run",
}
```

## Tests impactés (4 failures résolues)

| Test | Avant | Après |
|---|---|---|
| `TestGetKnownIds::test_exact_set` | FAIL (7 vs 9) | PASS |
| `TestGetKnownIds::test_count` | FAIL (7 vs 9) | PASS |
| `TestGetAllEntries::test_count` | FAIL (7 vs 9) | PASS |
| `TestGetAllEntries::test_all_known` | FAIL | PASS |

## Commandes de validation

```bash
python tools/strategy/validate_strategy_registry.py
python -m pytest tests/test_strategy_adapter.py -q
```

## Critère de succès

`PASS_STRATEGY_FRAMEWORK_REGISTRY_CLOSE_GATE_01` — 0 failure dans `tests/test_strategy_adapter.py`.
