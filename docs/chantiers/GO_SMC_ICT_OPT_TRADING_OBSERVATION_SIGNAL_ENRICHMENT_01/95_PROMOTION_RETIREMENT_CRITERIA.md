---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: promotion_retirement_criteria
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 95_PROMOTION_RETIREMENT_CRITERIA

## Criteres de Promotion et Retrait : SMC_ICT_CHOCH_BOS_RETEST v0.1.0

---

## 1_OBJECTIF

Definir les criteres specifiques de promotion et de retrait pour la strategie
`SMC_ICT_CHOCH_BOS_RETEST`, en applicant les lifecycle gates du parent.

---

## 2_LIFECYCLE_ACTUEL

```text
[CANDIDATE]  <- position actuelle (ouverture du chantier)
   ↓
[OBSERVED]
   ↓
[PAPER_VALIDATED]
   ↓
[MULTI_SIGNAL_ELIGIBLE]
   ↓
[LIVE_REVIEW_ONLY]
```

Chaque transition exige une decision humaine explicite.

---

## 3_GATE_CANDIDATE_TO_OBSERVED

**Conditions :**

```text
[ ] strategy_id = "SMC_ICT_CHOCH_BOS_RETEST" defini et stable
[ ] strategy_version = "0.1.0" fixee
[ ] setup_type = "SWEEP_CHOCH_BOS_FVG_OB_RETEST" documente
[ ] invalidation definie et testable (close_through_swing)
[ ] Premier ObservationEvent enrichi avec smc_ict_detail present
[ ] evidence_source pointe vers un fichier existant
[ ] confidence score calcule (>= 0.40 recommande)
[ ] Aucune anomalie bloquante dans le run associe
```

**Verdict attendu :**

```json
{
  "from_status": "CANDIDATE",
  "to_status": "OBSERVED",
  "verdict": "PENDING",
  "reason": "awaiting_first_observation_event",
  "evidence": {
    "observation_events": 0,
    "perf_status": "UNMEASURED"
  }
}
```

---

## 4_GATE_OBSERVED_TO_PAPER_VALIDATED

**Conditions quantitatives (heritees du parent + specifiques SMC/ICT) :**

```text
sample_size >= 30
observation_days >= 14
pass_rate >= 0.80
win_rate > 0.0
pnl_cumulative > 0.0
expectancy > 0.0
invalidation_respected_rate = 1.0 (absolu)
replay_coverage >= 0.80
fvg_ob_confluence_rate >= 0.50
premium_discount_compliance >= 0.70
avg_confidence_score >= 0.55
no closeout_required events dans le sample final
kill_switch_tested = true
telegram_dry_run_tested = true
confidence_calibration non contradictoire
```

**Conditions documentaires :**

```text
Spec complet et coherent (ce chantier)
Trading Lab replay d'au moins 10 events annotes
Perf Engine evidence pack presente
Aucun hard block actif
Decision humaine explicite documentee
```

**Verdict si conditions non remplies :**

```json
{
  "from_status": "OBSERVED",
  "to_status": "PAPER_VALIDATED",
  "verdict": "BLOCKED",
  "reason": "insufficient_sample",
  "evidence": {
    "observation_events": 8,
    "observation_days": 3,
    "perf_status": "MEASURING"
  }
}
```

---

## 5_GATE_PAPER_VALIDATED_TO_MULTI_SIGNAL

**Conditions supplementaires :**

```text
Phase 1 seuils valides sur au moins 2 periodes distinctes (14j chacune)
Kill switch valide sur paper expansion
Telegram dry-run valide sans BUY/SELL
Correlation avec d'autres signaux documentee (non exigee pour SMC/ICT seul)
Aucun signal Telegram BUY/SELL envoye directement
```

**Note :** `MULTI_SIGNAL_ELIGIBLE` n'est pas une cible imminente pour `v0.1.0`.

---

## 6_GATE_MULTI_SIGNAL_TO_LIVE_REVIEW_ONLY

```text
Dossier de readiness doc-only complet
Refusal criteria de PR #510 relus et confirmes
Aucun ordre live autorise
Decision humaine explicite requise
```

**Note :** `LIVE_REVIEW_ONLY` est hors scope `v0.1.0`.

---

## 7_CRITERES_RETRAIT

### 7.1_Retrait automatique recommande

| Condition | Action |
| --- | --- |
| `max_consecutive_failures >= 5` | Pause + review obligatoire |
| `invalidation_respected_rate < 1.0` | Retour `CANDIDATE` |
| `false_positive_rate > 0.50` | Pause + revue des regles de detection |
| `pnl_cumulative < 0` sur `sample_size >= 30` | `RETIRED` recommande |
| `confidence_calibration` inverse (high score -> loss) | Revue scoring |

### 7.2_Retrait manuel

| Condition | Action |
| --- | --- |
| `strategy_id` ambigu ou duplique | Retrait jusqu'a clarification |
| Drift de marche non documente | Pause + review |
| Telegram signal confondu avec ordre | Blocage du protocole Telegram |
| Vision-only decision sans invalidation | Rejet de l'observation |
| Changement de logique sans bump `strategy_version` | Invalidation du sample |

### 7.3_Message de retrait

Si `retirement_gate` recommande le retrait :

```json
{
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "0.1.0",
  "retirement_gate": {
    "verdict": "RETIRED_RECOMMENDED",
    "reason": "consecutive_failures_threshold",
    "consecutive_failures": 5,
    "action": "pause_observation_manual_review_required"
  }
}
```

---

## 8_HARD_BLOCKS_PERMANENTS

Les conditions suivantes bloquent toute promotion, quelle que soit la phase :

```text
No strategy_id
No strategy_version
No invalidation
No ObservationEvent evidence
No Perf Engine evidence
No kill switch validation for expansion
Telegram direct BUY/SELL
Vision-only decision
Automatic Sheets write as decision driver
Live or Bitget order path
```

Ces blocks sont absolus et herites de PR #510, #512, #513, #514.

---

## 9_DECISION_HUMAINE

Toute transition de lifecycle requiert une decision humaine documentee :

```text
Qui decide : operateur
Format     : note dans Trading Lab replay OU mise a jour manuelle du spec
Trace      : commit git sur spec file mis a jour
Historique : strategy_version bump si logique change
```

Le Perf Engine ne peut pas promouvoir seul.
Le bot vision ne peut pas promouvoir seul.
Le Telegram watch signal ne peut pas promouvoir seul.

---

## 10_TABLEAU_SYNTHESE

| Transition | Decideur | Conditions cles | Verdict initial |
| --- | --- | --- | --- |
| CANDIDATE -> OBSERVED | Humain + premier event | strategy_id, invalidation, 1er event | PENDING |
| OBSERVED -> PAPER_VALIDATED | Humain + Perf Engine | 30 runs, 14j, perf PASS | BLOCKED (< 30 runs) |
| PAPER_VALIDATED -> MULTI_SIGNAL | Humain | Phase 1 valide x2 periodes | Non ouvert en v0.1.0 |
| MULTI_SIGNAL -> LIVE_REVIEW_ONLY | Humain | Dossier complet, PR #510 | Non ouvert en v0.1.0 |
| -> RETIRED | Humain + gate | 5+ failures ou drift | Recommande automatiquement |

## RISKS

- À qualifier.
