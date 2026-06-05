---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
child_go: GO_STRATEGY_PERF_ENGINE_EVALUATION_01
doc_type: perf_engine_strategy_evaluation
repo: opt-trading
status: open
created_at: 2026-05-17
surface: doc-only
---

# 60_PERF_ENGINE_STRATEGY_EVALUATION

---

## 1_OBJECTIF

Definir comment le Perf Engine evalue une strategie a partir de
`ObservationEvent` enrichis.

Regle :

```text
No strategy promoted without Perf Engine evidence.
```

---

## 2_INPUTS

Perf Engine lit :

| Input | Source canonique |
| --- | --- |
| Strategy metadata | `ObservationEvent.strategy` |
| Signal metadata | `ObservationEvent.signal` |
| Trade plan | `ObservationEvent.trade_plan` |
| Evidence | `ObservationEvent.evidence` |
| Outcome | `ObservationEvent.outcome`, `pnl_net`, `status` |
| Gate state | `ObservationEvent.gates` |
| Journal source | `source_file` / `run_id` |

Perf Engine ne lit pas un flux parallele strategie comme source d'autorite.

---

## 3_METRICS_MINIMUM

| Metric | Description |
| --- | --- |
| `sample_size` | Nombre d'events exploitables pour `strategy_id`. |
| `observation_days` | Nombre de jours distincts observes. |
| `pass_rate` | Ratio events PASS / total. |
| `win_rate` | Ratio wins / events outcome connus. |
| `pnl_cumulative` | P&L paper cumule. |
| `expectancy` | P&L moyen ou R moyen par event. |
| `max_drawdown` | Drawdown paper sur serie ordonnee. |
| `profit_factor` | Gains bruts / pertes brutes si disponible. |
| `confidence_calibration` | Correlation confidence vs outcome. |
| `invalidation_respected_rate` | Taux d'observations avec invalidation exploitable. |
| `false_positive_rate` | Signals observes sans suite valide. |
| `replay_coverage` | Part des events rejouables en Trading Lab. |

---

## 4_STATUS_OUTPUT

| `perf_status` | Definition |
| --- | --- |
| `UNMEASURED` | Aucun event exploitable. |
| `MEASURING` | Events presents mais sample insuffisant. |
| `INSUFFICIENT_SAMPLE` | Sample ou jours sous seuil. |
| `PASS` | Metrics satisfont les gates. |
| `FAIL` | Metrics echouent sur sample suffisant. |
| `BLOCKED` | Donnees invalides, missing strategy_id, closeout, ou hard block. |

---

## 5_EVALUATION_PROTOCOL

Sequence :

```text
1. Charger ObservationEvent enrichis.
2. Filtrer par strategy_id + strategy_version.
3. Exclure events FAIL si leur cause invalide le run.
4. Calculer metrics.
5. Produire perf_status.
6. Produire promotion_gate verdict.
7. Produire retirement_gate verdict.
8. Publier evidence read-only pour LocalCMS et Trading Lab.
```

---

## 6_PROMOTION_MINIMUM

Conditions initiales :

```text
sample_size >= 30
observation_days >= 14
pass_rate acceptable
closeout_required_count = 0
invalidation present on every promoted event
confidence_calibration not contradictory
replay_coverage sufficient for review
no hard safety block
```

Les seuils numeriques finaux doivent etre ajustes par child Perf Engine, mais le
principe est fixe ici.

---

## 7_EVIDENCE_PACK

Un pack d'evidence strategie doit contenir :

```json
{
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "v0.1.0",
  "perf_status": "INSUFFICIENT_SAMPLE",
  "sample_size": 12,
  "observation_days": 4,
  "metrics": {
    "win_rate": null,
    "pnl_cumulative": null,
    "expectancy": null
  },
  "promotion_gate": {
    "verdict": "BLOCKED",
    "reason": "sample_size_below_threshold"
  },
  "retirement_gate": {
    "verdict": "KEEP_OBSERVING"
  }
}
```

---

## 8_NO_LIVE_DECISION

Perf Engine peut produire :

```text
PASS
FAIL
BLOCKED
INSUFFICIENT_SAMPLE
KEEP_OBSERVING
RETIRED_RECOMMENDED
```

Perf Engine ne produit jamais :

```text
BUY
SELL
MARKET_ORDER
BITGET_ORDER
LIVE_APPROVED
```

## RISKS

- À qualifier.
