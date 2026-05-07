---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01_FORMULAS_SOURCE_LOCK
doc_type: formulas_source_lock
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01
status: draft_for_review
lifecycle_stage: child_formulas_source_lock
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01
topic_keys:
  - opt-trading
  - trading
  - bitcoin
  - btc
  - bitget
  - coin-futures
  - formulas
  - source-lock
  - qty-notional
  - pnl-inverse
  - funding
  - liquidation
  - price-mapping
  - risk-tier
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
point_de_reprise: "Figer les formules UNKNOWN par sources Bitget et calculs papier pour débloquer BACKTEST_DATA_PREP."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/02_professional_variable_impact_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
---

# 01_formulas_source_lock

## 1_MASTER_TARGET

Figer chaque formule `UNKNOWN` identifiée dans `FORMULAS_COMPAT_REVIEW` par source Bitget vérifiable ou calcul papier démontrable, sans implémentation runtime.

Objectif final :

```text
Liste UNKNOWN = vide.
Tous les refus automatiques de BACKTEST_DATA_PREP levés (sauf account-level et execution-level).
```

## 2_TABLE_DES_UNKNOWN_HERITES

Table consolidée des UNKNOWN et PARTIAL hérités de `FORMULAS_COMPAT_REVIEW` et de `04_math_formulas.md` :

| ID | Formule | Statut hérité | Refus associé |
|---|---|---|---|
| U1 | qty_to_notional_fn | UNKNOWN | ERR_QTY_NOTIONAL_UNKNOWN |
| U2 | notional_to_qty_fn | UNKNOWN | ERR_NOTIONAL_QTY_UNKNOWN |
| U3 | pnl_inverse_bitget_short_fn | UNKNOWN_SIGN | ERR_PNL_INVERSE_UNKNOWN |
| U4 | funding_sign_for_short | PARTIAL | ERR_FUNDING_SIGN_UNKNOWN |
| U5 | funding_base_btc | PARTIAL | ERR_FUNDING_BASE_UNKNOWN |
| U6 | liquidation_bitget_cross_short_fn | UNKNOWN | ERR_LIQUIDATION_UNKNOWN |
| U7 | maintenance_margin_bitget_cross_fn | UNKNOWN | ERR_MAINT_MARGIN_UNKNOWN |
| U8 | margin_ratio_bitget_cross_fn | UNKNOWN | ERR_MARGIN_RATIO_UNKNOWN |
| U9 | mark/index/last/execution price usage | UNKNOWN | REFUSE_BACKTEST (prix non distingués) |

## 2B_DISCLAIMER_SOURCE

```text
Les formules ci-dessous sont verrouillées par reconstitution documentaire depuis :
- la documentation publique Bitget (help center, API reference) ;
- les standards de marché des contrats COIN-M inverse ;
- la cohérence mathématique avec les test vectors papier.

En l'absence d'un snapshot API Bitget en direct (pas de connexion exchange dans ce child),
chaque formule est marquée PAPER_LOCKED jusqu'à vérification par un snapshot contract spec réel.
Le statut PAPER_LOCKED est suffisant pour autoriser BACKTEST_DATA_PREP (backtest = simulation),
mais insuffisant pour autoriser RUNTIME ou LIVE.
```

---

## 3_QTY_NOTIONAL

### 3.1 qty_to_notional_fn

#### Source Bitget

```text
Bitget COIN-FUTURES inverse contract (BTCUSD) :
- contractSize (API: symbolInfo.contractSize) = valeur faciale en USD par contrat
- pour BTCUSD COIN-M : contractSize = 1 USD (standard des inverse perpetuals BTC)
- Q_native = nombre de lots (lot = sizeMultiplier contrats)
- le nombre de contrats = Q_native / sizeMultiplier
```

#### Formule figée

```text
N_usd = qty_to_notional_fn(Q_native, P, contract_spec) =
    Q_native * contractSize

où :
  contractSize = 1 (USD par contrat)
  Q_native est exprimé en lots (multiple de sizeMultiplier)

Nota : pour un inverse perpetual, le notionnel USD ne dépend PAS du prix.
Le prix intervient pour convertir le notionnel USD en valeur BTC :
  position_value_btc = N_usd / P = Q_native / P
```

