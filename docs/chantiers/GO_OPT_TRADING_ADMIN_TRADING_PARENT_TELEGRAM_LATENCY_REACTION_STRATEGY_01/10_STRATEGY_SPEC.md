---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01_STRATEGY_SPEC
repo: opt-trading
project: opt-trading
module: admin-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01
doc_type: strategy_spec
status: draft
lifecycle_stage: parent_spec
topic_keys: [opt-trading, admin-trading, telegram, latency, strategy]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-17
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_TELEGRAM_LATENCY_REACTION_STRATEGY_01/00_INITIAL_PROJECT_DOC.md
---

# 10_STRATEGY_SPEC — Telegram Signal Latency Reaction Strategy

## Objectif

Documenter une stratégie autonome qui réagit immédiatement à un call Telegram public afin de mesurer puis éventuellement exploiter la fenêtre entre publication et absorption marché.

## Non-objectif

Ce n’est pas :
- du MEV ;
- du front-running mempool ;
- une stratégie SMC/ICT ;
- une stratégie BTC accumulation / macro ;
- une stratégie de prédiction avant publication ;
- une chaîne conditionnelle avec les autres stratégies existantes.

## Hypothèse stratégique

```text
Telegram call publié
→ latence d’absorption par les abonnés / le marché
→ expansion courte mesurable
→ sortie rapide ou timeout
```

## Mode V1

La V1 est strictement :
- watch-only ;
- replay ;
- paper/simulated execution ;
- sans ordre réel ;
- sans broker ;
- sans mutation runtime dangereuse.

## Inputs

- canal Telegram ;
- message brut ;
- timestamp exact `T0` ;
- symbole détecté ;
- direction détectée ;
- prix marché à `T0` ;
- spread ;
- liquidité ;
- volatilité courte ;
- contexte minimal exchange/source.

## Outputs

- signal normalisé ;
- décision watch/paper ;
- entrée simulée ;
- TP court simulé ;
- timeout ;
- slippage estimé ;
- PnL simulé ;
- score expectancy ;
- journal replay.

## Critères de validité

La stratégie ne devient exploitable que si les données prouvent :
- une expansion moyenne post-call supérieure au coût slippage/spread ;
- une fenêtre temporelle suffisante ;
- une répétabilité par canal / actif / type de call ;
- un risque de distribution acceptable ;
- une exécution simulée robuste.

## Invalidation

Invalidation si :
- le prix bouge majoritairement avant la publication ;
- le canal publie trop tard ;
- le slippage absorbe l’edge ;
- les calls sont trop ambigus ;
- l’expectancy devient négative après coûts.

## Relation aux autres stratégies

Les autres stratégies peuvent être utilisées plus tard comme pondération par un Decision Engine, mais ne sont pas requises par la V1.

```text
Strategy Library
├── Telegram Latency Reaction
├── SMC/ICT
├── BTC Accumulation / Macro
├── Momentum
└── autres stratégies

Decision Engine futur
→ pondération / arbitrage / consensus
```

## Point de reprise

Prochaine étape : formaliser le schéma signal dans `20_SIGNAL_SCHEMA.md` puis préparer replay/backtest.