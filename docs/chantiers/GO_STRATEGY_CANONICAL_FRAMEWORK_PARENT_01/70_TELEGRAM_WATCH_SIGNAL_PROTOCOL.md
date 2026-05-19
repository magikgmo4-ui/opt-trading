---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
child_go: GO_STRATEGY_TELEGRAM_WATCH_SIGNAL_PROTOCOL_01
doc_type: telegram_watch_signal_protocol
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 70_TELEGRAM_WATCH_SIGNAL_PROTOCOL

---

## 1_OBJECTIF

Definir un protocole Telegram strategie en mode watch-only.

Telegram peut signaler :

```text
WATCH
OBSERVE
INVALIDATED
REPLAY_READY
PERF_UPDATE
GATE_BLOCKED
```

Telegram ne doit pas signaler avant validation :

```text
BUY
SELL
LONG NOW
SHORT NOW
EXECUTE
ORDER SENT
```

---

## 2_EXISTING_SURFACE

Le repo contient deja :

| Surface | Role |
| --- | --- |
| `scripts/tmux/sessions/screeners.sh` | Lance la fenetre `telegram` via `notification_dispatcher`. |
| `modules/notification_dispatcher/app/events.py` | Template `signal_received` avec `Strategy: {strategy_id}`. |
| `modules/notification_dispatcher/app/dispatcher.py` | `dry_run=True` retourne le message sans poster. |
| `tests/test_kill_switch_telegram_validation.py` | Valide kill switch et Telegram dry-run dans PR #513. |

Le protocole strategie doit s'appuyer sur cette surface.

---

## 3_MESSAGE_SCHEMA

Payload minimal :

```json
{
  "event_type": "strategy_watch_signal",
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "v0.1.0",
  "setup_type": "SWEEP_CHOCH_BOS_FVG_OB_RETEST",
  "symbol": "BTCUSDT",
  "timeframe": "15m",
  "direction": "WATCH_ONLY",
  "confidence": 0.62,
  "watch_status": "OBSERVE",
  "invalidation": "structure break invalidates setup",
  "source_run_id": "20260517_001",
  "observation_status": "CANDIDATE",
  "perf_status": "UNMEASURED",
  "promotion_gate": "BLOCKED_INSUFFICIENT_SAMPLE"
}
```

---

## 4_RENDERING_REQUIREMENTS

Message humain attendu :

```text
Strategy WATCH
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
setup: SWEEP_CHOCH_BOS_FVG_OB_RETEST
symbol/timeframe: BTCUSDT 15m
direction: WATCH_ONLY
confidence: 0.62
status: CANDIDATE / UNMEASURED
gate: BLOCKED_INSUFFICIENT_SAMPLE
invalidation: structure break invalidates setup
run: 20260517_001
```

Le message doit etre clair que c'est une observation, pas une instruction.

---

## 5_SAFETY_RULES

| Regle | Decision |
| --- | --- |
| Missing `strategy_id` | Ne pas envoyer de watch signal strategie. |
| Missing invalidation | Ne pas envoyer de watch signal strategie. |
| `perf_status != PASS` | Interdire tout langage BUY/SELL. |
| Kill switch actif | Telegram strategy signal bloque ou degrade en status info. |
| `dry_run` disponible | Utiliser dry-run pour tests et validation. |
| Vision-only source | Marquer evidence incomplete; pas de promotion. |

---

## 6_ALLOWED_EVENT_TYPES

Event types candidats pour child futur :

```text
strategy_watch_signal
strategy_invalidated
strategy_replay_ready
strategy_perf_update
strategy_gate_blocked
strategy_retirement_warning
```

Ces event types doivent etre ajoutes au dispatcher uniquement dans un child
runtime dedie, pas dans ce parent.

---

## 7_NO_DUPLICATE_PIPELINE

Telegram ne stocke pas la verite strategie.

Source canonique :

```text
ObservationEvent -> journal daily -> LocalCMS / Telegram / Perf Engine
```

Telegram est uniquement un consumer de notification.
