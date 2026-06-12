---
doc_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: orchestration
go_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
status: open
lifecycle_stage: cadrage_parent
topic_keys:
  - airtable
  - orchestration
  - trading_journal
  - bot_vision
  - workflow_ai
  - no_code_database
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT - reprendre par la validation du role exact Airtable dans la stack opt-trading"
updated_at: 2026-04-24
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01

## 1_MASTER_TARGET

Evaluer Airtable comme couche d'orchestration, journalisation, dashboard et workflow no-code/low-code pour les usages opt-trading : trading journal, backtests, Bot Vision, pipeline Telegram/TradingView, workflow AI/multi-agent et suivi de projets.

## 2_INITIAL_PROJECT_DOC

Ce document est le transporteur initial du chantier parent. Il fixe le besoin, le plan de recherche, les invariants et le point de reprise. Il ne valide pas encore Airtable comme solution finale ; il ouvre l'analyse.

## 3_INITIAL_NEED

Demande utilisateur : ouvrir un chantier parent dans une branche dédiée, documenter la réponse entière, approfondir les recherches sur Airtable en gardant l'usage opt-trading comme sortie, puis élaborer les possibilités et leurs limites.

## 4_MASTER_PROJECT_PLAN

Direction :
1. Vérifier le contexte canonique repo-first.
2. Ouvrir une branche dédiée au chantier parent.
3. Produire une documentation parent initiale.
4. Rechercher l'état actuel d'Airtable : plans, limites, API, automatisations, AI, intégrations.
5. Recroiser Airtable avec les usages réels : trading journal, backtest, Bot Vision, Telegram, TradingView, Google Sheets, DB layer, workflow AI.
6. Distinguer rôle recommandé, limites, risques, et architecture cible.

## 5_GO_PLAN

GO parent : GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01

Sous-lots potentiels :
- GO_OPT_TRADING_AIRTABLE_RESEARCH_CHILD_LIMITS_01
- GO_OPT_TRADING_AIRTABLE_ARCHITECTURE_CHILD_TRADING_JOURNAL_01
- GO_OPT_TRADING_AIRTABLE_ARCHITECTURE_CHILD_BOT_VISION_01
- GO_OPT_TRADING_AIRTABLE_DECISION_CHILD_VENDOR_FIT_01

## 6_FINAL_TARGET

Livrable de phase : une analyse exploitable permettant de décider si Airtable doit servir de :
- couche dashboard/journal rapide,
- couche de validation humaine,
- cockpit no-code pour signaux et backtests,
- CRM/workflow AI,
- ou seulement outil secondaire non critique.

## 7_CANONICAL_STATE

Etabli dans cette session :
- Connecteur GitHub disponible.
- Repo cible : magikgmo4-ui/opt-trading.
- Branche dédiée ouverte : go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01.
- Matrice canonique lue : docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md.
- Connecteur Airtable disponible et répond : pong.

## 8_VALIDATED_PLAN

Plan validé implicitement par la demande :
- branche dédiée parent,
- doc initiale parent,
- recherche approfondie,
- sortie orientée usage réel,
- séparation possibilités / limites.

## 9_SELECTED_SOLUTION

Aucune solution finale validée. Hypothèse de travail : Airtable est mieux positionné comme couche d'orchestration humaine, dashboard, validation et journalisation structurée, pas comme moteur de calcul, moteur de trading temps réel ou base de données massive.

## 10_SELECTED_SETUP

Setup candidat à évaluer :
- Airtable pour tables relationnelles légères et interfaces.
- Python / opt-trading pour calculs, backtests, ingestion et logique.
- Google Sheets pour reporting imprimable et calculs simples collaboratifs.
- TimescaleDB / ClickHouse / Postgres pour historique massif.
- Telegram / TradingView / scripts pour flux d'entrée.

## 11_KEY_DECISIONS

- Ne pas traiter Airtable comme moteur de trading live.
- Ne pas utiliser Airtable comme stockage primaire haute fréquence.
- Garder Airtable dans un rôle gouverné : journal, cockpit, review humaine, statut, feedback, enrichissement AI léger.
- Les limites de plan, API et automatisation doivent être vérifiées avant architecture définitive.

## 12_INVARIANTS

- Repo-first.
- Branche dédiée pour chantier parent.
- Pas de branche décorative : la branche sert un parent documentaire réel.
- Pas de décision solution sans limites prouvées.
- Airtable ne doit pas remplacer le repo canonique opt-trading.
- Airtable ne doit pas devenir source souveraine du système de trading.

## 13_ESTABLISHED

- Airtable est une plateforme no-code/low-code orientée bases relationnelles, vues, interfaces et automatisations.
- Le connecteur Airtable est actif côté ChatGPT.
- La recherche doit tenir compte des plans, quotas API, quotas records, quotas AI et limites de sync.

## 14_HYPOTHESIS

- Airtable peut être excellent pour MVP de journal trading/backtest et validation humaine.
- Airtable devient risqué si utilisé pour flux intraday dense, tick data, backtests massifs ou automatisations fréquentes.
- Airtable + API + Python peut suffire pour un cockpit opérateur sans remplacer la DB layer.

## 15_REMAINING_GAP

A valider :
- volume prévu de records par jour,
- fréquence API réelle,
- besoin d'interface mobile,
- besoin de dashboards temps réel,
- coût acceptable,
- rôle par rapport à Google Sheets déjà demandé par l'utilisateur,
- rôle par rapport à TimescaleDB / ClickHouse envisagés.

## 16_TODO

1. Finaliser la synthèse de recherche Airtable.
2. Comparer Airtable / Google Sheets / vraie DB / custom LocalCMS.
3. Définir architecture recommandée par usage.
4. Produire verdict : GO / NO_GO / GO_LIMITED.
5. Si GO_LIMITED : proposer schéma MVP minimal.

## 17_RESUME_POINT

Reprendre depuis : branche go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01, fichier docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/00_INITIAL_PROJECT_DOC.md. Prochaine action : finaliser l'analyse Airtable actuelle et décider du rôle exact dans la stack opt-trading.

## 18_TO_DOCUMENT

- AIRTABLE_ORCHESTRATION_RESEARCH_SYNTHESIS_01
- AIRTABLE_TRADING_JOURNAL_ARCHITECTURE_V1
- AIRTABLE_BOT_VISION_REVIEW_PIPELINE_V1
- AIRTABLE_LIMITS_AND_EXIT_STRATEGY_01

## 19_TO_REMEMBER

Memory Bricks projet, pas mémoire bio :
- Airtable est à considérer comme couche d'orchestration/journal/dashboard, non comme moteur de trading ni DB massive.
- Tout usage Airtable dans opt-trading doit garder une sortie exportable et une stratégie de sortie vers DB ou fichiers canoniques.

## RISKS

- À qualifier.
