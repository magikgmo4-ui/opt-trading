---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01_INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
module: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01
doc_type: initial_project_doc
status: draft
lifecycle_stage: parent_opening
topic_keys:
  - opt-trading
  - admin-trading
  - telegram
  - latency
  - strategy
  - bot-vision
  - openclaw
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-17
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/10_STRATEGY_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/20_SIGNAL_SCHEMA.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/30_REPLAY_BACKTEST_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/40_IMPLEMENTATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/50_OPENCLAW_TELEGRAM_BOTVISION_INTEGRATION.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/60_MACHINE_DEPLOYMENT_MAPPING.md
---

# 00_INITIAL_PROJECT_DOC — Telegram Latency Reaction Strategy

## 1_MASTER_TARGET

Créer un chantier parent autonome pour documenter puis préparer l’implémentation de la stratégie `Telegram Signal Latency Reaction Strategy` dans le format stratégie existant du repo `opt-trading`.

La stratégie vise à exploiter, en mode d’abord watch-only / replay / paper, la fenêtre courte entre la publication d’un call Telegram public et son absorption par le marché.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche initiale figée du parent :

`GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01`

Il transporte le plan validé depuis la session et sert de référence d’ouverture. Les documents enfants détaillent la spécification, le schéma signal, le replay/backtest, l’implémentation et l’intégration OpenClaw / Telegram / Bot Vision.

## 3_INITIAL_NEED

Documenter la nouvelle stratégie Telegram latency comme stratégie distincte, non fusionnée avec les stratégies déjà présentes.

Clarification validée :
- SMC/ICT est déjà présent ailleurs ;
- BTC accumulation / macro est déjà présent ailleurs ;
- les stratégies ne sont pas conditionnelles entre elles par défaut ;
- elles appartiennent à une bibliothèque de stratégies et peuvent ensuite être arbitrées par un moteur de décision ;
- la V1 Telegram latency doit être autonome.

## 4_MASTER_PROJECT_PLAN

Plan validé :

1. Créer un chantier parent sur branche dédiée.
2. Documenter la stratégie complète depuis la session.
3. Mapper le chantier sur une machine de déploiement.
4. Retrouver ensuite le format stratégie existant dans le repo.
5. Implémenter en V1 watch-only / replay / paper.
6. Brancher ensuite OpenClaw, Telegram et Bot Vision.
7. Définir ce qu’on screen, comment on le screen, comment on l’enregistre et comment on l’applique.

## 5_GO_PLAN

GO parent :

`GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01`

Branche dédiée :

`go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01`

Machine cible :

`ADMIN_TRADING`

Raison du mapping :
- le bloc machine existant contient déjà Telegram webhook, Bot Vision headless, Desk Pro runtime/smoke et Strategy Indicator ;
- la stratégie dépend du runtime d’observation Telegram, des snapshots marché et de la future application opérateur ;
- `ADMIN_TRADING` est donc la surface la plus cohérente pour le déploiement initial.

## 6_FINAL_TARGET

Livrable courant : dossier parent doc-only complet :

- `00_INITIAL_PROJECT_DOC.md`
- `10_STRATEGY_SPEC.md`
- `20_SIGNAL_SCHEMA.md`
- `30_REPLAY_BACKTEST_PLAN.md`
- `40_IMPLEMENTATION_PLAN.md`
- `50_OPENCLAW_TELEGRAM_BOTVISION_INTEGRATION.md`
- `60_MACHINE_DEPLOYMENT_MAPPING.md`
- entrée inbox locale sous `docs/index/inbox/`

## 7_CANONICAL_STATE

Établi :
- la stratégie est autonome ;
- elle n’est pas du MEV/front-running mempool ;
- elle ne fusionne pas SMC/ICT, macro ou BTC accumulation ;
- la V1 ne doit pas exécuter de trading réel ;
- elle démarre en watch-only / replay / paper ;
- l’intégration runtime vient après documentation et mapping.

## 8_VALIDATED_PLAN

Étapes approuvées :

1. ouvrir parent + branche dédiée ;
2. créer documentation entière ;
3. mapper sur machine ;
4. préparer implémentation Strategy Registry / Perf Engine / Trading Lab ;
5. intégrer OpenClaw / Telegram / Bot Vision après cadrage du screening.

## 9_SELECTED_SOLUTION

