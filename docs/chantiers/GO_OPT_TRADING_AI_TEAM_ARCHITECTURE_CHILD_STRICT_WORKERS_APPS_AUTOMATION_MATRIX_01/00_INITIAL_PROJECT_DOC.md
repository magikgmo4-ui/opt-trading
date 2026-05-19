---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: matrix
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01
status: draft_canonical
lifecycle_stage: opening
topic_keys:
  - opt-trading
  - ai_team
  - strict_workers
  - apps
  - automation
  - matrix
  - openclaw
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-05-19
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/03_decisions.md
  - docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/tasks.index.json
  - docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/10_TRACKING_APPS_CORE_TABLE.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/02_FULL_REPO_SURFACES_INVENTORY.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/05_OPERATIONAL_RUNTIME_PLAN.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/00_cadrage_parent.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/04_api_contract_openclaw_gateway.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/BRANCH_STATE.md
---

# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Produire une matrice documentaire complète reliant AI Team Architecture, Strict Workers / Auto Workers, rôles/métiers/jobs/tasks, IA candidates retenues, apps retenues et surfaces externes, maintenance par app, et automatisation/semi-automatisation OpenClaw par tâche retenue — le tout dans un dossier chantier enfant du parent AI Team Architecture.

## 2_INITIAL_PROJECT_DOC

Le présent fichier est le document transporteur initial du GO enfant matrice. Il fige le plan complet, l'état canonique des sources, les décisions, invariants, gaps et point de reprise. Il sert de fiche de référence obligatoire pour tout travail dans ce dossier.

## 3_INITIAL_NEED

Besoin : préparer une matrice exhaustive qui recroise :
1. Les rôles de l'AI Team Architecture (manager, spécialistes, memory, outils, validation)
2. Les strict workers définis dans la doctrine (READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, FAST_TRIAGE, ENDPOINT_AUDIT, WRITE_GATED)
3. Les 14+ modèles IA candidats recensés dans MODELS_MATRIX_01.md et models.registry.json
4. Les 9 apps/surfaces retenues (ClickUp, Repo KG, Airtable, Botpress, TradingView, Telegram, Google Sheets, Figma, LocalCMS consumer)
5. Les workers pipeline à produire (signal_router, proposition_engine, validation_gate, trade_executor, result_tracker, datasheet_writer, learning_feeder, notification_dispatcher, task_tracker)
6. Ce qui doit être automatisé ou semi-automatisé via OpenClaw Gateway

## 4_MASTER_PROJECT_PLAN

Direction validée :
1. Lire l'intégralité des sources de vérité dans l'ordre prescrit
2. Créer le dossier chantier enfant dédié
3. Produire 6 fichiers matriciels :
   - `00_INITIAL_PROJECT_DOC.md` — cadrage et transport
   - `10_ROLES_JOBS_TASKS_INVENTORY.md` — inventaire rôles/métiers/jobs/tasks
   - `20_AI_CANDIDATES_MATRIX.md` — matrice modèles IA
   - `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` — matrice apps retenues
   - `40_OPENCLAW_AUTOMATION_PLAN.md` — plan d'automatisation OpenClaw
   - `50_EXECUTION_SEQUENCE_AND_NEXT_GO.md` — séquence d'exécution et next GO
4. Valider : git status, git diff, fichiers uniquement dans le dossier dédié

## 5_GO_PLAN

Workstreams :
- Phase 1 : inventaire readonly des sources
- Phase 2 : matrice apps + workers
- Phase 3 : job packets strict workers
- Phase 4 : OpenClaw semi-automation dry-run
- Phase 5 : app sync limitée ClickUp / Repo KG / Airtable / Botpress
- Phase 6 : closeout

## 6_FINAL_TARGET

Livrable final : une matrice documentaire complète, 100% doc-only, 100% sourcée sur les documents canoniques listés, sans runtime, sans implémentation, sans modification des index globaux, prête à servir de fondation pour les GO enfants d'implémentation.

## 7_CANONICAL_STATE

État initial retenu :
- AI Team Architecture reste parent doc-only, aucun GO enfant d'implémentation validé
- Strict Workers = doctrine DRAFT_ONLY, smoke READ_INVENTORY PASS, non mergé dans sot/mainline
- Apps validées : ClickUp (USABLE_LIMITED), Repo KG (USABLE_NOW), Airtable (DOC_ONLY_READY/GO_LIMITED), Botpress (SIMULATED_PASS)
- OpenClaw Gateway existe côté db-layer (NIVEAU 3 — opérationnel prouvé)
- Workers pipeline (signal_router → learning_feeder) sont NIVEAU 0 — à produire
- 14 modèles IA recensés dans le registry : 9 VERIFIED, 3 VERIFIED_FREE, 2 RETIRED, 5 ABSENT, 1 OBSOLETE
- Aucun modèle n'est A4 (WRITE_GATED) sans preuve explicite
- Le repo, les commits, PR, docs et état Git réel restent la preuve canonique

## 8_VALIDATED_PLAN

Étapes validées :
1. Sources lues et vérifiées dans l'ordre
2. Dossier créé (uniquement docs/chantiers/<GO_ID>/)
3. 6 fichiers matriciels créés avec frontmatter conforme
4. Git status et diff vérifiés (aucune modification hors dossier)
5. JSON sources vérifiés parseables
6. Verdict final produit

