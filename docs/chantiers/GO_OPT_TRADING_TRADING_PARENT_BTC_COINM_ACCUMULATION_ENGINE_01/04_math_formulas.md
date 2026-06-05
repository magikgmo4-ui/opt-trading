---
doc_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01_MATH_FORMULAS
doc_type: math_formulas
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
status: draft_for_user_validation
lifecycle_stage: parent_math_formulas
topic_keys:
  - opt-trading
  - trading
  - btc
  - bitget
  - coin-futures
  - formulas
  - pnl
  - liquidation
  - funding
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
point_de_reprise: "Valider les formules Bitget COIN-FUTURES avant tout backtest, worker runtime ou connexion exchange."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/index/inbox/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01.md
---

# 04_math_formulas - BTC COIN-M Accumulation Engine

## 6_FINAL_TARGET

Figer les formules mathematiques minimales necessaires au futur worker, sans backtest, sans connexion exchange et sans execution live.

## 12_INVARIANTS

```text
- formules uniquement
- aucune execution live
- aucun ordre
- aucune connexion exchange
- aucun backtest
- toute formule inconnue reste UNKNOWN
- toute formule UNKNOWN bloque le worker runtime en mode simulation_exploitable
- aucune hypothese Binance contractSize = 100 USD n'est autorisee
```

## 13_ESTABLISHED

Parametres exchange deja figes dans `02_variables_bounds.md` :

```text
exchange = Bitget
productType = COIN-FUTURES
symbol = BTCUSD
marginCoin = BTC
marginMode = crossed
minTradeNum = 0.0001
sizeMultiplier = 0.0001
pricePlace = 1
priceEndStep = 1
tick_size = 0.1
fundInterval = 8h
```

Convention de signe retenue dans ce document :

```text
- un short gagnant produit un PnL > 0
- un cout de funding paye par le short produit Funding_increment < 0
- un funding recu par le short produit Funding_increment > 0
- les frais sont modelises comme couts negatifs dans les increments de richesse nette
```

## 1_HYPOTHESES_EXPLICITES

Hypotheses de travail autorisees :

```text
H1. `Q_native` designe la taille native exchange, quantifiee par `sizeMultiplier`.
H2. `P` designe un prix BTCUSD en USD/BTC.
H3. `N_usd` designe un notionnel USD equivalent du short.
H4. `M_btc` designe le collateral disponible en BTC sur la jambe COIN-FUTURES.
H5. Le modele doit pouvoir raisonner en double vue : BTC et USD.
H6. Les fonctions de conversion notionnel <-> taille doivent rester explicitement separables du PnL.
```

Hypotheses encore non autorisees :

```text
- H_UNKNOWN_1 : interpretation definitive de `Q_native` en contrat ou coin quote exact
- H_UNKNOWN_2 : formule exacte de maintenance margin cross Bitget pour BTCUSD COIN-FUTURES
- H_UNKNOWN_3 : formule exacte du prix de liquidation cross Bitget tous ajustements inclus
```

## 2_PREPARATORY_FUNCTIONS

### 2.1 price_to_tick_fn

```text
tick_size = priceEndStep * 10^-pricePlace

price_to_tick_fn(P, contract_meta) = round(P / tick_size)
```

### 2.2 tick_to_price_fn

```text
tick_to_price_fn(k, contract_meta) = k * tick_size
```

### 2.3 qty_quantize_fn

```text
qty_quantize_fn(Q_raw, contract_meta) = floor(Q_raw / sizeMultiplier) * sizeMultiplier
```

### 2.4 qty_valid_fn

```text
qty_valid_fn(Q, contract_meta) <=>
    Q >= minTradeNum
    and Q / sizeMultiplier is integer
```

## 3_QTY_NOTIONAL_FORMULAS

### 3.1 qty_to_notional_fn Bitget

Forme generique retenue pour le worker :

```text
N_usd = qty_to_notional_fn(Q_native, P, contract_meta)
```

Definition documentaire minimale :

```text
qty_to_notional_fn doit satisfaire :
1. N_usd >= 0
2. qty_to_notional_fn(0, P, meta) = 0
3. fonction monotone croissante en Q_native pour P fixe
4. resultat exprimable en USD equivalent
5. inverse compatible avec notional_to_qty_fn sous quantification exchange
```

Forme temporaire acceptable seulement en `spec_only` :

```text
qty_to_notional_fn(Q_native, P, meta) = UNKNOWN_BITGET_CONTRACT_MAPPING
```

Motif : la signification economique exacte de `Q_native` pour `BTCUSD` COIN-FUTURES doit etre figee depuis la documentation contractuelle Bitget finale, sans recycler le mapping Binance.

### 3.2 notional_to_qty_fn Bitget

Forme generique retenue :

```text
Q_native = notional_to_qty_fn(N_usd, P, contract_meta)
```

Contraintes minimales :

