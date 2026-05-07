---
doc_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01_VARIABLES_BOUNDS
doc_type: variables_bounds
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
status: draft_for_user_validation
lifecycle_stage: parent_variables_bounds
topic_keys:
  - opt-trading
  - trading
  - btc
  - bitget
  - coin-futures
  - accumulation
  - variables
  - bounds
  - risk-invariants
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
point_de_reprise: "Valider les variables, bornes, interdits, dependances et regles Bitget avant tout worker ou backtest."
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/index/inbox/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 02_variables_bounds - BTC COIN-M Accumulation Engine

## 13_ESTABLISHED

Le document `01_initial_project_doc.md` est valide `PASS` comme base canonique.

Le GO canonique actif est :

```text
GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
```

L'ancien libelle conceptuel :

```text
GO_BTC_COINM_ACCUMULATION_SHORT_ENGINE_MATH_BASE_01
```

est conserve comme ancien libelle non canonique et ne doit pas etre reutilise comme identifiant de chantier.

## 6_FINAL_TARGET

Deposer la table complete des variables, bornes, unites, dependances, valeurs interdites et garde-fous avant tout worker, backtest ou execution live.

## 12_INVARIANTS

```text
- short COIN-FUTURES = moteur de profit sur baisse, pas hedge principal
- objectif = accumulation BTC optimale
- BTC spot accumule non vendu dans le modele strategique normal
- pas de worker avant validation variables/bornes
- pas de backtest avant validation variables/bornes
- pas d'execution live
- z_short > z_dca
- funding, liquidation, PnL inverse et margin ratio doivent etre modelises precisement
- ne pas utiliser contractSize Binance
- ne pas supposer 1 contrat = 100 USD
- la taille short doit respecter minTradeNum
- la taille short doit respecter sizeMultiplier
- le prix doit respecter priceEndStep et tick_size derive
- le levier x125 est un maximum candidat, pas une obligation
- en cross margin Bitget, utiliser marginMode = crossed
```

## 13_ESTABLISHED - Exchange reference

Exchange cible : Bitget.

Product type :

```text
COIN-FUTURES
```

Contrat candidat :

```text
BTCUSD Coin-M perpetual futures
```

Parametres etablis publiquement :

```text
underlying_asset = BTC
settlement_asset = BTC
marginCoin = BTC
marginMode = crossed
tick_size_candidate = 0.1
max_leverage_candidate = 125
funding_interval_candidate = 8h
trading_time = 24/7
```

Endpoint de reference :

```text
GET /api/v2/mix/market/contracts?productType=COIN-FUTURES&symbol=BTCUSD
```

Parametres a recuperer par API avant toute borne finale :

```text
symbol
baseCoin
quoteCoin
supportMarginCoins
minTradeNum
sizeMultiplier
volumePlace
pricePlace
priceEndStep
minLever
maxLever
fundInterval
makerFeeRate
takerFeeRate
maxOrderQty
maxMarketOrderQty
maxSymbolOrderNum
symbolStatus
```

Funding endpoints de reference :

```text
GET /api/v2/mix/market/current-fund-rate?productType=COIN-FUTURES&symbol=BTCUSD
GET /api/v2/mix/market/history-fund-rate?productType=COIN-FUTURES&symbol=BTCUSD
```

Snapshot API public observe pendant la redaction de ce document :

```text
symbol = BTCUSD
baseCoin = BTC
quoteCoin = USD
supportMarginCoins = [BTC, STETH, XRP, ETH, USDE, USDC, BGB]
minTradeNum = 0.0001
sizeMultiplier = 0.0001
volumePlace = 4
pricePlace = 1
priceEndStep = 1
tick_size_derived = priceEndStep * 10^-pricePlace = 0.1
minLever = 1
maxLever = 125
fundInterval = 8
makerFeeRate = 0.0002
takerFeeRate = 0.0006
minTradeUSDT = 5
maxOrderQty = 200
maxMarketOrderQty = 50
maxSymbolOrderNum = 200
maxProductOrderNum = 1000
maxPositionNum = 150
symbolStatus = normal
fundingRate_snapshot = 0.0001
fundingRateInterval_snapshot = 8
minFundingRate_snapshot = -0.003
maxFundingRate_snapshot = 0.003
```

Interdits exchange immediats :

```text
- ne pas reprendre contractSize Binance
- ne pas supposer 1 contrat = 100 USD
- ne pas garder short_notional_usd arbitraire sans conversion Bitget reelle
- ne pas simuler sans minTradeNum, sizeMultiplier et tick_size derives
```