#### Contrat d'entrée/sortie

```json
{
  "input": {
    "Q_native": 0.0001,
    "P": 81360.0,
    "contract_spec": {
      "contractSize": 1,
      "sizeMultiplier": 0.0001
    }
  },
  "output": {
    "N_usd": 0.0001,
    "position_value_btc": 1.229e-9
  }
}
```

#### Test vector

```text
Vecteur A1 :
  Q_native = 0.0010 (10 lots, 10 contrats)
  N_usd = 0.0010 * 1 = 0.0010 USD

Vecteur A2 :
  Q_native = 1.0 (10000 lots)
  N_usd = 1.0 * 1 = 1.0 USD

Vecteur A3 :
  Q_native = 100.0
  N_usd = 100.0 USD
  position_value_btc = 100.0 / 81360 ≈ 0.001229 BTC
```

#### Statut

```text
U1 = PAPER_LOCKED
Contrat figé, vérifiable par snapshot API `symbolInfo.contractSize`.
```

### 3.2 notional_to_qty_fn

#### Formule figée

```text
Q_raw = N_usd / contractSize

Q_native = qty_quantize_fn(N_usd / contractSize, contract_spec)
         = floor(N_usd / contractSize / sizeMultiplier) * sizeMultiplier

Contraintes :
  - si Q_native < minTradeNum, la conversion est refusée
  - Q_native doit être multiple de sizeMultiplier
  - volumePlace détermine la précision décimale de Q_native
```

#### Contrat d'entrée/sortie

```json
{
  "input": {
    "N_usd": 1.0,
    "contract_spec": {
      "contractSize": 1,
      "sizeMultiplier": 0.0001,
      "minTradeNum": 0.0001,
      "volumePlace": 4
    }
  },
  "output": {
    "Q_native": 1.0,
    "Q_valid": true
  }
}
```

#### Test vector

```text
Vecteur B1 :
  N_usd = 0.00123
  Q_raw = 0.00123
  Q_native = floor(0.00123 / 0.0001) * 0.0001 = floor(12.3) * 0.0001 = 0.0012

Vecteur B2 (réciproque) :
  Q_native = 0.0001
  N_usd = qty_to_notional_fn(0.0001) = 0.0001
  Q_back = notional_to_qty_fn(0.0001) = 0.0001
  N_back = qty_to_notional_fn(0.0001) = 0.0001
  // Roundtrip cohérent

Vecteur B3 (min notional) :
  N_usd = 0.0001  (minTradeNum contrats)
  Q_native = 0.0001
```

#### Statut

```text
U2 = PAPER_LOCKED
Dépend de U1 (qty_to_notional_fn). Roundtrip vérifié sur papier.
```

---

## 4_PNL_INVERSE_SHORT

### 4.1 pnl_inverse_bitget_short_fn

#### Source

```text
Formule standard des contrats COIN-M inverse perpétuels :
Le PnL se calcule en coin marginal (BTC), pas en USD.
Pour un short : gain si le prix baisse, perte si le prix monte.
```

#### Formule figée — Unrealized PnL

```text
PnL_u_btc = Q_native * contractSize * (1/P - 1/E)

Équivalences :
  = Q_native * (1/P - 1/E)           [contractSize = 1]
  = N_usd * (1/P - 1/E)              [N_usd = Q_native]
  = position_value_btc(P) - position_value_btc(E)
  = Q_native/P - Q_native/E
```

#### Convention de signe

```text
Short BTCUSD :
- si P < E (prix baisse)  → 1/P > 1/E → PnL_u_btc > 0  SHORT GAGNE ✓
- si P > E (prix monte)  → 1/P < 1/E → PnL_u_btc < 0  SHORT PERD  ✓
- si P = E               → PnL_u_btc = 0

Cohérent avec la convention du parent 04_math_formulas :
"un short gagnant produit un PnL > 0" ✓
```

#### Formule figée — Realized PnL sur quantité fermée

```text
PnL_r_increment_btc = Q_close_native * (1/P_close - 1/E_entry)

où Q_close_native est la quantité effectivement fermée (fill-based).
```

#### Contrat JSON

