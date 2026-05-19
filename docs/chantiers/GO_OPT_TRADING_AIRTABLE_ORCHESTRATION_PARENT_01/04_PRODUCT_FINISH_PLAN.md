---
doc_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01_PRODUCT_FINISH_PLAN
doc_type: product_finish_plan
repo: opt-trading
project: opt-trading
module: orchestration
go_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
status: ready_for_review
lifecycle_stage: product_cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - airtable
  - product_finish_plan
  - trading_journal
  - bot_vision
  - orchestration
  - integration_ready
links:
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/01_RESEARCH_SYNTHESIS.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/02_INTEGRATION_ARCHITECTURE.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/03_AIRTABLE_SCHEMA_TRADING_JOURNAL_V1.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 04_PRODUCT_FINISH_PLAN — Airtable Orchestration pour opt-trading

## 1_MASTER_TARGET

Construire un produit fini limité mais exploitable : une couche Airtable d'orchestration humaine pour opt-trading, capable de recevoir des signaux, des trades, des analyses Bot Vision et des reviews, sans remplacer le coeur Python, le repo canonique ou la base historique.

## 2_INITIAL_PROJECT_DOC

Document initial de référence : `00_INITIAL_PROJECT_DOC.md`.

Ce document complète le cadrage en définissant le chemin vers le produit fini avant toute implémentation technique.

## 3_INITIAL_NEED

L'utilisateur demande de documenter la réponse et le plan vers le produit fini d'abord, en assurant une structure claire.

## 4_MASTER_PROJECT_PLAN

Le produit fini n'est pas Airtable seul.

Le produit fini est une intégration gouvernée composée de :

1. `opt-trading` comme coeur canonique.
2. `modules/airtable_bridge/` comme pont API optionnel.
3. Airtable comme interface humaine et couche de review.
4. Exports CSV/JSON comme stratégie de sortie.
5. DB future comme stockage historique si le volume dépasse Airtable.

## 5_GO_PLAN

### GO_PARENT courant

`GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`

### GO enfants proposés

| Ordre | GO | Objectif | Sortie attendue |
| --- | --- | --- | --- |
| 1 | `GO_OPT_TRADING_AIRTABLE_PRODUCT_CADRAGE_CHILD_01` | verrouiller le produit fini | présent document + structure claire |
| 2 | `GO_OPT_TRADING_AIRTABLE_SCHEMA_CHILD_01` | figer le modèle Airtable | schéma tables/champs/relations |
| 3 | `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` | créer module bridge Python | client API, config, sanity, cmd/menu |
| 4 | `GO_OPT_TRADING_AIRTABLE_BOT_VISION_CHILD_01` | brancher Bot Vision vers review Airtable | payload snapshot/analyse/review |
| 5 | `GO_OPT_TRADING_AIRTABLE_EXPORT_CHILD_01` | ajouter export / sortie DB-ready | JSON/CSV daily export |
| 6 | `GO_OPT_TRADING_AIRTABLE_CLOSEOUT_CHILD_01` | fermer le parent | closeout, limites, point de reprise |

## 6_FINAL_TARGET

### Produit fini V1

Nom proposé : `Airtable Orchestration Layer V1`.

Livrables finaux :

- base Airtable `opt-trading-journal` ou équivalent ;
- tables structurées : `trades`, `setups`, `signals`, `bot_vision_reviews`, `backtest_runs`, `exports`, `go_tracking` ;
- module repo : `modules/airtable_bridge/` ;
- scripts opérateur : `cmd.sh`, `menu.sh`, `sanity_check.sh` ;
- fichier `.env.example` sans secrets ;
- documentation d'installation ;
- export quotidien JSON/CSV ;
- closeout avec verdict `GO_LIMITED_PASS` ou `NO_GO_PROD`.

## 7_CANONICAL_STATE

Etabli au moment de ce document :

- branche dédiée parent ouverte : `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` ;
- connecteur GitHub validé ;
- connecteur Airtable validé par ping ;
- aucune base Airtable existante visible via connecteur ;
- docs existants :
  - `00_INITIAL_PROJECT_DOC.md`,
  - `01_RESEARCH_SYNTHESIS.md`,
  - `02_INTEGRATION_ARCHITECTURE.md`,
  - `03_AIRTABLE_SCHEMA_TRADING_JOURNAL_V1.md`.

## 8_VALIDATED_PLAN

Avant code :

1. clarifier le produit fini ;
2. figer les limites ;
3. figer les tables ;
4. figer les flux ;
5. seulement ensuite créer `modules/airtable_bridge/`.

## 9_SELECTED_SOLUTION

Solution retenue pour V1 : `GO_LIMITED`.

Airtable est utilisé comme couche :

