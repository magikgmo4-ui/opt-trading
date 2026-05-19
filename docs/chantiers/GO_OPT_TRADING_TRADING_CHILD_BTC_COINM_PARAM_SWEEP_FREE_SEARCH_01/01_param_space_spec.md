---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01_PARAM_SPACE_SPEC
doc_type: param_space_spec
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
status: draft_for_review
lifecycle_stage: child_param_space_spec
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
topic_keys:
  - opt-trading
  - trading
  - btc
  - bitget
  - coin-futures
  - param-space
  - sweep
  - free-search
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/01_param_space_spec.md
point_de_reprise: "Definir l'espace des variables modifiables et les bornes d'exploration du free search BTC COIN-M."
updated_at: 2026-05-08
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/02_simulation_result_schema.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/03_reality_classifier_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01/01_backtest_data_prep.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_SOURCE_LOCK_01/01_formulas_source_lock.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
---

# 01_param_space_spec

## 1_MASTER_TARGET

Definir une surface de recherche complete pour le free search BTC COIN-M, avec toutes les variables strategiques exposables, aucune valeur hardcodee, et seulement les contraintes de validite mathematique.

## 2_DESIGN_RULES

### 2.1 Regles obligatoires

```text
- toute variable strategique doit provenir d'une config externe
- aucune borne prudente n'est traitee comme blocage obligatoire pendant l'exploration
- la generation peut produire des configs irreelles exchange
- les configs irreelles sont conservees puis classees apres simulation
- pas de NaN, pas d'inf, pas de division par zero
- prix > 0, quantites finies, timestamps valides
```

### 2.2 Regles explicitement retirees pendant le free search

```text
- pas de contrainte obligatoire z_short > z_dca
- pas de contrainte obligatoire r_transfer <= 1
- pas de contrainte obligatoire leverage_target <= maxLever
- pas de freeze strategique obligatoire sur D_min, MR_max, Q_max_native
- pas de cooldown prudent impose a la source
- pas de cap funding/frais utilise comme refus de generation
```

### 2.3 Regles de coherence qui restent obligatoires

```text
- tp1, tp2 et runner appartiennent au simplex [0,1] avec somme = 1
- toutes les variables numeriques doivent etre finies
- tous les modes categoriels doivent appartenir a une liste connue
```

## 3_CANONICAL_PARAM_GROUPS

### 3.1 Signal et espacement

| Variable | Role | Unite | Min free search | Max free search | Sampler recommande | Note |
|---|---|---:|---:|---:|---|---|
| `z_dca` | ecart entre deux DCA | ratio | `0.0001` | `0.20` | log-uniform | aucun lien force avec `z_short` |
| `z_short` | ecart entre deux ajouts short | ratio | `0.0001` | `0.30` | log-uniform | `z_short <= z_dca` autorise |
| `g_up` | hausse qui autorise un short | ratio | `0.0001` | `0.30` | log-uniform | peut etre plus petit que `z_short` |
| `g_down` | baisse qui autorise un TP | ratio | `0.0001` | `0.30` | log-uniform | autorise des TP tres rapides ou tres lents |
| `cooldown_dca_h` | delai entre DCA | heures | `0` | `336` | entier uniforme | `0` autorise |
| `cooldown_short_h` | delai entre ajouts short | heures | `0` | `336` | entier uniforme | `0` autorise |

### 3.2 Allocation et taille

| Variable | Role | Unite | Min free search | Max free search | Sampler recommande | Note |
|---|---|---:|---:|---:|---|---|
| `r_transfer` | multiple de transfert marge par ticket DCA | ratio | `0` | `5` | uniforme | `> 1` autorise et classe apres coup |
| `y_dca_usdt` | ticket DCA brut | USDT | `1` | `100000` | log-uniform | borne large, a specialiser par capital initial |
| `q_add_native` | taille d'un ajout short | native | `0.00001` | `500` | log-uniform | hors grille Bitget autorise pendant la generation |
| `leverage_target` | levier cible | x | `0.1` | `200` | log-uniform | `< 1` et `> 125` possibles puis classes |
| `Q_max_native` | cap d'exposition total | native | `0.00001` | `500` | log-uniform | seuil de diagnostic, pas blocage free search |
| `U_floor_usdt` | reserve quote minimale | USDT | `0` | `100000` | log-uniform avec zero explicite | seuil de diagnostic |
| `M_floor_btc` | collateral BTC minimal | BTC | `0` | `10` | log-uniform avec zero explicite | seuil de diagnostic |

### 3.3 Decomposition TP

La triade `tp1`, `tp2`, `runner` doit etre echantillonnee sur un simplex, pas comme trois variables independantes sans contrainte.

