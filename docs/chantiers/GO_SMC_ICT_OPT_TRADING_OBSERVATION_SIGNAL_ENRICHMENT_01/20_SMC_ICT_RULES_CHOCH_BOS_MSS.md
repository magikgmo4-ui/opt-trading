---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: strategy_rules_structure
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 20_SMC_ICT_RULES_CHOCH_BOS_MSS

## Regles de detection : CHoCH, BOS, MSS

---

## 1_OBJECTIF

Definir precisement les regles de detection des signaux de structure utilises
dans `SMC_ICT_CHOCH_BOS_RETEST`.

Ces regles sont les criteres d'evaluation que `bot_vision`, `tradingview` ou
un operateur applique pour identifier un evenement d'observation valide.

---

## 2_DEFINITIONS

### 2.1_Swing High / Swing Low

| Terme | Definition |
| --- | --- |
| **Swing High (SH)** | Bougie dont le High est superieur aux Highs des N bougies adjacentes (N >= 2). |
| **Swing Low (SL)** | Bougie dont le Low est inferieur aux Lows des N bougies adjacentes (N >= 2). |
| **Higher High (HH)** | SH superieur au SH precedent. |
| **Lower High (LH)** | SH inferieur au SH precedent. |
| **Higher Low (HL)** | SL superieur au SL precedent. |
| **Lower Low (LL)** | SL inferieur au SL precedent. |

**Parametre** : N = 2 minimum par defaut sur `15m`. Sur `1h/4h`, N peut etre ajuste au jugement.

---

### 2.2_CHoCH — Change of Character

**Definition** :

```text
CHoCH = rupture d'une structure precedente DANS LA DIRECTION OPPOSEE
        a la tendance dominante recente, validant un renversement potentiel.
```

**Regle bullish (renversement haussier) :**

```text
Context : serie de LL et LH (tendance baissiere)
Trigger : le prix depasse (cloture au-dessus) le dernier LH
Valide   : si la bougie de rupture est distincte (pas un simple wick)
Invalide : si le SL ayant genere le LH n'a pas ete teste (pas de sweep)
```

**Regle bearish (renversement baissier) :**

```text
Context : serie de HH et HL (tendance haussiere)
Trigger : le prix depasse (cloture en-dessous) le dernier HL
Valide   : si la bougie de rupture est distincte
Invalide : si le SH ayant genere le HL n'a pas ete teste
```

**Cloture requise :** Oui. Wick-only non valide.

---

### 2.3_BOS — Break of Structure

**Definition** :

```text
BOS = rupture d'une structure precedente DANS LA DIRECTION
      de la tendance dominante, confirmant la continuation.
```

**Regle bullish (continuation haussiere) :**

```text
Context : serie de HH et HL
Trigger : le prix depasse (cloture au-dessus) le dernier HH
Valide   : confirmation de la structure de tendance
```

**Regle bearish (continuation baissiere) :**

```text
Context : serie de LL et LH
Trigger : le prix depasse (cloture en-dessous) le dernier LL
Valide   : confirmation de la structure de tendance
```

**Distinction CHoCH vs BOS** :

| Signal | Direction par rapport a la tendance | Signification |
| --- | --- | --- |
| CHoCH | Opposee | Renversement potentiel |
| BOS | Identique | Continuation |

---

### 2.4_MSS — Market Structure Shift

**Definition** :

```text
MSS = confirmation que le CHoCH est etabli :
      apres un CHoCH, le prix forme un nouveau SH (si bullish)
      ou un nouveau SL (si bearish) dans la nouvelle direction.
```

**Regle :**

```text
Apres CHoCH bullish : premier HL valide = MSS confirme (bullish)
Apres CHoCH bearish : premier LH valide = MSS confirme (bearish)
```

**MSS vs CHoCH** :

| Terme | Moment | Force du signal |
| --- | --- | --- |
| CHoCH | Premier break de structure contraire | Signal initial, non confirme |
| MSS | Formation du premier HL/LH post-CHoCH | Confirmation, plus fiable |

---

## 3_TIMEFRAME_HIERARCHY

| Timeframe | Role |
| --- | --- |
| `4h`, `1h` | Contexte de structure majeure; direction dominante; pools de liquidite HTF |
| `15m` | Detection CHoCH/BOS; point d'entree observation |
| `5m` (optionnel) | Precision de l'entree si retest zone fine |

**Regle :** Un CHoCH sur `15m` a plus de valeur si il aligne avec le contexte `1h`.

---

## 4_INVALIDATION_RULES

| Condition | Consequence |
| --- | --- |
| Cloture au-dela du swing ayant genere le CHoCH/BOS | Setup invalide; observation annulee |
| Cloture en-dessous du HL post-CHoCH bullish | MSS echoue; setup degrade |
| Gap non comble dans zone d'entree | Evidence incomplète; confiance reduite |
| Mouvement de structure identifie par wick seul | Non valide; ne pas enregistrer |

---

## 5_DETECTION_CHECKLIST

Pour valider un CHoCH ou BOS dans un `ObservationEvent` :

```text
[ ] Swing High/Low identifies sur N >= 2 bougies adjacentes
[ ] Cloture de bougie confirme le break (pas wick only)
[ ] Direction alignee avec contexte 1h/4h (facultatif mais scoreeable)
[ ] Liquidite relevante (BSL/SSL) presente avant le CHoCH/BOS
[ ] Invalidation definie (swing qui invalide le setup)
[ ] Aucun ordre live associe
[ ] source_file ou vision evidence presente
```

---

## 6_SIGNAL_SCORING_PARTIEL

| Critere | Score partiel |
| --- | --- |
| CHoCH cloture confirme | +0.20 |
| BOS cloture confirme | +0.15 |
| MSS confirme post-CHoCH | +0.15 |
| Alignement contexte `1h` | +0.10 |
| Sweep visible avant CHoCH | +0.10 (voir doc 30) |
| FVG ou OB dans zone de retest | +0.15 (voir doc 40) |
| Premium/Discount aligne | +0.10 (voir doc 40) |
| Invalidation claire | +0.05 |

Score total max CHoCH/BOS/MSS : `0.55` (sans sweep ni FVG/OB).

---

## 7_NO_RUNTIME_EFFECT

Ce document definit des regles de detection.

Il ne declenche pas :

```text
execution code
scheduler
Bitget order
Google Sheets write
Telegram message direct (hors dry-run explicite)
```

## RISKS

- À qualifier.
