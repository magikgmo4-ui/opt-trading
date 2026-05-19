---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01_ROLES_INVENTORY
doc_type: inventory
repo: opt-trading
project: opt-trading
module: matrix
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01
status: draft_canonical
lifecycle_stage: inventory
topic_keys:
  - opt-trading
  - roles
  - jobs
  - tasks
  - strict_workers
  - autonomy
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
---

# 10_ROLES_JOBS_TASKS_INVENTORY

## 1. Rôles AI Team Architecture

| Rôle AI Team | Description | Responsabilités | Niveau autonomie max | Worker machine cible |
| --- | --- | --- | --- | --- |
| Manager / Orchestrator | Coordonne les spécialistes, décide de l'affectation des tâches | Routage, priorisation, validation finale | A4 (HITL) | db-layer (OpenClaw Gateway) |
| Specialiste raisonnement | Propositions, analyse, patch complexe | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | A2 | db-layer |
| Specialiste volume | Extraction, inventaire, documentation masse | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | A2 | db-layer |
| Specialiste long contexte | Code reading, inventaire commits, cherry-pick | READ_INVENTORY, CHERRY_PICK_INVENTORY | A2 | db-layer |
| Specialiste flash/tri | Triage rapide, classification, formats courts | FAST_TRIAGE, READ_INVENTORY | A1 | db-layer |
| Consolidateur | Vérification des sorties DRAFT_ONLY | Revue, validation, rejet | A4 (humain ou modele fort) | db-layer / humain |
| Safety Gate | Blocage des actions interdites, validation des permissions | Filtrage, vérification invariants | A4 (system) | db-layer (OpenClaw Gateway) |

## 2. Métiers / Responsabilités Opérationnelles

| Métier | Responsabilité | Surfaces liées | GO associé |
| --- | --- | --- | --- |
| Architecture trading | Définir et maintenir l'architecture trading globale | desk_pro, execution_engine, risk_engine | GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 |
| Pilotage GO | Suivre et mettre à jour l'état des GO | ClickUp, GO_INDEX, BRANCH_STATE | GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01 |
| Cartographie repo | Maintenir le knowledge graph du repo | Repo KG | GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01 |
| Data cockpit | Gérer les données légères (journal, backtests, signaux) | Airtable | GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01 |
| Opérateur conversationnel | Gérer les intents Telegram → Botpress → surfaces | Telegram, Botpress, OpenClaw | GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01 |
| Infra / connectivité | Maintenir le backbone SSH, SFTP, SSHFS | reseau_ssh, shared_files_sftp | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 |
| Vision / artefacts | Pipeline vision bot headless | bot_vision, desk_pro | GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_* |
| Exécution trading | Gérer l'exécution des trades paper et production | execution_engine, simex_bitget_bridge | GO_OPT_TRADING_ADMIN_TRADING_PAPER_* |

## 3. Jobs Opérationnels (Pipeline Workers à Produire)

| Job | Description | Déclencheur | Sortie | Dépendances | Niveau confiance actuel |
| --- | --- | --- | --- | --- | --- |
| signal_router | Router un signal TradingView vers le pipeline | Webhook entrant | Signal JSON enrichi | market_scanner, collector_binance_spot | 0 — à produire |
| proposition_engine | Analyser un signal et produire une proposition | Signal JSON | Proposition JSON + confidence | decision_engine, opportunity_ranker, probability_engine | 0 — à produire |
| validation_gate | Valider/rejeter une proposition | Proposition JSON | APPROVED/REJECTED | risk_engine, kil_v1 | 0 — à produire |
| trade_executor | Exécuter un trade validé | APPROVED | trade_id + fill | execution_engine, simex_bitget_bridge | 0 — à produire |
| result_tracker | Suivre le résultat d'un trade | fill | P&L brut | position_engine, portfolio_engine | 0 — à produire |
| datasheet_writer | Écrire les résultats dans les datasheets | P&L | Datasheet mise à jour | journal_engine, Airtable | 0 — à produire |
| learning_feeder | Alimenter la boucle d'apprentissage | Résultat + contexte | Memory brick | memory_bricks | 0 — à produire |
| notification_dispatcher | Envoyer notifications Telegram | Tout événement | Message Telegram | Telegram API | 0 — à produire (Telegram OK) |
| task_tracker | Mettre à jour l'état des tâches dans ClickUp | Changement état GO | ClickUp update | ClickUp API | 0 — à produire (ClickUp OK) |