Nom stratégique retenu :

`Telegram Signal Latency Reaction Strategy`

Rôle :

`Exploiter la fenêtre courte entre publication Telegram publique et absorption marché, d’abord sans exécution réelle.`

## 10_SELECTED_SETUP

Modules attendus :

1. Telegram listener ;
2. Signal parser BUY/SELL ;
3. Timestamp exact `T0` ;
4. Market snapshot `T0` ;
5. Liquidity / spread / slippage check ;
6. Execution simulator ;
7. TP court / timeout exit ;
8. Journalisation ;
9. Backtest / replay ;
10. Perf Engine scoring.

## 11_KEY_DECISIONS

- Parent dédié ouvert au lieu d’un GO simple.
- Branche dédiée ouverte depuis `sot/mainline`.
- Machine cible : `ADMIN_TRADING`.
- V1 : watch-only / replay / paper.
- Aucun runtime live trading dans ce lot documentaire.

## 12_INVARIANTS

Ne pas mélanger :

- Telegram latency strategy ≠ SMC/ICT strategy ;
- Telegram latency strategy ≠ BTC accumulation / macro strategy ;
- Telegram latency strategy ≠ signal anticipation strategy ;
- Telegram latency strategy ≠ MEV/front-running mempool ;
- Telegram latency strategy ≠ manipulation de marché.

SMC/ICT et macro peuvent servir plus tard de pondération ou d’arbitrage, mais pas dans la V1.

## 13_ESTABLISHED

La stratégie suit ce flux minimal :

```text
Telegram call détecté
→ parsing signal
→ timestamp T0
→ snapshot marché
→ contrôle spread/liquidité/slippage
→ décision watch-only/paper
→ TP court simulé ou timeout
→ journalisation
→ replay/backtest
→ score Perf Engine
```

## 14_HYPOTHESIS

À valider par données :

- certains canaux Telegram produisent une expansion exploitable après publication ;
- la fenêtre exploitable est mesurable en secondes ou minutes ;
- le slippage ne détruit pas l’expectancy ;
- certains types d’actifs répondent mieux que d’autres ;
- certains canaux sont trop retardés ou trop distributeurs pour être exploitables.

## 15_REMAINING_GAP

Manque encore :

- localisation du format stratégie existant dans le repo ;
- liste des canaux Telegram à observer ;
- schéma canonique final des signaux ;
- stockage retenu ;
- règles d’application ;
- critères de passage de watch-only à paper ;
- critères de passage de paper à exécution contrôlée.

## 16_TODO

1. Recroiser le format stratégie existant dans le repo.
2. Créer le squelette Strategy Registry si absent ou mapper sur l’existant.
3. Définir les canaux Telegram observables.
4. Définir les assets screenés.
5. Définir le stockage replay.
6. Définir le module OpenClaw de supervision.
7. Définir le rôle exact Bot Vision.
8. Définir seuils paper-mode.

## 17_RESUME_POINT

Reprendre ici :

```text
Parent Telegram Latency Reaction Strategy ouvert sur branche dédiée.
Machine cible ADMIN_TRADING.
Prochaine action : retrouver le format stratégie existant, puis implémenter V1 watch-only / replay / paper.
```

## 18_TO_DOCUMENT

Blocs à maintenir :

- `10_STRATEGY_SPEC.md` : stratégie autonome ;
- `20_SIGNAL_SCHEMA.md` : structure signal et timestamp ;
- `30_REPLAY_BACKTEST_PLAN.md` : validation edge ;
- `40_IMPLEMENTATION_PLAN.md` : intégration code ;
- `50_OPENCLAW_TELEGRAM_BOTVISION_INTEGRATION.md` : orchestration runtime ;
- `60_MACHINE_DEPLOYMENT_MAPPING.md` : machine et déploiement.

## 19_TO_REMEMBER

MEM_CANDIDATE:
- [Telegram Latency Strategy Parent] : nouvelle stratégie autonome, distincte de SMC/ICT, macro/BTC accumulation et MEV mempool, à intégrer dans le format stratégie existant.
- [Machine Mapping] : ce chantier est mappé sur `ADMIN_TRADING` pour Telegram / Bot Vision / Desk Pro / Strategy Indicator.

SAVE_MEMORY:
- Aucun enregistrement mémoire durable automatique depuis ce chantier sans validation explicite.