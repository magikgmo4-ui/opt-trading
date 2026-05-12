---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01_SIMULATION_RESULT_SCHEMA
doc_type: simulation_result_schema
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
status: draft_for_review
lifecycle_stage: child_simulation_result_schema
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
topic_keys:
  - opt-trading
  - trading
  - btc
  - coin-futures
  - simulation
  - result-schema
  - ranking
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/02_simulation_result_schema.md
point_de_reprise: "Definir le contrat de sortie d'un run de sweep BTC COIN-M."
updated_at: 2026-05-08
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/01_param_space_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/03_reality_classifier_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/01_backtest_data_prep.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
---

# 02_simulation_result_schema

## 1_MASTER_TARGET

Definir un schema de resultat unique pour chaque run de free search BTC COIN-M, de sorte que le meme artefact puisse alimenter le classifieur realite, le ranker, les exports tabulaires et les audits de runs extremes.

## 2_OUTPUT_PRINCIPLES

```text
- un run = une ligne de resume canonique
- les gros artefacts (timeline, event_log) vivent a part
- le resume doit suffire pour trier, filtrer, classer et expliquer rapidement
- le format doit etre compatible JSONL et CSV
```

Convention de nommage :

```text
JSON canonique = snake_case
CSV humain = alias possibles si necessaire
```

## 3_ARTIFACT_SET

Artefacts recommandes par campagne :

```text
state/trading_lab_v1/param_sweep_runs_summary.jsonl
state/trading_lab_v1/param_sweep_runs_summary.csv
state/trading_lab_v1/param_sweep_top_best.md
state/trading_lab_v1/param_sweep_top_worst.md
state/trading_lab_v1/param_sweep_timelines/{run_id}.jsonl
state/trading_lab_v1/param_sweep_events/{run_id}.jsonl
```

Le chemin exact reste configurable, mais la separation resume / trace detaillee est obligatoire.

## 4_CANONICAL_SUMMARY_FIELDS

### 4.1 Identite du run

| Champ | Type | Role |
|---|---|---|
| `run_id` | string | identifiant unique du run |
| `batch_id` | string | identifiant de campagne |
| `config_hash` | string | hash stable de la config canonique |
| `seed` | int | seed du generateur |
| `generator_method` | string | `random`, `lhs`, `grid`, `stress`, `walk_forward` |
| `generator_stage` | string | ex: `phase_A_random_large` |
| `engine_version` | string | version logique du moteur de simulation |

### 4.2 Metadonnees dataset

| Champ | Type | Role |
|---|---|---|
| `dataset_id` | string | identifiant dataset historique |
| `dataset_start` | timestamp | debut de periode |
| `dataset_end` | timestamp | fin de periode |
| `timeframe_primary` | string | `1h`, `4h`, `1d` |
| `candle_count` | int | nombre de bougies |
| `funding_points` | int | nombre de settlements funding |
| `contract_snapshot_id` | string | snapshot contrat/risk tier utilise |

### 4.3 Echo de configuration

| Champ | Type | Role |
|---|---|---|
| `config` | object | config complete du run |
| `config_surface_version` | string | version du schema config |
| `apply_strategic_guards` | bool | doit etre `false` dans ce child par defaut |

Le champ `config` doit inclure toutes les variables de la surface de sweep.

## 5_NUMERIC_RESULT_FIELDS

### 5.1 Metriques de portefeuille

| Champ canonique | Type | Role |
|---|---|---|
| `net_btc_initial` | decimal | BTC net initial |
| `net_btc_final` | decimal | BTC net final |
| `delta_btc_net` | decimal | `net_btc_final - net_btc_initial` |
| `delta_btc_pct` | decimal | performance relative |
| `spot_btc_final` | decimal | BTC spot final |
| `margin_btc_final` | decimal | collateral BTC final |
| `reserve_usdt_final` | decimal | reserve quote finale |
| `realized_pnl_btc` | decimal | PnL short realise |
| `unrealized_pnl_btc` | decimal | PnL latent final |
| `funding_paid_btc` | decimal | funding paye par les shorts |
| `funding_received_btc` | decimal | funding recu par les shorts |
| `fees_btc` | decimal | frais cumules |

### 5.2 Metriques de risque

| Champ canonique | Type | Role |
|---|---|---|
| `max_drawdown_btc` | decimal | drawdown max en BTC |
| `max_drawdown_pct` | decimal | drawdown max relatif |
| `liquidation_count` | int | nombre de liquidations |
| `margin_breach_count` | int | nombre de breaches `MR_max` |
| `d_min_breach_count` | int | nombre de breaches `D_min` |
| `capital_exhaustion_count` | int | reserve vide / marge vide |
| `worst_margin_ratio` | decimal | extremum de risque observe selon la convention retenue |
| `min_distance_to_liq` | decimal | distance mini a liquidation |
| `max_position_native` | decimal | taille short max observee |
| `max_notional_usd` | decimal | notionnel USD max observe |
| `max_leverage_realized` | decimal | levier effectif max observe |

### 5.3 Activite et execution

| Champ canonique | Type | Role |
|---|---|---|
| `dca_count` | int | nombre de DCA executes |
| `short_add_count` | int | nombre d'ajouts short |
| `tp_count` | int | nombre de prises de profit |
| `funding_event_count` | int | nombre d'evenements funding |
| `fee_event_count` | int | nombre d'evenements de frais |
| `exchange_impossible_event_count` | int | nombre d'evenements hors contraintes exchange |
| `simulation_stop_reason` | string | `completed`, `math_invalid`, `data_invalid`, `liquidated`, `capital_depleted` |

