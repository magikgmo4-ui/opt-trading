---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01_PROFESSIONAL_VARIABLE_IMPACT_REVIEW
doc_type: professional_variable_impact_review
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01
status: draft_for_review
lifecycle_stage: professional_revalidation
parent_go_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
topic_keys:
  - opt-trading
  - trading
  - btc
  - bitcoin
  - gold
  - xauusd
  - bitget
  - coin-futures
  - formulas
  - compatibility
  - butterfly_effect
  - risk_review
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/02_professional_variable_impact_review.md
point_de_reprise: "Verdict PATCH_REQUIRED et conditions de passage a PASS avant tout BACKTEST_DATA_PREP."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
---

# 02_professional_variable_impact_review

## 1_MASTER_TARGET

Formaliser une revalidation professionnelle des variables BTC COIN-M avant toute autorisation de backtest, de worker runtime ou de live.

Objectif strict :

```text
confirmer que la base variable est solide,
documenter les effets de propagation manquants,
maintenir le blocage tant que le graphe dynamique complet n'est pas fige.
```

## 2_VERDICT_GLOBAL

```text
VERDICT = PATCH_REQUIRED
```

Ce n'est pas `FAIL` car les variables, garde-fous, interdits et dependances critiques sont deja largement poses.

Ce n'est pas `PASS` car l'effet papillon complet n'est pas encore formalise comme graphe dynamique et account-level.

Decision immediate :

```text
backtest_allowed = false
runtime_allowed = false
live_allowed = false
```

## 3_13_ESTABLISHED

### 3.1 Base variable deja bien couverte

Variables d'etat, de risque et d'exchange deja documentees dans `02_variables_bounds.md` :

```text
P_t
S_t_btc
U_t_usdt
M_t_btc
M_t_usd
Q_t_native
E_t
N_t_usd
PnL_u_t_btc
PnL_r_t_btc
Funding_t_btc
Fee_t_btc
MR_t
Liq_t
D_t
NAV_t_btc
DD_t
```

Variables de decision deja posees :

```text
z_dca
z_short
g_up
g_down
y_dca_usdt
r_transfer
q_add_native
tp1 / tp2 / runner
cooldown_dca_h
cooldown_short_h
leverage_target
```

Variables exchange Bitget deja posees :

```text
productType = COIN-FUTURES
symbol = BTCUSD
marginCoin = BTC
marginMode = crossed
supportMarginCoins
minTradeNum
sizeMultiplier
tick_size
maxLever
fundInterval
makerFeeRate
takerFeeRate
symbolStatus
fundingRate
qty_to_notional_fn
```

### 3.2 Decision saine deja en place

Les documents reconnaissent correctement que certains points restent `UNKNOWN` ou `PARTIAL` :

```text
qty_to_notional_fn
inverse pnl exact
funding signe
maintenance margin cross
liquidation cross margin
risk tier dynamique
```

Le systeme bloque donc correctement la suite operative tant que ces inconnues ne sont pas figees.

## 4_REVIEW_MATHEMATIQUE

### Verdict role math reviewer

```text
PATCH_REQUIRED
```

### Raison

Les variables existent, mais il manque un graphe causal formel du type :

```text
Variable A change
-> impact direct
-> impact indirect
-> risque secondaire
-> garde-fou
-> refus automatique
```

Exemple critique :

```text
BTC monte
-> la valeur USD du collateral BTC monte
-> mais le PnL short devient negatif
-> l'equity BTC peut baisser malgre un collateral USD plus haut
-> la liquidation price bouge
-> D_t doit etre recalcule
-> l'ajout short doit etre refuse si D_t < D_min
```

### Patch requis

Ajouter explicitement :

```text
dependency_graph
sensitivity_matrix
scenario_tree
path_dependency_rules
```

## 5_REVIEW_RISK_MANAGER

### Verdict role risk manager

```text
PATCH_REQUIRED
```

### Raison

Le modele dit bien `marginMode = crossed`, mais ne force pas encore assez la question account-level :

```text
la cross margin est-elle dediee a cette strategie,
ou partagee avec d'autres positions/collateraux ?
```

Le parent etablit aussi `supportMarginCoins = [BTC, STETH, XRP, ETH, USDE, USDC, BGB]`.
Donc `ExternalCollateral_t` ne doit pas rester un scalaire opaque : la composition du collateral externe peut changer l'equity, le margin ratio et la liquidation.

En cross margin partagee, d'autres surfaces peuvent changer :

```text
equity globale
margin ratio
liquidation price
risk tier
capacite d'ajout short
```

### Variables a ajouter

```text
AccountScope_t = isolated_strategy_account | shared_cross_account
ExternalPositions_t
ExternalCollateral_t
ExternalCollateralBreakdown_t
ExternalPnL_t
```

### Refus automatiques a ajouter

