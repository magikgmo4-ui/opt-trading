---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01_INTEGRATION_PLAN
doc_type: integration_plan
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01
status: draft_for_review
lifecycle_stage: child_integration_plan
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01
topic_keys:
  - opt-trading
  - trading
  - btc
  - coin-futures
  - integration
  - trading-lab
  - cli
  - testing
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/02_integration_plan.md
point_de_reprise: "Specifier l'integration du moteur de simulation dans trading_lab_v1 et les extensions CLI."
updated_at: 2026-05-08
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPLEMENTATION_SPEC_01/01_simulation_engine_contract.md
---

# 02_integration_plan

## 1_MASTER_TARGET

Definir comment le moteur de simulation s'integre dans `trading_lab_v1` : quels fichiers existants sont etendus, quels nouveaux fichiers sont crees, quelles commandes CLI sont ajoutees, et quel est le plan de tests.

## 2_REUSE_LIST

Ce qui est directement reutilisable depuis `trading_lab_v1` :

| Ressource | Usage |
|---|---|
| `append_jsonl()` / `load_jsonl()` | persistence des resumes de runs et des timelines |
| `count_jsonl()` | comptage rapide des lignes |
| `filter_records()` | filtrage par date/session dans le ranker |
| `avg()`, `counts_by()` | statistiques agregees dans le ranker |
| `STATE_DIR = .../state/trading_lab_v1` | meme espace de persistance |
| `render_markdown()` de `report_export_v1.py` | template pour les rapports Markdown |
| pattern `COMMANDS` dict | dispatch CLI |
| pattern `monkeypatch` des tests | isolation complete du filesystem |
| `parse_csv_timestamp()`, `to_minutes()` | parsing de timestamps |

Ce qui est IGNORE (non applicable au sweep BTC COIN-M) :

| Ressource | Raison |
|---|---|
| `PROFILE_PATH` et `load_profile()` | profil XAUUSD, pas BTC |
| `detect_fvg()`, `detect_sweep()` | feature engineering XAUUSD |
| `choose_variant_from_features()` | variant dual-stack |
| `build_market_event()`, `build_market_trade()` | schemas events/trades XAUUSD |
| `in_signal_window()`, `select_session_rows()` | fenetres de session XAUUSD |
| `SCHEMA` paths (event/trade XAUUSD) | non applicable |

## 3_NEW_FILES

### 3.1 Fichiers a creer

```text
modules/trading_lab_v1/app/param_sweep_engine_v1.py   # moteur de simulation
modules/trading_lab_v1/app/param_sweep_config_v1.py   # generateur de configs
modules/trading_lab_v1/app/param_sweep_classify_v1.py # classifieur realite
modules/trading_lab_v1/app/param_sweep_rank_v1.py     # ranker
modules/trading_lab_v1/tests/test_param_sweep_engine_v1.py  # tests moteur
modules/trading_lab_v1/tests/test_param_sweep_pipeline_v1.py # tests integration
```

### 3.2 Fichiers a modifier

```text
modules/trading_lab_v1/app/trading_lab_v1.py  # ajout COMMANDS sweep
modules/trading_lab_v1/scripts/cmd.sh          # ajout routes sweep
modules/trading_lab_v1/scripts/sanity.sh       # ajout checks existance fichiers
```

## 4_MODULE_DETAIL

### 4.1 param_sweep_engine_v1.py

Role : boucle de simulation candle-par-candle.

Fonctions exportees :

| Fonction | Signature | Role |
|---|---|---|
| `simulate_run(config, candles, contract_spec, initial_state, apply_guards) -> dict` | cf. section 5 de 01_simulation_engine_contract.md | run unique, retourne le dict conforme a `02_simulation_result_schema.md` |
| `resolve_price(candle, contract_spec) -> decimal` | utilise mark > index > close | resolution du prix de reference |
| `apply_funding(state, candle, contract_spec) -> state` | calcule funding_inc_btc | settlement funding 8h |
| `apply_dca(state, P, config) -> state` | calcule btc_bought, split spot/margin | DCA periodique |
| `apply_short_add(state, P, config, contract_spec) -> state` | calcule q_actual, MAJ E_k | ajout short |
| `apply_tp(state, P, config, contract_spec) -> state` | calcule q_close, PnL realise | prise de profit |
| `check_liquidation(state, P, contract_spec) -> state` | calcule liq_price | rupture liquidation |

Fonctions privees :

```text
_init_state(initial_state) -> state
_update_derived(state, P, contract_spec) -> state
_record_breaches(state, config) -> state
_build_output(state, input, stop_reason) -> dict
_validate_math(config) -> None  # leve ValueError si invalide
```

- `state` est un dict mutable passe de fonction en fonction.
- `input` est l'objet `SimulationInput` defini dans le contrat.