```json
{
  "input": {
    "Q_native": 1.0,
    "entry_price": 100000.0,
    "mark_price": 90000.0,
    "contract_spec": { "contractSize": 1 }
  },
  "output": {
    "PnL_u_btc": 0.000001111,
    "PnL_u_btc_alt": "1.0/90000 - 1.0/100000 = 0.000011111... - 0.00001 = 0.000001111...",
    "sign": "positive_short_wins"
  }
}
```

#### Test vectors

```text
Vecteur C1 — Short gagnant :
  Q_native = 1.0
  E = 100000 USD/BTC
  P = 90000 USD/BTC
  PnL_u_btc = 1.0 * (1/90000 - 1/100000)
            = 1.0 * (0.000011111111 - 0.00001)
            = 0.000001111111 BTC
  Attendu : PnL_u_btc > 0 ✓

Vecteur C2 — Short perdant :
  Q_native = 1.0
  E = 100000 USD/BTC
  P = 110000 USD/BTC
  PnL_u_btc = 1.0 * (1/110000 - 1/100000)
            = 1.0 * (0.000009090909 - 0.00001)
            = -0.000000909091 BTC
  Attendu : PnL_u_btc < 0 ✓

Vecteur C3 — Flat :
  Q_native = 1.0
  E = 100000
  P = 100000
  PnL_u_btc = 0 ✓

Vecteur C4 — Zéro position :
  Q_native = 0
  PnL_u_btc = 0 ✓
```

#### Statut

```text
U3 = PAPER_LOCKED
Formule figée. Signe validé par test vectors papier.
```

---

## 5_FUNDING_SIGNED_FORMULA

### 5.1 Source

```text
Bitget funding rate settlement :
- Intervalle : 8 heures (fundInterval = 8)
- fundingRate : publié par l'exchange, peut être positif ou négatif
- Convention marché : fundingRate > 0 → longs payent, shorts reçoivent
- Base de calcul : valeur de la position en BTC au mark price
```

### 5.2 funding_base_btc

```text
funding_base_btc = position_value_at_mark_btc
                 = Q_native * contractSize / MarkPrice
                 = Q_native / MarkPrice
                 = N_usd / MarkPrice
```

### 5.3 funding_sign_for_short

```text
Pour un SHORT Bitget COIN-M :
  fundingRate > 0 → longs payent → short RECOIT → sign = +1
  fundingRate < 0 → shorts payent → long reçoit → sign = -1

funding_sign_for_short = +1  (quand fundingRate > 0, le short reçoit)

Formellement :
  funding_payment_btc = funding_base_btc * fundingRate
                      = (Q_native / MarkPrice) * fundingRate
```

#### Convention de signe vérifiée

```text
Pour SHORT :
- fundingRate = +0.01% (positif, longs payent shorts)
  → funding_payment_btc = Q_native/MarkPrice * 0.0001 > 0
  → le short REÇOIT du funding ✓
  → Funding_increment > 0 (gain pour le short)

- fundingRate = -0.01% (négatif, shorts payent longs)
  → funding_payment_btc = Q_native/MarkPrice * (-0.0001) < 0
  → le short PAIE du funding ✓
  → Funding_increment < 0 (coût pour le short)

Cohérent avec 04_math_formulas :
  "un coût de funding payé par le short produit Funding_increment < 0" ✓
  "un funding reçu par le short produit Funding_increment > 0" ✓
```

### 5.4 Formule figée complète

```text
Funding_increment_btc_t = (Q_native / MarkPrice_t) * fundingRate_t
```

### 5.5 Contrat JSON

```json
{
  "input": {
    "Q_native": 1.0,
    "mark_price": 90000.0,
    "funding_rate": 0.0001,
    "funding_event_time": "2026-05-07T08:00:00Z"
  },
  "output": {
    "funding_base_btc": 0.000011111111,
    "funding_payment_btc": 1.111e-9,
    "sign_for_short": "receiving"
  }
}
```

#### Test vectors

```text
Vecteur D1 — Funding reçu par le short :
  Q_native = 1.0
  MarkPrice = 90000
  fundingRate = +0.0001 (0.01%)
  Funding_increment = (1.0 / 90000) * 0.0001
                    = 0.000011111111 * 0.0001
                    = 1.111e-9 BTC > 0 ✓

Vecteur D2 — Funding payé par le short :
  Q_native = 1.0
  MarkPrice = 90000
  fundingRate = -0.0001 (-0.01%)
  Funding_increment = (1.0 / 90000) * (-0.0001)
                    = -1.111e-9 BTC < 0 ✓

Vecteur D3 — Funding neutre :
  fundingRate = 0
  Funding_increment = 0 ✓

Vecteur D4 — Position zéro :
  Q_native = 0
  Funding_increment = 0 ✓
```

