---
doc_id: GO_OPT_TRADING_RUNTIME_TELEGRAM_XAUUSD_SIGNAL_REACTION_BACKTEST_01_INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_TELEGRAM_XAUUSD_SIGNAL_REACTION_BACKTEST_01
doc_type: initial_project_doc
status: approved
lifecycle_stage: opened
surface: runtime
source_kind: canonical_chantier
created_at: 2026-05-19
updated_at: 2026-05-19
owner_machine: admin-trading
branch: go/GO_OPT_TRADING_RUNTIME_TELEGRAM_XAUUSD_SIGNAL_REACTION_BACKTEST_01
index_policy: local_chantier_plus_inbox_only
execution_mode: paper_replay_only
live_trading: disabled
mutation_scope: doc_only_opening
---

# GO_OPT_TRADING_RUNTIME_TELEGRAM_XAUUSD_SIGNAL_REACTION_BACKTEST_01

## 1_MASTER_TARGET

Créer un module de screening et de backtest réactionnel pour les signaux Telegram XAU/USD CFD afin de mesurer objectivement, par canal et par mode d'exécution, ce qui est le plus rentable : suivre le signal, l'inverser, tester les deux sens, trader la réaction initiale, fader la réaction, ou ignorer.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche de référence initiale du GO. Il fixe le plan validé au démarrage et doit rester stable sauf changement explicite ou implicite du projet.

## 3_INITIAL_NEED

Besoin original validé :

- screener les signaux Telegram XAU/USD CFD ;
- parser BUY / SELL / ENTRY / SL / TP ;
- logger le message brut et les métadonnées de source ;
- logguer le prix XAU/USD au moment du signal puis à intervalles réguliers, minimum toutes les 30 secondes ;
- comparer plusieurs modes d'exploitation du signal ;
- classer les canaux et les modes par performance réelle observée ;
- rester en mode observation / paper / replay au départ.

## 4_MASTER_PROJECT_PLAN

Direction validée : bâtir un système simple, vérifiable et extensible qui transforme les signaux Telegram en dataset exploitable.

Axes majeurs :

1. Capture Telegram
   - lire les canaux autorisés ou accessibles ;
   - conserver le message brut ;
   - extraire les champs de trading ;
   - générer un `signal_id` stable.

2. Capture prix
   - capturer le prix XAU/USD CFD à `T0` ;
   - enregistrer des snapshots à `T+30s`, `T+60s`, `T+2m`, `T+5m`, `T+15m`, `T+30m` ;
   - permettre extension future à d'autres cadences.

3. Simulation multi-options
   - `FOLLOW_SIGNAL` : entrée dans le sens du signal ;
   - `INVERSE_SIGNAL` : entrée contraire avec TP/SL inversés ;
   - `BOTH_SIDES` : simulation long et short en parallèle ;
   - `DELAYED_FOLLOW_30S` : attendre 30 secondes puis suivre ;
   - `REACTION_CHASE` : entrer après confirmation du mouvement initial ;
   - `REACTION_FADE` : contrer le spike ou gap provoqué par la publication ;
   - `NO_TRADE` : baseline comparative.

4. Ledger et scoring
   - calculer le résultat par stratégie ;
   - agréger par canal, session horaire, direction, volatilité, délai et format du signal ;
   - produire un ranking exploitable.

5. Intégration future
   - DeskPro / Telegram notifier ;
   - webhook server ;
   - perf engine ;
   - Google Sheet ou export CSV ;
   - backtest replay.

## 5_GO_PLAN

Flux MVP :

```text
Telegram signal
  -> parse + normalize
  -> JSONL raw event
  -> XAU/USD price snapshots every 30s
  -> strategy simulations
  -> result ledger
  -> channel + strategy ranking
```

## 6_FINAL_TARGET

Livrable de phase 1 : documentation et contrat technique pour implémenter un logger minimal capable de :

- détecter un signal XAU/USD dans Telegram ;
- créer un événement JSONL ;
- capturer les prix à cadence fixe ;
- calculer au moins `FOLLOW_SIGNAL`, `INVERSE_SIGNAL`, `DELAYED_FOLLOW_30S`, `REACTION_FADE` ;
- sortir un premier classement après 50 à 100 signaux.

## 7_CANONICAL_STATE

Statut au démarrage : GO approuvé et ouvert doc-only.

Base validée :

- objectif = screening + comparaison statistique ;
- instrument initial = XAU/USD CFD ;
- source initiale = canaux Telegram de signaux ;
- cadence minimale = 30 secondes ;
- exécution réelle = désactivée ;
- priorité = logger et mesurer, pas trader.

NEXT_GO : implémenter le logger minimal en branche dédiée, puis lancer une collecte paper.

## 8_VALIDATED_PLAN

Étapes approuvées :

1. Créer le contrat de données `signal_event`.
2. Créer le contrat de données `price_snapshot`.
3. Créer le contrat de données `strategy_result`.
4. Définir les règles de parsing minimal.
5. Définir les simulations de base.
6. Logger en JSONL.
7. Calculer les résultats offline.
8. Classer les canaux et modes.

## 9_SELECTED_SOLUTION

Solution retenue : MVP simple, journalisé, sans auto-trade.

Structure logique :

- `collector` Telegram ;
- `parser` signal XAU/USD ;
- `price_sampler` XAU/USD ;
- `simulator` follow / inverse / delayed / reaction ;
- `ledger` JSONL ;
- `report` ranking.