### 4.2 param_sweep_config_v1.py

Role : generer des configurations de sweep.

Fonctions exportees :

| Fonction | Signature | Role |
|---|---|---|
| `generate_configs(space, count, method, seed) -> list[dict]` | espace = spec parametrique, count = nb configs, method = random/lhs/grid, seed = int | genere count configs |
| `serialize_config(config) -> str` | dict canonique | produit une string stable pour le hash |
| `config_hash(config) -> str` | dict canonique | sha256 tronque du serialize |
| `sample_tp_triad(rng) -> (tp1, tp2, runner)` | random generator | echantillonnage Dirichlet + cas bord |

Methodes implementees (phase 1) :

```text
- random_search : tirage uniforme/log-uniform par variable
- latin_hypercube : via scipy.stats.qmc si dispo, sinon fallback manuel
```

Methodes futures (phase 2+) :

```text
- grid_search : produit cartesien sur un sous-ensemble de dims
- stress_sweep : banque de cas bord predefinis
- walk_forward : split temporel du dataset
```

### 4.3 param_sweep_classify_v1.py

Role : classer un run post-simulation.

Fonction exportee :

```text
classify_run(run_result: dict) -> dict
```

Retourne le meme dict avec les champs `classification_primary`, `classification_tags`, `reject_reasons` completes.

Implemente l'ordre de precedence defini dans `03_reality_classifier_spec.md` :

```text
MATH_INVALID -> DATA_INVALID -> LIQUIDATED -> EXCHANGE_IMPOSSIBLE -> PAPER_ONLY -> REALISTIC
```

### 4.4 param_sweep_rank_v1.py

Role : trier et produire les leaderboards.

Fonction exportee :

```text
rank_runs(runs: list[dict], mode: str) -> list[dict]
```

Modes :

| Mode | Population | Tri |
|---|---|---|
| `raw_best` | tous `math_valid` et `data_valid` | `delta_btc_net` desc |
| `raw_worst` | tous `math_valid` et `data_valid` | `delta_btc_net` asc |
| `realistic_best` | `classification_primary = REALISTIC` | `delta_btc_net` desc |
| `feasible_best` | `classification_primary in {REALISTIC, PAPER_ONLY}` | `delta_btc_net` desc |
| `non_liquidated_best` | `liquidation_count = 0` | `delta_btc_net` desc |

Tie-breakers par defaut (si `delta_btc_net` egal) :

```text
liquidation_count asc, max_drawdown_btc asc, (fees+funding_paid) asc, config_hash lex
```

## 5_CLI_EXTENSIONS

### 5.1 Nouvelles commandes dans trading_lab_v1.py

Ajouter au dict `COMMANDS` :

| Commande | Args | Handler |
|---|---|---|
| `param-sweep-run` | `[config_json_path] [data_jsonl_path]` | `param_sweep_run(args)` |
| `param-sweep-batch` | `[campaign_config_path]` | `param_sweep_batch(args)` |
| `param-sweep-report` | `[batch_id]` | `param_sweep_report(args)` |
| `param-sweep-export` | `[batch_id]` | `param_sweep_export(args)` |

### 5.2 Contrats des handlers

```text
param_sweep_run(args: list[str]) -> int
  args[0] = path vers un fichier JSON de config unique
  args[1] = path vers le JSONL de donnees historiques
  Retourne 0 si OK, 1 si erreur.
  Ecrit une ligne dans param_sweep_runs_summary.jsonl.

param_sweep_batch(args: list[str]) -> int
  args[0] = path vers un fichier JSON de config de campagne
    (contient : data_path, contract_spec, initial_state, space, count, method, seed)
  Genere count configs, simule chaque config,
  ecrit chaque resume dans param_sweep_runs_summary.jsonl.
  Affiche progression (compteur + ETA).

param_sweep_report(args: list[str]) -> int
  args[0] = batch_id (optionnel, dernier batch si absent)
  Charge les runs du batch, applique classify_run + rank_runs,
  produit top_100 en Markdown dans state/trading_lab_v1/.

param_sweep_export(args: list[str]) -> int
  args[0] = batch_id (optionnel)
  Exporte le CSV complet des runs + top_100_best.md + top_100_worst.md.
```

### 5.3 Extensions cmd.sh

Ajouter dans le case/switch :

```bash
param-sweep-run)
    python3 "$APP" param-sweep-run "$A2" "$A3"
    ;;
param-sweep-batch)
    python3 "$APP" param-sweep-batch "$A2"
    ;;
param-sweep-report)
    python3 "$APP" param-sweep-report "$A2"
    ;;
param-sweep-export)
    python3 "$APP" param-sweep-export "$A2"
    ;;
```

### 5.4 Extensions sanity.sh

Verifier l'existence de :

