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
