---
doc_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01_WORKER_SPEC
doc_type: worker_spec
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
status: draft_for_user_validation
lifecycle_stage: parent_worker_spec
topic_keys:
  - opt-trading
  - trading
  - btc
  - bitget
  - coin-futures
  - accumulation
  - worker
  - calculator
  - corrector
  - optimizer
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
point_de_reprise: "Valider la spec pseudo-code des workers avant tout code reel, backtest ou connexion exchange."
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/index/inbox/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 03_worker_spec - BTC COIN-M Accumulation Engine

## 13_ESTABLISHED

Les prealables documentaires sont poses :

```text
01_initial_project_doc.md = valide comme base canonique
02_variables_bounds.md = cree puis pousse
exchange cible = Bitget
productType = COIN-FUTURES
symbol = BTCUSD
marginCoin = BTC
marginMode = crossed
```

Le present document ne definit que des specs de workers en pseudo-code.

Hors perimetre explicite :

```text
- aucun backtest reel
- aucune connexion exchange
- aucune execution live
- aucun ordre reel
- aucun calcul final fige tant que les formules Bitget manquantes ne sont pas validees
```

## 6_FINAL_TARGET

Definir trois workers documentaires et leur contrat d'interface :

```text
1. worker calculateur
2. worker correcteur
3. worker optimiseur
```

Chaque worker doit avoir :

```text
- entrees normalisees
- sorties normalisees
- regles de refus
- pseudo-code uniquement
```

## 12_INVARIANTS

```text
- le short COIN-FUTURES reste un moteur de profit sur baisse, pas un hedge principal
- le BTC spot accumule n'est pas vendu dans le modele strategique normal
- le correcteur doit passer avant tout calcul de simulation exploitable
- l'optimiseur ne peut pas contourner le correcteur
- aucune hypothese Binance legacy n'est autorisee
- aucune formule PnL / liquidation Bitget absente n'est tolerable en mode calcul exploitable
- aucune lecture reseau n'est autorisee dans ces workers specifiques
- aucun worker ne doit envoyer d'ordre, changer un mode marge ou appeler une API live
```

## 1_MASTER_SCOPE

Pipeline logique vise :

```text
evaluation unitaire :
config candidate
-> worker correcteur
-> worker calculateur

evaluation multi-candidats :
search_space
-> worker optimiseur
-> worker correcteur
-> worker calculateur
-> classement documentaire des politiques
```

Ordre obligatoire :

```text
correcteur avant calculateur
optimiseur = orchestrateur, pas calculateur autonome
```

Le worker optimiseur ne calcule rien directement ; il orchestre des appels au correcteur puis au calculateur.

## 2_SHARED_INPUT_CONTRACT

Tous les workers utilisent des objets d'entree normalises.

### 2.1 ContractMeta

| Champ | Type | Role | Obligatoire |
|---|---|---|---|
| `exchange` | string | nom de l'exchange | oui |
| `product_type` | string | `COIN-FUTURES` | oui |
| `symbol` | string | `BTCUSD` | oui |
| `margin_coin` | string | `BTC` | oui |
| `margin_mode` | string | `crossed` | oui |
| `min_trade_num` | decimal | taille minimale | oui |
| `size_multiplier` | decimal | pas de taille | oui |
| `volume_place` | int | precision taille | oui |
| `price_place` | int | precision prix | oui |
| `price_end_step` | int | pas terminal prix | oui |
| `tick_size` | decimal | pas prix derive | oui |
| `min_lever` | decimal | levier min | oui |
| `max_lever` | decimal | levier max | oui |
| `fund_interval_h` | int | intervalle funding | oui |
| `maker_fee_rate` | decimal | frais maker | oui |
| `taker_fee_rate` | decimal | frais taker | oui |
| `max_order_qty` | decimal | borne ordre limite | oui |
| `max_market_order_qty` | decimal | borne ordre market | oui |
| `max_symbol_order_num` | int | borne ordres ouverts | oui |
| `support_margin_coins` | list[string] | collateraux supportes | oui |
| `symbol_status` | string | statut de trading | oui |

