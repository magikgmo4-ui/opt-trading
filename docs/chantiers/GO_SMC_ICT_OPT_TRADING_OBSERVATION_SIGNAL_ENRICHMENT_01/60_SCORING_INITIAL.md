---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: scoring_initial
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 60_SCORING_INITIAL

## Scoring initial de confiance : SMC_ICT_CHOCH_BOS_RETEST v0.1.0

---

## 1_OBJECTIF

Definir le calcul du champ `confidence` dans `ObservationEvent.signal.confidence`
pour la strategie `SMC_ICT_CHOCH_BOS_RETEST`.

`confidence` est un score entre 0.0 et 1.0.

Il reflette la qualite du setup observe, pas la probabilite de gain.

---

## 2_PRINCIPES

```text
confidence n'est pas un signal d'execution.
confidence seul ne peut pas promouvoir une strategie.
confidence est recalibre par le Perf Engine apres observation.
confidence est humainement verifiable via Trading Lab replay.
```

---

## 3_COMPOSANTES_DU_SCORE

### 3.1_Structure (max 0.35)

| Critere | Score |
| --- | --- |
| CHoCH cloture confirme sur `15m` | +0.20 |
| BOS cloture confirme sur `15m` | +0.15 |
| MSS confirme post-CHoCH | +0.15 |
| Alignement contexte `1h` | +0.10 |
| Alignement contexte `4h` supplementaire | +0.05 |

> Note : CHoCH et BOS ne sont pas additionnes, prendre le plus eleve.
> MSS s'ajoute si CHoCH presente.
> Score max structure = CHoCH (0.20) + MSS (0.15) + `1h` (0.10) + `4h` (0.05) = **0.50**

### 3.2_Liquidite / Sweep (max 0.30)

| Critere | Score |
| --- | --- |
| BSL/SSL identifie et sweep wick observe | +0.10 |
| EQH/EQL identifie et sweep observe | +0.12 |
| PDH/PDL ou PWH/PWL sweep | +0.15 |
| Sweep HTF confirme (`1h` ou `4h`) | +0.08 |
| Retour rapide apres sweep (< 3 bougies) | +0.05 |

> Note : les criteres de liquidite sont additifs jusqu'au max.
> Score max liquidite = PDH sweep (0.15) + HTF (0.08) + retour rapide (0.05) = **0.28**

### 3.3_FVG / OB / Premium-Discount (max 0.35)

| Critere | Score |
| --- | --- |
| FVG bullish/bearish identifie et valide | +0.10 |
| FVG retest partiel confirme (>= 50%) | +0.08 |
| Order Block identifie et valide | +0.08 |
| Confluence FVG + OB | +0.07 |
| Retest dans zone OTE (62-79% Fibonacci) | +0.07 |
| Filtre Premium/Discount respecte | +0.10 |

> Score max FVG/OB = FVG (0.10) + retest (0.08) + OB (0.08) + confluence (0.07) + OTE (0.07) + PD (0.10) = **0.50**

---

## 4_FORMULE

```text
confidence = min(
  CHoCH_or_BOS_score
  + MSS_score
  + HTF_alignment_score
  + sweep_score
  + fvg_ob_score
  + premium_discount_score,
  1.0
)
```

Plafonne a 1.0.

---

## 5_GRILLE_DE_REFERENCE

| Setup | Score attendu | Interpretation |
| --- | --- | --- |
| CHoCH + MSS + 1h alignement + PDH sweep + FVG+OB confluence + PD filtre | 0.80 - 1.00 | Setup de haute qualite |
| CHoCH + 1h alignement + FVG seul + PD filtre | 0.55 - 0.70 | Setup moyen, observable |
| CHoCH sans sweep + FVG seul | 0.35 - 0.50 | Setup faible, observation partielle |
| BOS seul sans sweep ni FVG | 0.15 - 0.30 | Observation tres limitee |
| Aucun signal clair | 0.00 - 0.15 | Pas d'observation |

---

## 6_SEUILS

| Seuil | Effet |
| --- | --- |
| `confidence >= 0.60` | Observation eligible pour Telegram watch signal |
| `confidence >= 0.70` | Observation eligible pour Trading Lab replay prioritaire |
| `confidence < 0.40` | Observation enregistree mais non envoyee en Telegram watch |
| `confidence` seul >= 0.90 | Non suffisant pour promotion (Perf Engine requis) |

Ces seuils sont provisoires en v0.1.0. Ils seront recalibres par le Perf Engine
apres accumulation de sample.

---

## 7_CONFIDENCE_CALIBRATION

Le Perf Engine calcule a posteriori :

```text
confidence_calibration = correlation(confidence_score, outcome_positive)
```

Si la correlation est faible ou negative, les poids du scoring sont revus.

En v0.1.0 : score non calibre, defini par design uniquement.

---

## 8_ANTI_PATTERNS

| Anti-pattern | Traitement |
| --- | --- |
| Bot vision seul sans CHoCH/BOS identifie | Score maximum 0.20 |
| Vision qui dit "BUY" sans regles SMC | Non valide; confidence = 0.0 |
| Screenshot seul sans invalidation definie | confidence plafonee a 0.30 |
| Score eleve sans evidence source definie | Non valide |

---

## 9_EXEMPLE_CONCRET

Setup observe le 2026-05-17 sur BTCUSDT 15m :

```text
CHoCH bullish cloture confirme     -> +0.20
MSS confirme post-CHoCH            -> +0.15
Alignement 1h (bearish -> reversal)-> +0.10
BSL sweep wick avant CHoCH         -> +0.10
Retour rapide apres sweep          -> +0.05
FVG bullish identifie et valide    -> +0.10
FVG retest 60% confirme            -> +0.08
OB valide en confluence            -> +0.08
FVG+OB confluence                  -> +0.07
Discount zone active               -> +0.10
OTE zone (entre 62-79%)            -> +0.07

Total brut                         = 1.10
Plafonne a                         = 1.00
confidence retenu                  = 0.92
```

En pratique, toutes les conditions optimales sont rarement reunies.
Une confidence de 0.62-0.72 est representatif d'un bon setup.

---

## 10_NO_RUNTIME_EFFECT

Ce document definit la formule de scoring.

Il ne declenche pas de trade, d'execution, de write Sheets, de Telegram
direct (hors dry-run valide) ni de modification de module runtime.

## RISKS

- À qualifier.