Contrat :

```text
0 <= tp1 <= 1
0 <= tp2 <= 1
0 <= runner <= 1
tp1 + tp2 + runner = 1
```

Methode recommandee :

```text
- echantillonnage Dirichlet pour la masse interne
- plus une banque explicite de cas bord :
  (1,0,0)
  (0,1,0)
  (0,0,1)
  (0.5,0.5,0)
  (0.5,0,0.5)
  (0,0.5,0.5)
```

## 4_SOFT_GUARD_PARAMS

Ces parametres restent configurables mais, dans ce child, ils servent d'abord a logger des breaches et a classer les runs, pas a bloquer la simulation a priori.

| Variable | Role | Unite | Min free search | Max free search | Usage dans le free search |
|---|---|---:|---:|---:|---|
| `D_min` | distance mini a liquidation | ratio | `0` | `1.5` | tag breach si non respecte |
| `MR_max` | margin ratio max | ratio | `0` | `5` | tag breach si depasse |
| `funding_limit` | perte funding toleree | BTC | `0` | `5` | seuil de diagnostic |
| `fee_limit` | cout fees tolere | BTC | `0` | `5` | seuil de diagnostic |
| `slippage_max_bps` | slippage max de reference | bps | `0` | `5000` | seuil de diagnostic |

Note de nommage :

```text
Le sweep expose les champs `funding_limit` et `fee_limit`.
Si une implementation future reutilise des objets plus anciens nommes
`funding_limit_btc_30d` ou `fee_limit_btc_30d`, le mapping devra etre explicite.
```

## 5_OPTIONAL_WEEKLY_GATE_PARAMS

La gate weekly reste optionnelle dans ce child de free search.

| Variable | Type | Domaine | Regle |
|---|---|---|---|
| `weekly_structure_gate_mode` | enum | `off`, `loose`, `strict` | `off` = gate desactivee |
| `weekly_k` | int | `1..12` | profondeur de confirmation pivots |
| `weekly_epsilon_lambda` | decimal | `0..0.10` | tolerance topologique |
| `max_pivot_gap_weeks` | int | `1..52` | ecart maximal entre pivots valides |

Interpretation :

```text
- si mode = off, les autres parametres weekly sont conserves mais inactifs
- si mode != off et que la gate weekly n'est pas executable dans le moteur cible,
  la simulation peut tourner mais la classification devra inclure PAPER_ONLY
```

## 6_PARAM_GENERATOR_METHODS

Ordre recommande :

```text
1. random search large
2. latin hypercube pour une meilleure couverture
3. refinement autour du top 5 %
4. walk-forward sur les meilleurs candidats
```

Usages :

| Methode | Usage |
|---|---|
| `grid_search` | debug local sur peu de dimensions |
| `random_search` | ouverture large du domaine |
| `latin_hypercube` | couverture reguliere du volume |
| `stress_sweep` | batterie de cas bord et cas absurdes |
| `walk_forward` | test de robustesse et anti-overfit |

## 7_RECOMMENDED_OPENING_BUDGET

Budget initial recommande, ajustable :

```text
phase_A_random_large      = 50000 runs
phase_B_latin_hypercube   = 20000 runs
phase_C_refine_top_5_pct  = 10000 runs
phase_D_walk_forward      = top 1000 configs
```

Rien ici n'est fige en dur. Le budget fait partie de la config de campagne.

## 8_RUN_CONTROLS_OUTSIDE_STRATEGY

Les controles suivants ne font pas partie des variables strategiques mais doivent rester configurables pour la campagne :

| Controle | Domaine recommande |
|---|---|
| `dataset_start` | ISO-8601 |
| `dataset_end` | ISO-8601 |
| `timeframe_primary` | `1h`, `4h`, `1d` |
| `simulation_count_target` | entier positif |
| `sampler_kind` | `random`, `lhs`, `grid`, `stress`, `walk_forward` |
| `apply_strategic_guards` | `false` par defaut dans ce child |

Recommandation actuelle :

```text
timeframe primaire prefere = 1h
motif : funding 8h, finesse suffisante, cout encore raisonnable
```

## 9_OUTPUT_EXPECTATION

Le generateur doit produire pour chaque config :

```text
- un config_hash stable
- la config complete serialisee
- la methode d'echantillonnage utilisee
- le seed de generation
- un indicateur de respect des seules contraintes mathematiques
```

## 17_RESUME_POINT

```text
Le free search autorise les configs aggressives, absurdes ou irreelles,
tant qu'elles restent mathematiquement definies.
Les garde-fous deviennent des dimensions ou des seuils de diagnostic,
pas des filtres obligatoires de generation.
```
