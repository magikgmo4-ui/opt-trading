# 10 — Registry Current State Audit

## Source

`docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md`

## Entrées (9 total)

| # | strategy_id | version | lifecycle | docs_path | docs_path_exists |
|---|---|---|---|---|---|
| 1 | `SMC_ICT_CHOCH_BOS_RETEST` | `0.1.0` | `CANDIDATE` | `GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01/` | OK |
| 2 | `xau_session_open_v1` | `v0.1.0` | `CANDIDATE` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_REGISTRY_REGULARIZATION_01/` | OK |
| 3 | `COINM_SHORT` | `v0.1.0` | `CANDIDATE` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01/` | OK |
| 4 | `USDTM_LONG` | `v0.1.0` | `CANDIDATE` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_USDTM_LONG_REGISTRY_REGULARIZATION_01/` | OK |
| 5 | `GOLD_CFD_LONG` | `v0.1.0` | `CANDIDATE` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_GOLD_CFD_LONG_REGISTRY_REGULARIZATION_01/` | OK |
| 6 | `range_strategy_v1` | `v0.1.0` | `CANDIDATE` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_RANGE_STRATEGY_V1_REGISTRY_REGULARIZATION_01/` | OK |
| 7 | `btc_coinm_accumulation` | `v0.1.0` | `CANDIDATE` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_BTC_COINM_ACCUMULATION_REGISTRY_REGULARIZATION_01/` | OK |
| 8 | `DCA_ON_FEAR_SOLID_STOCKS` | `v0.1.0` | `CANDIDATE` | `GO_OPT_TRADING_STOCKS_PARENT_DCA_ON_FEAR_SOLID_STOCKS_01/` | OK |
| 9 | `e2e_dry_run` | `v0.1.0` | `FIXTURE` | `GO_SIGNAL_CHAIN_E2E_DRY_RUN_01/` | OK |

## Résultat

- Tous les `strategy_id` sont non-null : **OK**
- Tous les `docs_path` existent sur disque : **OK**
- Tous les `lifecycle` sont cohérents (8 × CANDIDATE, 1 × FIXTURE) : **OK**
- `UNREGISTERED` runtime : **0**

## Invariant check

- `e2e_dry_run` est dans le registre avec `lifecycle=FIXTURE` ET dans `_FIXTURE_STRATEGY_IDS` dans l'adapter — double-protection intentionnelle, pas de conflit

## Observations supplémentaires

`validate_strategy_registry.py` retourne 6 `TEST_UNREGISTERED` dans des fichiers de test. Ce sont des stubs (`breakout_v2`, `test_v1`, `s1`, `v1`, `t`, `test`) dans des fixtures de test — comportement normal, pas à corriger.