## 1_TABLE_COMPLETE_DES_VARIABLES

### 1.1 Variables d'etat

| Variable | Role | Unite | Min | Max | Dependances | Valeurs interdites | Hypothese initiale |
|---|---|---:|---:|---:|---|---|---|
| `P_t` | prix BTC de reference a `t` | USD/BTC | `> 0` | `<= 1000000` domaine de simulation | flux prix exchange | `<= 0`, `NaN` | `100000` |
| `S_t_btc` | stock BTC spot strategique | BTC | `0` | non borne par le modele | DCA spot, aucun sell normal | `< 0`, baisse strategique volontaire | `0.1000` |
| `U_t_usdt` | reserve liquide pour DCA | USDT | `0` | non borne par le modele | tresorerie, DCA | `< 0` | `10000` |
| `M_t_btc` | collateral COIN-FUTURES en BTC | BTC | `0` | non borne par le modele | transferts, PnL realise, fees, funding | `< 0` | `0.0200` |
| `M_t_usd` | valeur USD du collateral | USD | `0` | non borne par le modele | `M_t_btc`, `P_t` | calcule independamment de `M_t_btc * P_t` | derive |
| `Q_t_native` | taille short totale ouverte en unite native Bitget | native | `0` | `Q_max_native` et bornes exchange | fills, `sizeMultiplier`, `minTradeNum` | negative, hors grille | `0` |
| `E_t` | prix moyen d'entree short | USD/BTC | `> 0` si short ouvert | `<= 1000000` domaine de simulation | historique des fills | `<= 0` sur position ouverte | `null` tant que `Q_t_native = 0` |
| `N_t_usd` | notionnel USD equivalent du short | USD | `0` | derive du modele exchange | `Q_t_native`, `P_t`, `qty_to_notional_fn` | formule arbitraire copiee de Binance | `pending_exchange_formula` |
| `PnL_u_t_btc` | PnL latent short en BTC | BTC | non borne | non borne | `Q_t_native`, `E_t`, `P_t`, formule inverse Bitget | signe ignore, formule non validee | `0` |
| `PnL_r_t_btc` | PnL realise cumule en BTC | BTC | non borne | non borne | prises de profit, fermetures | double comptage avec wallet | `0` |
| `Funding_t_btc` | funding cumule en BTC | BTC | non borne | non borne | `fundingRate_t`, notionnel, `fundInterval` | signe ignore, intervalle ignore | `0` |
| `Fee_t_btc` | frais cumules en BTC | BTC | `0` si stocke en cout absolu | non borne | `makerFeeRate`, `takerFeeRate`, fills | cout negatif en valeur absolue | `0` |
| `MR_t` | margin ratio | ratio | `0` | non borne en theorie, borne de securite via `MR_max` | formule exchange | `< 0` | derive |
| `Liq_t` | prix de liquidation estime du short | USD/BTC | `> 0` si short ouvert | `<= 1000000` domaine de simulation | formule liquidation exchange | `<= 0`, manquant sur position ouverte | derive |
| `D_t` | distance a liquidation cote short | ratio | non borne | non borne | `Liq_t`, `P_t` | formule cote long, signe inverse | derive |
| `NAV_t_btc` | valeur nette systeme en BTC-equivalent | BTC | non borne | non borne | convention comptable choisie | double comptage PnL realise et marge | derive |
| `DD_t` | drawdown relatif du NAV | ratio | `0` | `1` | `NAV_t_btc`, pic historique | `< 0`, `> 1` | `0` |

### 1.2 Variables de decision

