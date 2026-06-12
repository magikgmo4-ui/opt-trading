---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: perf_engine_metrics_instance
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 80_PERF_ENGINE_METRICS

## Metriques Perf Engine : SMC_ICT_CHOCH_BOS_RETEST v0.1.0

---

## 1_OBJECTIF

Definir les metriques Perf Engine specifiques a la strategie
`SMC_ICT_CHOCH_BOS_RETEST`, en instanciant le protocole general du parent
(`60_PERF_ENGINE_STRATEGY_EVALUATION.md`).

---

## 2_INPUTS_PERF_ENGINE

Le Perf Engine pour `SMC_ICT_CHOCH_BOS_RETEST` filtre les `ObservationEvent` sur :

```text
ObservationEvent.strategy.strategy_id = "SMC_ICT_CHOCH_BOS_RETEST"
ObservationEvent.strategy.strategy_version = "0.1.0"
```

Et requiert la presence de :

```text
smc_ict_detail.choch_observed OR smc_ict_detail.bos_observed = true
trade_plan.invalidation present
signal.confidence defini
```

---

## 3_METRIQUES_STANDARD

Heritees du parent, appliquees a `SMC_ICT_CHOCH_BOS_RETEST` :

| Metric | Description | Cible v0.1.0 |
| --- | --- | --- |
| `sample_size` | Nombre d'events exploitables | >= 30 pour promotion |
| `observation_days` | Jours distincts observes | >= 14 pour promotion |
| `pass_rate` | Ratio events PASS pipeline / total | >= 0.80 |
| `win_rate` | Ratio outcomes positifs / outcomes connus | A definir post-observation |
| `pnl_cumulative` | P&L paper cumule | Positif requis pour promotion |
| `expectancy` | P&L moyen par event (paper) | > 0.0 |
| `max_drawdown` | Drawdown paper max sur serie | < seuil defini apres 30 runs |
| `profit_factor` | Gains bruts / pertes brutes | > 1.0 |
| `confidence_calibration` | Correlation confidence vs outcome | Defini post-30 runs |
| `invalidation_respected_rate` | Taux d'observations avec invalidation | 1.0 requis |
| `false_positive_rate` | Signals sans suite valide | < 0.30 cible |
| `replay_coverage` | Part des events rejouables | >= 0.80 cible |

---

## 4_METRIQUES_SMC_ICT_SPECIFIQUES

Metriques additionnelles pour `SMC_ICT_CHOCH_BOS_RETEST` :

| Metric | Description |
| --- | --- |
| `choch_rate` | Ratio events avec CHoCH vs BOS seul |
| `sweep_prerequisite_rate` | Ratio events avec sweep avant CHoCH |
| `fvg_ob_confluence_rate` | Ratio events avec confluence FVG+OB |
| `htf_alignment_rate` | Ratio events avec alignement `1h`/`4h` confirme |
| `premium_discount_compliance` | Ratio LONG en Discount ou SHORT en Premium |
| `mss_confirmation_rate` | Ratio CHoCH suivi de MSS confirme |
| `avg_confidence_score` | Moyenne de `signal.confidence` sur le sample |
| `confidence_vs_win_correlation` | Correlation score vs win |
| `invalidation_hit_rate` | Taux d'invalidations triggees dans le sample |

---

## 5_STATUTS_PERF_ENGINE

| `perf_status` | Definition |
| --- | --- |
| `UNMEASURED` | Aucun event `SMC_ICT_CHOCH_BOS_RETEST` valide |
| `MEASURING` | Events presents, sample < 30 ou jours < 14 |
| `INSUFFICIENT_SAMPLE` | Sample ou jours sous seuil |
| `PASS` | Metriques satisfont les gates de promotion |
| `FAIL` | Metriques echouent sur sample suffisant |
| `BLOCKED` | Strategy_id manquant ou donnees invalides |

---

## 6_EVIDENCE_PACK_CONCRET

Format du pack d'evidence pour `SMC_ICT_CHOCH_BOS_RETEST` :

```json
{
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "0.1.0",
  "perf_status": "MEASURING",
  "sample_size": 8,
  "observation_days": 3,
  "metrics": {
    "pass_rate": 0.88,
    "win_rate": null,
    "pnl_cumulative": null,
    "expectancy": null,
    "max_drawdown": null,
    "profit_factor": null,
    "confidence_calibration": null,
    "invalidation_respected_rate": 1.0,
    "false_positive_rate": null,
    "replay_coverage": 0.75
  },
  "smc_ict_metrics": {
    "choch_rate": 1.0,
    "sweep_prerequisite_rate": 0.75,
    "fvg_ob_confluence_rate": 0.625,
    "htf_alignment_rate": 0.50,
    "premium_discount_compliance": 0.875,
    "mss_confirmation_rate": 0.50,
    "avg_confidence_score": 0.64,
    "confidence_vs_win_correlation": null,
    "invalidation_hit_rate": 0.125
  },
  "promotion_gate": {
    "verdict": "BLOCKED",
    "reason": "insufficient_sample",
    "sample_needed": 22,
    "days_needed": 11
  },
  "retirement_gate": {
    "verdict": "KEEP_OBSERVING",
    "consecutive_failures": 0
  }
}
```

---

## 7_PROTOCOLE_EVALUATION

Sequence pour `SMC_ICT_CHOCH_BOS_RETEST` :

```text
1. Charger ObservationEvent avec strategy_id = "SMC_ICT_CHOCH_BOS_RETEST"
2. Filtrer: smc_ict_detail.choch_observed OR bos_observed = true
3. Filtrer: trade_plan.invalidation present
4. Exclure events FAIL si cause invalide le run (ex. closeout_required)
5. Calculer metriques standard (section 3)
6. Calculer metriques SMC/ICT specifiques (section 4)
7. Produire perf_status
8. Produire promotion_gate verdict
9. Produire retirement_gate verdict
10. Publier evidence pack (lecture seule) vers LocalCMS et Trading Lab
```

---

## 8_SEUILS_PROMOTION_MINIMUM

Pour `SMC_ICT_CHOCH_BOS_RETEST v0.1.0` :

```text
sample_size >= 30
observation_days >= 14
pass_rate >= 0.80
win_rate > 0.0 (au moins un outcome positif mesure)
pnl_cumulative > 0.0
expectancy > 0.0
invalidation_respected_rate = 1.0 (absolu)
replay_coverage >= 0.80
fvg_ob_confluence_rate >= 0.50 (specifique SMC/ICT)
premium_discount_compliance >= 0.70 (specifique SMC/ICT)
no closeout_required events dans le sample final
kill_switch_tested = true
telegram_dry_run_tested = true
```

---

## 9_NO_LIVE_DECISION

Le Perf Engine pour `SMC_ICT_CHOCH_BOS_RETEST` produit :

```text
PASS
FAIL
BLOCKED
MEASURING
INSUFFICIENT_SAMPLE
KEEP_OBSERVING
RETIRED_RECOMMENDED
```

Il ne produit jamais :

```text
BUY
SELL
EXECUTE
BITGET_ORDER
LIVE_APPROVED
```

## RISKS

- À qualifier.
