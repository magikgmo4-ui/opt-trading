---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_REGISTRY_REGULARIZATION_01
doc_type: strategy_spec_instance
strategy_id: xau_session_open_v1
strategy_version: v0.1.0
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 20_STRATEGY_SPEC_XAU_SESSION_OPEN_V1

## Spec stratégique minimal

---

## 1_IDENTITE

| Champ | Valeur |
|---|---|
| `strategy_id` | `xau_session_open_v1` |
| `strategy_version` | `v0.1.0` |
| `family` | `session_open` |
| `model` | `mechanical` |
| `symbol` | XAUUSD |
| `timeframe` | LIVE (M1 ticks) |
| `direction` | LONG/SHORT (contextual) |
| `signal_source` | `trading_realtime_v1` |

---

## 2_PROFIL_DE_REFERENCE

La configuration complète est définie dans le profil YAML :

```text
docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml
```

Références clés du profil :

| Paramètre | Valeur |
|---|---|
| `sessions` | `gold_open_18h` (18:00-18:30), `midnight_00h` (00:00-00:30) |
| `max_trades_per_day` | 2 |
| `risk_per_trade_pct` | 1.0 |
| `rr_min` | 2.0 |
| `require_sweep` | configurable par variant |
| `require_fvg` | configurable par variant |
| `mode` | `observation` (pas d'exécution live) |

---

## 3_DESCRIPTION

La stratégie `xau_session_open_v1` observe les sessions d'ouverture du XAUUSD
(gold_open_18h, midnight_00h) en timeframe réel (M1/LIVE). Elle détecte des
configurations de sweep et/ou FVG en début de session pour produire des
observations enrichies via `trading_realtime_v1`.

Elle ne produit pas d'ordre. Elle produit des events d'observation.

---

## 4_SPEC_JSON

```json
{
  "strategy_id": "xau_session_open_v1",
  "strategy_version": "v0.1.0",
  "family": "session_open",
  "model": "mechanical",
  "symbol": "XAUUSD",
  "direction": "contextual",
  "timeframe": "LIVE",
  "signal_source": "trading_realtime_v1",
  "runtime_profile": "xauusd_dual_stack_v1",
  "variants": [
    "xau_open_sweep_fvg",
    "xau_open_no_sweep_fvg",
    "xau_open_sweep_no_fvg",
    "xau_open_no_sweep_no_fvg"
  ],
  "sessions": ["gold_open_18h", "midnight_00h"],
  "lifecycle_status": "ACTIVE",
  "perf_status": "UNMEASURED",
  "promotion_gate": "BLOCKED_REGISTRY_REGULARIZATION",
  "retirement_gate": "KEEP_RUNNING"
}
```

---

## 5_SURFACES_INTEGREES

| Surface | Intégration |
|---|---|
| `trading_realtime_v1` | Runtime producteur d'events |
| `trading_lab_v1` | Lab replay + features |
| `docs/ot/trading/schemas/` | Profil YAML complet |
| `state/trading_realtime_v1/` | State runtime |

---

## 6_VERSIONING

`strategy_version` passe à `v0.2.0` si :

```text
- sessions ajoutées ou modifiées
- variants changés (structurellement)
- risk profile modifié
- nouveau symbol ajouté
```

## RISKS

- À qualifier.
