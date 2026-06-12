---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
status: draft_for_user_validation
lifecycle_stage: child_opening_plan
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01
topic_keys:
  - opt-trading
  - trading
  - bitcoin
  - btc
  - bitget
  - coin-futures
  - param-sweep
  - free-search
  - simulation
  - ranking
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Ouvrir le child documentaire du sweep parametrique libre BTC COIN-M, sans runtime ni garde-fous strategiques actifs."
updated_at: 2026-05-08
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/01_param_space_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/02_simulation_result_schema.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/03_reality_classifier_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/04_ranking_method.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/01_backtest_data_prep.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
---

# GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01

## 1_MASTER_TARGET

Creer un moteur de recherche parametrique BTC COIN-M, strictement `simulation only`, ou toutes les variables strategiques sont modifiables afin de classer objectivement les configurations par resultat net en BTC.

Objectif primaire :

```text
max(delta_btc_net) = max(net_btc_final - net_btc_initial)
```

Objectif inverse :

```text
min(delta_btc_net) = min(net_btc_final - net_btc_initial)
```

## 2_INITIAL_PROJECT_DOC

Ce child ouvre la phase documentaire du `free search` BTC COIN-M.

Ici, on ne code pas encore le sweep massif. On fixe d'abord :

```text
- l'espace complet des parametres
- le schema de resultat
- les regles de classification realite / impossible
- la methode de ranking
```

## 3_INITIAL_NEED

Le parent accumulation et les childs `FORMULAS_SOURCE_LOCK_01` puis `BACKTEST_DATA_PREP_01` ont pose :

```text
- les variables candidates
- les formules PAPER_LOCKED
- le pipeline de donnees historiques
```

Il manque maintenant un cadre canonique pour explorer massivement les configurations sans bloquer a priori les cas dangereux ou irreels, puis trier apres coup :

```text
- mathematiquement valide
- possible en realite exchange
- impossible exchange
- profitable en BTC
- destructeur en BTC
```

## 4_MASTER_PROJECT_PLAN

### Phase 1 - Free Search Engine

Definir une surface de recherche ou aucune variable strategique n'est hardcodee :

```text
z_dca
z_short
g_up
g_down
r_transfer
y_dca_usdt
q_add_native
tp1
tp2
runner
cooldown_dca_h
cooldown_short_h
leverage_target
D_min
MR_max
Q_max_native
U_floor_usdt
M_floor_btc
funding_limit
fee_limit
slippage_max_bps
weekly_structure_gate_mode
weekly_k
weekly_epsilon_lambda
max_pivot_gap_weeks
```

### Phase 2 - Massive Simulation

Pour chaque configuration :

```text
1. charger un dataset historique valide
2. appliquer les formules PAPER_LOCKED
3. simuler DCA / short / TP / funding / fees / liquidation
4. sortir un resultat complet
5. ne pas bloquer la configuration si elle est irreelle
6. logger les causes de non-realite apres simulation
```

### Phase 3 - Reality Classifier

Chaque run doit recevoir une classification primaire et des tags secondaires :

```text
REALISTIC
PAPER_ONLY
EXCHANGE_IMPOSSIBLE
MATH_INVALID
LIQUIDATED
DATA_INVALID
OVERFIT_SUSPECT
```

### Phase 4 - Ranking

Deux classements doivent coexister :

```text
A. classement brut mathematique
B. classement realite / exchange
```

## 6_FINAL_TARGET

Ce child doit produire les livrables documentaires suivants :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/00_INITIAL_PROJECT_DOC.md
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/01_param_space_spec.md
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/02_simulation_result_schema.md
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/03_reality_classifier_spec.md
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/04_ranking_method.md
```

Puis seulement ensuite :

```text
implementation du sweep simulation
```

## 8_VALIDATED_PLAN - Sequence

```text
1. Ouvrir le child documentaire.
2. Figer l'espace des parametres modifiables.
3. Figer le contrat de sortie des simulations.
4. Figer le classifieur realite / impossible.
5. Figer le ranking primaire par delta_btc_net.
6. Choisir ensuite la surface d'implementation la plus petite possible.
```

Preference d'implementation future :

```text
etendre trading_lab_v1 si cela suffit,
et ne creer un moteur supplementaire que si un manque reel est demontre.
```

## 10_SELECTED_SETUP - Architecture cible

Pipeline documentaire retenu :

```text
PARAM_GENERATOR
      -> SIMULATION_ENGINE
      -> RESULT_NORMALIZER
      -> REALITY_CLASSIFIER
      -> RANKER
      -> REPORT_EXPORTER
```

## 12_INVARIANTS

```text
- simulation only
- pas de live
- pas d'ordre reel
- pas de cle API privee
- pas de runtime loop
- pas de nouvelle UI
- pas de nouveau backtest engine si trading_lab_v1 suffit
- toutes les variables strategiques sont modifiables
- aucun garde-fou strategique ne doit etre hardcode comme blocage obligatoire dans ce child
- la validite mathematique reste obligatoire
- les resultats impossibles doivent etre conserves et classes
- le classement primaire est delta_btc_net
- PAPER_LOCKED autorise la simulation, pas le runtime
```

## 15_REMAINING_GAP

Avant implementation du sweep, il faut encore confirmer :

```text
1. plage min/max finale de chaque variable
2. nombre de simulations cible
3. periode historique BTC
4. timeframe principal : 1h, 4h ou 1d
5. mode weekly gate : off / loose / strict
6. frontiere exacte impossible vs paper_only
7. format final des rapports d'export
```

## 16_TODO

```text
1. Relire et valider le present 00_INITIAL_PROJECT_DOC.md.
2. Valider 01_param_space_spec.md.
3. Valider 02_simulation_result_schema.md.
4. Valider 03_reality_classifier_spec.md.
5. Valider 04_ranking_method.md.
6. Ensuite seulement ouvrir le lot d'implementation du sweep simulation.
```

## GAP_INDEXATION

Ce lot ouvre un child documentaire sur branche dediee.

Les index globaux ne sont pas modifies dans ce passage.

Trace canonique de reprise :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/00_INITIAL_PROJECT_DOC.md
```

## 17_RESUME_POINT

```text
Child ouvert pour le free search BTC COIN-M.
But : tester librement les variables, conserver meme les cas impossibles,
puis classer objectivement les gains et destructions de BTC avant toute version realiste.
```

## RISKS

- À qualifier.
