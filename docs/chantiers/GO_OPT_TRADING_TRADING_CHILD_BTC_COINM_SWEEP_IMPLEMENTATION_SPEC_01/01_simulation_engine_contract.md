---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01_SIMULATION_ENGINE_CONTRACT
doc_type: simulation_engine_contract
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01
status: draft_for_review
lifecycle_stage: child_simulation_engine_contract
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01
topic_keys:
  - opt-trading
  - trading
  - btc
  - coin-futures
  - simulation
  - engine
  - contract
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/01_simulation_engine_contract.md
point_de_reprise: "Definir le contrat du moteur de simulation BTC COIN-M candle-par-candle."
updated_at: 2026-05-08
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/01_param_space_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/02_simulation_result_schema.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
---

# 01_simulation_engine_contract

## 1_MASTER_TARGET

Definir le contrat de la boucle de simulation BTC COIN-M candle-par-candle, la machine d'etat interne, et les signatures des fonctions de calcul, sans implementation Python.

## 2_CONTEXT_RECALL

Le moteur reutilise :

```text
- les formules PAPER_LOCKED de FORMULAS_SOURCE_LOCK_01
- le schema de sortie de 02_simulation_result_schema.md
- l'espace de parametres de 01_param_space_spec.md
- la donnee d'entree JSONL definie par BACKTEST_DATA_PREP_01
```

Il n'utilise pas :

```text
- les fonctions FVG/sweep de trading_lab_v1
- le profil XAUUSD
- les schemas xauusd_dual_stack
- les strategies dual-stack existantes
```

## 3_INPUT_CONTRACT

### 3.1 SimulationInput

Objet d'entree d'un run unique :

| Champ | Type | Source |
|---|---|---|
| `config` | dict | surface de sweep (24 params) |
| `candles` | list[dict] | JSONL data prep (OHLCV + mark + funding) |
| `contract_spec` | dict | snapshot contract Bitget (24 champs) |
| `initial_state` | dict | `P_0`, `S_0_btc`, `U_0_usdt`, `M_0_btc` |
| `apply_strategic_guards` | bool | `false` dans le free search |

### 3.2 Data row (une bougie enrichie)

Chaque ligne du JSONL doit contenir au minimum :

| Champ | Type | Usage |
|---|---|---|
| `ts` | ISO-8601 | timestamp de la bougie |
| `open` | decimal | prix d'ouverture |
| `high` | decimal | prix haut |
| `low` | decimal | prix bas |
| `close` | decimal | prix de cloture |
| `mark_price` | decimal or null | MarkPrice ou proxy IndexPrice |
| `index_price` | decimal | fallback si MarkPrice absent |
| `funding_rate` | decimal or null | taux funding si settlement |
| `funding_settled` | bool | true si cette bougie porte un settlement |

## 4_STATE_MACHINE

### 4.1 State object (a chaque pas k)

```text
State_k = {
    P_k:              decimal    prix de reference (close ou mark)
    S_k_btc:          decimal    BTC spot accumule
    U_k_usdt:         decimal    reserve quote
    M_k_btc:          decimal    collateral COIN-M
    Q_k_native:       decimal    taille short ouverte
    E_k:              decimal    prix moyen d'entree short (null si Q=0)
    PnL_r_cumul_btc:  decimal    PnL short realise cumule
    Funding_cumul_btc:decimal    funding cumule
    Fee_cumul_btc:    decimal    frais cumules
    NAV_peak_btc:     decimal    pic de NAV pour drawdown
    event_log:        list[dict] journal d'evenements
    last_dca_ts:      timestamp  dernier DCA
    last_short_ts:    timestamp  dernier ajout short
    last_pivot_price: decimal    dernier pivot pour g_up / g_down
}
```

### 4.2 Derived values (calcules a chaque pas si besoin)

| Valeur | Formule | Source |
|---|---|---|
| `N_k_usd` | `Q_k_native * contractSize` | U1 PAPER_LOCKED |
| `PnL_u_k_btc` | `Q_k_native * (1/P_k - 1/E_k)` if Q_k>0, else 0 | U3 PAPER_LOCKED |
| `MM_k_btc` | `(Q_k_native / P_k) * MMR_tier(N_k_usd)` | U7 PAPER_LOCKED |
| `Equity_k_btc` | `M_k_btc + PnL_u_k_btc` | |
| `NAV_k_btc` | `S_k_btc + Equity_k_btc + U_k_usdt / P_k_ref` | convention comptable |
| `LiqPrice_k` | cf. U6 PAPER_LOCKED (cross short) | |
| `D_k` | `(LiqPrice_k - P_k) / P_k` if Q_k>0, else null | |
| `MR_k` | `Equity_k_btc / MM_k_btc` if Q_k>0, else null | U8 PAPER_LOCKED |
| `DD_k` | `max(0, 1 - NAV_k_btc / NAV_peak_btc)` | |