## 6_VALIDITY_AND_CLASSIFICATION_FIELDS

| Champ | Type | Role |
|---|---|---|
| `math_valid` | bool | aucune erreur numerique bloquante |
| `data_valid` | bool | dataset exploitable |
| `exchange_feasible` | bool | passe les contraintes exchange observees |
| `used_paper_locked_formula` | bool | au moins une formule PAPER_LOCKED a servi |
| `used_mark_proxy` | bool | MarkPrice remplace par proxy |
| `classification_primary` | string | classe principale |
| `classification_tags` | list[string] | tags secondaires |
| `reject_reasons` | list[string] | codes machine lisibles |
| `overfit_score` | decimal | score ou suspicion calculee |
| `notes` | list[string] | remarques libres ou derivees |

## 7_REQUIRED_EXPORT_COLUMNS

Colonnes obligatoires pour tout export tabulaire resume :

```text
run_id
config_hash
net_btc_initial
net_btc_final
delta_btc_net
delta_btc_pct
max_drawdown_btc
liquidation_count
margin_breach_count
funding_paid_btc
funding_received_btc
fees_btc
spot_btc_final
margin_btc_final
realized_pnl_btc
unrealized_pnl_btc
classification_primary
reject_reasons
```

Alias CSV humain autorises si necessaire :

```text
net_btc_initial     -> NetBTC_initial
net_btc_final       -> NetBTC_final
delta_btc_net       -> delta_btc
classification_primary -> classification
```

## 8_MINIMAL_JSON_EXAMPLE

```json
{
  "run_id": "sweep_20260508_000001",
  "batch_id": "btc_coinm_free_search_01",
  "config_hash": "sha256:example",
  "seed": 104729,
  "generator_method": "random",
  "generator_stage": "phase_A_random_large",
  "engine_version": "free_search_spec_v1",
  "dataset_id": "btcusd_coinm_1h_2024_2026",
  "dataset_start": "2024-01-01T00:00:00Z",
  "dataset_end": "2026-05-01T00:00:00Z",
  "timeframe_primary": "1h",
  "candle_count": 20000,
  "funding_points": 2500,
  "contract_snapshot_id": "bitget_btcusd_snapshot_20260507",
  "config": {
    "z_dca": 0.005,
    "z_short": 0.003,
    "g_up": 0.01,
    "g_down": 0.015,
    "r_transfer": 1.4,
    "y_dca_usdt": 250,
    "q_add_native": 0.00013,
    "tp1": 0.5,
    "tp2": 0.25,
    "runner": 0.25,
    "cooldown_dca_h": 0,
    "cooldown_short_h": 0,
    "leverage_target": 140,
    "D_min": 0.1,
    "MR_max": 0.8,
    "Q_max_native": 5,
    "U_floor_usdt": 0,
    "M_floor_btc": 0,
    "funding_limit": 0.5,
    "fee_limit": 0.1,
    "slippage_max_bps": 200,
    "weekly_structure_gate_mode": "off",
    "weekly_k": 3,
    "weekly_epsilon_lambda": 0.01,
    "max_pivot_gap_weeks": 8
  },
  "apply_strategic_guards": false,
  "net_btc_initial": 0.12,
  "net_btc_final": 0.118,
  "delta_btc_net": -0.002,
  "delta_btc_pct": -0.0166666667,
  "spot_btc_final": 0.101,
  "margin_btc_final": 0.017,
  "reserve_usdt_final": 25,
  "realized_pnl_btc": 0.003,
  "unrealized_pnl_btc": -0.001,
  "funding_paid_btc": 0.002,
  "funding_received_btc": 0.0004,
  "fees_btc": 0.0007,
  "max_drawdown_btc": 0.015,
  "max_drawdown_pct": 0.11,
  "liquidation_count": 0,
  "margin_breach_count": 3,
  "d_min_breach_count": 4,
  "capital_exhaustion_count": 1,
  "worst_margin_ratio": 0.22,
  "min_distance_to_liq": 0.04,
  "max_position_native": 12,
  "max_notional_usd": 12,
  "max_leverage_realized": 137,
  "dca_count": 42,
  "short_add_count": 58,
  "tp_count": 31,
  "funding_event_count": 2500,
  "fee_event_count": 89,
  "exchange_impossible_event_count": 58,
  "simulation_stop_reason": "completed",
  "math_valid": true,
  "data_valid": true,
  "exchange_feasible": false,
  "used_paper_locked_formula": true,
  "used_mark_proxy": true,
  "classification_primary": "EXCHANGE_IMPOSSIBLE",
  "classification_tags": ["OVERFIT_SUSPECT"],
  "reject_reasons": ["ERR_QTY_OFF_GRID", "ERR_LEVERAGE_ABOVE_MAX"],
  "overfit_score": 0.82,
  "notes": ["raw_math_explorable_but_exchange_invalid"]
}
```

## 9_TRACE_FIELDS_FOR_DETAILED_AUDIT

Pour audit ou replay, chaque resume peut aussi porter :

| Champ | Type | Role |
|---|---|---|
| `timeline_path` | string or null | chemin vers la timeline detaillee |
| `event_log_path` | string or null | chemin vers le journal d'evenements |
| `risk_log_path` | string or null | chemin vers le journal de risque |

## 17_RESUME_POINT

```text
Le resume canonique doit tenir en une ligne par run,
mais cette ligne doit suffire pour classer, filtrer, expliquer,
et retrouver ensuite la trace detaillee si necessaire.
```
