---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: trading_lab_replay_instance
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 90_TRADING_LAB_REPLAY

## Trading Lab Replay : SMC_ICT_CHOCH_BOS_RETEST

---

## 1_OBJECTIF

Definir comment une observation `SMC_ICT_CHOCH_BOS_RETEST` devient rejouable
dans Trading Lab.

Replay = revoir le contexte, le signal, l'evidence, le plan et l'outcome.
Replay != reexecuter un ordre.

---

## 2_PREREQUIS_REPLAY

Un event `SMC_ICT_CHOCH_BOS_RETEST` est rejouable si :

```text
[ ] ObservationEvent complet avec strategy_id, strategy_version
[ ] smc_ict_detail presente (choch_observed ou bos_observed = true)
[ ] trade_plan.invalidation defini
[ ] evidence_source pointe vers au moins un fichier existant
[ ] source_file (journal daily) accessible
```

---

## 3_ARTEFACTS_NECESSAIRES

Pour `SMC_ICT_CHOCH_BOS_RETEST`, les artefacts de replay prioritaires :

| Type | Chemin | Priorite |
| --- | --- | --- |
| Vision summary | `data/desk_pro/vision/<run>/summary.json` | Haute |
| Vision analysis | `data/desk_pro/vision/<run>/analysis.md` | Haute |
| Vision screenshot | `data/desk_pro/vision/<run>/<timestamp>.png` | Haute |
| Journal daily | `data/journal/daily/<run_id>.json` | Haute |
| Webhook payload | `data/execution/<run_id>_webhook.json` | Moyenne |
| Perf Engine evidence | Produit par Perf Engine | Basse (apres accumulation) |

---

## 4_LABELS_SMC_ICT

Labels d'annotation specifiques a `SMC_ICT_CHOCH_BOS_RETEST` :

**Labels structure :**

```text
choch_confirmed
bos_confirmed
mss_confirmed
structure_ambiguous
structure_invalid
```

**Labels sweep/liquidite :**

```text
sweep_clear
sweep_absent
sweep_micro_only
liquidity_level_identified
liquidity_level_missing
```

**Labels FVG/OB :**

```text
fvg_valid
fvg_absent
ob_valid
ob_absent
fvg_ob_confluence
entry_zone_clear
entry_zone_ambiguous
entry_zone_missing
```

**Labels premium/discount :**

```text
pd_filter_respected
pd_filter_violated
ote_zone_active
ote_zone_absent
```

**Labels invalidation :**

```text
invalidation_clear
invalidation_missing
invalidation_triggered
invalidation_not_triggered
```

**Labels outcome :**

```text
valid_setup
invalid_setup
late_signal
early_signal
vision_unclear
market_data_missing
```

---

## 5_ETATS_REPLAY

| State | Definition |
| --- | --- |
| `REPLAY_MISSING` | Evidence insuffisante (pas de vision, pas de journal) |
| `REPLAY_READY` | Vision summary + journal present |
| `REPLAY_REVIEWED` | Operateur a annote avec labels |
| `REPLAY_INVALID` | Replay montre que le signal ne respecte pas le spec |

---

## 6_OUTPUT_CONCRET

```json
{
  "run_id": "20260517_001",
  "strategy_id": "SMC_ICT_CHOCH_BOS_RETEST",
  "strategy_version": "0.1.0",
  "replay_status": "REPLAY_READY",
  "labels": [
    "choch_confirmed",
    "sweep_clear",
    "fvg_ob_confluence",
    "pd_filter_respected",
    "invalidation_clear",
    "valid_setup"
  ],
  "review_notes": "CHoCH bullish confirme sur 15m apres BSL sweep. FVG et OB en confluence en zone Discount. Invalidation definie sous le swing precedent. Setup de qualite. Conserver en CANDIDATE jusqu'au seuil sample.",
  "confidence_review": 0.72,
  "promotion_impact": "NO_CHANGE",
  "perf_contribution": "VALID_SAMPLE"
}
```

---

## 7_WORKFLOW_REVIEW

Sequence d'un replay `SMC_ICT_CHOCH_BOS_RETEST` :

```text
1. Charger ObservationEvent du run_id
2. Charger vision summary et analysis
3. Verifier: CHoCH ou BOS sur 15m identifie dans la vision
4. Verifier: sweep de liquidite dans le contexte
5. Verifier: FVG ou OB dans la zone de retest
6. Verifier: filtre premium/discount respecte
7. Verifier: invalidation definie et testable
8. Annoter avec labels
9. Produire review_notes
10. Determiner promotion_impact:
    - NO_CHANGE si sample insuffisant
    - POSITIVE_EVIDENCE si setup confirme
    - NEGATIVE_EVIDENCE si setup invalide ou vision ambigue
11. Publier replay output (lecture seule pour Perf Engine)
```

---

## 8_INTEGRATION_PERF_ENGINE

Le replay output alimente Perf Engine via :

```text
labels -> contribution a false_positive_rate, invalidation_respected_rate
confidence_review -> contribution a confidence_calibration
perf_contribution = VALID_SAMPLE -> incremente sample_size
perf_contribution = INVALID_SETUP -> event exclu du sample positif
```

---

## 9_NO_RUNTIME_EFFECT

Trading Lab replay pour `SMC_ICT_CHOCH_BOS_RETEST` :

- ne modifie pas les journaux source;
- ne poste pas Telegram;
- ne declenche pas Google Sheets;
- ne declenche pas Bitget;
- ne change pas seul le lifecycle;
- ne modifie pas les modules runtime.

Il produit uniquement une evidence de review lisible par Perf Engine et LocalCMS.
