---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: strategy_registry
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 95_STRATEGY_REGISTRY

## Inventaire des stratégies concrètes filles

---

## 1_OBJECTIF

Lister toutes les stratégies concrètes instanciées via le cadre canonique
(`GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01`). Chaque entrée correspond à un
child GO unique avec un `strategy_id` et `strategy_version` définis.

Toute stratégie utilisable dans le pipeline doit figurer ici.

---

## 2_REGISTRY

| # | strategy_id | strategy_version | setup_type | status | lifecycle | parent_go | telegram_latency |
|---|-------------|-----------------|-----------|--------|-----------|-----------|----------------|
| 1 | `SMC_ICT_CHOCH_BOS_RETEST` | `0.1.0` | `SWEEP_CHOCH_BOS_FVG_OB_RETEST` | open | ACTIVE_PAPER | `GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01` | UNMEASURED |
| 2 | `xau_session_open_v1` | `v0.1.0` | `session_open` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | UNMEASURED |
| 3 | `COINM_SHORT` | `v0.1.0` | `lower_high_structure_ma_break` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | UNMEASURED |
| 4 | `USDTM_LONG` | `v0.1.0` | `bullish_confirmation_pullback` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | UNMEASURED |
| 5 | `GOLD_CFD_LONG` | `v0.1.0` | `hl_structure_ma_buy` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | UNMEASURED |
| 6 | `range_strategy_v1` | `v0.1.0` | `range_boundary_reversal` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | UNMEASURED |
| 7 | `btc_coinm_accumulation` | `v0.1.0` | `dca_accumulation_hedge` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | UNMEASURED |
| 8 | `DCA_ON_FEAR_SOLID_STOCKS` | `v0.1.0` | `dca_fear_entry` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` | UNMEASURED |
| 9 | `e2e_dry_run` | `v0.1.0` | `fixture_e2e` | open | FIXTURE | `GO_SIGNAL_CHAIN_E2E_DRY_RUN_01` | N/A |
| 10 | `SPCX_IPO_BREAKOUT` | `v0.1.0` | `ipo_orderflow` | open | CANDIDATE | `GO_SPACEX_SUPER_DESK_PARENT_01` | UNMEASURED |
| 11 | `SPCX_VWAP_CONFLUENCE` | `v0.1.0` | `vwap_microstructure` | open | CANDIDATE | `GO_SPACEX_SUPER_DESK_PARENT_01` | UNMEASURED |
| 12 | `SPCX_SMC_STRUCTURE` | `v0.1.0` | `smc_microstructure` | open | CANDIDATE | `GO_SPACEX_SUPER_DESK_PARENT_01` | UNMEASURED |
| 13 | `SPCX_MOMENTUM_VOLUME` | `v0.1.0` | `volume_momentum` | open | CANDIDATE | `GO_SPACEX_SUPER_DESK_PARENT_01` | UNMEASURED |
| 14 | `SPCX_CATALYST_NEWS` | `v0.1.0` | `catalyst_news` | open | CANDIDATE | `GO_SPACEX_SUPER_DESK_PARENT_01` | UNMEASURED |
| 15 | `SPCX_ACCUMULATION_ZONES` | `v0.1.0` | `accumulation` | open | CANDIDATE | `GO_SPACEX_SUPER_DESK_PARENT_01` | UNMEASURED |
| 16 | `SPCX_ORDERFLOW_MICROSTRUCTURE` | `v0.1.0` | `orderflow_tape_depth` | open | CANDIDATE | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` | UNMEASURED |
| 17 | `SPCX_OWNERSHIP_PRESSURE` | `v0.1.0` | `ownership_ledger` | open | CANDIDATE | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` | UNMEASURED |

---

## 3_ENTRIES

### 3.1_SMC_ICT_CHOCH_BOS_RETEST

| Champ | Valeur |
|---|---|
| `strategy_id` | `SMC_ICT_CHOCH_BOS_RETEST` |
| `strategy_version` | `0.1.0` |
| `setup_type` | `SWEEP_CHOCH_BOS_FVG_OB_RETEST` |
| `family` | `SMC_ICT` |
| `direction` | `WATCH_ONLY` |
| `observation_status` | `ACTIVE_PAPER` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01/` |
| `created_at` | `2026-05-17` |

