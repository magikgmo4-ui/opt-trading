---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01_REALITY_CLASSIFIER_SPEC
doc_type: reality_classifier_spec
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
status: draft_for_review
lifecycle_stage: child_reality_classifier_spec
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
topic_keys:
  - opt-trading
  - trading
  - btc
  - coin-futures
  - classifier
  - reality
  - exchange
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/03_reality_classifier_spec.md
point_de_reprise: "Definir le classifieur apres simulation pour separer validite math, realite exchange et irrealisme."
updated_at: 2026-05-08
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/01_param_space_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/02_simulation_result_schema.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/01_backtest_data_prep.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
---

# 03_reality_classifier_spec

## 1_MASTER_TARGET

Classer chaque resultat de simulation apres execution, sans avoir empeche a priori les configurations agressives ou irreelles, afin de separer clairement :

```text
- validite mathematique
- validite des donnees
- faisabilite exchange
- dependance a des hypotheses papier
- destruction ou gain net de BTC
```

## 2_OUTPUT_MODEL

Le classifieur produit :

```text
classification_primary : une seule classe dominante
classification_tags    : zero a n tags secondaires
reject_reasons         : liste machine-readable de causes
```

## 3_PRIMARY_CLASSES

Classes principales autorisees :

```text
MATH_INVALID
DATA_INVALID
LIQUIDATED
EXCHANGE_IMPOSSIBLE
PAPER_ONLY
REALISTIC
```

`OVERFIT_SUSPECT` est retenu comme tag secondaire par defaut, pas comme classe dominante, afin de ne pas ecraser la nature technique du run.

## 4_PRECEDENCE_ORDER

Ordre de priorite du classifieur :

```text
1. MATH_INVALID
2. DATA_INVALID
3. LIQUIDATED
4. EXCHANGE_IMPOSSIBLE
5. PAPER_ONLY
6. REALISTIC
```

Interpretation :

```text
- une erreur mathematique prime sur tout le reste
- un run liquide reste LIQUIDATED meme s'il etait aussi hors grille exchange
- un run exchange-impossible prime sur PAPER_ONLY
- REALISTIC n'est reserve qu'aux runs qui passent toutes les verifications disponibles
```

## 5_CLASS_RULES

### 5.1 MATH_INVALID

Classe `MATH_INVALID` si au moins une condition est vraie :

```text
- NaN ou inf dans un etat ou une metrique critique
- prix <= 0
- division par zero non recouverte
- timestamp non monotone ou manquant dans une trace critique
- tp1 + tp2 + runner != 1
- quantite ou reserve non finie
```

Codes conseilles :

```text
ERR_NAN_STATE
ERR_INF_STATE
ERR_NON_POSITIVE_PRICE
ERR_DIV_ZERO
ERR_TIME_NON_MONOTONIC
ERR_TP_SIMPLEX_INVALID
```

### 5.2 DATA_INVALID

Classe `DATA_INVALID` si les entrees historiques ne sont pas exploitables :

```text
- candles absentes ou corrompues
- funding history manquante pour des periodes requises
- contract snapshot absent
- gap temporel non documente au-dela de la tolerance admise
- mark/index mapping impossible pour les calculs requis
```

Codes conseilles :

```text
ERR_CANDLE_GAP
ERR_FUNDING_HISTORY_MISSING
ERR_CONTRACT_SNAPSHOT_MISSING
ERR_MARK_INDEX_MAPPING_MISSING
```

### 5.3 LIQUIDATED

Classe `LIQUIDATED` si la simulation atteint une liquidation effective :

```text
- prix de liquidation touche ou depasse
- equity <= maintenance margin au point de rupture defini
- position forcee a zero par logique de liquidation
```

Codes conseilles :

```text
ERR_LIQUIDATION_TRIGGERED
ERR_MARGIN_RATIO_COLLAPSE
```

Un run peut survivre a des breaches `D_min` ou `MR_max` sans etre liquide.
Dans ce cas il ne doit pas etre force dans `LIQUIDATED`.

### 5.4 EXCHANGE_IMPOSSIBLE

Classe `EXCHANGE_IMPOSSIBLE` si le run reste mathematiquement defini mais viole des contraintes exchange observables :

```text
- q_add_native non multiple de sizeMultiplier
- q_add_native < minTradeNum
- prix hors tick_size / priceEndStep
- leverage_target > maxLever ou < minLever
- ordre unitaire > maxOrderQty sans regle de split explicite
- nombre d'ordres > maxSymbolOrderNum sans mecanisme supporte
- marginCoin, symbol, productType ou marginMode incompatibles
```

