---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
child_go: GO_STRATEGY_OBSERVATION_EVENT_EXTENSION_01
doc_type: observation_event_extension
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 40_OBSERVATION_EVENT_EXTENSION

---

## 1_OBJECTIF

Definir l'extension strategie de `ObservationEvent` sans remplacer le schema V1
du PR #524.

Principe :

```text
ObservationEvent V1 reste le point de passage.
Les champs strategie sont ajoutes comme enrichissement nullable/versionne.
```

---

## 2_BASELINE_PR_524

`ObservationEvent` V1 contient deja :

```text
run_id
session_id
run_date
started_at
status
dry_run
paper_mode
outcome
pnl_net
localcms_ok
closeout_required
ingested_at
source_file
```

`ObservationSummary` contient deja :

```text
total_runs
pass_count
fail_count
pnl_cumulative
win_rate
days_elapsed
runs_to_threshold
days_to_threshold
eligible
```

Extension cible :

```text
strategy_id
strategy_version
setup_type
direction
signal_source
evidence_source
confidence
entry_zone
invalidation
target_zone
risk_profile
observation_status
perf_status
promotion_gate
retirement_gate
```

---

## 3_EXTENSION_FIELDS

| Champ | Type | Requis pour nouveaux signaux strategie | Backfill anciens runs |
| --- | --- | --- | --- |
| `strategy_id` | string | Oui | Nullable |
| `strategy_version` | string | Oui | Nullable |
| `setup_type` | string | Oui | Nullable |
| `direction` | enum | Oui | Nullable |
| `symbol` | string | Oui | Derivable si present dans `signal_source` |
| `timeframe` | string | Oui | Nullable |
| `signal_source` | string/object | Oui | Existe partiellement dans journal |
| `evidence_source` | array | Oui | Nullable |
| `confidence` | float | Oui | Nullable |
| `entry_zone` | object/string | Oui | Nullable |
| `invalidation` | object/string | Oui | Nullable |
| `target_zone` | object/string | Oui | Nullable |
| `risk_profile` | object/string | Oui | Nullable |
| `observation_status` | enum | Oui | Default `UNCLASSIFIED` pour anciens runs |
| `perf_status` | enum | Oui | Default `UNMEASURED` |
| `promotion_gate` | object | Oui | Nullable |
| `retirement_gate` | object | Oui | Nullable |

---

## 4_RECOMMENDED_STRUCTURE

```json
{
  "strategy": {
    "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
    "strategy_version": "v0.1.0",
    "setup_type": "SWEEP_CHOCH_BOS_FVG_OB_RETEST",
    "lifecycle_status": "CANDIDATE"
  },
  "signal": {
    "direction": "WATCH_ONLY",
    "symbol": "BTCUSDT",
    "timeframe": "15m",
    "signal_source": "bot_vision",
    "confidence": 0.62
  },
  "trade_plan": {
    "entry_zone": null,
    "invalidation": "structure break invalidates setup",
    "target_zone": "prior liquidity or opposing imbalance",
    "risk_profile": "paper_only"
  },
  "evidence": [
    {
      "type": "vision_summary",
      "path": "data/desk_pro/vision/latest/summary.json"
    }
  ],
  "gates": {
    "observation_status": "CANDIDATE",
    "perf_status": "UNMEASURED",
    "promotion_gate": "requires_perf_engine_evidence",
    "retirement_gate": "manual_review_required"
  }
}
```

---

## 5_COMPATIBILITY_RULES

| Regle | Decision |
| --- | --- |
| Anciens `data/journal/daily/*.json` sans strategie | Valides, non backfill obligatoire. |
| Nouveaux events strategie sans `strategy_id` | Invalides. |
| LocalCMS actuel | Peut ignorer les champs inconnus. |
| Perf Engine futur | Lit les champs strategie depuis `ObservationEvent`. |
| Google Sheets | Exporte ces champs seulement via mapping controle. |
| Telegram | Affiche `strategy_id` uniquement en watch mode avant validation. |

---

## 6_EVENT_STATUS_MAPPING

| `ObservationEvent.status` | `observation_status` strategie | Sens |
| --- | --- | --- |
| `PASS` | `OBSERVED` ou `CANDIDATE` | Le run pipeline est valide; la strategie peut rester candidate. |
| `FAIL` | `BLOCKED` | Le run ne peut pas servir de preuve positive. |
| `PASS` + Perf insufficient | `OBSERVED` | Observation utile mais non promouvable. |
| `PASS` + Perf pass | `PAPER_VALIDATED` | Promotion possible si autres gates OK. |

---

## 7_NO_PARALLEL_PIPELINE_RULE

Interdit :

```text
strategy_events.jsonl separe comme source canonique
telegram_strategy_signal sans ObservationEvent
localcms_strategy_metrics sans journal daily
perf_strategy_score sans ObservationEvent evidence
trading_lab_replay sans source_file ou evidence_source
```

Autorise :

```text
views, exports, dashboards et reports derives de ObservationEvent
```