```text
REFUSE_BACKTEST si AccountScope_t != isolated_strategy_account
REFUSE_BACKTEST si ExternalPositions_t est inconnu
REFUSE_RUNTIME tant que liquidation cross margin exacte reste non figee
```

## 6_REVIEW_TRADING_EXECUTION

### Verdict role trading reviewer

```text
PATCH_REQUIRED
```

### Raison

Le modele n'integre pas encore assez la dynamique d'execution reelle :

```text
partial fills
slippage reel
spread
ordre rejete
latence
funding timestamp
mark price / index price / last price
liquidite disponible
```

### Variables a ajouter

```text
OrderState_t = planned | submitted | partial | filled | rejected | canceled
FillQty_t
AvgFillPrice_t
UnfilledQty_t
ExecutionLatency_ms
```

### Effet secondaire critique

```text
ordre short prevu mais non rempli
-> q reel inferieur
-> PnL attendu faux
-> funding attendu faux
-> distance de liquidation fausse
```

### Regle requise

```text
toute comptabilite runtime/backtest doit etre fill-based, pas intent-based.
```

## 7_REVIEW_SOFTWARE_ET_COMPATIBILITE

### Verdict role software architect

```text
PASS CONDITIONNEL
```

### Raison

La gouvernance anti-double-codage reste bonne :

```text
trading_lab_v1 pour le futur backtest
Desk Pro / ops_menu_hub / dashboard pour l'operateur
probability_engine pour le scoring si requis
risk_engine si compatible
```

Invariants a conserver :

```text
pas de nouvelle UI
pas de nouveau backtest engine
pas de second probability engine
pas de second risk engine si l'existant est compatible
pas de worker runtime avant PASS
```

## 8_REVIEW_PRODUIT_BTC_GOLD

### Verdict role product reviewer

```text
PASS CONDITIONNEL
```

### Raison

L'objectif final est clair :

```text
STRATEGIE_ROBUSTE_ACCUMULATION_BITCOIN_GOLD
```

Mais Gold doit rester hors scope du child BTC courant.

### Regle produit a expliciter

```text
Gold variables = OUT_OF_SCOPE_CURRENT_CHILD
```

### Variables futures Gold/XAUUSD

```text
XAU_P_t
GoldExposure_t
GoldDCA_t
GoldRisk_t
BTC_Gold_Correlation_t
CrossAssetAllocation_t
```

## 9_15_REMAINING_GAP

### 9.1 Graphe d'impact dynamique absent

Le modele reconnait les inconnues mais ne decrit pas encore formellement la propagation complete variable -> risque -> refus.

### 9.2 Cross margin pas assez account-level

Il faut distinguer :

```text
isolated_strategy_account
vs
shared_cross_account
```

### 9.3 Mark / index / last price non separes

`P_t` ne suffit pas pour liquidation, funding et PnL.

Variables a ajouter :

```text
LastPrice_t
MarkPrice_t
IndexPrice_t
EntryPrice_t
ExecutionPrice_t
```

Regle requise :

```text
toute formule de liquidation doit utiliser MarkPrice_t si l'exchange le fait.
```

### 9.4 Risk tier / maintenance margin dynamique insuffisant

Propagation a formaliser :

```text
Q_t augmente
-> notional augmente
-> risk tier peut changer
-> maintenance margin rate augmente
-> liquidation price peut se rapprocher brutalement
```

Garde-fou requis :

```text
REFUSE_ADD_SHORT si l'ajout change de risk tier,
sauf si le stress test tier+1 reste PASS.
```

### 9.5 Funding discret et path-dependent

Variables a ajouter :

```text
FundingEventTime_t
FundingAccrualMode_t
PositionSizeAtFunding_t
```

Regle requise :

```text
le funding doit etre calcule par evenement temporel,
pas seulement par bougie.
```

### 9.6 DCA spot -> marge COIN-M : latence et credit reel

Variables a ajouter :

```text
SpotBuyPrice_t
SpotFee_t
TransferLatency_t
MarginCreditTimestamp_t
```

Garde-fou requis :

```text
ne jamais compter le BTC transfere comme marge avant MarginCreditTimestamp_t.
```

## 10_MATRICE_BUTTERFLY_EFFECT

| Variable qui change | Impact direct | Impact secondaire | Garde-fou |
| --- | --- | --- | --- |
| `P_t` monte | short perd | equity peut baisser malgre collateral USD plus haut | recalcul `Liq_t`, `D_t`, `MR_t` |
| `P_t` baisse | short gagne | collateral BTC vaut moins en USD | recalcul NAV BTC/USD |
| `M_t_btc` augmente | marge renforcee | liquidation peut s'eloigner | ne compter qu'apres credit reel |
| `Q_t_native` augmente | exposition short monte | risk tier / maintenance peut changer | cap `Q_max`, tier stress |
| `z_short` baisse | shorts plus frequents | suraccumulation short | imposer `z_short > z_dca` |
| `r_transfer` augmente | marge COIN-M renforcee | accumulation spot reduite | borne `r_min/r_max` |
| `fundingRate_t` change | cout/revenu change | strategie peut devenir negative | funding stress 30j |
| `maker/taker fee` change | cout trading change | TP peut devenir non rentable | fee stress |
| `symbolStatus` change | trading suspendu/limite | ordres non executables | freeze |
| `MarkPrice_t` diverge | liquidation change | le chart peut tromper | utiliser mark price |
| `risk tier` change | maintenance augmente | liquidation se rapproche | tier+1 stress |
| `partial fill` | position reelle differente | PnL/funding faux | fill-based accounting |
| `Gold exposure` futur | allocation globale change | correlation BTC/Gold | child Gold separe |