Codes conseilles :

```text
ERR_QTY_OFF_GRID
ERR_QTY_BELOW_MIN
ERR_PRICE_OFF_TICK
ERR_LEVERAGE_ABOVE_MAX
ERR_LEVERAGE_BELOW_MIN
ERR_ORDER_QTY_ABOVE_MAX
ERR_TOO_MANY_OPEN_ORDERS
ERR_UNSUPPORTED_MARGIN_MODE
```

### 5.5 PAPER_ONLY

Classe `PAPER_ONLY` si le run est mathematiquement valide, non liquide, et exchange-feasible au mieux de ce qui est testable, mais depend encore d'une hypothese non verifiee ou d'un proxy documentaire.

Cas typiques :

```text
- formule encore PAPER_LOCKED et non API_VERIFIED
- MarkPrice historique remplace par un proxy
- table de risk tiers issue d'une reconstruction papier
- weekly gate demandee mais seulement specifiee, pas validee par implementation canonique
```

Codes conseilles :

```text
WARN_PAPER_LOCKED_FORMULA
WARN_MARK_PROXY_USED
WARN_PAPER_RISK_TIER
WARN_WEEKLY_GATE_SPEC_ONLY
```

### 5.6 REALISTIC

Classe `REALISTIC` seulement si tout ceci est vrai :

```text
- math_valid = true
- data_valid = true
- liquidation_count = 0
- aucune violation exchange bloquante
- aucune hypothese papier restante critique
- toutes les donnees et formules critiques sont verifiees au niveau requis
```

Note pratique :

```text
Tant que le projet reste sur des formules PAPER_LOCKED,
la plupart des runs seront probablement PAPER_ONLY plutot que REALISTIC.
```

## 6_SECONDARY_TAGS

Tags secondaires recommandes :

```text
OVERFIT_SUSPECT
BTC_POSITIVE
BTC_NEGATIVE
GUARD_BREACH_D_MIN
GUARD_BREACH_MR_MAX
GUARD_BREACH_Q_MAX
CAPITAL_EXHAUSTED
FUNDING_DESTRUCTIVE
EXTREME_DRAWDOWN
```

## 7_IMPOSSIBLE_VS_PAPER_ONLY

Frontiere retenue :

```text
EXCHANGE_IMPOSSIBLE
= le run viole une contrainte que l'exchange demanderait effectivement
  pour accepter la position ou l'ordre.

PAPER_ONLY
= le run pourrait etre coherent exchange, mais repose sur une approximation,
  une formule non API_VERIFIED, ou une source proxy non encore verrouillee.
```

Exemples :

```text
Profit fort mais q_add_native hors grille Bitget
-> EXCHANGE_IMPOSSIBLE

Profit fort, hors liquidation, grille respectee, mais MarkPrice historique proxifie
-> PAPER_ONLY

Profit fort, tout verifie, aucune approximation critique restante
-> REALISTIC
```

## 8_OVERFIT_SUSPECT_RULES

Le tag `OVERFIT_SUSPECT` est ajoute si au moins une situation apparait :

```text
- performance top in-sample mais negative en walk-forward
- resultat porte par tres peu de trades
- top score obtenu sur des parametres colles aux bornes
- resultat concentre sur une seule sous-periode anormale
```

Codes conseilles :

```text
WARN_WALK_FORWARD_COLLAPSE
WARN_TOO_FEW_TRADES
WARN_PARAMETER_AT_BOUNDARY
WARN_SINGLE_WINDOW_DOMINANCE
```

## 9_GUARD_BREACH_POLICY

Dans ce child, les garde-fous strategiques ne doivent pas recategoriser a eux seuls un run en `EXCHANGE_IMPOSSIBLE`.

Politique :

```text
- breach D_min / MR_max / Q_max_native -> tags et compteurs
- liquidation effective -> classe LIQUIDATED
- simple depassement prudent sans liquidation -> pas de refus primaire automatique
```

## 17_RESUME_POINT

```text
Le classifieur ne sert pas a empecher la simulation.
Il sert a dire, apres coup, ce qui etait numeriquement sain,
ce qui pouvait vraiment exister sur exchange,
et ce qui n'etait qu'un resultat papier ou impossible.
```