### 2.2 StrategyConfig

| Champ | Type | Role | Obligatoire |
|---|---|---|---|
| `z_dca` | decimal | ecart DCA | oui |
| `z_short` | decimal | ecart short | oui |
| `g_up` | decimal | signal hausse short | oui |
| `g_down` | decimal | signal baisse TP | oui |
| `y_dca_usdt` | decimal | ticket DCA | oui |
| `r_transfer` | decimal | part du DCA vers marge BTC | oui |
| `q_add_native` | decimal | increment short | oui |
| `tp1` | decimal | premier TP | oui |
| `tp2` | decimal | second TP | oui |
| `runner` | decimal | residuel position | oui |
| `cooldown_dca_h` | int | cooldown DCA | oui |
| `cooldown_short_h` | int | cooldown short | oui |
| `leverage_target` | decimal | levier de travail | oui |
| `D_min` | decimal | distance liquidation minimale | oui |
| `MR_max` | decimal | margin ratio maximal | oui |
| `Q_max_native` | decimal | exposition short max | oui |
| `U_floor_usdt` | decimal | reserve minimale | oui |
| `M_floor_btc` | decimal | marge minimale | oui |
| `funding_limit_btc_30d` | decimal | borne funding | oui |
| `fee_limit_btc_30d` | decimal | borne frais | oui |
| `slippage_max_bps` | decimal | borne slippage | oui |
| `drawdown_max_nav` | decimal | borne drawdown | oui |
| `max_short_adds_24h` | int | cadence short max | oui |
| `max_open_orders` | int | borne ordres | oui |

### 2.3 InitialState

| Champ | Type | Role | Obligatoire |
|---|---|---|---|
| `P_0` | decimal | prix initial | oui |
| `S_0_btc` | decimal | stock BTC spot initial | oui |
| `U_0_usdt` | decimal | reserve initiale | oui |
| `M_0_btc` | decimal | collateral initial | oui |
| `Q_0_native` | decimal | taille short initiale | oui |
| `E_0` | decimal or null | prix moyen initial short | oui |
| `PnL_r_0_btc` | decimal | PnL realise initial | oui |
| `Funding_0_btc` | decimal | funding initial | oui |
| `Fee_0_btc` | decimal | frais initiaux | oui |

### 2.4 ScenarioInput

| Champ | Type | Role | Obligatoire |
|---|---|---|---|
| `price_path` | list[decimal] | trajectoire prix deja preparee hors worker | oui |
| `funding_path` | list[decimal] | trajectoire funding deja preparee hors worker | oui |
| `time_path` | list[timestamp] | temps associes | oui |
| `scenario_id` | string | identifiant du scenario | oui |
| `scenario_kind` | string | `synthetic` ou `offline_replay` | oui |

### 2.5 FormulaPack

| Champ | Type | Role | Obligatoire |
|---|---|---|---|
| `qty_to_notional_fn` | function | conversion taille native -> notionnel | oui |
| `pnl_inverse_bitget_short_fn` | function | PnL inverse short | oui |
| `liquidation_bitget_cross_short_fn` | function | prix liquidation cross | oui |
| `margin_ratio_bitget_cross_fn` | function | margin ratio cross | oui |
| `funding_bitget_short_fn` | function | funding incremental short | oui |

Le `FormulaPack` est obligatoire mais peut rester au statut :

```text
placeholder_documented = oui
validated_for_execution = non
```

Dans ce cas, le correcteur peut accepter un mode `spec_only`, mais doit refuser un mode `simulation_exploitable`.

## 3_WORKER_CALCULATEUR

### 3.1 Role

Transformer une configuration valide et un scenario prepare en trace de simulation deterministe, sans aucun acces reseau ni action exchange.

### 3.2 Entrees

