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

| # | strategy_id | strategy_version | setup_type | status | lifecycle | parent_go |
|---|-------------|-----------------|-----------|--------|-----------|-----------|
| 1 | `SMC_ICT_CHOCH_BOS_RETEST` | `0.1.0` | `SWEEP_CHOCH_BOS_FVG_OB_RETEST` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| 2 | `xau_session_open_v1` | `v0.1.0` | `session_open` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| 3 | `COINM_SHORT` | `v0.1.0` | `lower_high_structure_ma_break` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| 4 | `USDTM_LONG` | `v0.1.0` | `bullish_confirmation_pullback` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| 5 | `GOLD_CFD_LONG` | `v0.1.0` | `hl_structure_ma_buy` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| 6 | `range_strategy_v1` | `v0.1.0` | `range_boundary_reversal` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| 7 | `btc_coinm_accumulation` | `v0.1.0` | `dca_accumulation_hedge` | open | CANDIDATE | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |

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
| `observation_status` | `CANDIDATE` |
| `perf_status` | `UNMEASURED` |
| `go_id` | `GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01/` |
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
| `go_id` | `GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_BTC_COINM_ACCUMULATION_REGISTRY_REGULARIZATION_01` |
| `parent_go` | `GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01` |
| `docs_path` | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_BTC_COINM_ACCUMULATION_REGISTRY_REGULARIZATION_01/` |
| `runtime_surfaces` | `(aucune — doc-only concept)` |
| `priority` | `P4` |
| `created_at` | `2026-05-18` |

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