## 9_SELECTED_SOLUTION

Solution documentaire retenue :
- GO enfant du parent GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
- 6 fichiers matriciels indépendants, lisibles séparément
- Chaque fichier suit les conventions de frontmatter et de nommage canonique
- Aucune modification des index globaux (GO_INDEX.md, ACTIVE_STREAMS.md, REPRISE.md, BRANCH_STATE.md)
- Aucune écriture runtime, aucun secret, aucune automatisation trade réelle

## 10_SELECTED_SETUP

Setup documentaire retenu :
- Dossier : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/`
- Fichiers : `00_INITIAL_PROJECT_DOC.md`, `10_ROLES_JOBS_TASKS_INVENTORY.md`, `20_AI_CANDIDATES_MATRIX.md`, `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md`, `40_OPENCLAW_AUTOMATION_PLAN.md`, `50_EXECUTION_SEQUENCE_AND_NEXT_GO.md`
- Support Git : sot/mainline (doc-only, aucun besoin d'isolement fort)
- Aucun runtime, aucun secret, aucune modification hors dossier

## 11_KEY_DECISIONS

- Ce GO est un CHILD du parent AI Team Architecture
- La matrice ne modifie aucun index global
- Les modèles VERIFIED_FREE sont limités à A1 maximum
- Les modèles ABSENT_CURRENT_ENDPOINT / RETIRED_CURRENT_ENDPOINT / OBSOLETE_REPLACED sont exclus ou A0
- Aucune promotion A4 sans preuve explicite documentée
- Les apps ne sont pas des sources canoniques (le repo reste la source de vérité)
- ClickUp est utilisable avec limites Free
- Botpress reste contrôlé par safety gate, dry-run, zéro trade réel automatique V1
- Les workers pipeline sont à produire, pas encore opérationnels

## 12_INVARIANTS

- Ne pas modifier GO_INDEX.md, ACTIVE_STREAMS.md, REPRISE.md ou BRANCH_STATE.md sauf preuve explicite
- Ne pas écrire dans runtime
- Ne pas toucher aux secrets, .env, tokens, clés, credentials
- Ne pas créer d'automatisation trade réelle
- Ne pas traiter ClickUp/Airtable/Botpress/Repo KG comme source canonique
- Ne pas promouvoir un worker en décideur final
- Ne pas inventer de modèle IA absent des sources
- Ne pas mélanger implémentation réelle et plan documentaire
- Ne pas ouvrir de GO enfant d'implémentation dans ce lot

## 13_ESTABLISHED

- AI Team Architecture = parent doc-only, setup documentaire complet (00_cadrage, 01_initial_project_doc, 02_journal, 03_decisions)
- Strict Workers = doctrine définie, 8 tâches autorisées, registry 14+ modèles, tasks.index.json, runner
- Apps = 4 validées (ClickUp → Repo KG → Airtable → Botpress), 5 surfaces connexes (TradingView, Telegram, Google Sheets, Figma, LocalCMS consumer)
- OpenClaw Gateway = opérationnel sur db-layer (ws://127.0.0.1:18789)
- Workers pipeline = 9 workers à produire (NIVEAU 0)
- Niveaux d'autonomie : A0 DISABLED, A1 READ_ONLY, A2 DRAFT_ONLY, A3 SANDBOX_TEST, A4 WRITE_GATED
- Aucun modèle A4 sans preuve

## 14_HYPOTHESIS

- La matrice produite servira de fondation pour ouvrir des GO enfants d'implémentation
- Les modèles VERIFIED pourront monter en autonomie après tests read-only et patch-draft
- Les 9 workers pipeline pourront être implémentés comme strict workers wrappant les moteurs existants
- L'automatisation OpenClaw pourra être déployée en semi-automation avant full automation
- ClickUp restera utilisable en plan Free avec les limitations documentées

## 15_REMAINING_GAP

- Aucun GO enfant d'implémentation n'est encore ouvert
- Les workers pipeline sont tous NIVEAU 0
- Airtable bridge n'est pas encore matérialisé
- Botpress E2E Telegram réel n'est pas connecté
- Google Sheets et Figma sont NIVEAU 0
- Les tests read-only et patch-draft par modèle ne sont pas encore exécutés
- La consolidation des sorties workers n'a pas encore été testée bout-en-bout

## 16_TODO

1. Créer le dossier chantier
2. Écrire 00_INITIAL_PROJECT_DOC.md (présent fichier)
3. Écrire 10_ROLES_JOBS_TASKS_INVENTORY.md
4. Écrire 20_AI_CANDIDATES_MATRIX.md
5. Écrire 30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md
6. Écrire 40_OPENCLAW_AUTOMATION_PLAN.md
7. Écrire 50_EXECUTION_SEQUENCE_AND_NEXT_GO.md
8. Valider : git status, git diff, parse JSON sources
9. Produire le verdict final

## 17_RESUME_POINT

Reprendre depuis `7_CANONICAL_STATE` de ce fichier. Consulter `10_ROLES_JOBS_TASKS_INVENTORY.md` pour l'inventaire des rôles, `20_AI_CANDIDATES_MATRIX.md` pour les modèles, `30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md` pour les apps, `40_OPENCLAW_AUTOMATION_PLAN.md` pour l'automatisation, `50_EXECUTION_SEQUENCE_AND_NEXT_GO.md` pour la séquence suivante. Le parent reste GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01.
