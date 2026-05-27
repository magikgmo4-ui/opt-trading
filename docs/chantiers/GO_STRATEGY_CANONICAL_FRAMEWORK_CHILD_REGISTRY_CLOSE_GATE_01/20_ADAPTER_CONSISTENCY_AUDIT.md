# 20 — Adapter Consistency Audit

## Adapter : modules/strategy/adapter.py

- Charge le registry depuis `95_STRATEGY_REGISTRY.md` via `load_strategy_registry()`
- `_FIXTURE_STRATEGY_IDS = {"e2e_dry_run"}` — guard indépendant du fichier registry
- `get_known_ids()` retourne `{entrées registry} | {_FIXTURE_STRATEGY_IDS}` = 9 IDs
- `validate_strategy_id()` retourne `True` pour les 9 IDs, `False` pour tout autre

## Cohérence registry → adapter : OK

Tous les IDs présents dans le registry sont chargés et reconnus par `validate_strategy_id()`.

## Drift identifié : tests/test_strategy_adapter.py

Le fichier de test contient une constante `KNOWN_IDS` hardcodée avec 7 IDs, écrite avant l'ajout de `DCA_ON_FEAR_SOLID_STOCKS` (2026-05-19) et avant que `e2e_dry_run` apparaisse dans le registry.

### État avant correction

```python
KNOWN_IDS = {
    "SMC_ICT_CHOCH_BOS_RETEST",
    "xau_session_open_v1",
    "COINM_SHORT",
    "USDTM_LONG",
    "GOLD_CFD_LONG",
    "range_strategy_v1",
    "btc_coinm_accumulation",
}  # 7 IDs
```

### Entrées manquantes

| ID | Ajouté | Raison manquant |
|---|---|---|
| `DCA_ON_FEAR_SOLID_STOCKS` | 2026-05-19 | Ajout post-écriture des tests |
| `e2e_dry_run` | présent dans registry via `FIXTURE` | Exclusion implicite erronée |

### Correction

Ajouter les 2 IDs manquants à `KNOWN_IDS` et mettre à jour les assertions de count de 7 à 9.

## Impact correction

- Les 4 failures pré-existantes disparaissent
- Aucun comportement runtime modifié
- `validate_strategy_id()` inchangé