### 3.2_xau_session_open_v1

| Champ | Valeur |
|---|---|
| `strategy_id` | `xau_session_open_v1` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `session_open` |
| `family` | `session_open` |
| `direction` | `contextual` |
| `observation_status` | `ACTIVE` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_REGISTRY_REGULARIZATION_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_REGISTRY_REGULARIZATION_01/` |
| `runtime_surfaces` | `trading_realtime_v1`, `trading_lab_v1` |
| `profile_ref` | `docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml` |
| `created_at` | `2026-05-18` |

### 3.3_COINM_SHORT

| Champ | Valeur |
|---|---|
| `strategy_id` | `COINM_SHORT` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `lower_high_structure_ma_break` |
| `family` | `trend_following` |
| `direction` | `SHORT` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01/` |
| `runtime_surfaces` | `strategy_logic.py` (engine), `engines/registry.py`, `webhook_server.py`, `paper_guards.py`, `risk_calculator.py`, `bitget_to_tv_runner.py` |
| `priority` | `P0` |
| `created_at` | `2026-05-18` |

### 3.4_USDTM_LONG

| Champ | Valeur |
|---|---|
| `strategy_id` | `USDTM_LONG` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `bullish_confirmation_pullback` |
| `family` | `trend_following` |
| `direction` | `LONG` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_USDTM_LONG_REGISTRY_REGULARIZATION_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_USDTM_LONG_REGISTRY_REGULARIZATION_01/` |
| `runtime_surfaces` | `strategy_logic.py` (engine), `engines/registry.py`, `webhook_server.py`, `paper_guards.py` |
| `priority` | `P1` |
| `created_at` | `2026-05-18` |

### 3.5_GOLD_CFD_LONG

| Champ | Valeur |
|---|---|
| `strategy_id` | `GOLD_CFD_LONG` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `hl_structure_ma_buy` |
| `family` | `trend_following` |
| `direction` | `LONG` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_GOLD_CFD_LONG_REGISTRY_REGULARIZATION_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_GOLD_CFD_LONG_REGISTRY_REGULARIZATION_01/` |
| `runtime_surfaces` | `strategy_logic.py` (engine), `engines/registry.py`, `webhook_server.py`, `risk_calculator.py` |
| `priority` | `P2` |
| `created_at` | `2026-05-18` |

### 3.6_range_strategy_v1

| Champ | Valeur |
|---|---|
| `strategy_id` | `range_strategy_v1` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `range_boundary_reversal` |
| `family` | `range_trading` |
| `direction` | `LONG_SHORT` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_RANGE_STRATEGY_V1_REGISTRY_REGULARIZATION_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_RANGE_STRATEGY_V1_REGISTRY_REGULARIZATION_01/` |
| `cadrage_ref` | `GO_RANGE_STRATEGY_V1_STRUCT_01` |
| `runtime_surfaces` | `(aucune — doc-only)` |
| `priority` | `P3` |
| `created_at` | `2026-05-18` |

### 3.7_btc_coinm_accumulation

| Champ | Valeur |
|---|---|
| `strategy_id` | `btc_coinm_accumulation` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `dca_accumulation_hedge` |
| `family` | `accumulation` |
| `direction` | `LONG_SHORT` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_BTC_COINM_ACCUMULATION_REGISTRY_REGULARIZATION_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_BTC_COINM_ACCUMULATION_REGISTRY_REGULARIZATION_01/` |
| `runtime_surfaces` | `(aucune — doc-only concept)` |
| `priority` | `P4` |
| `created_at` | `2026-05-18` |

### 3.8_DCA_ON_FEAR_SOLID_STOCKS