| Entree | Source |
|---|---|
| `contract_meta` | `ContractMeta` |
| `strategy_config` | `StrategyConfig` |
| `initial_state` | `InitialState` |
| `scenario_input` | `ScenarioInput` |
| `formula_pack` | `FormulaPack` |
| `run_mode` | `spec_only` ou `simulation_exploitable` |

### 3.3 Sorties

| Sortie | Role |
|---|---|
| `timeline` | etats successifs du systeme |
| `event_log` | DCA, ajout short, TP, funding, frais, freeze |
| `risk_log` | `MR_t`, `D_t`, drawdown, breaches |
| `summary_metrics` | BTC final, PnL, funding, frais, nb shorts |
| `calculator_verdict` | `PASS`, `PASS_WITH_WARNINGS` ou `REJECT` |

### 3.4 Regles de refus

```text
- REJECT si contract_meta incomplet
- REJECT si scenario_input incomplet
- REJECT si `symbol != BTCUSD`
- REJECT si `product_type != COIN-FUTURES`
- REJECT si `margin_mode != crossed`
- REJECT si `symbol_status != normal`
- REJECT si `z_short <= z_dca`
- REJECT si `tp1 + tp2 + runner != 1`
- REJECT si `q_add_native` ne respecte pas `min_trade_num` ou `size_multiplier`
- REJECT si `leverage_target > max_lever`
- REJECT si `run_mode = simulation_exploitable` et formule Bitget manquante
- REJECT si les longueurs `price_path`, `funding_path`, `time_path` ne correspondent pas
```

### 3.5 Pseudo-code

```text
function worker_calculateur(contract_meta, strategy_config, initial_state, scenario_input, formula_pack, run_mode):
    assert_basic_shape(contract_meta, strategy_config, initial_state, scenario_input)
    assert_bitget_identity(contract_meta)
    assert_strategy_bounds(strategy_config, contract_meta)
    assert_series_alignment(scenario_input)

    if run_mode == simulation_exploitable:
        assert_formula_pack_complete(formula_pack)

    state = build_initial_state(initial_state)
    steps = zip_series(scenario_input.price_path, scenario_input.funding_path, scenario_input.time_path)
    timeline = []
    event_log = []
    risk_log = []

    for step in steps:
        price_t = step.price
        funding_t = step.funding
        time_t = step.time

        assert_price_grid_if_needed(price_t, contract_meta)

        desired_dca = decide_dca(state, strategy_config, price_t, time_t)
        desired_short_add = decide_short_add(state, strategy_config, price_t, time_t)
        desired_tp = decide_short_tp(state, strategy_config, price_t, time_t)

        quantized_dca = quantize_dca(desired_dca, strategy_config, state)
        quantized_short_add = quantize_qty(desired_short_add, contract_meta)
        quantized_tp = quantize_qty(desired_tp, contract_meta)

        if breach_freeze_rules(state, strategy_config):
            quantized_short_add = 0
            event_log.append(freeze_event(time_t, state))

        btc_bought = dca_usdt_to_btc(quantized_dca, price_t)
        btc_to_margin = transfer_usdt_to_margin_btc(quantized_dca, strategy_config.r_transfer, price_t)
        btc_to_spot = btc_bought - btc_to_margin

        if run_mode == simulation_exploitable:
            pnl_u_btc = formula_pack.pnl_inverse_bitget_short_fn(state.Q_native, state.E, price_t, contract_meta)
            liq_t = formula_pack.liquidation_bitget_cross_short_fn(state, contract_meta)
            mr_t = formula_pack.margin_ratio_bitget_cross_fn(state, contract_meta)
            funding_increment = formula_pack.funding_bitget_short_fn(state.Q_native, funding_t, contract_meta)
            fee_increment = estimate_fees(state, quantized_short_add, quantized_tp, contract_meta)
        else:
            pnl_u_btc = placeholder_value("pnl")
            liq_t = placeholder_value("liq")
            mr_t = placeholder_value("mr")
            funding_increment = placeholder_value("funding")
            fee_increment = placeholder_value("fees")

        state = evolve_state(state, btc_to_spot, btc_to_margin, quantized_short_add, quantized_tp, pnl_u_btc, funding_increment, fee_increment, price_t, liq_t, mr_t)

        timeline.append(snapshot_state(time_t, state))
        risk_log.append(snapshot_risk(time_t, state))
        event_log.extend(snapshot_events(time_t, quantized_dca, quantized_short_add, quantized_tp))

        if breach_hard_stop_rules(state, strategy_config):
            return reject_calculation(timeline, event_log, risk_log, code="ERR_RISK_BREACH")

    summary_metrics = summarize_run(timeline, event_log, risk_log)
    return pass_calculation(timeline, event_log, risk_log, summary_metrics)
```