## 10_SELECTED_SETUP

Format minimal `signal_event` :

```json
{
  "signal_id": "xau_20260519_000001",
  "source": "telegram_channel_a",
  "source_message_id": "12345",
  "symbol": "XAUUSD",
  "asset_class": "CFD",
  "side": "BUY",
  "entry": 2385.0,
  "sl": 2378.0,
  "tp": [2392.0, 2400.0],
  "signal_time_utc": "2026-05-19T12:00:00Z",
  "raw_text": "BUY XAUUSD ENTRY 2385 SL 2378 TP 2392 TP 2400"
}
```

Format minimal `price_snapshot` :

```json
{
  "signal_id": "xau_20260519_000001",
  "snapshot_time_utc": "2026-05-19T12:00:30Z",
  "offset_seconds": 30,
  "symbol": "XAUUSD",
  "bid": 2385.8,
  "ask": 2386.1,
  "mid": 2385.95,
  "source": "price_feed"
}
```

Format minimal `strategy_result` :

```json
{
  "signal_id": "xau_20260519_000001",
  "strategy_mode": "FOLLOW_SIGNAL",
  "entry_time_offset_seconds": 0,
  "side": "BUY",
  "entry_price": 2385.0,
  "exit_price": 2392.0,
  "exit_reason": "TP1",
  "result_r": 1.0,
  "result_points": 7.0,
  "max_favorable_excursion": 8.2,
  "max_adverse_excursion": -1.4
}
```

## 11_KEY_DECISIONS

- Le module démarre en paper / replay uniquement.
- Les signaux Telegram sont des données d'observation, pas des ordres.
- Le message brut doit toujours être conservé.
- Le prix observé réel prime sur le prix annoncé par le canal.
- Les performances sont calculées par canal et par mode.
- Le terme `front-running` ne doit pas être utilisé comme finalité opérationnelle ; la finalité correcte est `signal reaction backtest` / `reaction latency analysis`.

## 12_INVARIANTS

- Pas d'auto-trade live dans ce GO.
- Pas d'exécution broker.
- Pas de contournement d'accès Telegram.
- Pas d'utilisation d'information privée ou non autorisée.
- Pas de promesse de rentabilité.
- Chaque signal doit avoir un `signal_id` unique.
- Chaque résultat doit être recalculable depuis les logs.
- Les index globaux ne sont pas modifiés dans cette ouverture sauf instruction explicite.

## 13_ESTABLISHED

Établi par validation utilisateur :

- la bonne approche est de logger les signaux et leurs résultats ;
- la cadence 30 secondes est suffisante pour un MVP ;
- les options à tester incluent entrée identique, entrée contraire, deux sens, réaction post-signal, calcul statistique ;
- le projet doit être documenté immédiatement comme GO.

## 14_HYPOTHESIS

À valider par données :

- certains canaux sont plus rentables à suivre qu'à inverser ;
- certains canaux créent un gap exploitable très court terme ;
- certaines réactions initiales sont mieux fadées que suivies ;
- la performance dépend de la session horaire et du délai d'exécution ;
- les signaux XAU/USD CFD ont une alpha mesurable uniquement sur certains horizons.

## 15_REMAINING_GAP

Manques à combler :

- liste réelle des canaux Telegram à monitorer ;
- choix du flux de prix XAU/USD CFD ;
- parsing robuste des formats de signaux ;
- définition exacte des règles `REACTION_CHASE` et `REACTION_FADE` ;
- stockage durable final : JSONL seul, SQLite, Postgres, Google Sheet ou combinaison ;
- intégration DeskPro / notifier.

## 16_TODO

1. Ajouter un document `10_DATA_CONTRACTS.md`.
2. Ajouter un document `20_RUNTIME_MVP_PLAN.md`.
3. Ajouter un document `30_BACKTEST_METRICS.md`.
4. Implémenter un parser minimal XAU/USD.
5. Implémenter un logger JSONL.
6. Brancher un price sampler paper.
7. Produire un premier rapport après 50 signaux.

## 17_RESUME_POINT

Reprendre ici : créer les contrats de données et le plan runtime MVP, puis ouvrir l'implémentation minimale du collector/logger en mode paper-only.

## 18_TO_DOCUMENT

- `10_DATA_CONTRACTS.md` : schémas `signal_event`, `price_snapshot`, `strategy_result`.
- `20_RUNTIME_MVP_PLAN.md` : composants, commandes, variables, stockage.
- `30_BACKTEST_METRICS.md` : métriques, ranking, seuils et rapports.

## 19_TO_REMEMBER

### MEM_CANDIDATE

- `TELEGRAM_XAUUSD_SIGNAL_REACTION_BACKTEST` : logger les signaux Telegram XAU/USD CFD, capturer les prix toutes les 30 secondes et comparer follow, inverse, both-sides, delayed follow, reaction chase, reaction fade et no-trade.

### SAVE_MEMORY

- `GO_OPT_TRADING_RUNTIME_TELEGRAM_XAUUSD_SIGNAL_REACTION_BACKTEST_01` : GO approuvé pour bâtir un screener/backtest paper-only des signaux Telegram XAU/USD CFD, avec logs bruts, snapshots prix 30 secondes et ranking par canal/mode d'exécution.