## 5_MAIN_LOOP_CONTRACT

### 5.1 Signature

```text
simulate_run(input: SimulationInput) -> SimulationOutput
```

### 5.2 Pseudo-code contractuel

```text
func simulate_run(input):
    state = init_state(input.initial_state)
    validate_math(input)          # prix>0, quantites finies, simplex TP=1

    for each candle k in input.candles:
        P = resolve_price(candle, input.contract_spec)
        # ordre obligatoire : funding -> DCA -> short -> TP -> checks

        state = apply_funding(state, candle, input.contract_spec)
        state = apply_dca(state, P, input.config)
        state = apply_short_add(state, P, input.config, input.contract_spec)
        state = apply_tp(state, P, input.config, input.contract_spec)

        state = update_derived(state, P, input.contract_spec)
        state = check_liquidation(state, P, input.contract_spec)
        if state.liquidated:
            break

        state = record_breaches(state, input.config)
        state.NAV_peak_btc = max(state.NAV_peak_btc, NAV_k_btc)

    return build_output(state, input, error_stop_reason)
```

### 5.3 Ordre des etapes (justification)

```text
1. funding d'abord : le settlement funding se fait au debut de la bougie
2. DCA ensuite : peut augmenter la marge avant les decisions short
3. short ensuite : ajoute si conditions reunies
4. TP ensuite : reduit la position short
5. checks a la fin : apres tous les changements de la bougie
```

## 6_FUNCTION_CONTRACTS

### 6.1 resolve_price

```text
resolve_price(candle, contract_spec) -> P_k

Regle :
- MarkPrice si dispo et non null
- sinon IndexPrice si dispo
- sinon close de la bougie + flag mark proxy
```

### 6.2 apply_funding

```text
apply_funding(state, candle, contract_spec) -> state

Condition : candle.funding_settled = true et state.Q_k_native > 0

Calcul :
  funding_inc_btc = (state.Q_k_native / P_mark) * candle.funding_rate
  # U5 + U4 PAPER_LOCKED : signe = +1 quand fundingRate > 0 (longs paient shorts)

  state.Funding_cumul_btc += funding_inc_btc
  state.M_k_btc += funding_inc_btc

  si funding_inc_btc >= 0 : state.funding_received += funding_inc_btc
  si funding_inc_btc < 0  : state.funding_paid += abs(funding_inc_btc)

  state.event_log.append(funding_event)
```

### 6.3 apply_dca

```text
apply_dca(state, P, config) -> state

Conditions :
  z_dca_check    = last_dca_ts absent OU (P - last_dca_price)/last_dca_price <= -z_dca
  cooldown_check = cooldown_dca_h = 0 OU (k_ts - last_dca_ts) >= cooldown_dca_h heures
  reserve_check  = U_k_usdt >= config.y_dca_usdt

Si les 3 conditions reunies :
  btc_bought = y_dca_usdt / P
  btc_to_margin = btc_bought * r_transfer
  btc_to_spot   = btc_bought - btc_to_margin

  state.S_k_btc += btc_to_spot
  state.M_k_btc += btc_to_margin
  state.U_k_usdt -= y_dca_usdt
  state.last_dca_ts = timestamp courant
  state.last_dca_price = P
  state.event_log.append(dca_event)
```

### 6.4 apply_short_add

```text
apply_short_add(state, P, config, contract_spec) -> state

Conditions :
  signal_check  = P >= last_pivot_price * (1 + g_up) ET Q_k_native > 0 OU premier short
  spacing_check = z_short = 0 OU (last_short_ts absent OU (P - last_short_price)/last_short_price >= z_short)
  cooldown_check = cooldown_short_h = 0 OU (k_ts - last_short_ts) >= cooldown_short_h heures

  weekly_gate_check = true  # si gate_mode=off ; sinon depend de l'implementation future

Si les conditions reunies :
  fees_btc = q_add_native * takerFeeRate  # U2 PAPER_LOCKED
  q_actual = q_add_native

  # mise a jour prix moyen d'entree
  state.E_k = (state.E_k * state.Q_k_native + P * q_actual) / (state.Q_k_native + q_actual)
  state.Q_k_native += q_actual
  state.Fee_cumul_btc += fees_btc
  state.M_k_btc -= fees_btc  # les fees sont payes en BTC
  state.last_short_ts = timestamp courant
  state.last_short_price = P
  state.event_log.append(short_add_event)
```

