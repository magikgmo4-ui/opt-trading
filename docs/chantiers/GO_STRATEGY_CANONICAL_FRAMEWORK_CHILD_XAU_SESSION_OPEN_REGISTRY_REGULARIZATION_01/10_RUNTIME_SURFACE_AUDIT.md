---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_XAU_SESSION_OPEN_REGISTRY_REGULARIZATION_01
doc_type: runtime_surface_audit
strategy_id: xau_session_open_v1
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 10_RUNTIME_SURFACE_AUDIT

## Surfaces runtime utilisant xau_session_open_v1

---

## 1_RUNTIME_REFERENCES

| # | Fichier | Type | Usage |
|---|---------|------|-------|
| 1 | `modules/trading_realtime_v1/app/runtime_loop_v1.py` | Hardcode | `STRATEGY_ID = "xau_session_open_v1"` (l.13) → `build_event` l.93 |
| 2 | `modules/trading_realtime_v1/app/event_bridge_v1.py` | Hardcode | `STRATEGY_ID = "xau_session_open_v1"` (l.11) → `build_event` l.71 |
| 3 | `modules/trading_lab_v1/app/trading_lab_v1.py` | Fallback | `profile["strategy"].get("strategy_id") or "xau_session_open_v1"` (l.396) |
| 4 | `modules/trading_lab_v1/tests/test_core_runner_v1.py` | Test | Assert `strategy_id == "xau_session_open_v1"` (l.38, 121) |
| 5 | `docs/ot/trading/schemas/xauusd_dual_stack_v1.profile.yaml` | Config | `strategy_id: "xau_session_open_v1"` (l.49) |

---

## 2_PROFILE_EXISTANT

Le profil `xauusd_dual_stack_v1.profile.yaml` définit déjà :

```yaml
strategy:
  strategy_id: "xau_session_open_v1"
  family: "session_open"
  model: "mechanical"
  variants: [xau_open_sweep_fvg, xau_open_no_sweep_fvg, xau_open_sweep_no_fvg, xau_open_no_sweep_no_fvg]
```

4 variants opérationnels avec configurations sweep/FVG.

---

## 3_PAYLOAD_VIA_RUNTIME

Les events produits par `trading_realtime_v1` incluent déjà `strategy_id` dans
le payload JSON :

```json
{
  "profile_id": "xauusd_dual_stack_v1",
  "strategy_id": "xau_session_open_v1",
  "symbol": "XAUUSD",
  "mode": "observation",
  "event_type": "runtime_observed",
  "decision_state": "observed"
}
```

---

## 4_SURFACES_NON_TOUCHÉES

| Surface | Raison |
|---------|--------|
| `decision_engine` | Aucune référence à xau_session_open_v1 |
| `signal_router` | Ne référence pas cette stratégie |
| `proposition_engine` | Ne référence pas cette stratégie |
| `notification_dispatcher` | Ne référence pas cette stratégie |
| `position_engine` | Ne référence pas cette stratégie |
| `execution_engine` | Ne référence pas cette stratégie |
| `portfolio_engine` | Ne référence pas cette stratégie |

---

## 5_CONSTAT

`xau_session_open_v1` est déjà intégrée dans le pipeline runtime réel.
La régularisation est documentaire : le code produit déjà des events avec
`strategy_id`, le profil YAML définit déjà la config. Ce qui manque :

```text
- Registration dans le strategy registry du framework canonique
- Spec documentaire officielle
- Gates de lifecycle documentées
- Lien explicite child GO → parent GO
```