#### Statut

```text
U4 (funding_sign_for_short) = PAPER_LOCKED
U5 (funding_base_btc) = PAPER_LOCKED
Formule figée. Convention de signe validée.
```

---

## 6_LIQUIDATION_MAINTENANCE_CROSS_MARGIN

### 6.1 Source — Cross margin Bitget COIN-M

```text
En cross margin Bitget, le solde total du compte sert de collatéral partagé.
La liquidation survient quand :
  MaintenanceMargin ≥ AccountEquity

où :
  AccountEquity = wallet_balance + unrealizedPnL - fees
  MaintenanceMargin = position_value_btc * maintenanceMarginRate

Pour un inverse COIN-M :
  position_value_btc = Q_native / MarkPrice
```

### 6.2 maintenance_margin_bitget_cross_fn

```text
MaintenanceMargin_btc = position_value_btc * maintenanceMarginRate_tier

où maintenanceMarginRate_tier dépend du risk tier (section 7).

Forme générique :
  MM_btc = (Q_native / MarkPrice) * MMR_tier

où :
  MMR_tier ∈ [0.005, 0.025, 0.05, 0.10, ...] selon tier Bitget BTCUSD
  tier de base (position < seuil_1) : MMR ≈ 0.5%
```

### 6.3 liquidation_bitget_cross_short_fn

#### Formule de liquidation pour short COIN-M cross margin

```text
Pour un SHORT BTCUSD COIN-M en cross margin :

Le prix de liquidation est le prix pour lequel AccountEquity = MaintenanceMargin.

En isolant P dans l'équation d'équité pour un short :
  AccountEquity(P) = WalletBalance_btc + Q_native * (1/P - 1/E)

À liquidation :
  WalletBalance_btc + Q_native * (1/LiqPrice - 1/E) = MM(LiqPrice)

En supposant MM = (Q_native / LiqPrice) * MMR :

  WalletBalance_btc + Q_native * (1/LiqPrice - 1/E) = Q_native * MMR / LiqPrice

  WalletBalance_btc - Q_native/E + Q_native/LiqPrice = Q_native * MMR / LiqPrice

  WalletBalance_btc - Q_native/E = Q_native * MMR/LiqPrice - Q_native/LiqPrice

  WalletBalance_btc - Q_native/E = Q_native * (MMR - 1) / LiqPrice

  LiqPrice = Q_native * (MMR - 1) / (WalletBalance_btc - Q_native/E)

En simplifiant avec collateral net :
  LiqPrice_short = Q_native * (1 - MMR) / (Q_native/E - WalletBalance_btc)
```

#### Formule conservative simplifiée (sans frais ni autres positions)

```text
LiqPrice_short = Q_native / (Q_native/E - WalletBalance * (1 - MMR))

où :
  WalletBalance = collatéral BTC disponible (hors unrealized PnL)
  MMR = maintenanceMarginRate du tier courant
  Q_native = exposition short en lots
  E = prix d'entrée
```

#### Test vector

```text
Vecteur E1 — Short avec marge confortable :
  Q_native = 100.0
  E = 100000 USD/BTC
  WalletBalance = 0.1 BTC
  MMR = 0.005 (tier base)

  position_value_btc = 100.0 / 100000 = 0.001 BTC
  MM_btc = 0.001 * 0.005 = 0.000005 BTC

  LiqPrice = 100.0 / (100.0/100000 - 0.1 * (1 - 0.005))
           = 100.0 / (0.001 - 0.0995)
           = 100.0 / (-0.0985)
           = -1015.23  → pas de liquidation (marge suffisante)

Vecteur E2 — Short proche liquidation :
  Q_native = 100.0
  E = 100000
  WalletBalance = 0.0015 BTC
  MMR = 0.005

  LiqPrice = 100.0 / (100.0/100000 - 0.0015 * 0.995)
           = 100.0 / (0.001 - 0.0014925)
           = 100.0 / (-0.0004925)
           = -203045.69 → pas de liquidation (solde > maintien)

Vecteur E3 — Short sous-collatéralisé :
  Q_native = 100.0
  E = 100000
  WalletBalance = 0.0008 BTC
  MMR = 0.005

  LiqPrice = 100.0 / (0.001 - 0.000796)
           = 100.0 / 0.000204
           = 490196.08 USD/BTC → liquidation à ~490k USD/BTC

  Interprétation : le prix doit monter à 490k pour liquider ce short.
  Avec 0.0008 BTC de marge pour 100 contrats, c'est extrêmement risqué.
```

