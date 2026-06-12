---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: strategy_rules_liquidity
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 30_SMC_ICT_RULES_SWEEP_LIQUIDITY

## Regles de detection : Sweep et Liquidite

---

## 1_OBJECTIF

Definir les regles SMC/ICT relatives au sweep de liquidite qui conditionne la
validite du CHoCH/BOS dans `SMC_ICT_CHOCH_BOS_RETEST`.

Un sweep de liquidite est le prerequis (non obligatoire mais scoreeable) qui
filtre les faux CHoCH.

---

## 2_DEFINITIONS

### 2.1_Liquidite

**Buy-Side Liquidity (BSL) :**

```text
Pool de stops/ordres situe au-dessus des Swing Highs.
Les longs qui vendent leurs stops sont la.
Les short sellers qui placent des SL au-dessus des SH sont la.
```

**Sell-Side Liquidity (SSL) :**

```text
Pool de stops/ordres situe en-dessous des Swing Lows.
Les longs qui placent des SL en-dessous des SL sont la.
Les short sellers qui protegent leur position sont la.
```

**Equal Highs (EQH) :**

```text
Deux Swing Highs ou plus au meme niveau.
Concentration de BSL visible et donc cible preferentielle.
```

**Equal Lows (EQL) :**

```text
Deux Swing Lows ou plus au meme niveau.
Concentration de SSL visible.
```

---

### 2.2_Sweep

**Definition :**

```text
Sweep = le prix depasse temporairement un niveau de liquidite
        (SH/SL, EQH/EQL, previous day high/low)
        avant de revenir dans le range.
```

**Formes de sweep :**

| Forme | Description |
| --- | --- |
| Wick sweep | Wick long qui traverse le niveau sans cloture au-dela |
| Body sweep | Cloture au-dela puis retour rapide (1-3 bougies) |
| Fast sweep | Mouvement impulsif rapide suivi de retour immediat |

---

### 2.3_Liquidite HTF

Les pools de liquidite sur `1h` et `4h` sont prioritaires car :

```text
Le marche va chercher la liquidite la plus significative.
Un sweep HTF suivi d'un CHoCH LTF (15m) est plus fiable.
```

**Types de liquidite HTF cibles :**

```text
Previous Day High / Low (PDH/PDL)
Previous Week High / Low (PWH/PWL)
Previous Session High / Low
Asian Range High / Low (pour crypto 00h-08h UTC)
```

---

## 3_REGLE_SWEEP_AVANT_CHOCH

**Regle principale :**

```text
Un CHoCH est PLUS VALIDE si un sweep de liquidite le precede.
Un CHoCH sans sweep est valide mais score moins.
```

**Sequence ideale :**

```text
1. Pool de liquidite visible (BSL ou SSL)
2. Prix sweepte la liquidite (wick ou body)
3. Prix retourne dans le range
4. CHoCH forme (break de structure contraire)
5. Retest FVG/OB -> observation
```

**Sequence acceptable (sans sweep) :**

```text
1. CHoCH forme sur structure technique
2. Retest FVG/OB -> observation (score reduit)
```

---

## 4_VALIDATION_SWEEP

Criteres de validation d'un sweep :

```text
[ ] Niveau de liquidite identifie avant le sweep (SH, SL, EQH, EQL, PDH, PDL)
[ ] Prix traverse le niveau (wick ou body)
[ ] Retour rapide observe (1 a 5 bougies max en 15m)
[ ] Volume spike optionnel (si disponible dans la source d'evidence)
[ ] Aucune cloture loin au-dela du niveau sans retour
```

---

## 5_SCORING_LIQUIDITE

| Critere | Score partiel |
| --- | --- |
| BSL/SSL identifie et sweep observe | +0.10 |
| EQH/EQL identifie et sweep observe | +0.12 |
| PDH/PDL ou PWH/PWL sweep | +0.15 |
| Sweep HTF (`1h`/`4h`) confirme | +0.08 |
| Retour rapide apres sweep (< 3 bougies) | +0.05 |
| Volume spike lors du sweep (si disponible) | +0.05 |

Score max liquidite : `0.55` (sur les criteres les plus favorables).

---

## 6_ANTI_PATTERNS

Situations a ne pas scorer comme sweep valide :

| Anti-pattern | Raison |
| --- | --- |
| Breakout directionnel sans retour | Ce n'est pas un sweep, c'est un break |
| Mouvement sans niveau de liquidite identifie | Score impossible, evidence insuffisante |
| Sweep micro (< 1 pip au-dela d'un SH mineur) | Signification faible |
| Sweep sur structure sans contexte `1h` etabli | Contexte manquant |

---

## 7_MAPPING_VERS_OBSERVATION_EVENT

Les champs d'evidence sweep attendus dans `ObservationEvent` :

```json
{
  "smc_ict": {
    "liquidity_level": "BSL",
    "liquidity_type": "swing_high",
    "sweep_observed": true,
    "sweep_form": "wick",
    "htf_reference": "PDH",
    "sweep_timeframe": "15m",
    "sweep_candle_index": null
  }
}
```

Ces champs sont des extensions nullables du champ `evidence` de `ObservationEvent`.

---

## 8_NO_RUNTIME_EFFECT

Ce document definit des regles de detection.

Il ne declenche pas de trade, d'ordre, de message Telegram direct, de write
Sheets, ni de modification de module runtime.

## RISKS

- À qualifier.