| Variable | Role | Unite | Min | Max | Dependances | Valeurs interdites | Hypothese initiale |
|---|---|---:|---:|---:|---|---|---|
| `z_dca` | ecart de prix entre deux DCA | ratio | `0.001` | `0.02` | volatilite, horizon | `<= 0` | `0.005` |
| `z_short` | ecart de prix entre deux ajouts de short | ratio | `z_dca + tick_size / P_t` | `0.10` | `z_dca`, volatilite | `<= z_dca` | `0.015` |
| `g_up` | hausse depuis pivot autorisant un short | ratio | `0.001` | `0.15` | logique signal | `<= 0` | `0.015` |
| `g_down` | baisse autorisant un TP short | ratio | `0.001` | `0.20` | logique signal | `<= 0` | `0.010` |
| `y_dca_usdt` | ticket DCA brut | USDT | `10` | `U_t_usdt` | reserve disponible | `<= 0`, `> U_t_usdt` | `200` |
| `r_transfer` | part du DCA transferee vers la marge BTC | ratio | `0` | `1` | regime de risque | `< 0`, `> 1` | `0.30` |
| `q_add_native` | taille d'un ajout short | native | `minTradeNum` | `min(maxOrderQty, Q_max_native - Q_t_native)` | `minTradeNum`, `sizeMultiplier`, risque | `< minTradeNum`, hors grille | `0.0010` |
| `tp1` | part de la position fermee au premier TP | ratio | `0` | `1` | `tp2`, `runner` | negatif, somme > `1` | `0.50` |
| `tp2` | part de la position fermee au second TP | ratio | `0` | `1` | `tp1`, `runner` | negatif, somme > `1` | `0.25` |
| `runner` | part residuelle laissee ouverte | ratio | `0` | `1` | `tp1`, `tp2` | negatif, `tp1 + tp2 + runner != 1` | `0.25` |
| `cooldown_dca_h` | delai minimal entre deux DCA | heures | `0` | `168` | cadence execution | negatif | `8` |
| `cooldown_short_h` | delai minimal entre deux ajouts short | heures | `0` | `168` | cadence execution | negatif | `8` |
| `leverage_target` | levier de travail cible | x | `1` | `maxLever` | exchange, politique risque | `< 1`, `> maxLever` | `2` |
| `margin_add_buffer_btc` | top-up manuel minimal de marge si risque | BTC | `0` | `S_t_btc` disponible ou apport externe | reserve BTC | negatif | `0.0020` |

### 1.3 Variables de risque

| Variable | Role | Unite | Min | Max | Dependances | Valeurs interdites | Hypothese initiale |
|---|---|---:|---:|---:|---|---|---|
| `D_min` | distance minimale a liquidation avant freeze short | ratio | `0.05` | `0.80` | `Liq_t`, volatilite | `<= 0` | `0.20` |
| `MR_max` | margin ratio maximal avant blocage | ratio | `0.05` | `0.95` | formule exchange | `<= 0`, `>= 1` | `0.60` |
| `Q_max_native` | exposition short totale maximale | native | `minTradeNum` | `maxOrderQty` ou cap strategie | capital, levier, conversion notionnel | hors grille, `> maxOrderQty` sans split explicite | `0.0200` |
| `U_floor_usdt` | reserve USDT minimale a conserver | USDT | `0` | `U_0_usdt` | tresorerie | negatif, `> U_0_usdt` | `1000` |
| `M_floor_btc` | collateral BTC minimal a conserver | BTC | `0` | `M_0_btc + transferts` | risque liquidation | negatif | `0.0100` |
| `funding_limit_btc_30d` | perte funding max toleree sur 30 jours | BTC | `0` | non borne par le modele | historique funding | negatif | `0.0010` |
| `fee_limit_btc_30d` | cout frais max tolere sur 30 jours | BTC | `0` | non borne par le modele | activite execution | negatif | `0.0005` |
| `slippage_max_bps` | slippage max accepte par ordre | bps | `0` | `1000` | liquidite, spread | negatif | `10` |
| `drawdown_max_nav` | drawdown NAV max tolere | ratio | `0` | `0.99` | convention comptable | negatif, `>= 1` | `0.35` |
| `max_short_adds_24h` | nombre max d'ajouts short par 24h | compte | `0` | `100` | regime execution | negatif, non entier | `6` |
| `max_open_orders` | nombre max d'ordres futures ouverts | compte | `0` | `maxSymbolOrderNum` | exchange, orchestration | negatif, `> maxSymbolOrderNum` | `20` |

### 1.4 Variables exchange et realite