## 4_WORKER_CORRECTEUR

### 4.1 Role

Verifier qu'une configuration est coherente, complete et conforme aux bornes documentaires avant tout calcul exploitable.

### 4.2 Entrees

| Entree | Source |
|---|---|
| `contract_meta` | `ContractMeta` |
| `strategy_config` | `StrategyConfig` |
| `initial_state` | `InitialState` |
| `scenario_input` | `ScenarioInput` optionnel en mode `spec_only` |
| `formula_pack` | `FormulaPack` |
| `validation_mode` | `spec_only` ou `simulation_exploitable` |

### 4.3 Sorties

| Sortie | Role |
|---|---|
| `corrector_verdict` | `PASS`, `PASS_WITH_WARNINGS` ou `REJECT` |
| `blocking_errors` | liste des erreurs bloquantes |
| `warnings` | liste des alertes |
| `normalized_config` | version nettoyee et quantifiee |
| `evidence` | details des controles effectues |

### 4.4 Regles de refus

```text
- REJECT si le GO canonique ne correspond pas
- REJECT si l'exchange cible n'est pas Bitget
- REJECT si `product_type != COIN-FUTURES`
- REJECT si `symbol != BTCUSD`
- REJECT si `margin_coin != BTC`
- REJECT si `margin_mode != crossed`
- REJECT si `BTC` absent de `support_margin_coins`
- REJECT si `min_trade_num`, `size_multiplier`, `tick_size` sont absents
- REJECT si `contractSize = 100 USD` apparait dans la config ou les formules
- REJECT si `tp1 + tp2 + runner != 1`
- REJECT si `z_short <= z_dca`
- REJECT si `U_0_usdt < U_floor_usdt`
- REJECT si `M_0_btc < M_floor_btc`
- REJECT si `Q_max_native > max_order_qty` sans regle de split explicite
- REJECT si `validation_mode = simulation_exploitable` et `FormulaPack` incomplet
- REJECT si les series scenario sont absentes en mode calcul
```

### 4.5 Pseudo-code

```text
function worker_correcteur(contract_meta, strategy_config, initial_state, scenario_input, formula_pack, validation_mode):
    errors = []
    warnings = []
    evidence = []

    check_canonical_identity(errors, evidence)
    check_exchange_identity(contract_meta, errors, evidence)
    check_exchange_fields(contract_meta, errors, evidence)
    check_strategy_bounds(strategy_config, contract_meta, errors, evidence)
    check_initial_capital(initial_state, strategy_config, errors, evidence)
    check_binance_legacy_absence(strategy_config, formula_pack, errors, evidence)

    normalized_config = normalize_to_bitget_grids(strategy_config, contract_meta)

    if normalized_config.changed_values:
        warnings.append("WARN_GRID_NORMALIZATION")

    if validation_mode == simulation_exploitable:
        check_formula_pack_complete(formula_pack, errors, evidence)
        check_scenario_presence(scenario_input, errors, evidence)
        check_series_alignment(scenario_input, errors, evidence)
        check_funding_presence(scenario_input, errors, evidence)
    else:
        check_formula_placeholders_documented(formula_pack, warnings, evidence)

    if errors not empty:
        return reject_corrector(errors, warnings, normalized_config, evidence)

    if warnings not empty:
        return pass_with_warnings_corrector(errors, warnings, normalized_config, evidence)

    return pass_corrector(errors, warnings, normalized_config, evidence)
```

