---
go_id: GO_SMC_ICT_OPT_TRADING_OBSERVATION_SIGNAL_ENRICHMENT_01
parent_go: GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01
doc_type: strategy_rules_zones
strategy_id: SMC_ICT_CHOCH_BOS_RETEST
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-17
---

# 40_SMC_ICT_RULES_FVG_OB_PREMIUM_DISCOUNT

## Regles de detection : FVG, Order Block, Premium/Discount

---

## 1_OBJECTIF

Definir les regles SMC/ICT relatives aux zones d'entree observee :
Fair Value Gap (FVG), Order Block (OB), et filtre Premium/Discount.

Ces zones constituent la `entry_zone` du spec `SMC_ICT_CHOCH_BOS_RETEST`.

---

## 2_FAIR_VALUE_GAP

### 2.1_Definition

```text
FVG (Imbalance) = ecart de prix entre les corps de 3 bougies consecutives
                  tel que la bougie 1 et la bougie 3 ne se chevauchent pas.
```

**Bullish FVG :**

```text
Bougie 1 High < Bougie 3 Low
L'espace entre Bougie1.High et Bougie3.Low est le FVG bullish.
```

**Bearish FVG :**

```text
Bougie 1 Low > Bougie 3 High
L'espace entre Bougie1.Low et Bougie3.High est le FVG bearish.
```

### 2.2_Validite

| Critere | Regle |
| --- | --- |
| Taille minimale | > 0.1% du prix de la bougie centrale (evite micro-FVG) |
| Formation dans un mouvement impulsif | Preferable (FVG dans tendance = plus fort) |
| FVG partiellement comble | Valide mais score reduit |
| FVG totalement comble | Non valide comme zone d'entree |

### 2.3_Retest du FVG

```text
L'observation se fait quand le prix retourne dans le FVG
apres le CHoCH/BOS, sans le cloturer totalement.
```

Le retest partiel (50%+ du FVG atteint) est acceptable.

---

## 3_ORDER_BLOCK

### 3.1_Definition

```text
Order Block (OB) = derniere bougie contraire avant un mouvement impulsif
                   qui a engendre un CHoCH, BOS ou une rupture significative.
```

**Bullish OB :**

```text
Derniere bougie baissiere avant un mouvement haussier impulsif.
Zone : [Low de l'OB, High de l'OB] ou [Open, Close] selon variante.
```

**Bearish OB :**

```text
Derniere bougie haussiere avant un mouvement baissier impulsif.
Zone : [High de l'OB, Low de l'OB] ou [Open, Close] selon variante.
```

### 3.2_Variantes

| Variante | Definition |
| --- | --- |
| Standard OB | Derniere bougie contraire avant le mouvement impulsif |
| Breaker Block | OB precedemment casse qui devient resistance/support |
| Mitigation Block | OB partiellement comble puis reprend la direction |
| Rejection Block | Concentration de wicks au niveau d'un OB |

Pour `SMC_ICT_CHOCH_BOS_RETEST v0.1.0` : Standard OB uniquement.

### 3.3_Validation

```text
[ ] Mouvement impulsif identifiable apres l'OB
[ ] OB non totalement comble precedemment
[ ] OB dans direction alignee avec CHoCH/BOS
[ ] Zone d'OB definie (High/Low de la bougie)
```

---

## 4_CONFLUENCE_FVG_OB

**Confluence = FVG et OB se superposent partiellement ou totalement.**

```text
Score maximal quand le retest touche a la fois la zone OB et le FVG.
```

| Situation | Score |
| --- | --- |
| FVG seul valide | Score partiel (voir section scoring) |
| OB seul valide | Score partiel |
| FVG + OB en confluence | Score maximal |
| Ni FVG ni OB | Zone d'entree non definie -> observation partielle |

---

## 5_PREMIUM_DISCOUNT

### 5.1_Definition

```text
Premium = prix au-dessus du 50% (midpoint) du dernier mouvement de structure majeure.
Discount = prix en-dessous du 50% du dernier mouvement de structure majeure.
```

**Calcul du range :**

```text
Range = du dernier Swing Low significatif au dernier Swing High significatif (sur 1h ou 4h).
Midpoint (50%) = (High + Low) / 2
Premium > Midpoint
Discount < Midpoint
```

**Equilibrium (EQ) :**

```text
Zone autour du Midpoint (+/- 5%).
Zone de rebalancement sans biais fort.
```

### 5.2_Regle de filtre

| Direction signal | Zone attendue pour entree |
| --- | --- |
| LONG watch | Discount (< 50% du range) ou EQ |
| SHORT watch | Premium (> 50% du range) ou EQ |
| LONG en Premium | Score reduit; non optimal |
| SHORT en Discount | Score reduit; non optimal |

### 5.3_Niveaux complementaires

| Niveau | Position dans le range |
| --- | --- |
| 79% (OTE - Optimal Trade Entry) | Zone d'entree ideale ICT en Premium |
| 62-79% (OTE zone) | Zone de Fibonacci ICT cle |
| 50% (Equilibrium) | Midpoint |
| 21-38% (OTE zone) | Zone Fibonacci cle en Discount |
| 21% (OTE - Discount) | Zone d'entree ideale ICT en Discount |

Ces niveaux sont informatifs et alimentent le scoring.

---

## 6_SCORING_FVG_OB_PREMIUM

| Critere | Score partiel |
| --- | --- |
| FVG bullish/bearish identifie et valide | +0.10 |
| FVG retest confirme (partiel >= 50%) | +0.08 |
| Order Block identifie et valide | +0.08 |
| Confluence FVG + OB | +0.07 |
| Retest dans zone OTE (21% ou 79%) | +0.07 |
| Filtre Premium/Discount respecte | +0.10 |
| Contexte EQ (zone neutre) | +0.03 |

Score max FVG/OB/Premium : `0.53` (cumulatif optimal).

---

## 7_ENTRY_ZONE_DEFINITION

La `entry_zone` dans le spec JSON est definie comme :

```json
{
  "entry_zone": {
    "kind": "fvg_ob_confluence",
    "description": "FVG ou OB retest apres CHoCH/BOS, idealement en zone Discount (LONG) ou Premium (SHORT)",
    "fvg": {
      "upper": null,
      "lower": null
    },
    "ob": {
      "upper": null,
      "lower": null
    },
    "premium_discount_filter": "active",
    "ote_zone": {
      "fib_lower": 0.62,
      "fib_upper": 0.79
    }
  }
}
```

Les valeurs `upper`/`lower` sont nulles dans le spec template et remplies
lors de l'observation concrete.

---

## 8_INVALIDATION_FVG_OB

| Condition | Consequence |
| --- | --- |
| FVG totalement comble avant retest | FVG invalide; chercher OB seul |
| OB totalement traverse sans reaction | OB invalide; setup degrade |
| Retest en zone Premium (pour LONG) | Score reduit; observation non optimale |
| Absence de FVG et OB apres CHoCH | Entry zone non definie; observation partielle seulement |

---

## 9_NO_RUNTIME_EFFECT

Ce document definit des regles de detection et de scoring.

Il ne declenche pas de trade, d'ordre, de write Sheets, de message Telegram
direct, ni de modification de module runtime.