| Variable | Role | Unite | Min | Max | Dependances | Valeurs interdites | Hypothese initiale |
|---|---|---:|---:|---:|---|---|---|
| `bitget_product_type` | product type Bitget | enum | `COIN-FUTURES` | `COIN-FUTURES` | GO actif | autre valeur | `COIN-FUTURES` |
| `bitget_symbol` | symbole exchange | enum | `BTCUSD` | `BTCUSD` | GO actif | autre valeur | `BTCUSD` |
| `underlying_asset` | sous-jacent | enum | `BTC` | `BTC` | contrat | autre valeur | `BTC` |
| `settlement_asset` | actif de reglement | enum | `BTC` | `BTC` | contrat | autre valeur | `BTC` |
| `marginCoin` | coin de marge utilise par API | enum | `BTC` | `BTC` | `supportMarginCoins` | coin non supporte ou non BTC dans ce GO | `BTC` |
| `marginMode` | mode de marge | enum | `crossed` | `crossed` | etat compte | `isolated` dans ce GO | `crossed` |
| `minTradeNum` | taille minimale de trade | native | API | API | endpoint contrats | `null`, `<= 0` | `0.0001` |
| `sizeMultiplier` | pas minimal de taille | native | API | API | endpoint contrats | `null`, `<= 0` | `0.0001` |
| `volumePlace` | precision max sur taille | digits | API | API | endpoint contrats | negatif, non entier | `4` |
| `pricePlace` | precision max sur prix | digits | API | API | endpoint contrats | negatif, non entier | `1` |
| `priceEndStep` | pas sur dernier digit de prix | entier | API | API | endpoint contrats | `null`, `<= 0` | `1` |
| `tick_size` | pas prix derive valide | USD | `priceEndStep * 10^-pricePlace` | `priceEndStep * 10^-pricePlace` | `priceEndStep`, `pricePlace` | valeur fixee hors API | `0.1` |
| `minLever` | levier minimal | x | API | API | endpoint contrats | `< 1` | `1` |
| `maxLever` | levier maximal | x | API | API | endpoint contrats | `< minLever` | `125` |
| `fundInterval` | intervalle funding | heures | API | API | endpoint contrats | `<= 0` | `8` |
| `makerFeeRate` | taux maker | ratio | API | API | endpoint contrats | negatif | `0.0002` |
| `takerFeeRate` | taux taker | ratio | API | API | endpoint contrats | negatif | `0.0006` |
| `supportMarginCoins` | liste collateraux supportes | ensemble | API | API | endpoint contrats | BTC absent | `[BTC, STETH, XRP, ETH, USDE, USDC, BGB]` |
| `maxOrderQty` | taille max ordre limite | native | API | API | endpoint contrats | `<= 0` | `200` |
| `maxMarketOrderQty` | taille max ordre market | native | API | API | endpoint contrats | `<= 0` | `50` |
| `maxSymbolOrderNum` | nombre max d'ordres ouverts sur le symbole | compte | API | API | endpoint contrats | `<= 0` | `200` |
| `symbolStatus` | statut de trading du contrat | enum | `normal` pour trader | `normal` pour trader | endpoint contrats | `maintain`, `suspend`, inconnu | `normal` |
| `fundingRate_t` | funding courant par intervalle | ratio | `fundingRateMin_api` | `fundingRateMax_api` | endpoint funding courant | `null`, stale | `0.0001` snapshot |
| `fundingRateMin_api` | borne min funding exchange | ratio | API | API | endpoint funding courant | `null` | `-0.003` |
| `fundingRateMax_api` | borne max funding exchange | ratio | API | API | endpoint funding courant | `null` | `0.003` |
| `qty_to_notional_fn` | regle de conversion taille native -> notionnel | fonction | requise | requise | specs Bitget finales | hypothese Binance `1 contrat = 100 USD` | `pending_bitget_formula` |

## 2_DEPENDANCES_ENTRE_VARIABLES

Dependances a figer pour toute simulation :

```text
tick_size = priceEndStep * 10^-pricePlace

price_valid(p) <=> p > 0 et p / tick_size est entier
qty_valid(q) <=> q >= minTradeNum et q / sizeMultiplier est entier

BTC_bought_t = y_dca_usdt / P_t
BTC_to_margin_t = (y_dca_usdt * r_transfer) / P_t
BTC_to_spot_t = (y_dca_usdt * (1 - r_transfer)) / P_t

S_t_btc_next = S_t_btc + BTC_to_spot_t
M_t_btc_next = M_t_btc + BTC_to_margin_t + PnL_r_increment_t - Funding_increment_t - Fee_increment_t

Q_t_native_next = Q_t_native + q_add_native - q_tp_native
Q_t_native_next <= Q_max_native

D_t = (Liq_t - P_t) / P_t   [orientation short uniquement]

freeze_new_shorts si D_t <= D_min
freeze_new_shorts si MR_t >= MR_max
freeze_new_shorts si U_t_usdt <= U_floor_usdt
freeze_new_shorts si symbolStatus != normal

tp1 + tp2 + runner = 1
z_short > z_dca > 0
1 <= leverage_target <= maxLever
```

