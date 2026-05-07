---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01_FORMULAS_COMPAT_REVIEW
doc_type: formulas_compat_review
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01
status: draft_for_review
lifecycle_stage: child_formulas_compat_review
parent_go_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
topic_keys:
  - opt-trading
  - trading
  - bitcoin
  - gold
  - btc
  - bitget
  - coin-futures
  - xauusd
  - formulas
  - compatibility
  - no-duplicate-coding
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
point_de_reprise: "Valider les formules BTC Bitget et leur compatibilité avec l'existant avant BACKTEST_DATA_PREP."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/02_professional_variable_impact_review.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
  - modules/trading_lab_v1/docs/ETABLI.txt
  - modules/desk_pro_runner/app/desk_pro_runner.py
  - modules/probability_engine/app/probability_engine.py
  - docs/ui_indexation/01_ui_registry_modules.md
---

# 01_formulas_compat_review

## 1_MASTER_TARGET

Figer la compatibilité des formules BTC Bitget COIN-FUTURES avec l'existant `opt-trading`, sans implémenter, sans backtester, sans connexion exchange, sans nouvelle UI et sans créer de module doublon.

Objectif final du programme :

```text
STRATEGIE_ROBUSTE_ACCUMULATION_BITCOIN_GOLD
```

Ce document reste focalisé sur BTC COIN-M. Gold/XAUUSD est reconnu comme cible finale produit, mais non implémenté ici.

## 2_INITIAL_PROJECT_DOC

