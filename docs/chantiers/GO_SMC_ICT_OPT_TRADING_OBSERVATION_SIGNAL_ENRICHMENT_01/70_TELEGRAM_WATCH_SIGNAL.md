---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: telegram_watch_signal_instance
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 70_TELEGRAM_WATCH_SIGNAL

## Telegram Watch Signal : SMC_ICT_CHOCH_BOS_RETEST

---

## 1_OBJECTIF

Definir le payload et le message Telegram watch signal concret pour
`SMC_ICT_CHOCH_BOS_RETEST`.

Ce document instancie le protocole general du parent
(`70_TELEGRAM_WATCH_SIGNAL_PROTOCOL.md`) pour ce strategy_id specifique.

---

## 2_SURFACE_EXISTANTE

Le repo dispose deja de :

| Module | Fichier | Role |
| --- | --- | --- |
| `notification_dispatcher` | `app/events.py` | Template `signal_received` |
| `notification_dispatcher` | `app/dispatcher.py` | `dry_run=True` disponible |
| `screeners.sh` | `scripts/tmux/sessions/screeners.sh` | Session tmux Telegram |

Les event types SMC/ICT ne sont PAS encore ajoutes au dispatcher.
Ce document les definit pour un child runtime futur.

---

## 3_PAYLOAD_CONCRET

```json
{
  "event_type": "strategy_watch_signal",
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "0.1.0",
  "setup_type": "SWEEP_CHOCH_BOS_FVG_OB_RETEST",
  "symbol": "BTCUSDT",
  "timeframe": "15m",
  "context_timeframes": ["1h", "4h"],
  "direction": "WATCH_ONLY",
  "confidence": 0.72,
  "watch_status": "OBSERVE",
  "choch_observed": true,
  "bos_observed": false,
  "sweep_observed": true,
  "sweep_type": "BSL_sweep",
  "fvg_ob_confluence": true,
  "premium_discount": "DISCOUNT",
  "invalidation": "close_through_swing_that_generated_choch",
  "invalidation_level": null,
  "target_zone": "prior_BSL",
  "source_run_id": "20260517_001",
  "observation_status": "CANDIDATE",
  "perf_status": "UNMEASURED",
  "promotion_gate": "BLOCKED_INSUFFICIENT_SAMPLE",
  "dry_run": true
}
```

---

## 4_MESSAGE_HUMAIN

Format attendu du message Telegram :

```text
[WATCH] Strategy Observation
strategy : SMC_ICT_CHOCH_BOS_RETEST
version  : 0.1.0
setup    : SWEEP_CHOCH_BOS_FVG_OB_RETEST

symbol   : BTCUSDT
tf       : 15m (context: 1h, 4h)
direction: WATCH_ONLY

signals  :
  - CHoCH bullish confirme
  - BSL sweep detecte
  - FVG + OB confluence

confidence : 0.72
status     : CANDIDATE / UNMEASURED
gate       : BLOCKED_INSUFFICIENT_SAMPLE

invalidation: close through swing that generated CHoCH

run: 20260517_001

[OBSERVATION ONLY - NO TRADE]
```

---

## 5_CONDITIONS_ENVOI

| Condition | Regle |
| --- | --- |
| `strategy_id` present | Obligatoire |
| `invalidation` present | Obligatoire |
| `confidence >= 0.60` | Seuil minimal pour envoi |
| `perf_status = PASS` | Non requis pour WATCH; interdit pour BUY/SELL |
| `dry_run = true` | Par defaut jusqu'a validation explicite |
| Kill switch actif | Bloque ou degrade en status info |
| `choch_observed or bos_observed = true` | Obligatoire |

---

## 6_TYPES_DEVENTS

Event types pour child dispatcher futur :

| Event type | Declencheur |
| --- | --- |
| `strategy_watch_signal` | Nouveau signal CHoCH/BOS observe |
| `strategy_invalidated` | Invalidation confimee (close through swing) |
| `strategy_replay_ready` | Evidence Trading Lab disponible |
| `strategy_perf_update` | Mise a jour Perf Engine (weekly) |
| `strategy_gate_blocked` | Tentative de promotion bloquee |
| `strategy_retirement_warning` | Seuil max failures approche |

Ces event types ne sont pas encore dans le dispatcher.
Ils sont reserves pour un child runtime `GO_SMC_ICT_TELEGRAM_DISPATCHER_01`
(non ouvert, futur).

---

## 7_SAFETY_RULES

| Regle | Application SMC/ICT |
| --- | --- |
| Interdire BUY/SELL avant `perf_status = PASS` | Oui, absolu |
| Interdire signal sans `strategy_id` | Oui |
| Interdire signal sans `invalidation` | Oui |
| `dry_run` actif par defaut | Oui |
| Vision-only -> evidence incomplete | Marquer `confidence <= 0.20` |
| Confluence absente -> confiance reduite | Oui, scoring automatique |
| Kill switch -> bloquer ou degrader | Oui, heritage PR #513 |

---

## 8_DISTINCTION_WATCH_VS_EXECUTE

Le message Telegram ne doit JAMAIS contenir :

```text
BUY
SELL
LONG NOW
SHORT NOW
EXECUTE
ORDER SENT
ENTER HERE
```

Il peut contenir :

```text
WATCH
OBSERVE
CANDIDATE
INVALIDATED
REPLAY READY
PERF UPDATE
```

---

## 9_NO_RUNTIME_EFFECT

Ce document definit le payload et les conditions du Telegram watch signal.

Il ne declenche pas d'envoi Telegram reel.
L'envoi reel necessite un child runtime dedie avec `dry_run = false` explicitement valide.