Dependances qui restent explicitement en attente de spec exchange :

```text
N_t_usd = qty_to_notional_fn(Q_t_native, P_t, contract_meta)
PnL_u_t_btc = pnl_inverse_bitget_short(Q_t_native, E_t, P_t, contract_meta)
Liq_t = liquidation_bitget_cross_short(account_state, contract_meta)
MR_t = margin_ratio_bitget_cross(account_state, contract_meta)
Funding_increment_t = funding_bitget_short(Q_t_native, fundingRate_t, contract_meta)
```

## 3_VALEURS_INTERDITES

```text
- prix <= 0
- reserve ou collateral negatifs
- z_short <= z_dca
- g_up <= 0 ou g_down <= 0
- r_transfer < 0 ou > 1
- tp1 + tp2 + runner != 1
- leverage_target > maxLever
- q_add_native < minTradeNum
- q_add_native non multiple de sizeMultiplier
- prix ordre non multiple de tick_size
- marginMode != crossed dans ce GO
- symbolStatus != normal
- utilisation de contractSize Binance
- hypothese 1 contrat = 100 USD
- notionnel short sans qty_to_notional_fn validee Bitget
- simulation sans formule PnL inverse Bitget
- simulation sans formule liquidation Bitget
- simulation sans funding et fees
```

## 4_VALEURS_HYPOTHETIQUES_INITIALES

Jeu initial non optimise, uniquement pour premiers tests de coherence documentaire :

```text
P_0 = 100000 USD/BTC
S_0_btc = 0.1000 BTC
U_0_usdt = 10000 USDT
M_0_btc = 0.0200 BTC

z_dca = 0.005
z_short = 0.015
g_up = 0.015
g_down = 0.010
y_dca_usdt = 200
r_transfer = 0.30
q_add_native = 0.0010
tp1 = 0.50
tp2 = 0.25
runner = 0.25
cooldown_dca_h = 8
cooldown_short_h = 8
leverage_target = 2
margin_add_buffer_btc = 0.0020

D_min = 0.20
MR_max = 0.60
Q_max_native = 0.0200
U_floor_usdt = 1000
M_floor_btc = 0.0100
funding_limit_btc_30d = 0.0010
fee_limit_btc_30d = 0.0005
slippage_max_bps = 10
drawdown_max_nav = 0.35
max_short_adds_24h = 6
max_open_orders = 20
```

## 5_GARDE_FOUS_MATHEMATIQUES

```text
- Toujours suivre a la fois la vue BTC et la vue USD du collateral.
- Ne jamais melanger deux conventions comptables incompatibles dans NAV_t_btc.
- Ne jamais compter deux fois PnL realise et solde marge.
- Toute quantite derivee doit etre re-quantifiee sur la grille Bitget avant validation.
- Le funding doit rester signe ; pas de valeur absolue qui masque le sens du flux.
- La distance a liquidation doit etre calculee avec la formule cote short et non cote long.
- Un TP ne peut jamais rendre Q_t_native negatif.
- Q_t_native doit rester monotone avec les fills reels, pas avec des intentions d'ordre.
- Toute borne dependante de l'exchange doit etre rehydratee depuis l'API avant calcul.
```

## 6_GARDE_FOUS_EXCHANGE_REALITE

```text
- relire les metadonnees du contrat via /mix/market/contracts avant toute simulation serieuse
- bloquer toute simulation si symbolStatus != normal
- bloquer toute simulation si BTC n'est pas dans supportMarginCoins
- bloquer toute simulation si minTradeNum, sizeMultiplier ou tick_size sont absents
- bloquer toute simulation si marginMode != crossed pour ce GO
- ne pas changer de marginMode automatiquement si position ou ordre ouvert existent deja
- ne pas envoyer d'ordre limite > maxOrderQty
- ne pas envoyer d'ordre market > maxMarketOrderQty
- ne pas depasser maxSymbolOrderNum ordres ouverts sur le symbole
- relire current-fund-rate avant run et history-fund-rate pour les backtests
- considerer minTradeUSDT = 5 comme borne exchange actuelle tant que l'API confirme cette valeur
- utiliser makerFeeRate et takerFeeRate reels dans tous les calculs de cout
```

## 7_CONFLITS_DETECTABLES_AUTOMATIQUEMENT