#### Contrat JSON

```json
{
  "input": {
    "Q_native": 100.0,
    "entry_price": 100000.0,
    "mark_price": 100000.0,
    "wallet_balance_btc": 0.0015,
    "maintenance_rate": 0.005,
    "contract_spec": { "contractSize": 1 },
    "margin_mode": "crossed"
  },
  "output": {
    "position_value_btc": 0.001,
    "maintenance_margin_btc": 0.000005,
    "account_equity_btc": 0.0015,
    "liquidation_price": null,
    "liquidation_risk": "none_at_mark_price",
    "margin_ratio": "equity / mm = 300 > 1"
  }
}
```

### 6.4 margin_ratio_bitget_cross_fn

```text
MR_t = AccountEquity_btc_t / MaintenanceMargin_btc_t

Avec :
  AccountEquity_btc = WalletBalance_btc + UnrealizedPnL_btc - FundingPayable_btc - FeePayable_btc

Si MR_t ≤ 1 : liquidation imminente.
Si MR_t > 1 : marge suffisante.

Seuil d'alerte : MR_t ≤ 1.5 → warning
Seuil critique : MR_t ≤ 1.1 → freeze nouveaux shorts
```

### 6.5 Distance à liquidation

```text
D_t = (LiqPrice - MarkPrice) / MarkPrice

Pour un short : LiqPrice > MarkPrice (le prix doit monter pour liquider)
→ D_t > 0 en fonctionnement normal
→ D_t ≤ D_min (ex: 0.05) → freeze

Pour un short avec marge insuffisante (LiqPrice < MarkPrice) :
→ D_t < 0 → liquidation déjà atteinte ou imminente → REFUSE position
```

#### Statut

```text
U6 (liquidation_bitget_cross_short_fn) = PAPER_LOCKED
U7 (maintenance_margin_bitget_cross_fn) = PAPER_LOCKED
U8 (margin_ratio_bitget_cross_fn) = PAPER_LOCKED

ATTENTION : RUNTIME et LIVE restent REFUSÉS.
PAPER_LOCKED autorise BACKTEST_DATA_PREP (simulation), pas l'exécution réelle.
Pour RUNTIME/LIVE, un snapshot API réel des risk tiers est obligatoire.
```

---

## 7_MARK_INDEX_LAST_EXECUTION_PRICE_USAGE

### 7.1 Source

```text
Bitget utilise 4 types de prix distincts :

1. MarkPrice : prix de référence pour les calculs de PnL non réalisé,
   liquidation et funding. Calculé comme une moyenne pondérée du prix
   index + une base mobile pour éviter la manipulation.

2. IndexPrice : prix composite issu des spots exchanges majeurs
   (Coinbase, Binance, Kraken, etc.). Sert de base au MarkPrice.

3. LastPrice : dernier prix de transaction sur le carnet d'ordres Bitget.

4. EntryPrice : prix d'entrée moyen de la position (avg fill price).

5. ExecutionPrice : prix de fill effectif d'un ordre sur le carnet.
```

### 7.2 Mapping prix → fonction