```text
1. Q_native >= 0
2. qty_valid_fn(qty_quantize_fn(Q_native)) = true si N_usd >= notionnel minimal tradable
3. qty_to_notional_fn(notional_to_qty_fn(N_usd, P, meta), P, meta) approx N_usd
```

Statut actuel :

```text
notional_to_qty_fn = UNKNOWN tant que qty_to_notional_fn n'est pas figee
```

## 4_PNL_INVERSE_COINM

### 4.1 Forme generique de PnL inverse short

```text
PnL_u_btc = pnl_inverse_bitget_short_fn(Q_native, E, P, contract_meta)
```

Contraintes mathematiques minimales :

```text
1. pnl_inverse_bitget_short_fn(0, E, P, meta) = 0
2. si P = E, alors PnL_u_btc = 0
3. pour un short, si P baisse sous E, alors PnL_u_btc > 0
4. pour un short, si P monte au-dessus de E, alors PnL_u_btc < 0
5. la fonction doit etre coherente avec qty_to_notional_fn
```

Forme conceptuelle attendue d'un produit inverse BTC-margined :

```text
PnL_u_btc = exposure_factor(Q_native, contract_meta) * (1 / P - 1 / E)
```

ou, de facon equivalente :

```text
PnL_u_btc = inverse_multiplier(Q_native, contract_meta) * (E - P) / (P * E)
```

Zones UNKNOWN :

```text
- exposure_factor(Q_native, contract_meta) exact = UNKNOWN
- inverse_multiplier(Q_native, contract_meta) exact = UNKNOWN
```

Le worker runtime doit refuser toute simulation exploitable tant que ce facteur n'est pas fige.

### 4.2 PnL realise short

```text
PnL_r_increment_btc = realized_pnl_short_fn(Q_close_native, E_ref, P_close, contract_meta)
```

Contrainte de coherence :

```text
PnL_r_increment_btc doit suivre la meme famille de formule que PnL_u_btc,
mais appliquee uniquement a la quantite effectivement fermee.
```

## 5_MARGIN_BALANCE_EQUITY_UNREALIZED

### 5.1 Unrealized PnL

```text
UnrealizedPnL_btc_t = pnl_inverse_bitget_short_fn(Q_t_native, E_t, P_t, contract_meta)
```

### 5.2 Margin balance documentaire

Forme minimale preparatoire :

```text
MarginBalance_btc_t = M_wallet_btc_t + UnrealizedPnL_btc_t + FundingAccrued_btc_t + FeeAccrued_btc_t
```

avec :

```text
FeeAccrued_btc_t <= 0
FundingAccrued_btc_t peut etre > 0 ou < 0
```

### 5.3 Equity documentaire

```text
Equity_btc_t = MarginBalance_btc_t
```

ou, si Bitget distingue `wallet balance` et `equity` avec d'autres ajustements :

```text
Equity_btc_t = UNKNOWN_EXCHANGE_ADJUSTMENT_LAYER
```

Statut actuel :

```text
wallet_balance_vs_equity_exact_bitget = PARTIAL
```

Le document retient donc une forme minimale, sans pretendre reproduire tous les ajustements exchange runtime.

## 6_LIQUIDATION_DISTANCE

### 6.1 Distance a liquidation

Formule documentaire deja retenue :

```text
D_t = (Liq_t - P_t) / P_t
```

pour un short uniquement.

Interpretation :

```text
- D_t > 0 : le prix de liquidation est au-dessus du prix courant
- D_t proche de 0 : risque critique
- D_t <= D_min : freeze des nouveaux shorts
```

### 6.2 Prix de liquidation

```text
Liq_t = liquidation_bitget_cross_short_fn(account_state, contract_meta)
```

Statut actuel :

```text
liquidation_bitget_cross_short_fn = UNKNOWN
```

Contrainte minimale :

```text
si le collateral augmente a exposition constante, Liq_t doit s'eloigner du prix courant
si l'exposition short augmente a collateral constant, Liq_t doit se rapprocher du prix courant
```

## 7_MAINTENANCE_MARGIN_PLACEHOLDER

Forme documentaire cible :

```text
MaintenanceMargin_btc_t = maintenance_margin_bitget_cross_fn(Q_t_native, P_t, contract_meta, risk_tier_meta)
```

Statut actuel :

```text
maintenance_margin_bitget_cross_fn = UNKNOWN
risk_tier_meta = UNKNOWN
```

Forme de controle minimale en attendant :

```text
MR_t = margin_ratio_bitget_cross_fn(account_state, contract_meta)
MR_t = UNKNOWN tant que maintenance_margin_bitget_cross_fn reste UNKNOWN
```

Conclusion operative :

```text
pas de mode simulation_exploitable tant que maintenance margin et margin ratio ne sont pas figes
```

## 8_FUNDING_SIGNED_FORMULA

### 8.1 Funding incremental signe

```text
Funding_increment_btc_t = funding_bitget_short_fn(Q_t_native, fundingRate_t, contract_meta)
```