| Champ | Valeur |
|---|---|
| `strategy_id` | `DCA_ON_FEAR_SOLID_STOCKS` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `dca_fear_entry` |
| `family` | `equity_dca` |
| `direction` | `LONG` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_OPT_TRADING_STOCKS_PARENT_DCA_ON_FEAR_SOLID_STOCKS_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_OPT_TRADING_STOCKS_PARENT_DCA_ON_FEAR_SOLID_STOCKS_01/` |
| `runtime_surfaces` | `(aucune — doc-only framework)` |
| `priority` | `P5` |
| `created_at` | `2026-05-19` |

### 3.10_SPCX_IPO_BREAKOUT

| Champ | Valeur |
|---|---|
| `strategy_id` | `SPCX_IPO_BREAKOUT` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `ipo_orderflow` |
| `family` | `ipo_event` |
| `direction` | `LONG_SHORT` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `parent_go` | `GO_SPACEX_SUPER_DESK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01/` |
| `runtime_surfaces` | `spcx_v2/setup_detector.py` (detect, gate_2_setup_match: ipo category) |
| `sub_setups` | `FIRST_PRINT_OBSERVATION`, `IPO_ORB_5M`, `IPO_ORB_15M`, `IPO_ORB_30M`, `IPO_PRICE_RECLAIM`, `IPO_PRICE_LOSS`, `GAP_AND_GO`, `FAILED_BREAKOUT_TRAP` |
| `created_at` | `2026-06-14` |

### 3.11_SPCX_VWAP_CONFLUENCE

| Champ | Valeur |
|---|---|
| `strategy_id` | `SPCX_VWAP_CONFLUENCE` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `vwap_microstructure` |
| `family` | `vwap_anchored` |
| `direction` | `LONG_SHORT` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `parent_go` | `GO_SPACEX_SUPER_DESK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01/` |
| `runtime_surfaces` | `spcx_v2/setup_detector.py` (detect, gate_2_setup_match: vwap category) |
| `sub_setups` | `VWAP_HOLD_LONG`, `VWAP_RECLAIM`, `VWAP_REJECT`, `VWAP_DISTANCE_EXTREME` |
| `created_at` | `2026-06-14` |

### 3.12_SPCX_SMC_STRUCTURE

| Champ | Valeur |
|---|---|
| `strategy_id` | `SPCX_SMC_STRUCTURE` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `smc_microstructure` |
| `family` | `smc_ict` |
| `direction` | `LONG_SHORT` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `parent_go` | `GO_SPACEX_SUPER_DESK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01/` |
| `runtime_surfaces` | `spcx_v2/setup_detector.py` (detect, gate_2_setup_match: smc category) |
| `sub_setups` | `FVG_BULLISH_RECLAIM`, `FVG_BEARISH_REJECT`, `BOS_CONTINUATION`, `CHOCH_REVERSAL`, `LIQUIDITY_SWEEP_LOW_RECLAIM`, `LIQUIDITY_SWEEP_HIGH_REJECT`, `ORDER_BLOCK_RETEST` |
| `created_at` | `2026-06-14` |

### 3.13_SPCX_MOMENTUM_VOLUME

| Champ | Valeur |
|---|---|
| `strategy_id` | `SPCX_MOMENTUM_VOLUME` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `volume_momentum` |
| `family` | `momentum` |
| `direction` | `LONG_SHORT` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `parent_go` | `GO_SPACEX_SUPER_DESK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01/` |
| `runtime_surfaces` | `spcx_v2/setup_detector.py` (detect, gate_2_setup_match: momentum category) |
| `sub_setups` | `RELATIVE_VOLUME_BREAKOUT`, `VOLUME_ACCELERATION`, `HIGH_VOLUME_PULLBACK`, `LOW_VOLUME_FADE`, `DOLLAR_VOLUME_FILTER` |
| `created_at` | `2026-06-14` |

### 3.14_SPCX_CATALYST_NEWS

| Champ | Valeur |
|---|---|
| `strategy_id` | `SPCX_CATALYST_NEWS` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `catalyst_news` |
| `family` | `catalyst` |
| `direction` | `LONG_SHORT` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `parent_go` | `GO_SPACEX_SUPER_DESK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01/` |
| `runtime_surfaces` | `spcx_v2/setup_detector.py` (detect, gate_2_setup_match: news category) |
| `sub_setups` | `NEWS_CATALYST_BREAKOUT`, `SEC_FILING_REACTION`, `CONTRACT_NEWS_REACTION`, `NEGATIVE_HEADLINE_RISK_OFF`, `NEWS_SPIKE_FADE` |
| `created_at` | `2026-06-14` |

### 3.15_SPCX_ACCUMULATION_ZONES

| Champ | Valeur |
|---|---|
| `strategy_id` | `SPCX_ACCUMULATION_ZONES` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `accumulation` |
| `family` | `accumulation` |
| `direction` | `LONG` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `parent_go` | `GO_SPACEX_SUPER_DESK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01/` |
| `runtime_surfaces` | `spcx_v2/setup_detector.py` (detect, gate_2_setup_match: accumulation category) |
| `sub_setups` | `BUY_ZONE`, `ACCUMULATE_ZONE`, `WAIT_ZONE`, `DANGER_ZONE` |
| `created_at` | `2026-06-14` |

### 3.16_SPCX_ORDERFLOW_MICROSTRUCTURE

| Champ | Valeur |
|---|---|
| `strategy_id` | `SPCX_ORDERFLOW_MICROSTRUCTURE` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `orderflow_tape_depth` |
| `family` | `orderflow` |
| `direction` | `CONTEXTUAL` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `parent_go` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `docs_path` | `docs/chantiers/GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01/` |
| `runtime_surfaces` | `modules/ipo_tracking/scoring/spcx_orderflow_score.py` (score_orderflow), `modules/ipo_tracking/collectors/spcx_sip_tape.py` (collect_spcx_sip_tape), `modules/ipo_tracking/collectors/spcx_l2_depth.py` (collect_spcx_l2_depth), `modules/ipo_tracking/pipeline.py` (_collect_orderflow) |
| `produces` | `spcx_orderflow_bucket_v1`, `spcx_orderflow_score` (0-100), component scores (liquidity, tape_flow, auction, volume_quality, price_context) |
| `created_at` | `2026-06-14` |

### 3.17_SPCX_OWNERSHIP_PRESSURE

| Champ | Valeur |
|---|---|
| `strategy_id` | `SPCX_OWNERSHIP_PRESSURE` |
| `strategy_version` | `v0.1.0` |
| `setup_type` | `ownership_ledger` |
| `family` | `ownership` |
| `direction` | `CONTEXTUAL` |
| `lifecycle` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `telegram_latency_status` | `UNMEASURED` |
| `go_id` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `parent_go` | `GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01` |
| `docs_path` | `docs/chantiers/GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01/` |
| `runtime_surfaces` | `modules/ipo_tracking/scoring/spcx_ownership_pressure_score.py` (score_ownership_pressure), `modules/ipo_tracking/collectors/spcx_sec_ownership.py` (collect_spcx_sec_ownership), `modules/ipo_tracking/pipeline.py` (_collect_orderflow) |
| `produces` | `spcx_ownership_ledger_v1`, `spcx_ownership_pressure_score` (0-100), component scores (insider_concentration, lockup_overhang, institutional_quality, cost_basis_overhang, greenshoe_status) |
| `created_at` | `2026-06-14` |

---

## 4_MAINTENANCE

| Action | Quand |
|--------|-------|
| Ajouter une entrée | Nouveau child GO stratégie créé |
| Mettre à jour `strategy_version` | Version bump dans le spec |
| Mettre à jour `status` / `lifecycle` | Transition de gate documentée |
| Retirer une entrée | Stratégie retirée (retirement confirmé) |

---

## 5_INVARIANTS

- Toute entrée doit avoir un `strategy_id` non null.
- Toute entrée doit avoir un child GO ouvert avec `parent_go` référencé.
- Toute entrée doit avoir un `docs_path` pointant vers des fichiers existants.
- `lifecycle` initial = `CANDIDATE`.
- `perf_status` initial = `UNMEASURED`.
- Aucune entrée ne déclenche de runtime par sa seule présence dans ce registre.

---

## 6_NO_RUNTIME_EFFECT

Ce document est un inventaire doc-only. Il ne déclenche pas :

```text
execution code
scheduler
Bitget order
Google Sheets write
Telegram message
```

## RISKS

- À qualifier.