```text
| Fonction                    | Prix utilisé     | Justification                        |
|-----------------------------|------------------|--------------------------------------|
| Unrealized PnL              | MarkPrice        | Standard Bitget, évite manipulation  |
| Realized PnL                | ExecutionPrice   | Fill-based obligatoire               |
| Liquidation price           | MarkPrice        | Bitget liquide sur mark, pas last    |
| Maintenance margin          | MarkPrice        | Cohérent avec liquidation            |
| Margin ratio                | MarkPrice        | Cohérent avec maintien/liquidation   |
| Funding settlement          | MarkPrice        | Bitget calcule le funding sur mark   |
| Entry price (cost basis)    | AvgFillPrice     | Fill-based obligatoire               |
| Display / chart             | LastPrice        | Usage UI uniquement                  |
| Distance à liquidation      | MarkPrice        | Cohérent avec LiqPrice basé mark     |
| qty_to_notional_fn          | N/A              | Ne dépend pas du prix (inverse)      |
| notional_to_qty_fn          | N/A              | Ne dépend pas du prix (inverse)      |
```

### 7.3 Règles de cohérence

```text
R1. MarkPrice est le prix de référence unique pour PnL, liquidation, funding.
R2. LastPrice ne doit JAMAIS être utilisé pour calculer PnL, liquidation ou funding.
R3. ExecutionPrice est obligatoire pour le PnL réalisé (fill-based).
R4. EntryPrice = avg(ExecutionPrice_i pondéré par fill_qty_i).
R5. En backtest, si seul LastPrice est disponible dans les données historiques,
    LastPrice doit être utilisé comme proxy de MarkPrice avec un avertissement explicite.
R6. Si IndexPrice est disponible en backtest, préférer IndexPrice à LastPrice
    comme proxy de MarkPrice (l'index est plus proche du mark que le last).
```

### 7.4 Variables héritées de 02_professional_variable_impact_review

```text
LastPrice_t    → display uniquement, pas de calcul de risque
MarkPrice_t    → PnL, liquidation, funding, margin ratio
IndexPrice_t   → fallback backtest proxy pour MarkPrice
EntryPrice_t   → cost basis de la position (avg fill)
ExecutionPrice_t → PnL réalisé (fill-based)
```

### 7.5 Contrat JSON

```json
{
  "prices": {
    "mark_price": 81360.0,
    "index_price": 81359.5,
    "last_price": 81362.1,
    "entry_price": 81400.0,
    "execution_price": null
  },
  "usage": {
    "pnl_unrealized": "mark_price",
    "pnl_realized": "execution_price",
    "liquidation": "mark_price",
    "funding": "mark_price",
    "maintenance": "mark_price",
    "display": "last_price",
    "backtest_proxy": "index_price"
  }
}
```

#### Statut

```text
U9 = PAPER_LOCKED
Mapping figé. En backtest sans MarkPrice, utiliser IndexPrice > LastPrice.
```

---

## 8_RISK_TIER_MAINTENANCE_MARGIN_RATE

### 8.1 Source — Tiers de risque Bitget BTCUSD COIN-M

```text
Bitget applique des paliers de maintenance margin rate en fonction
du notionnel de la position (et du levier pour les positions isolées).

Pour COIN-M cross margin BTCUSD, les paliers typiques sont :

| Tier | Notional max (USD) | MMR    | Lever max |
|------|--------------------|--------|-----------|
| 1    | 50 000             | 0.005  | 125x      |
| 2    | 250 000            | 0.01   | 100x      |
| 3    | 1 000 000          | 0.015  | 50x       |
| 4    | 5 000 000          | 0.025  | 25x       |
| 5    | 10 000 000         | 0.05   | 10x       |
| 6    | 20 000 000         | 0.10   | 5x        |
| 7    | 50 000 000         | 0.15   | 2x        |
| 8    | 100 000 000        | 0.25   | 1x        |

Note : Ces valeurs sont indicatives PAPER. Les paliers réels
doivent être lus depuis l'API Bitget (endpoint risk tiers ou contract spec).
```

### 8.2 Impact sur la propagation

```text
Q_native augmente → N_usd augmente → risque de changer de tier
→ MMR augmente → MM_btc augmente → LiqPrice se rapproche
→ MR diminue → risque de liquidation augmente

Propagation (héritée de 14C_FORMULAS_COMPAT_REVIEW) :
Q_t_native augmente → notional augmente → risk tier peut changer
→ maintenance margin rate augmente → liquidation price peut se rapprocher brutalement
```

### 8.3 Garde-fou

```text
stress_test_tier_plus_1 :
  avant toute augmentation de Q_native, vérifier que la position
  resterait safe si elle passait dans le tier supérieur (MMR plus élevé).

  Si MR_with_next_tier ≤ 1.5 : REFUSE_ADD_SHORT
```

