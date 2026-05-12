---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01_RANKING_METHOD
doc_type: ranking_method
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
status: draft_for_review
lifecycle_stage: child_ranking_method
parent_go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01
topic_keys:
  - opt-trading
  - trading
  - btc
  - coin-futures
  - ranking
  - reporting
  - free-search
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/04_ranking_method.md
point_de_reprise: "Definir comment classer les runs du free search BTC COIN-M."
updated_at: 2026-05-08
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/02_simulation_result_schema.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/03_reality_classifier_spec.md
---

# 04_ranking_method

## 1_MASTER_TARGET

Classer les configurations du free search BTC COIN-M d'abord par gain ou perte nette de BTC, puis fournir des vues secondaires permettant de distinguer le meilleur resultat mathematique brut du meilleur resultat reellement exploitable.

## 2_PRIMARY_SORT_KEY

Cle de tri primaire obligatoire :

```text
delta_btc_net = net_btc_final - net_btc_initial
```

Sens des vues :

```text
best  = tri descendant sur delta_btc_net
worst = tri ascendant sur delta_btc_net
```

## 3_MANDATORY_LEADERBOARDS

### 3.1 Classement brut mathematique

Population :

```text
tous les runs avec math_valid = true et data_valid = true
```

Ce leaderboard peut donc contenir :

```text
- des PAPER_ONLY
- des EXCHANGE_IMPOSSIBLE
- des LIQUIDATED si le run a produit des chiffres exploitables avant la rupture
```

### 3.2 Classement realiste strict

Population :

```text
classification_primary = REALISTIC
```

### 3.3 Classement exchange-feasible pragmatique

Population :

```text
classification_primary in {REALISTIC, PAPER_ONLY}
```

Cette vue est obligatoire car, dans l'etat actuel du projet, elle risque d'etre plus utile que `REALISTIC` seul tant que des hypotheses restent PAPER_LOCKED.

### 3.4 Classement destructeur BTC

Population :

```text
tous les runs math_valid = true et data_valid = true
```

Tri :

```text
delta_btc_net asc
```

But : identifier clairement les configurations qui detruisent le plus de BTC.

## 4_TIE_BREAKERS

En cas d'egalite sur `delta_btc_net`, appliquer dans cet ordre :

```text
1. liquidation_count le plus faible
2. max_drawdown_btc le plus faible
3. fees_btc + funding_paid_btc le plus faible
4. overfit_score le plus faible
5. config_hash ordre lexical stable
```

## 5_RECOMMENDED_FILTERS

Filtres utiles a exposer dans le rapport :

| Filtre | Role |
|---|---|
| `delta_btc_net > 0` | configs BTC positives |
| `delta_btc_net < 0` | configs destructrices |
| `liquidation_count = 0` | runs survivants |
| `exchange_feasible = true` | runs compatibles exchange au niveau observe |
| `classification_tags not contains OVERFIT_SUSPECT` | vue plus robuste |
| `used_mark_proxy = false` | vue sans proxy mark si disponible |

## 6_REPORT_VIEWS

Rapports minimaux a exporter :

```text
1. top_100_raw_best
2. top_100_raw_worst
3. top_100_exchange_feasible_best
4. top_100_realistic_best
5. top_100_non_liquidated_best
6. reject_reason_frequency
```

## 7_REQUIRED_COLUMNS_IN_RANKED_REPORTS

Chaque leaderboard doit au minimum contenir :

```text
rank
run_id
config_hash
delta_btc_net
delta_btc_pct
net_btc_final
max_drawdown_btc
liquidation_count
funding_paid_btc
fees_btc
classification_primary
classification_tags
reject_reasons
```

## 8_WALK_FORWARD_AND_OVERFIT_HANDLING

Une config peut etre numero 1 en brut et quand meme etre etiquetee `OVERFIT_SUSPECT`.

Politique recommandee :

```text
- le ranking principal ne modifie pas delta_btc_net
- l'overfit ne change pas la metrique primaire
- il ajoute un signal de prudence dans les vues pragmatiques
```

Vue complementaire conseillee :

```text
top_stable_configs
= configs avec delta_btc_net eleve ET overfit_score faible
```

## 9_PARETO_SECONDARY_VIEW

En plus du tri principal, conserver une vue Pareto sur :

```text
delta_btc_net       a maximiser
max_drawdown_btc    a minimiser
liquidation_count   a minimiser
```

Cette vue est secondaire. Elle ne remplace jamais le classement principal par `delta_btc_net`.

## 10_REPORT_FORMAT_RECOMMENDATION

Format recommande :

```text
- JSONL pour la machine
- CSV pour le tri manuel rapide
- Markdown pour les tops lisibles en revue humaine
```

## 11_INTERPRETATION_RULES

Regles de lecture :

```text
- le meilleur brut peut etre impossible exchange
- le meilleur realistic est la cible finale la plus importante
- si aucun REALISTIC n'existe, regarder le meilleur PAPER_ONLY exchange-feasible
- le pire ranking est utile pour identifier les zones de destruction BTC a bannir
```

## 17_RESUME_POINT

```text
Le ranking principal reste simple : delta_btc_net.
La sophistication arrive ensuite via les filtres, les tie-breakers,
et les vues separees brut / realistic / exchange-feasible / destructif.
```