Note : dans ce child, `apply_strategic_guards=false` signifie que `D_min`, `MR_max`, `Q_max_native`, `funding_limit`, `fee_limit` ne sont pas bloquants. Les breaches sont enregistres comme des tags et compteurs, pas comme des refus.

### 6.5 apply_tp

```text
apply_tp(state, P, config, contract_spec) -> state

Condition : Q_k_native > 0 ET P <= last_pivot_price * (1 - g_down)

Si condition reunie :
  q_close_1 = min(Q_k_native, q_add_native * tp1)  # premier TP
  q_close_2 = min(Q_k_native - q_close_1, q_add_native * tp2)  # deuxieme TP
  runner_portion = Q_k_native - q_close_1 - q_close_2  # reste ouvert

  pnl_tp1 = pnl_inverse_short(q_close_1, E_k, P)   # U3 PAPER_LOCKED
  pnl_tp2 = pnl_inverse_short(q_close_2, E_k, P)

  state.Q_k_native = runner_portion
  state.PnL_r_cumul_btc += pnl_tp1 + pnl_tp2
  state.M_k_btc += pnl_tp1 + pnl_tp2
  state.last_pivot_price = P  # reset du pivot apres TP
  state.event_log.append(tp_event)
```

Si Q_k_native devient 0 apres TP : `state.E_k = null`.

### 6.6 check_liquidation

```text
check_liquidation(state, P, contract_spec) -> state

Condition : Q_k_native > 0

Calcul :
  liq_price = liquidation_cross_short(Q_k_native, E_k, M_k_btc, MMR_tier, contract_spec)
  # U6 PAPER_LOCKED

  si P >= liq_price :
    state.liquidated = true
    state.liquidation_count += 1
    pnl_liq = pnl_inverse_short(Q_k_native, E_k, liq_price)
    state.PnL_r_cumul_btc += pnl_liq
    state.M_k_btc += pnl_liq
    state.Q_k_native = 0
    state.E_k = null
    state.event_log.append(liquidation_event)
```

### 6.7 record_breaches

```text
record_breaches(state, config) -> state

Pour chaque parametre de seuil (D_min, MR_max, Q_max_native, funding_limit, fee_limit) :
  si la valeur de seuil est depassee ET config.apply_strategic_guards = false :
    le breach est enregistre en compteur et tag,
    mais la simulation n'est PAS arretee

  si config.apply_strategic_guards = true (mode non free-search, a venir) :
    le breach peut declencher une action de blocage (freeze short, etc.)
```

## 7_OUTPUT_CONTRACT

### 7.1 SimulationOutput

L'objet de sortie doit respecter le schema defini dans `02_simulation_result_schema.md`.

Signature :

```text
build_output(state, input, stop_reason) -> dict
```

Le dict de sortie doit etre directement serialisable en JSONL et contenir au minimum les 19 colonnes obligatoires definies dans le schema.

### 7.2 Simulation stop reasons

| Valeur | Declencheur |
|---|---|
| `completed` | toutes les bougies parcourues sans erreur |
| `liquidated` | liquidation effective du short |
| `math_invalid` | NaN, inf, division par zero |
| `data_invalid` | donnees corrompues, gap non documente |
| `capital_depleted` | reserve + marge <= 0 |

## 8_PERFORMANCE_ENVELOPPE

Contrat de performance pour l'implementation reelle (non verifie ici, spec only) :

```text
- un run sur 20000 bougies (env. 2.3 ans en 1h) doit tenir en < 100 ms
- cela permet 50000 runs en < 1.5 h sur un CPU moderne
- l'echantillonnage de config ne fait pas partie du temps de simulation
- la persistance JSONL est append-only, pas de reecriture
```

## 17_RESUME_POINT

```text
Le moteur de simulation est une boucle candle-par-candle avec 6 etapes par bougie :
funding -> DCA -> short -> TP -> checks -> breaches.
Les calculs sont figeables en Python directement depuis les formules PAPER_LOCKED.
Aucune connexion exchange, aucun worker runtime.
```

## RISKS

- À qualifier.