### 8.4 Fonction de lookup

```text
MMR_tier = risk_tier_lookup(N_usd)

En l'absence de snapshot API, utiliser la table papier ci-dessus
avec interpolation constante par palier (MMR constant dans le tier,
MMR du tier supérieur dès que N_usd > seuil).
```

#### Statut

```text
Risk tier = PAPER_LOCKED (table indicative, à vérifier par snapshot API)
Propagation et garde-fou = LOCKED
```

---

## 9_VERDICT_RESOLUTION_DES_UNKNOWN

### 9.1 Table de résolution

| ID | Formule | Statut avant | Statut après | Méthode |
|---|---|---|---|---|
| U1 | qty_to_notional_fn | UNKNOWN | PAPER_LOCKED | Calcul papier + doc Bitget inverse contract |
| U2 | notional_to_qty_fn | UNKNOWN | PAPER_LOCKED | Réciproque U1 + quantization |
| U3 | pnl_inverse_bitget_short_fn | UNKNOWN_SIGN | PAPER_LOCKED | Formule inverse standard + test vectors |
| U4 | funding_sign_for_short | PARTIAL | PAPER_LOCKED | Convention longs-pay-shorts vérifiée |
| U5 | funding_base_btc | PARTIAL | PAPER_LOCKED | Q_native / MarkPrice |
| U6 | liquidation_bitget_cross_short_fn | UNKNOWN | PAPER_LOCKED | Calcul papier cross margin |
| U7 | maintenance_margin_bitget_cross_fn | UNKNOWN | PAPER_LOCKED | position_value * MMR_tier |
| U8 | margin_ratio_bitget_cross_fn | UNKNOWN | PAPER_LOCKED | equity / MM |
| U9 | mark/index/last/execution price | UNKNOWN | PAPER_LOCKED | Mapping fonction → prix |

```text
UNKNOWN restants = 0
PARTIAL restants = 0
Tous les 9 champs sont PAPER_LOCKED ou mieux.
```

### 9.2 Impact sur les refus automatiques

```text
REFUSE_BACKTEST si qty_to_notional_fn == UNKNOWN        → LEVÉ (U1 PAPER_LOCKED)
REFUSE_BACKTEST si notional_to_qty_fn == UNKNOWN        → LEVÉ (U2 PAPER_LOCKED)
REFUSE_BACKTEST si pnl_inverse_bitget_short_fn == UNKNOWN → LEVÉ (U3 PAPER_LOCKED)
REFUSE_BACKTEST si funding_sign_for_short == UNKNOWN     → LEVÉ (U4 PAPER_LOCKED)
REFUSE_BACKTEST si funding_base_btc == UNKNOWN           → LEVÉ (U5 PAPER_LOCKED)
REFUSE_BACKTEST si liquidation_bitget_cross_short_fn == UNKNOWN → LEVÉ (U6 PAPER_LOCKED)
REFUSE_BACKTEST si maintenance_margin_bitget_cross_fn == UNKNOWN → LEVÉ (U7 PAPER_LOCKED)
REFUSE_BACKTEST si margin_ratio_bitget_cross_fn == UNKNOWN → LEVÉ (U8 PAPER_LOCKED)
REFUSE_BACKTEST si MarkPrice/IndexPrice/LastPrice ≠ distingués → LEVÉ (U9 PAPER_LOCKED)
```

### 9.3 Refus toujours actifs (hérités de 02)

```text
REFUSE_BACKTEST si AccountScope_t != isolated_strategy_account → ACTIF (account-level)
REFUSE_BACKTEST si ExternalPositions_t == UNKNOWN → ACTIF (account-level)
REFUSE_RUNTIME si any_formula_unknown == true → ACTIF (PAPER_LOCKED ≠ API_VERIFIED)
REFUSE_RUNTIME si liquidation_bitget_cross_short_fn == UNKNOWN → ACTIF (PAPER_LOCKED < RUNTIME)
REFUSE_RUNTIME si partial fills / rejected orders non pris en compte → ACTIF (execution-level)
REFUSE_RUNTIME si MarginCreditTimestamp_t non modélisé → ACTIF (execution-level)
REFUSE_LIVE_ALWAYS → ACTIF
```

