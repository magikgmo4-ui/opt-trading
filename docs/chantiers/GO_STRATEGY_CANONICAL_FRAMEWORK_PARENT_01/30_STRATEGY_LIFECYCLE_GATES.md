---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
child_go: GO_STRATEGY_LIFECYCLE_GATES_01
doc_type: lifecycle_gates
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 30_STRATEGY_LIFECYCLE_GATES

---

## 1_LIFECYCLE

```text
CANDIDATE
↓
OBSERVED
↓
PAPER_VALIDATED
↓
MULTI_SIGNAL_ELIGIBLE
↓
LIVE_REVIEW_ONLY
```

Ces etats sont des statuts de gouvernance. Ils ne donnent jamais a eux seuls
le droit d'envoyer un ordre live.

---

## 2_STATE_DEFINITIONS

| Etat | Definition | Droit maximal |
| --- | --- | --- |
| `CANDIDATE` | Idee strategique decrite par un spec minimal. | Documentation + observation passive. |
| `OBSERVED` | Strategie observee dans `ObservationEvent` avec evidence. | Watch-only, dry-run, replay. |
| `PAPER_VALIDATED` | Perf Engine montre des resultats suffisants en paper/shadow. | Paper expansion controlee. |
| `MULTI_SIGNAL_ELIGIBLE` | Strategie eligible a la combinaison avec autres signaux valides. | Multi-signal paper seulement. |
| `LIVE_REVIEW_ONLY` | Dossier assez solide pour revue live humaine. | Revue documentaire, pas execution. |

---

## 3_PROMOTION_GATES

| Transition | Conditions minimales |
| --- | --- |
| `CANDIDATE -> OBSERVED` | `strategy_id`, `strategy_version`, `setup_type`, `invalidation`, evidence source et premier `ObservationEvent` enrichi. |
| `OBSERVED -> PAPER_VALIDATED` | Sample minimal, jours minimaux, Perf Engine evidence, absence d'anomalie bloquante, replay Trading Lab possible. |
| `PAPER_VALIDATED -> MULTI_SIGNAL_ELIGIBLE` | Phase 1 seuils respectes, kill switch valide, Telegram dry-run valide, correlation avec autres signaux documentee. |
| `MULTI_SIGNAL_ELIGIBLE -> LIVE_REVIEW_ONLY` | Dossier de readiness doc-only, refusal criteria relus, aucun ordre live, decision humaine explicite requise. |

Seuils initiaux herites des PR #514 et #512 :

```text
min_sample_size = 30 runs
min_observation_days = 14 jours
kill_switch_tested = true
telegram_dry_run_tested = true
no_closeout_required = true
```

---

## 4_RETIREMENT_GATES

Une strategie doit pouvoir etre retiree, pausee ou retrogradee.

| Condition | Action |
| --- | --- |
| `strategy_id` ambigu ou duplique | Retrait jusqu'a clarification. |
| Invalidation non testable | Retour `CANDIDATE`. |
| Perf Engine `FAIL` sur sample suffisant | `RETIRED` ou `OBSERVED_ONLY`. |
| Drift de marche non documente | Pause + review. |
| Telegram signal confondu avec ordre | Blocage du protocole Telegram strategie. |
| Vision-only decision detectee | Rejet de l'observation comme preuve de promotion. |
| Closeout requis non acknowledge | Promotion bloquee. |

---

## 5_PHASE_GATE_OUTPUT

Chaque gate doit produire un verdict structurable :

```json
{
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "from_status": "OBSERVED",
  "to_status": "PAPER_VALIDATED",
  "verdict": "BLOCKED",
  "reason": "insufficient_sample",
  "evidence": {
    "observation_events": 12,
    "observation_days": 4,
    "perf_status": "INSUFFICIENT_SAMPLE"
  }
}
```

---

## 6_HARD_BLOCKS

Promotion interdite si :

```text
No strategy_id
No strategy_version
No invalidation
No ObservationEvent evidence
No Perf Engine evidence
No kill switch validation for expansion
Telegram direct BUY/SELL before validation
Vision-only decision
Automatic Sheets write
Live or Bitget order path
```

---

## 7_LIVE_REVIEW_ONLY

`LIVE_REVIEW_ONLY` signifie :

```text
La strategie peut entrer dans une revue humaine de readiness.
Elle ne peut pas envoyer d'ordre live.
Elle ne peut pas activer Bitget.
Elle ne peut pas contourner les refusal criteria de PR #510.
```