## 5_WORKER_OPTIMISEUR

### 5.1 Role

Explorer un espace de politiques candidates, sans acces exchange, et classer les configurations qui passent le correcteur puis le calculateur.

### 5.2 Entrees

| Entree | Source |
|---|---|
| `search_space` | bornes et discretisations de `StrategyConfig` |
| `contract_meta` | `ContractMeta` |
| `initial_state` | `InitialState` |
| `scenario_set` | liste de `ScenarioInput` |
| `formula_pack` | `FormulaPack` |
| `optimization_mode` | `spec_only` ou `simulation_exploitable` |
| `objective_weights` | ponderation BTC final / drawdown / survie / cout |

### 5.3 Sorties

| Sortie | Role |
|---|---|
| `ranked_candidates` | liste classee des policies valides |
| `pareto_frontier` | candidats non domines |
| `rejected_candidates` | candidats refuses avec motifs |
| `optimizer_summary` | synthese de la recherche |

### 5.4 Regles de refus

```text
- REJECT si `search_space` est vide
- REJECT si une borne du `search_space` contredit `02_variables_bounds.md`
- REJECT si `optimization_mode = simulation_exploitable` et `FormulaPack` incomplet
- REJECT si `scenario_set` est vide
- REJECT si l'optimiseur tente d'appeler directement l'exchange
- REJECT si l'optimiseur saute le correcteur
```

### 5.5 Pseudo-code

```text
function worker_optimiseur(search_space, contract_meta, initial_state, scenario_set, formula_pack, optimization_mode, objective_weights):
    assert_search_space_present(search_space)
    assert_scenarios_present(scenario_set)
    assert_no_live_connectors()

    ranked_candidates = []
    rejected_candidates = []

    for candidate_config in enumerate_candidates(search_space):
        corrector_result = worker_correcteur(contract_meta, candidate_config, initial_state, optional_scenario_probe(scenario_set), formula_pack, optimization_mode)

        if corrector_result.verdict == REJECT:
            rejected_candidates.append(record_rejection(candidate_config, corrector_result))
            continue

        scenario_scores = []

        for scenario_input in scenario_set:
            calculator_result = worker_calculateur(contract_meta, corrector_result.normalized_config, initial_state, scenario_input, formula_pack, optimization_mode)

            if calculator_result.verdict == REJECT:
                rejected_candidates.append(record_rejection(candidate_config, calculator_result))
                scenario_scores = []
                break

            scenario_scores.append(score_candidate(calculator_result.summary_metrics, objective_weights))

        if scenario_scores is empty:
            continue

        ranked_candidates.append(record_candidate(candidate_config, aggregate_scores(scenario_scores)))

    ranked_candidates = sort_by_objective(ranked_candidates)
    pareto_frontier = compute_pareto_frontier(ranked_candidates)

    return build_optimizer_result(ranked_candidates, pareto_frontier, rejected_candidates)
```

## 7_WORKER_PIPELINE_RULES

```text
- le correcteur est le seul point d'entree autorise pour valider une configuration
- le calculateur n'accepte que des entrees deja passees par le correcteur
- l'optimiseur ne manipule jamais de config non normalisee directement en calcul final
- tout mode `simulation_exploitable` exige un `FormulaPack` complet et valide
- tout mode `spec_only` autorise des placeholders documentes mais doit marquer les sorties comme non exploitables
```

## 8_REFUSAL_CODES