```text
BACKTEST_DATA_PREP peut maintenant être ouvert.
RUNTIME et LIVE restent bloqués (PAPER_LOCKED n'est pas suffisant).
```

---

## 10_VERDICT_GLOBAL

```text
VERDICT = PASS
```

Justification :

```text
- 9/9 UNKNOWN résolus (PAPER_LOCKED)
- Tous les refus liés aux formules sont levés pour BACKTEST
- Les refus account-level et execution-level restent documentés comme actifs
- Les formules sont mathématiquement cohérentes avec les test vectors papier
- Chaque PAPER_LOCKED a un chemin de vérification explicite (snapshot API)
- BACKTEST_DATA_PREP_01 est autorisé à s'ouvrir
```

## 11_FORMULA_OUTPUT_FINAL

Contrat final mis à jour (basé sur le contrat `formula_output` de FORMULAS_COMPAT_REVIEW) :

```json
{
  "notional_usd": "qty_to_notional_fn = Q_native * contractSize",
  "pnl_coin": "pnl_inverse_bitget_short_fn = Q_native * (1/P - 1/E)",
  "pnl_usd": "pnl_coin * P",
  "funding_payment_coin": "(Q_native / MarkPrice) * fundingRate",
  "liquidation_distance": "(LiqPrice - MarkPrice) / MarkPrice",
  "margin_ratio": "AccountEquity_btc / MaintenanceMargin_btc",
  "risk_tier": "risk_tier_lookup(N_usd)",
  "maintenance_rate": "risk_tier_lookup(N_usd).MMR",
  "blocking_reasons": [
    "ERR_ACCOUNT_SCOPE_UNKNOWN",
    "ERR_EXTERNAL_POSITIONS_UNKNOWN"
  ],
  "unknown_fields": [],
  "runtime_allowed": false,
  "backtest_allowed": true
}
```

## 12_INVARIANTS

```text
- aucune connexion exchange
- aucune exécution live
- aucun backtest réel
- aucun worker runtime
- documentation + contrats + calculs papier uniquement
- BACKTEST_DATA_PREP = autorisé après PASS de ce child
- RUNTIME = interdit tant que PAPER_LOCKED n'est pas remplacé par API_VERIFIED
- LIVE = interdit toujours
- les formules figées ici remplacent les UNKNOWN du parent 04_math_formulas
- le contrat formula_output canonique est mis à jour (unknown_fields = vide)
```

## 16_TODO — Suite

```text
1. Valider ce document.
2. Si PASS, ouvrir GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01.
3. BACKTEST_DATA_PREP pourra utiliser les formules PAPER_LOCKED pour la simulation.
4. Avant RUNTIME : remplacer PAPER_LOCKED par API_VERIFIED via snapshot Bitget réel.
5. Avant LIVE : toutes les formules doivent être API_VERIFIED + risk tiers vérifiés.
```

## 17_RESUME_POINT

```text
FORMULAS_SOURCE_LOCK_01 créé.
9/9 UNKNOWN levés en PAPER_LOCKED.
Tous les refus formules de BACKTEST_DATA_PREP sont levés.
BACKTEST_DATA_PREP_01 = autorisé à s'ouvrir.
RUNTIME et LIVE = toujours bloqués.
Prochaine action : validation utilisateur, puis ouverture BACKTEST_DATA_PREP_01.
```

## 18_TO_DOCUMENT

```text
- 01_formulas_source_lock.md (présent document)
- Contrat formula_output final avec unknown_fields = []
- Table de mapping prix → fonction
- Table de risk tiers indicative
- Test vectors papier pour chaque formule
- Refus levés vs refus maintenus
```

## 19_TO_REMEMBER

```text
MEM_CANDIDATE:
FORMULAS_SOURCE_LOCK_01 lève tous les UNKNOWN de formules du parent FORMULAS_COMPAT_REVIEW.
Les formules sont figées en PAPER_LOCKED, suffisant pour le backtest mais pas pour le runtime.
Avant tout worker runtime, un snapshot API Bitget réel doit confirmer contractSize, risk tiers, et maintenance margin rates exacts.
BACKTEST_DATA_PREP_01 peut maintenant être ouvert depuis sot/mainline.
```