## 4. Tasks Strict Workers (Indexées dans tasks.index.json)

| Task ID | Autonomie max | Write code | Outputs autorisés | Sections requises | Statut |
| --- | --- | --- | --- | --- | --- |
| READ_INVENTORY | A1 | false | reports/ai/workers/** | 13_ESTABLISHED, 14_HYPOTHESIS, 15_REMAINING_GAP, 16_TODO, FICHIERS_LUS, RISQUES, VERDICT_DRAFT_ONLY | DRAFT_ONLY |
| PATCH_DRAFT | A2 | false | reports/ai/workers/** | OBJECTIF_PATCH, FICHIERS_TOUCHES, DIFF_ATTENDU, RISQUES, TESTS_A_EXECUTER, VERDICT_DRAFT_ONLY | DRAFT_ONLY |
| DOC_DRAFT | A2 | false | reports/ai/workers/**, docs/chantiers/** | CONTEXTE, ETAT_INITIAL, CHANGEMENTS, VALIDATIONS, LIMITES, POINT_DE_REPRISE, VERDICT_DRAFT_ONLY | DRAFT_ONLY |
| TESTPLAN | A2 | false | reports/ai/workers/** | TESTS_UNITAIRES, TESTS_SMOKE, COMMANDES, CRITERES_PASS_FAIL, RISQUES_RESTANTS, VERDICT_DRAFT_ONLY | DRAFT_ONLY |
| CHERRY_PICK_INVENTORY | A2 | false | reports/ai/workers/** | COMMITS_CANDIDATS, FICHIERS_TOUCHES, DEPENDANCES, RISQUES_CONFLITS, ORDRE_RECOMMANDE, COMMANDES_NON_EXECUTEES, VERDICT_DRAFT_ONLY | DRAFT_ONLY |
| FAST_TRIAGE | A1 | false | reports/ai/workers/** | RESUME, CLASSEMENT, RISQUES, TODO, VERDICT_DRAFT_ONLY | DRAFT_ONLY |
| ENDPOINT_AUDIT | A1 | false | reports/ai/workers/** | ENDPOINT_CONSULTE, MODELES_TROUVES, COMPARAISON_REGISTRY, AJOUTS, RETRAITS, RECOMMANDATIONS, VERDICT_DRAFT_ONLY | DRAFT_ONLY |
| WRITE_GATED | A4 | false (dry-run) | docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_*/**, reports/ai/workers/**, scripts/ai/workers/job_packets/** | 13_ESTABLISHED, 14_HYPOTHESIS, WRITE_PLAN, WRITE_DIFF_ATTENDU, VALIDATION_EXTERNE, DRY_RUN_RESULT, RISQUES, VERDICT_WRITE_GATED | DRAFT_ONLY |

## 5. Correspondance Rôles → Jobs → Tasks

| Rôle AI Team | Jobs opérationnels | Tasks strict workers autorisées |
| --- | --- | --- |
| Manager / Orchestrator | task_tracker, notification_dispatcher | WRITE_GATED, READ_INVENTORY |
| Specialiste raisonnement | proposition_engine, validation_gate | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, ENDPOINT_AUDIT |
| Specialiste volume | datasheet_writer, learning_feeder | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT |
| Specialiste long contexte | signal_router, result_tracker | READ_INVENTORY, CHERRY_PICK_INVENTORY |
| Specialiste flash/tri | notification_dispatcher (triage) | FAST_TRIAGE, READ_INVENTORY |
| Consolidateur | validation_gate (validation finale) | REVIEW_DRAFT |
| Safety Gate | Tous (filtrage amont) | Aucune (rôle systeme) |
| Agent d'exécution | trade_executor | WRITE_GATED (dry-run) |

## 6. Niveaux d'Autonomie par Task

| Task | Autonomie max | Validation requise | Owner validation |
| --- | --- | --- | --- |
| READ_INVENTORY | A1 | Modele fort + tests | Consolidateur |
| PATCH_DRAFT | A2 | Modele fort + tests | Consolidateur |
| DOC_DRAFT | A2 | Revue externe | Humain / modele fort |
| TESTPLAN | A2 | Modele fort + tests | Consolidateur |
| CHERRY_PICK_INVENTORY | A2 | Revue externe stricte | Consolidateur |
| FAST_TRIAGE | A1 | Revue par echantillon | Consolidateur |
| ENDPOINT_AUDIT | A1 | Test read-only | Consolidateur |
| WRITE_GATED | A4 | Approbation ecrite explicite + dry-run | Humain |