```text
app/param_sweep_engine_v1.py
app/param_sweep_config_v1.py
app/param_sweep_classify_v1.py
app/param_sweep_rank_v1.py
```

## 6_STATE_PERSISTENCE

Nouveaux fichiers dans `state/trading_lab_v1/` :

| Fichier | Format | Contenu |
|---|---|---|
| `param_sweep_runs_summary.jsonl` | JSONL | une ligne par run (= resume canonique) |
| `param_sweep_runs_summary.csv` | CSV | export tabulaire des memes donnees |
| `param_sweep_top_best.md` | Markdown | top 100 raw best |
| `param_sweep_top_worst.md` | Markdown | top 100 raw worst |
| `param_sweep_timelines/{run_id}.jsonl` | JSONL | timeline etat-par-etat d'un run (optionnel) |
| `param_sweep_events/{run_id}.jsonl` | JSONL | journal d'evenements d'un run (optionnel) |
| `param_sweep_campaigns.jsonl` | JSONL | metadonnees de campagne (batch_id, date, nb runs, etc.) |

## 7_TEST_PLAN

### 7.1 test_param_sweep_engine_v1.py

Tests unitaires du moteur :

| Test | Description |
|---|---|
| `test_simulate_run_empty_candles_returns_initial_state` | aucune bougie, etat inchange |
| `test_simulate_run_no_position_does_nothing` | pas de short, pas de DCA si fonds insuffisants |
| `test_apply_funding_positive_rate_adds_btc` | fundingRate > 0 -> M_k augmente |
| `test_apply_funding_negative_rate_deducts_btc` | fundingRate < 0 -> M_k diminue |
| `test_apply_dca_with_sufficient_reserve` | reserve OK -> spot + marge augmentent |
| `test_apply_dca_with_insufficient_reserve_skips` | reserve KO -> skip DCA |
| `test_apply_dca_with_r_transfer_split` | r_transfer > 0 -> BTC partage spot/margin |
| `test_apply_short_add_with_signal` | prix monte de g_up -> short ajoute |
| `test_apply_short_add_no_signal_skips` | prix stable -> skip short |
| `test_apply_short_add_updates_entry_price` | E_k mis a jour apres ajout |
| `test_apply_tp_closes_position_partial` | tp1 + tp2 reduisent Q, runner reste |
| `test_apply_tp_closes_position_full` | tp1=1 -> Q=0, E=null |
| `test_check_liquidation_detects_breach` | P >= liq_price -> liquidation_count += 1 |
| `test_check_liquidation_no_breach_passes` | P < liq_price -> pas de liquidation |
| `test_output_matches_required_columns` | toutes les colonnes obligatoires sont presentes |
| `test_stop_reason_completed` | fin de boucle normale |
| `test_stop_reason_liquidated` | liquidation interrompt la boucle |
| `test_stop_reason_math_invalid` | NaN dans le state -> stop |
| `test_record_breaches_logs_D_min` | D_k < D_min -> breach enregistre |
| `test_z_short_le_z_dca_not_blocked_in_free_search` | garde-fou non bloquant |

### 7.2 test_param_sweep_pipeline_v1.py

Tests d'integration :

| Test | Description |
|---|---|
| `test_full_pipeline_single_config` | generate -> simulate -> classify -> rank |
| `test_batch_10_random_configs` | 10 configs random simulees sans erreur |
| `test_classify_math_invalid` | config invalide -> MATH_INVALID |
| `test_classify_liquidated` | liquidation simulee -> LIQUIDATED |
| `test_classify_exchange_impossible` | q_add_native hors grille -> EXCHANGE_IMPOSSIBLE |
| `test_classify_paper_only` | mark proxy -> PAPER_ONLY |
| `test_rank_raw_best_descending` | tri desc sur delta_btc_net |
| `test_rank_raw_worst_ascending` | tri asc sur delta_btc_net |
| `test_tp_simplex_sum_is_one` | Dirichlet produit tp1+tp2+runner=1 |
| `test_config_hash_is_stable` | meme config -> meme hash |

## 8_WHAT_IS_OUT_OF_SCOPE

Dans ce child (spec only) :

```text
- pas de code Python produit
- pas de tests executes
- pas de simulation lancee
- pas de donnees historiques telechargees
- pas de fichier JSONL de donnees cree
- pas de state/trading_lab_v1/ initialise
- pas de benchmark de performance
- pas d'implementation de la weekly gate
```

## 17_RESUME_POINT

```text
L'integration repose sur l'extension de trading_lab_v1 avec 4 nouveaux modules
et 4 nouvelles commandes CLI, en reutilisant la persistence JSONL, le dispatch CLI,
et l'isolation des tests deja en place.
Aucun module existant n'est casse : le code XAUUSD reste intact.
```
