---
doc_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01_RESEARCH_SYNTHESIS
doc_type: research_synthesis
repo: opt-trading
project: opt-trading
module: orchestration
go_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
status: draft_ready
lifecycle_stage: research
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
topic_keys:
  - airtable
  - api_limits
  - sync_limits
  - automation_limits
  - ai_credits
  - trading_orchestration
links:
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 01_RESEARCH_SYNTHESIS — Airtable pour opt-trading

## 1_MASTER_TARGET

Qualifier Airtable comme couche possible d'orchestration, journalisation, interface humaine, review et dashboard pour opt-trading.

## 3_INITIAL_NEED

L'utilisateur veut poursuivre la suite recommandée directement dans le repo, avec recherche nécessaire et documentation prête pour intégration.

## 7_CANONICAL_STATE

- Branche parent : `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01`.
- Document initial : `00_INITIAL_PROJECT_DOC.md`.
- Connecteur GitHub : validé.
- Connecteur Airtable : validé par `pong`.
- Bases Airtable accessibles via connecteur : aucune base listée au moment de cette passe.

## 13_ESTABLISHED — faits techniques vérifiés

### API

- Airtable Web API est REST/JSON.
- Les listes de records sont paginées à 100 records maximum par page.
- Limite API générale : 5 requêtes/seconde/base.
- Limite supplémentaire : 50 requêtes/seconde pour tout le trafic via personal access token d'un utilisateur ou compte de service.
- Dépassement : status 429, attente nécessaire avant reprise.
- Batching : jusqu'à 10 records par requête sur les opérations de création/mise à jour/suppression.

### Plans / capacité

- Free : 1 000 records/base, 1 000 API calls/workspace/mois, 1 GB attachments/base.
- Team : 50 000 records/base, 100 000 API calls/workspace/mois, 20 GB attachments/base.
- Business : plan plus large, prix et limites plus élevés selon Airtable.
- Enterprise Scale : capacité plus large / custom.
- Les records par base sont cumulés entre tables.
- Limites structurantes mentionnées par Airtable : jusqu'à 1 000 tables/base, 1 000 views/base, 500 fields/table.

### Sync

- Airtable Sync indisponible sur Free.
- Team : sync limité comparativement à Business/Enterprise.
- Sync API : CSV jusqu'à 10 000 lignes, 500 colonnes et 2 MB par requête.
- Sync API : 20 requêtes / 5 minutes / base.
- Integrated sync : limite 10 000 records/source intégrée.

### Webhooks

- Airtable Webhooks API permet d'être notifié de changements dans une base : création de record, update field, entrée/sortie d'une vue.
- Airtable précise que les webhooks ne sont pas toujours la meilleure option selon le workflow ; alternative possible : automation script.

### AI

- Airtable AI est disponible avec des crédits mensuels selon plan.
- Les crédits sont mutualisés au niveau workspace/organization selon le plan.
- AI Airtable utile pour enrichissement, classification et synthèse légère, pas comme pipeline AI critique de trading.

## 14_HYPOTHESIS

- Airtable est adapté à la couche humaine : review, annotation, statut, cockpit, follow-up, backlog.
- Airtable est inadapté comme base historique principale pour flux haute fréquence, tick data, snapshots massifs ou backtests volumineux.
- Airtable peut servir de MVP rapide si l'architecture garde une sortie DB/fichiers.

## 9_SELECTED_SOLUTION — verdict provisoire

`GO_LIMITED_RECOMMENDED`

Airtable est recommandé uniquement comme :
- cockpit opérateur,
- trading journal V1,
- couche review humaine pour Bot Vision,
- suivi de signaux et décisions,
- couche workflow AI légère,
- support projet/GO tracking.

Airtable est déconseillé comme :
- moteur temps réel,
- système d'exécution trading,
- stockage primaire de marché,
- moteur backtest massif,
- source canonique repo.

## 12_INVARIANTS

- opt-trading reste le repo canonique.
- Python / modules opt-trading restent le moteur logique.
- Airtable ne doit jamais bloquer l'exécution trading.
- Tout record important doit être exportable vers JSON/CSV/DB.
- Aucune clé API Airtable ne doit être committée.

## 15_REMAINING_GAP

- Choisir plan Airtable réel si intégration active.
- Créer base Airtable cible ou connecter une base existante.
- Décider si Google Sheets reste surface de reporting principale.
- Mesurer volume réel journalier : trades, signaux, screenshots, analyses.
- Définir TTL/rétention : combien de jours restent dans Airtable avant export/archive.

## 16_TODO

1. Créer ou sélectionner une base Airtable.
2. Créer les tables V1 proposées dans `03_AIRTABLE_SCHEMA_TRADING_JOURNAL_V1.md`.
3. Ajouter secrets localement : `.env` non committé.
4. Implémenter un client Python minimal avec backoff et batching.
5. Tester ingestion depuis Bot Vision et trading journal.
6. Exporter quotidiennement vers fichier/DB.

## Sources consultées

- Airtable Support — Getting started with Airtable Web API.
- Airtable Support — Managing API Call Limits in Airtable.
- Airtable Support — Airtable plans overview.
- Airtable Support — Airtable Sync overview.
- Airtable Support — Sync API.
- Airtable Support — Airtable Webhooks API overview.
- Airtable Support — Airtable AI billing.
- Airtable pricing page.