- journal ;
- cockpit humain ;
- review Bot Vision ;
- suivi de signaux ;
- annotation de setups ;
- sortie CSV/JSON.

Airtable n'est pas utilisé comme :

- moteur trading ;
- moteur décisionnel live ;
- stockage tick data ;
- DB historique ;
- source canonique du repo.

## 10_SELECTED_SETUP

### Couches produit

| Couche | Surface | Rôle |
| --- | --- | --- |
| Core | opt-trading Python | calcul, ingestion, logique, validation |
| Bridge | `modules/airtable_bridge/` | API client, retry, batching, payload mapping |
| UI | Airtable | lecture humaine, statut, review, dashboard |
| Reporting | Sheets/CSV/JSON | exports, partage, stats simples |
| Historique | TimescaleDB/ClickHouse/Postgres | stockage massif futur |

### Flux cible

```text
TradingView / Telegram / Bot Vision / manual input
                  ↓
            opt-trading core
                  ↓
        modules/airtable_bridge
                  ↓
               Airtable
                  ↓
       review humaine + statut
                  ↓
          export JSON/CSV/DB
```

## 11_KEY_DECISIONS

1. Airtable reste optionnel : si Airtable tombe, opt-trading continue.
2. Tous les payloads envoyés à Airtable doivent exister en JSON local ou être reconstructibles.
3. Les secrets restent hors repo.
4. Le bridge doit gérer rate limit et retry.
5. Les tables Airtable doivent être lisibles par humain, pas optimisées comme une vraie DB.
6. Les gros volumes doivent sortir vers fichier ou DB.

## 12_INVARIANTS

- Pas de secret dans Git.
- Pas de dépendance runtime critique à Airtable.
- Pas de tick data dans Airtable.
- Pas de boucle temps réel à haute fréquence.
- Pas de remplacement du journal repo ou des docs canoniques par Airtable.
- Pas de création de code avant verrouillage du plan produit.

## 13_ESTABLISHED

Airtable est adapté pour :

- records structurés ;
- vues humaines ;
- relations simples ;
- automations modérées ;
- webhooks ;
- enrichissement AI léger ;
- review et workflow.

Airtable est limité pour :

- volume massif ;
- débit API ;
- backtests lourds ;
- historiques longs ;
- temps réel critique ;
- logique complexe.

## 14_HYPOTHESIS

Hypothèse produit V1 :

Airtable peut accélérer la validation humaine et la lecture opérateur sans dégrader l'architecture si l'intégration est strictement découplée.

## 15_REMAINING_GAP

Avant implémentation :

- choisir nom réel de base Airtable ;
- créer la base ou fournir baseId existant ;
- finaliser noms exacts des champs ;
- choisir si `go_tracking` est inclus en V1 ou repoussé ;
- décider si export va vers `data/airtable_exports/` ou `/srv/sftp/shared_files/shared`.

## 16_TODO

### Phase A — verrouillage produit

- valider ce document ;
- compléter le schéma `03_AIRTABLE_SCHEMA_TRADING_JOURNAL_V1.md` avec types de champs exacts ;
- produire `05_IMPLEMENTATION_SPEC.md`.

### Phase B — module repo

- créer `modules/airtable_bridge/` ;
- ajouter `app/client.py` ;
- ajouter `app/payloads.py` ;
- ajouter `scripts/sanity_check.sh`, `cmd.sh`, `menu.sh` ;
- ajouter `.env.example` ;
- ajouter tests sans réseau.

### Phase C — intégration Bot Vision

- définir payload snapshot ;
- définir payload analyse ;
- définir statut review ;
- connecter en mode fail-open.

### Phase D — export

- export quotidien JSON/CSV ;
- fichier sidecar de statut ;
- doc d'import DB future.

### Phase E — closeout

- tests exécutés ;
- limites documentées ;
- verdict PASS/FAIL ;
- point de reprise stable.

## 17_RESUME_POINT

Reprise :

- branche : `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` ;
- document actif : `04_PRODUCT_FINISH_PLAN.md` ;
- prochaine action : produire `05_IMPLEMENTATION_SPEC.md` puis seulement ensuite ouvrir le GO enfant d'implémentation du bridge.

## 18_TO_DOCUMENT

Documents à produire ensuite :

- `05_IMPLEMENTATION_SPEC.md` ;
- `06_OPERATOR_RUNBOOK.md` ;
- `07_SECURITY_AND_SECRETS.md` ;
- `90_CLOSEOUT.md`.

## 19_TO_REMEMBER

Memory Bricks projet :

- Produit fini V1 = Airtable Orchestration Layer, pas Airtable seul.
- Le bridge doit être optionnel et fail-open.
- Airtable sert la lecture humaine ; opt-trading reste le coeur logique.
- Aucun code d'intégration ne doit être produit avant verrouillage du plan produit.
