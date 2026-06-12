---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_PHASE_A_RANDOM_LARGE_01_CLOSEOUT
doc_type: closeout
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_PHASE_A_RANDOM_LARGE_01
status: pass
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
topic_keys:
  - opt-trading
  - trading
  - btc
  - coin-m
  - bitget
  - param-sweep
  - phase-a
  - random-large
  - simulation-only
surface: trading
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_PHASE_A_RANDOM_LARGE_01/90_CLOSEOUT.md
point_de_reprise: "Après merge PR #319 : ouvrir GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_PHASE_B_LATIN_HYPERCUBE_01."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_PHASE_A_RANDOM_LARGE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_PARAM_SWEEP_FREE_SEARCH_01/04_ranking_method.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_IMPL_01
  - docs/index/GO_INDEX.md
---

# CLOSEOUT — GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_PHASE_A_RANDOM_LARGE_01

## 13_ESTABLISHED

```text
PHASE_A_RANDOM_LARGE_01 = PASS expérimental
PR = #319
scope = simulation only
runtime = bloqué
live = bloqué
nouvelle_ui = bloquée
```

## Résultats établis

Campagne initiale :

```text
1000 configurations
20K bougies synthétiques
653 PAPER_ONLY
347 EXCHANGE_IMPOSSIBLE
0 liquidation
45 ms / run
top delta_btc_net = +0.227 BTC
meilleure classe = PAPER_ONLY via DCA
```

Artefacts runtime générés sous `state/trading_lab_v1/` : non commités, gitignored, utilisés comme preuve opératoire locale.

## 12_INVARIANTS maintenus

```text
- simulation only
- pas de live
- pas d'ordre réel
- pas de clé API privée
- pas de runtime
- pas de nouvelle UI
- pas d'utilisation trading réelle du top PAPER_ONLY
- les résultats impossibles restent utiles pour le classement, pas pour l'exécution
```

## 15_REMAINING_GAP

```text
- les meilleurs résultats sont encore PAPER_ONLY, pas REALISTIC
- données réelles longues insuffisantes via API Bitget directe
- EXCHANGE_IMPOSSIBLE encore élevé
- phase B doit améliorer l'exploration paramétrique
- phase C devra raffiner le top 5%
```

## 16_TODO — suite validée

GO de reprise à inscrire dans l'index global :

```text
GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_PHASE_B_LATIN_HYPERCUBE_01
```

Objectif :

```text
lancer la phase B de recherche paramétrique par latin hypercube,
après extension ou proxy des données historiques BTC COIN-M,
en conservant le scope simulation only.
```

## 17_RESUME_POINT

```text
Après merge PR #319, reprendre sur :
GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_SWEEP_PHASE_B_LATIN_HYPERCUBE_01

But : phase B latin hypercube + données historiques plus longues/proxy.
Ne pas ouvrir runtime/live/UI.
```

## RISKS

- À qualifier.