| Code | Conflit | Detection automatique | Action |
|---|---|---|---|
| `ERR_CANONICAL_GO` | mauvais identifiant de chantier | `go_id != GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01` | rejet |
| `ERR_LEGACY_BINANCE_ASSUMPTION` | hypothese Binance injectee | presence de `contractSize = 100 USD` ou formule Binance legacy | rejet |
| `ERR_SYMBOL_MISMATCH` | mauvais contrat | `bitget_symbol != BTCUSD` ou `bitget_product_type != COIN-FUTURES` | rejet |
| `ERR_MARGIN_MODE` | mauvais mode de marge | `marginMode != crossed` | rejet |
| `ERR_PRICE_GRID` | prix hors grille | `price % tick_size != 0` | rejet |
| `ERR_QTY_GRID` | taille hors grille | `qty < minTradeNum` ou `qty % sizeMultiplier != 0` | rejet |
| `ERR_SHORT_TOO_DENSE` | short plus serre que DCA | `z_short <= z_dca` | rejet |
| `ERR_TP_SUM` | decomposition TP incoherente | `tp1 + tp2 + runner != 1` | rejet |
| `ERR_LEVERAGE_CAP` | levier hors borne | `leverage_target < minLever` ou `> maxLever` | rejet |
| `ERR_RISK_BREACH` | risque deja hors borne | `D_t <= D_min` ou `MR_t >= MR_max` | freeze short + alerte |
| `ERR_CAPITAL_FLOOR` | reserve insuffisante | `U_t_usdt < U_floor_usdt` ou `M_t_btc < M_floor_btc` | freeze short + alerte |
| `ERR_PNL_FORMULA_MISSING` | formule PnL manquante | `qty_to_notional_fn` ou `pnl_inverse_bitget_short` absent | rejet |
| `ERR_LIQ_FORMULA_MISSING` | formule liquidation manquante | `liquidation_bitget_cross_short` absent | rejet |
| `ERR_FUNDING_SERIES_MISSING` | funding absent ou stale | pas de `fundingRate_t` courant ou historique requis | rejet |
| `ERR_DOUBLE_COUNT_NAV` | comptabilite invalide | NAV reconstruit par deux conventions incompatibles | rejet |

## 8_PREPARATION_WORKER_CORRECTEUR

Entrees minimales du correcteur :

```text
- config strategie candidate
- snapshot contrat Bitget COIN-FUTURES BTCUSD
- snapshot funding courant
- serie funding historique si backtest
- etat initial capital spot / marge / reserve
- formule qty_to_notional_fn validee
- formule pnl_inverse_bitget_short validee
- formule liquidation_bitget_cross_short validee
```

Pipeline minimal du correcteur :

```text
1. verifier le GO, le symbole et le productType
2. verifier la presence des metadonnees exchange obligatoires
3. verifier la grille prix et taille
4. verifier les dependances mathematiques
5. verifier les bornes de risque
6. verifier l'absence d'hypothese Binance legacy
7. verifier la convention comptable NAV/PnL/funding/fees
8. produire verdict PASS ou REJECT avec codes d'erreur
```

Sorties attendues du correcteur :

```text
- verdict global
- liste des erreurs bloquantes
- liste des alertes non bloquantes
- snapshot normalise des bornes retenues
- trace des conversions prix / taille / notionnel
- justification explicite des rejets
```

## 9_REMAINING_GAP

Points encore a figer avant worker/backtest :

```text
- formule exacte qty_to_notional_fn pour BTCUSD COIN-FUTURES Bitget
- formule exacte de PnL inverse Bitget cote short
- formule exacte de liquidation / maintenance en cross margin Bitget
- regle definitive d'alimentation du DCA spot si la jambe spot n'est pas sur Bitget
- historique funding Bitget sur la fenetre de backtest ciblee
- politique finale de conversion entre reserve USDT et collateral BTC
```

## 10_RESUME_POINT

```text
Exchange cible corrige : Bitget.
Reference Binance exclue du modele.
Le contrat de reference est BTCUSD en COIN-FUTURES avec marge et settlement en BTC.
Les bornes exchange critiques disponibles sont deja : minTradeNum = 0.0001, sizeMultiplier = 0.0001, tick_size derive = 0.1, maxLever = 125, fundInterval = 8h.
Le moteur ne doit pas simuler sans formule Bitget validee pour conversion notionnel, PnL inverse, liquidation et margin ratio.
Le worker correcteur devra refuser toute configuration hors grille, hors bornes ou contenant une hypothese Binance legacy.
```