## 11_NOUVELLES_VARIABLES_A_AJOUTER

Ajouter explicitement dans le modele ou dans le prochain patch documentaire :

```text
LastPrice_t
MarkPrice_t
IndexPrice_t
EntryPrice_t
ExecutionPrice_t
AccountScope_t
ExternalPositions_t
ExternalCollateral_t
ExternalPnL_t
RiskTier_t
MaintenanceRate_t
OrderState_t
FillQty_t
AvgFillPrice_t
UnfilledQty_t
ExecutionLatency_ms
FundingEventTime_t
FundingAccrualMode_t
PositionSizeAtFunding_t
SpotBuyPrice_t
SpotFee_t
TransferLatency_t
MarginCreditTimestamp_t
```

## 12_NOUVEAUX_REFUS_AUTOMATIQUES

Ces refus s'ajoutent aux refus deja poses dans `01_formulas_compat_review.md` et `04_math_formulas.md` ; ils ne les remplacent pas.

```text
REFUSE_BACKTEST si qty_to_notional_fn reste UNKNOWN
REFUSE_BACKTEST si notional_to_qty_fn reste UNKNOWN
REFUSE_BACKTEST si pnl_inverse_bitget_short_fn reste UNKNOWN
REFUSE_BACKTEST si AccountScope_t != isolated_strategy_account
REFUSE_BACKTEST si ExternalPositions_t est inconnu
REFUSE_BACKTEST si MarkPrice_t / IndexPrice_t / LastPrice_t ne sont pas distingues
REFUSE_BACKTEST si funding_sign_for_short ou funding_base_btc restent UNKNOWN
REFUSE_BACKTEST si l'historique funding exploitable manque
REFUSE_ADD_SHORT si l'ajout change de risk tier sans stress test tier+1 PASS
REFUSE_RUNTIME si maintenance_margin_bitget_cross_fn ou margin_ratio_bitget_cross_fn restent UNKNOWN
REFUSE_RUNTIME si liquidation cross margin exacte reste non figee
REFUSE_RUNTIME si partial fills / rejected orders ne sont pas pris en compte
REFUSE_RUNTIME si MarginCreditTimestamp_t n'est pas modele
```

## 13_CONDITIONS_DE_PASS

Le child, et non ce document pris seul, ne peut passer a `PASS` que si les deux blocs suivants sont documentes et relies au modele :

```text
Bloc A - prerequis formules deja bloquants dans 01/04
- qty_to_notional_fn / notional_to_qty_fn
- pnl_inverse_bitget_short_fn
- liquidation_bitget_cross_short_fn
- maintenance_margin_bitget_cross_fn / margin_ratio_bitget_cross_fn
- funding_sign_for_short / funding_base_btc
- historique funding exploitable avant backtest

Bloc B - completude professionnelle ajoutee par cette review
- MarkPrice_t / IndexPrice_t / LastPrice_t
- AccountScope_t / ExternalPositions_t / ExternalCollateral_t / ExternalCollateralBreakdown_t
- RiskTier_t / MaintenanceRate_t
- OrderState_t / FillQty_t / AvgFillPrice_t
- FundingEventTime_t
- TransferLatency_t / MarginCreditTimestamp_t
- matrice butterfly effect complete
- confirmation que la liquidation cross margin reste bloquante tant qu'elle n'est pas figee
```

## 14_DECISION_OPERATOIRE

```text
BACKTEST_DATA_PREP reste bloque.
```

Cette revue professionnelle confirme que la base documentaire est bonne, mais qu'une formalisation supplementaire est requise avant toute suite operative.

## 16_TODO

1. relier explicitement les nouvelles variables au document `02_variables_bounds.md` ;
2. enrichir `01_formulas_compat_review.md` avec la logique account-level et execution-level ;
3. garder `BACKTEST_DATA_PREP` bloque tant que ces patches ne sont pas faits ;
4. ouvrir un futur child Gold/XAUUSD separe si la couche cross-asset doit etre modelisee.

## 17_RESUME_POINT

```text
Revalidation pro effectuee.
Verdict = PATCH_REQUIRED.
La base est bonne, mais il faut documenter la matrice butterfly effect et les variables manquantes.
BACKTEST_DATA_PREP reste bloque.
```