| Code | Worker | Cause |
|---|---|---|
| `ERR_CANONICAL_GO` | correcteur | GO non canonique |
| `ERR_EXCHANGE_IDENTITY` | correcteur | exchange ou symbole incorrect |
| `ERR_MARGIN_MODE` | correcteur, calculateur | mode marge incorrect |
| `ERR_GRID_QTY` | correcteur, calculateur | taille hors `min_trade_num` ou `size_multiplier` |
| `ERR_GRID_PRICE` | correcteur, calculateur | prix hors `tick_size` |
| `ERR_TP_SUM` | correcteur, calculateur | `tp1 + tp2 + runner != 1` |
| `ERR_SHORT_TOO_DENSE` | correcteur, calculateur | `z_short <= z_dca` |
| `ERR_LEVERAGE_CAP` | correcteur, calculateur | levier hors borne |
| `ERR_CAPITAL_FLOOR` | correcteur, calculateur | reserve ou marge sous le plancher |
| `ERR_FORMULA_PACK_MISSING` | correcteur, calculateur, optimiseur | pack de formules incomplet |
| `ERR_FUNDING_SERIES_MISSING` | correcteur, calculateur | funding absent en mode calcul |
| `ERR_SCENARIO_ALIGNMENT` | correcteur, calculateur | series scenario desynchronisees |
| `ERR_LEGACY_BINANCE_ASSUMPTION` | correcteur | hypothese Binance legacy detectee |
| `ERR_RISK_BREACH` | calculateur | distance liquidation ou margin ratio hors borne |
| `ERR_SEARCH_SPACE_EMPTY` | optimiseur | espace d'optimisation vide |
| `ERR_LIVE_CONNECTOR_FORBIDDEN` | optimiseur | tentative de connexion live |

## 9_SELECTED_PSEUDO_OUTPUTS

Exemple de structure de sortie du calculateur :

```text
calculator_result = {
  verdict,
  timeline[],
  event_log[],
  risk_log[],
  summary_metrics {
    btc_final,
    btc_spot_final,
    collateral_btc_final,
    pnl_realized_btc,
    pnl_unrealized_btc,
    funding_btc,
    fees_btc,
    max_drawdown,
    min_distance_to_liq,
    max_margin_ratio,
    short_add_count,
    tp_count
  }
}
```

Exemple de structure de sortie du correcteur :

```text
corrector_result = {
  verdict,
  blocking_errors[],
  warnings[],
  normalized_config,
  evidence[]
}
```

Exemple de structure de sortie de l'optimiseur :

```text
optimizer_result = {
  ranked_candidates[],
  pareto_frontier[],
  rejected_candidates[],
  optimizer_summary
}
```

## 15_REMAINING_GAP

Les gaps remontes depuis `02_variables_bounds.md` restent bloquants pour tout mode `simulation_exploitable` :

```text
- qty_to_notional_fn Bitget
- PnL inverse short Bitget
- liquidation / maintenance cross margin Bitget
- historique funding avant backtest
```

Ces gaps ne bloquent pas la redaction pseudo-code du present document, mais bloquent toute implementation de calcul fiable.

## 16_TODO

```text
1. Valider le present document 03.
2. Figer les signatures finales du FormulaPack.
3. Documenter la formule de conversion notionnel Bitget.
4. Documenter la formule PnL inverse short Bitget.
5. Documenter la formule liquidation / maintenance cross margin Bitget.
6. Definir le format documentaire des scenarios offline.
7. N'ouvrir un chantier d'implementation qu'apres validation explicite.
```

## 17_RESUME_POINT

```text
03_worker_spec.md definit la spec pseudo-code des workers calculateur, correcteur et optimiseur.
Le correcteur est obligatoire avant tout calcul.
L'optimiseur ne contourne jamais le correcteur.
Le mode simulation exploitable reste bloque tant que les formules Bitget et l'historique funding ne sont pas figes.
Aucune connexion exchange, aucun backtest reel et aucune execution live ne sont autorises depuis ce document.
```

## RISKS

- À qualifier.