Document initial validé :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/00_INITIAL_PROJECT_DOC.md
```

Validation utilisateur reçue :

```text
Validé.
```

## 3_INITIAL_NEED

Besoin actuel :

```text
Créer 01_formulas_compat_review.md après validation du 00_INITIAL_PROJECT_DOC.md.
```

Objectifs :

```text
- figer les fonctions/formules BTC Bitget encore critiques ;
- statuer leur compatibilité avec les modules existants ;
- refuser toute duplication ;
- préparer BACKTEST_DATA_PREP seulement après PASS.
```

## 4_MASTER_PROJECT_PLAN

1. Relire les documents parent `01/02/03/04`.
2. Consolider les surfaces existantes à réutiliser.
3. Mapper les fonctions mathématiques BTC vers l'existant.
4. Définir les contrats JSON minimaux.
5. Lister les formules qui restent `UNKNOWN`.
6. Refuser explicitement les duplications.
7. Produire un verdict `PASS / PATCH_REQUIRED / FAIL`.
8. Autoriser ou bloquer `BACKTEST_DATA_PREP`.

## 6_FINAL_TARGET

Sortie attendue du child :

```text
PASS si les formules critiques ont un emplacement d'intégration clair,
si les UNKNOWN restants sont explicitement bloquants,
si les blocages account-level et execution-level validés par `02` sont hérités ici,
et si aucun module/UI/backtest engine doublon n'est requis.
```

## 7_CANONICAL_STATE

Parent canonique mergé :

```text
GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
```

Child courant :

```text
GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01
```

Objectif final statué :

```text
Stratégie robuste d'accumulation Bitcoin + Gold
```

Portée courante :

```text
BTC Bitget COIN-FUTURES formulas compatibility review uniquement.
```

## 10_SELECTED_SETUP — Surfaces existantes à réutiliser

| Besoin | Surface existante à privilégier | Décision |
|---|---|---|
| Backtest futur | `modules/trading_lab_v1` | réutiliser / étendre, ne pas recréer |
| UI / opérateur | `desk_pro_runner`, `desk_pro_dashboard`, `ops_menu_hub` | réutiliser |
| Score / résumé analytique | `modules/probability_engine` | réutiliser si scoring requis |
| Risque / liquidation | `risk_engine` si compatible | adapter ou documenter gap, ne pas dupliquer |
| Dashboard | `desk_pro_dashboard` | pas de nouvelle UI |
| Menu opérateur | `ops_menu_hub` | pas de menu isolé |
| Gold/XAUUSD futur | Trading Dual Stack / Trading Lab / Desk Pro | child séparé |

## 12_INVARIANTS

```text
- aucune connexion exchange ;
- aucune exécution live ;
- aucun backtest réel ;
- aucun worker runtime ;
- aucune nouvelle UI ;
- aucun second backtest engine ;
- aucun second probability engine ;
- aucun second risk engine si risk_engine est compatible ;
- aucune duplication de fonction si une fonction existante peut être adaptée ;
- la cross margin doit rester modélisée account-level avant PASS ;
- toute comptabilité future doit rester fill-based et funding-event-based ;
- BTC et Gold partagent l'objectif produit mais gardent des formules séparées ;
- BACKTEST_DATA_PREP attend un verdict PASS du child complet, pas seulement de `02`.
```

## 13_ESTABLISHED — Existant utilisable

### trading_lab_v1

Établi : le module `trading_lab_v1` existe, suit le standard minimal `docs/scripts/app/install_shortcuts`, pointe vers des profils/schémas V1, sait produire des exemples event/trade, mais n'ouvre pas encore de backtest réel. Il sert de squelette opératoire de départ pour le LAB.

Décision :

```text
BACKTEST futur doit passer par trading_lab_v1 ou son extension cadrée.
Interdit de créer un moteur parallèle BTC backtest isolé.
```

### desk_pro_runner / desk_pro_dashboard / ops_menu_hub

Établi : `desk_pro_runner` orchestre le workflow Desk Pro, vérifie orchestrator/dashboard, lance l'orchestration, rend le dashboard, exporte JSON/HTML.

Décision :

```text
Toute sortie opérateur future doit viser Desk Pro existant.
Pas de nouvelle UI BTC/Gold isolée.
```

### probability_engine

Établi : `probability_engine` calcule des scores directionnels long/short à partir de features pondérées et d'un contexte derivatives optionnel, avec sortie JSON.

Décision :

```text
Si un score analytique BTC/Gold est requis, produire un contrat de features compatible probability_engine plutôt qu'un nouveau moteur.
```

### ui registry

Établi : le registre UI liste déjà `ops_menu_hub`, `desk_pro_dashboard`, `desk_pro_runner`, `probability_engine`, `risk_engine`, `market_scanner`, etc.

Décision :

```text
L'intégration opérateur doit passer par les surfaces UI déjà indexées.
```

## 14_HYPOTHESIS — Formules à figer

### H1 — qty_to_notional_fn Bitget

Hypothèse de travail :

```text
qty_to_notional_fn(qty, price, contract_spec) -> notional_usd
```

Dépend de :

```text
- productType = COIN-FUTURES
- symbol = BTCUSD
- sizeMultiplier
- minTradeNum
- contract value / contract unit Bitget réel
- mode coin-margined inverse
```

Statut :

```text
UNKNOWN tant que la formule exacte Bitget n'est pas validée par doc/API officielle.
```

### H2 — notional_to_qty_fn Bitget

Hypothèse de travail :

```text
notional_to_qty_fn(notional_usd, price, contract_spec) -> qty
```

Doit respecter :

```text
minTradeNum
sizeMultiplier
volumePlace
maxOrderQty
```

Statut :

```text
UNKNOWN tant que qty_to_notional_fn n'est pas figée.
```

### H3 — PnL inverse COIN-M short

Hypothèse générique inverse :

```text
pnl_coin = position_contract_value * (1 / exit_price - 1 / entry_price)
```

Pour un short, le signe doit être validé par convention Bitget.

Statut :

```text
UNKNOWN_SIGN tant que la convention exacte Bitget n'est pas figée.
```

### H4 — Funding signed formula

Formule conceptuelle :

```text
funding_payment = position_notional * funding_rate
```

Sens :

```text
positive/negative dépend du côté position et de la convention Bitget.
```

Statut :

```text
PARTIAL — formule notionnelle connue conceptuellement, signe Bitget à figer.
```

### H5 — Liquidation / maintenance cross margin

Formule conceptuelle :

```text
liquidation_distance = abs(mark_price - liquidation_price) / mark_price
```

Mais le calcul de `liquidation_price` dépend de :

```text
cross margin balance
maintenance margin rate
unrealized PnL
funding/frais
positions ouvertes
risk tier
```

Statut :

```text
UNKNOWN — doit bloquer tout worker runtime/backtest sérieux.
```

## 14B_BLOCKERS_HERITES_DE_02

Le document `02_professional_variable_impact_review.md` est validé comme revue professionnelle.

Conséquence canonique :

```text
02_PASS != CHILD_PASS
```

Le présent document hérite donc des blocages suivants avant toute autorisation de `BACKTEST_DATA_PREP`.

### B1 — Cross margin account-level

Variables minimales à relier explicitement au modèle :

```text
AccountScope_t = isolated_strategy_account | shared_cross_account
ExternalPositions_t
ExternalCollateral_t
ExternalCollateralBreakdown_t
ExternalPnL_t
```

Règles :

```text
- `supportMarginCoins` doit être conservé dans le snapshot contractuel ;
- une cross margin partagée ne peut pas être traitée comme un simple scalaire de marge ;
- si le compte n'est pas isolé stratégie ou si l'état externe est inconnu, le backtest reste refusé.
```

### B2 — Séparation des prix de travail

Variables minimales :

```text
LastPrice_t
MarkPrice_t
IndexPrice_t
EntryPrice_t
ExecutionPrice_t
```

Règle :

```text
la liquidation doit utiliser `MarkPrice_t` si Bitget s'appuie sur ce prix.
```

### B3 — Risk tier / maintenance margin dynamique

Variables minimales :

```text
RiskTier_t
MaintenanceRate_t
```

Propagation à figer :

```text
Q_t_native augmente
-> notional augmente
-> risk tier peut changer
-> maintenance margin rate augmente
-> liquidation price peut se rapprocher brutalement
```

### B4 — État d'exécution et partial fills

Variables minimales :

```text
OrderState_t = planned | submitted | partial | filled | rejected | canceled
FillQty_t
AvgFillPrice_t
UnfilledQty_t
ExecutionLatency_ms
```

Règle :

```text
toute comptabilité runtime/backtest doit être fill-based, pas intent-based.
```

### B5 — Funding discret et time-based

Variables minimales :

```text
FundingEventTime_t
FundingAccrualMode_t
PositionSizeAtFunding_t
```

Règle :

```text
le funding doit être calculé par événement temporel, pas seulement par bougie.
```

### B6 — DCA spot vers marge avec latence réelle

Variables minimales :

```text
SpotBuyPrice_t
SpotFee_t
TransferLatency_t
MarginCreditTimestamp_t
```

Règle :

```text
ne jamais compter le BTC transféré comme marge avant `MarginCreditTimestamp_t`.
```

## 14C_MATRICE_BUTTERFLY_EFFECT_MINIMALE

| Variable qui change | Impact direct | Impact secondaire | Garde-fou |
|---|---|---|---|
| `P_t` monte | short perd | l'equity peut baisser malgré un collateral USD plus haut | recalcul `Liq_t`, `D_t`, `MR_t` |
| `P_t` baisse | short gagne | le collateral BTC vaut moins en USD | recalcul NAV BTC/USD |
| `Q_t_native` augmente | l'exposition short monte | le risk tier peut changer | stress test tier+1 |
| `r_transfer` augmente | la marge COIN-M augmente | l'accumulation spot diminue | bornes `r_min/r_max` |
| `fundingRate_t` change | le coût/revenu change | la stratégie peut devenir négative | stress funding 30j |
| `MarkPrice_t` diverge | la liquidation change | le chart last price peut tromper | utiliser `MarkPrice_t` |
| `partial fill` | la position réelle diffère du plan | PnL/funding/liquidation faux | comptabilité fill-based |
| `symbolStatus` change | le trading devient suspendu ou limité | les ordres deviennent non exécutables | freeze |

## 15_REMAINING_GAP

```text
- formule exacte qty_to_notional_fn Bitget ;
- formule exacte notional_to_qty_fn Bitget ;
- signe exact PnL inverse short Bitget ;
- formule liquidation / maintenance cross margin ;
- risk tiers Bitget ;
- historique funding avant backtest ;
- modèle account-level de cross margin (`AccountScope_t`, `ExternalPositions_t`, `ExternalCollateral_t`, `ExternalCollateralBreakdown_t`, `ExternalPnL_t`) ;
- séparation explicite `LastPrice_t` / `MarkPrice_t` / `IndexPrice_t` / `ExecutionPrice_t` ;
- logique d'exécution fill-based (`OrderState_t`, `FillQty_t`, `AvgFillPrice_t`, `UnfilledQty_t`) ;
- timing de funding par événement (`FundingEventTime_t`, `FundingAccrualMode_t`, `PositionSizeAtFunding_t`) ;
- latence spot -> marge (`TransferLatency_t`, `MarginCreditTimestamp_t`) ;
- matrice butterfly effect reliée aux refus automatiques ;
- contrat JSON final compatible trading_lab_v1 ;
- contrat features compatible probability_engine si scoring requis ;
- contrat risk compatible risk_engine si disponible.
```

## 16_TODO — Contrats à produire dans la suite

### Contrat `contract_spec_snapshot`

```json
{
  "exchange": "bitget",
  "productType": "COIN-FUTURES",
  "symbol": "BTCUSD",
  "marginCoin": "BTC",
  "marginMode": "crossed",
  "supportMarginCoins": ["BTC", "STETH", "XRP", "ETH", "USDE", "USDC", "BGB"],
  "minTradeNum": 0.0001,
  "sizeMultiplier": 0.0001,
  "volumePlace": 4,
  "pricePlace": 1,
  "priceEndStep": 1,
  "tickSize": 0.1,
  "maxLever": 125,
  "fundInterval": 8,
  "makerFeeRate": 0.0002,
  "takerFeeRate": 0.0006,
  "symbolStatus": "normal",
  "source": "api_snapshot_or_official_doc",
  "captured_at": "ISO-8601"
}
```

### Contrat `formula_input`

```json
{
  "timestamp": "ISO-8601",
  "symbol": "BTCUSD",
  "last_price": 81360.0,
  "mark_price": 81360.0,
  "index_price": 81359.5,
  "execution_price": null,
  "qty": 0.0001,
  "fill_qty": 0.0,
  "side": "short",
  "entry_price": 81360.0,
  "funding_rate": 0.00005,
  "funding_event_time": "ISO-8601",
  "funding_accrual_mode": "event_based",
  "position_size_at_funding": 0.0001,
  "account_scope": "isolated_strategy_account",
  "external_positions": [],
  "external_collateral": 0.0,
  "external_collateral_breakdown": [],
  "external_pnl_btc": 0.0,
  "risk_tier": null,
  "maintenance_rate": null,
  "order_state": "planned",
  "avg_fill_price": null,
  "unfilled_qty": 0.0001,
  "execution_latency_ms": null,
  "spot_buy_price": null,
  "spot_fee_btc": null,
  "transfer_latency_ms": null,
  "margin_credit_timestamp": null,
  "contract_spec_snapshot": {}
}
```

### Contrat `formula_output`

```json
{
  "notional_usd": null,
  "pnl_coin": null,
  "pnl_usd": null,
  "funding_payment_coin": null,
  "liquidation_distance": null,
  "margin_ratio": null,
  "risk_tier": null,
  "maintenance_rate": null,
  "blocking_reasons": [
    "ERR_ACCOUNT_SCOPE_UNKNOWN",
    "ERR_MARK_PRICE_MODEL_MISSING"
  ],
  "unknown_fields": [
    "qty_to_notional_fn",
    "notional_to_qty_fn",
    "pnl_inverse_bitget_short_fn",
    "liquidation_bitget_cross_short_fn",
    "maintenance_margin_bitget_cross_fn",
    "margin_ratio_bitget_cross_fn",
    "funding_sign_for_short",
    "funding_base_btc"
  ],
  "runtime_allowed": false,
  "backtest_allowed": false
}
```

## 16_TODO — Refus automatiques

Ces refus héritent de `02_professional_variable_impact_review.md` et de `04_math_formulas.md`.

```text
REFUSE_BACKTEST si qty_to_notional_fn == UNKNOWN
REFUSE_BACKTEST si notional_to_qty_fn == UNKNOWN
REFUSE_BACKTEST si pnl_inverse_bitget_short_fn == UNKNOWN
REFUSE_BACKTEST si funding_sign_for_short == UNKNOWN
REFUSE_BACKTEST si funding_base_btc == UNKNOWN
REFUSE_BACKTEST si liquidation_bitget_cross_short_fn == UNKNOWN
REFUSE_BACKTEST si maintenance_margin_bitget_cross_fn == UNKNOWN
REFUSE_BACKTEST si margin_ratio_bitget_cross_fn == UNKNOWN
REFUSE_BACKTEST si funding_history_exploitable == MISSING
REFUSE_BACKTEST si AccountScope_t != isolated_strategy_account
REFUSE_BACKTEST si ExternalPositions_t == UNKNOWN
REFUSE_BACKTEST si MarkPrice_t / IndexPrice_t / LastPrice_t ne sont pas distingués
REFUSE_RUNTIME si any_formula_unknown == true
REFUSE_RUNTIME si liquidation_bitget_cross_short_fn == UNKNOWN
REFUSE_RUNTIME si partial fills / rejected orders ne sont pas pris en compte
REFUSE_RUNTIME si MarginCreditTimestamp_t n'est pas modélisé
REFUSE_ADD_SHORT si changement de risk tier sans stress test tier+1 PASS
REFUSE_UI_NEW_BUILD si desk_pro_dashboard compatible
REFUSE_MODULE_NEW_BUILD si trading_lab_v1/probability_engine/risk_engine compatible
REFUSE_LIVE_ALWAYS dans ce child
```

## 8_VALIDATED_PLAN — Prochaine séquence après ce document

1. Relire ce `01_formulas_compat_review.md`.
2. Produire verdict : `PASS / PATCH_REQUIRED / FAIL`.
3. Si `PATCH_REQUIRED`, corriger ce document.
4. Si `PASS`, ouvrir `GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01`.
5. Ne pas ouvrir Gold/XAUUSD avant décision sur BTC formulas ou avant cadrage explicitement séparé.

## 17_RESUME_POINT

```text
01_formulas_compat_review.md créé.
Portée : documentation + contrats uniquement.
Aucun backtest, aucun worker runtime, aucune connexion exchange, aucune nouvelle UI.
Prochaine action : validation ou correction de ce document.
BACKTEST_DATA_PREP reste bloqué tant que ce document n'est pas PASS.
```

## 18_TO_DOCUMENT

```text
- 01_formulas_compat_review.md
- mapping vers trading_lab_v1
- mapping vers desk_pro_runner/dashboard
- mapping vers probability_engine
- refus automatiques
- contrats JSON formula_input / formula_output
```

## 19_TO_REMEMBER

```text
MEM_CANDIDATE:
Dans le chantier BTC/Gold accumulation, la suite validée impose FORMULAS_COMPAT_REVIEW avant BACKTEST_DATA_PREP. Objectif final global = stratégie robuste accumulation Bitcoin + Gold. Toute intégration doit réutiliser trading_lab_v1, Desk Pro, probability_engine/risk_engine si compatibles ; pas de nouveau module, backtest engine, UI ou worker runtime avant validation des formules.
```