Contraintes minimales :

```text
1. fundingRate_t = 0 => Funding_increment_btc_t = 0
2. la fonction est lineaire en exposition a premiere approximation
3. le signe du funding recu/paye par le short doit etre explicite
```

Forme generique preparatoire :

```text
Funding_increment_btc_t = funding_sign_for_short(fundingRate_t, market_convention_t) * funding_base_btc(Q_t_native, P_t, contract_meta) * abs(fundingRate_t)
```

Zone UNKNOWN :

```text
- funding_sign_for_short exact selon convention Bitget finalisee = UNKNOWN
- funding_base_btc exact coherent avec le mapping contrat = UNKNOWN
```

Le backtest doit etre refuse tant que l'historique funding et la convention de signe ne sont pas figes.

## 9_NET_BTC_ACCUMULATION_FORMULA

### 9.1 Increment net BTC systeme

Forme documentaire minimale :

```text
NetBTC_increment_t = BTC_to_spot_t + PnL_r_increment_btc_t + Funding_increment_btc_t + Fee_increment_btc_t + ExternalMarginTopUp_btc_t - ForcedLoss_btc_t
```

avec :

```text
BTC_to_spot_t >= 0
Fee_increment_btc_t <= 0
ForcedLoss_btc_t >= 0
```

### 9.2 Stock net BTC final

```text
NetBTC_final = S_final_btc + M_final_btc + PendingReceivables_btc - PendingPayables_btc
```

Version strictement conservative pour premier worker :

```text
NetBTC_final_conservative = S_final_btc + M_final_btc
```

si et seulement si le modele prouve qu'il n'y a ni double comptage ni passif omis.

## 10_REFUSAL_CONDITIONS_IF_FORMULA_UNKNOWN

Le worker correcteur doit rejeter tout mode `simulation_exploitable` si l'un des champs suivants reste `UNKNOWN` :

```text
- qty_to_notional_fn
- notional_to_qty_fn
- pnl_inverse_bitget_short_fn
- liquidation_bitget_cross_short_fn
- maintenance_margin_bitget_cross_fn
- margin_ratio_bitget_cross_fn
- funding_sign_for_short
- funding_base_btc
```

Codes de refus a produire :

```text
ERR_QTY_NOTIONAL_UNKNOWN
ERR_NOTIONAL_QTY_UNKNOWN
ERR_PNL_INVERSE_UNKNOWN
ERR_LIQUIDATION_UNKNOWN
ERR_MAINT_MARGIN_UNKNOWN
ERR_MARGIN_RATIO_UNKNOWN
ERR_FUNDING_SIGN_UNKNOWN
ERR_FUNDING_BASE_UNKNOWN
ERR_FUNDING_HISTORY_MISSING
```

## 11_TEST_VECTORS_PAPIER

Ces vecteurs ne sont pas executables. Ils servent a verifier le sens des formules.

### Vecteur A - Short gagnant

```text
Q_native > 0
E = 100000
P = 90000

Attendu :
- qty_to_notional_fn > 0
- PnL_u_btc > 0
- Liq_t > P
- D_t > 0
```

### Vecteur B - Short perdant

```text
Q_native > 0
E = 100000
P = 110000

Attendu :
- PnL_u_btc < 0
- Liq_t se rapproche du prix courant
- D_t diminue
```

### Vecteur C - Zero position

```text
Q_native = 0

Attendu :
- N_usd = 0
- PnL_u_btc = 0
- Funding_increment_btc = 0
```

### Vecteur D - Funding neutre

```text
fundingRate_t = 0

Attendu :
- Funding_increment_btc = 0
```

### Vecteur E - Renfort marge

```text
Q_native constant
M_btc augmente

Attendu :
- Liq_t s'eloigne du prix courant
- D_t augmente
```

## 15_REMAINING_GAP

```text
- qty_to_notional_fn Bitget a figer
- notional_to_qty_fn Bitget a figer
- PnL inverse COIN-M a figer
- liquidation / maintenance cross margin a figer
- historique funding requis avant backtest
```

## 16_TODO

```text
1. Definir qty_to_notional_fn.
2. Definir notional_to_qty_fn.
3. Definir PnL inverse short.
4. Definir funding signe.
5. Definir equity / margin balance.
6. Definir distance liquidation.
7. Definir conditions de refus si formule UNKNOWN.
8. Ajouter test vectors papier.
```

## 17_RESUME_POINT

```text
04_math_formulas.md pose les fonctions mathematiques preparatoires pour le futur worker.
Les conversions notionnel <-> taille, le PnL inverse, le funding et la liquidation sont definis au moins comme contrats de fonction et contraintes de signe.
Les zones UNKNOWN sont explicites et bloquantes pour tout mode simulation_exploitable.
Le document reste purement documentaire : aucune connexion exchange, aucun backtest, aucune execution live.
```

## RISKS

- À qualifier.
