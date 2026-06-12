---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
child_go: GO_STRATEGY_TRADING_LAB_REPLAY_PROTOCOL_01
doc_type: trading_lab_replay_protocol
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 80_TRADING_LAB_REPLAY_PROTOCOL

---

## 1_OBJECTIF

Definir comment une strategie devient rejouable dans Trading Lab a partir de
`ObservationEvent` enrichis.

Replay signifie :

```text
Revoir le contexte, le signal, l'evidence, le plan, l'invalidation et l'outcome.
```

Replay ne signifie pas :

```text
Reexecuter un ordre.
```

---

## 2_REPLAY_INPUTS

| Input | Source |
| --- | --- |
| `run_id` | `ObservationEvent.run_id` |
| `strategy_id` | `ObservationEvent.strategy.strategy_id` |
| `strategy_version` | `ObservationEvent.strategy.strategy_version` |
| `symbol` | `ObservationEvent.signal.symbol` |
| `timeframe` | `ObservationEvent.signal.timeframe` |
| `direction` | `ObservationEvent.signal.direction` |
| `entry_zone` | `ObservationEvent.trade_plan.entry_zone` |
| `invalidation` | `ObservationEvent.trade_plan.invalidation` |
| `target_zone` | `ObservationEvent.trade_plan.target_zone` |
| `evidence_source` | screenshots, webhook payloads, market data, notes |
| `outcome` | `ObservationEvent.outcome`, `pnl_net` |

---

## 3_REPLAY_ARTIFACTS

Un replay strategie doit pouvoir pointer vers :

```text
source_file
vision summary
analysis markdown
webhook payload
market snapshot
strategy spec version
Perf Engine evaluation
Telegram watch message dry-run output
```

Pour Bot Vision, les artefacts existants incluent :

```text
data/desk_pro/vision/<run>/summary.json
data/desk_pro/vision/<run>/analysis.txt
data/desk_pro/vision/<run>/analysis.md
```

---

## 4_REPLAY_STATES

| State | Definition |
| --- | --- |
| `REPLAY_MISSING` | Event non rejouable, evidence insuffisante. |
| `REPLAY_READY` | Evidence minimale presente. |
| `REPLAY_REVIEWED` | Operateur a annote le replay. |
| `REPLAY_INVALID` | Replay montre que le signal ne respecte pas le spec. |

---

## 5_LABELS

Labels minimum :

```text
valid_setup
invalid_setup
late_signal
early_signal
invalidation_clear
invalidation_missing
target_clear
target_missing
vision_unclear
market_data_missing
```

Ces labels alimentent Perf Engine et retirement gates.

---

## 6_REPLAY_OUTPUT

Output attendu :

```json
{
  "run_id": "20260517_001",
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "replay_status": "REPLAY_READY",
  "labels": [
    "valid_setup",
    "invalidation_clear"
  ],
  "review_notes": "Setup observed, keep in CANDIDATE until sample threshold.",
  "promotion_impact": "NO_CHANGE"
}
```

---

## 7_NO_RUNTIME_EFFECT

Trading Lab replay :

- ne modifie pas les journaux source;
- ne poste pas Telegram;
- ne declenche pas Google Sheets;
- ne declenche pas Bitget;
- ne change pas seul le lifecycle.

Il produit une evidence de review pour les gates.

## RISKS

- À qualifier.
