---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01_EXECUTION_SEQUENCE
doc_type: execution_plan
repo: opt-trading
project: opt-trading
module: matrix
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01
status: draft_canonical
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - execution
  - sequence
  - next_go
  - phases
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/BRANCH_STATE.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 50_EXECUTION_SEQUENCE_AND_NEXT_GO

## Phase 1 — Inventaire Readonly

**Objectif** : Lire toutes les sources de vérité dans l'ordre prescrit, s'imprégner de l'état canonique courant.

| Action | Source | Verdict attendu |
| --- | --- | --- |
| Lire MATRICE_DOC_OPS_MASTER_MATRIX_01 | docs/governance/ | Compréhension de la hiérarchie canonique |
| Lire AI Team Architecture cadrage | docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md | État du parent AI Team |
| Lire AI Team initial project doc | docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/01_initial_project_doc.md | Plan initial figé |
| Lire AI Team decisions | docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/03_decisions.md | Décisions validées |
| Lire Strict Workers initial | docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/00_INITIAL_PROJECT_DOC.md | Doctrine strict workers |
| Lire autonomie étroite | docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md | Définition et modes |
| Lire MODELS_MATRIX_01 | docs/agents/strict_workers/MODELS_MATRIX_01.md | Matrice modèles initiale |
| Lire models.registry.json | scripts/ai/workers/models.registry.json | Registry vérifié |
| Lire tasks.index.json | scripts/ai/workers/tasks.index.json | Index tâches |
| Lire Apps validated plan | docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/00_INITIAL_PROJECT_DOC.md | Plan apps validé |
| Lire Tracking apps core | docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/10_TRACKING_APPS_CORE_TABLE.md | Suivi apps |
| Lire Full repo surfaces inventory | docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/02_FULL_REPO_SURFACES_INVENTORY.md | Inventaire surfaces |
| Lire Operational runtime plan | docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/05_OPERATIONAL_RUNTIME_PLAN.md | Plan runtime |
| Lire Botpress cadrage | docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/00_cadrage_parent.md | Cadrage Botpress |
| Lire API contract | docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/04_api_contract_openclaw_gateway.md | Contrat API |
| Lire Machine work split | docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md | Routage machine |
| Lire BRANCH_STATE | docs/index/BRANCH_STATE.md | État branches |

**Durée estimée** : 1 session
**Verdict** : PASS si toutes les sources sont lues et comprises

## Phase 2 — Matrice Apps + Workers

**Objectif** : Produire les fichiers matriciels reliant apps, workers, rôles et maintenance.

| Action | Livrable | Dépendances |
| --- | --- | --- |
| Créer 10_ROLES_JOBS_TASKS_INVENTORY.md | Inventaire rôles/métiers/jobs/tasks | Phase 1 complète |
| Créer 20_AI_CANDIDATES_MATRIX.md | Matrice modèles IA | models.registry.json, MODELS_MATRIX_01 |
| Créer 30_APPS_RETAINED_AND_MAINTENANCE_MATRIX.md | Matrice apps retenues | Apps validated plan, tracking core table |

**Durée estimée** : 1 session
**Verdict** : PASS si les 3 matrices sont complètes et cohérentes entre elles

## Phase 3 — Job Packets Strict Workers

**Objectif** : Préparer les descriptions détaillées des jobs strict workers par tâche autorisée.

| Action | Livrable | Dépendances |
| --- | --- | --- |
| Documenter les 8 tâches indexées (READ_INVENTORY → WRITE_GATED) | Sections dans 10_ROLES_JOBS_TASKS_INVENTORY.md | tasks.index.json |
| Croiser avec les 9 workers pipeline (signal_router → task_tracker) | Table de correspondance | Phase 2 |

**Durée estimée** : 1 session
**Verdict** : PASS si chaque tâche a un niveau d'autonomie, validation et worker recommandé

## Phase 4 — OpenClaw Semi-Automation Dry-Run

**Objectif** : Produire le plan d'automatisation OpenClaw pour chaque tâche retenue.

| Action | Livrable | Dépendances |
| --- | --- | --- |
| Créer 40_OPENCLAW_AUTOMATION_PLAN.md | Plan d'automatisation complet | Phases 2-3 |
| Définir trigger, input, worker, appel, sortie, stockage, validation, interdits, rollback, niveau, healthcheck | Par tâche | API contract OpenClaw Gateway |

**Durée estimée** : 1 session
**Verdict** : PASS si chaque tâche a son plan d'automatisation complet

## Phase 5 — App Sync Limitée

**Objectif** : Croiser avec l'état réel des apps validées sans écriture directe.

| Action | Cible | Dépendances |
| --- | --- | --- |
| Vérifier cohérence ClickUp / GO_INDEX | ClickUp (lecture) | Phase 2 |
| Vérifier cohérence Repo KG / cartographie | Repo KG (lecture) | Phase 2 |
| Vérifier cohérence Airtable / plan data | Airtable (lecture) | Phase 2 |
| Vérifier cohérence Botpress / API contract | Botpress (lecture) | Phase 2 |

**Durée estimée** : 1 session
**Verdict** : PASS si cohérence vérifiée sans écriture

## Phase 6 — Closeout

**Objectif** : Finaliser le GO enfant matrice et produire le verdict.

| Action | Livrable | Dépendances |
| --- | --- | --- |
| Exécuter git status --short --branch --untracked-files=all | Validation | Toutes les phases |
| Exécuter git diff --check | Validation | Toutes les phases |
| Vérifier fichiers créés uniquement dans le dossier dédié | Validation | Toutes les phases |
| Vérifier JSON sources parseables | Validation | Toutes les phases |
| Produire le verdict final | Résumé | Validations PASS |

**Durée estimée** : 30 min
**Verdict** : PASS_DOC_ONLY_MATRIX_CREATED ou BLOCKED_WITH_REASON

## NEXT_GO Recommandés

### Priorité Haute

| GO | Raison | Dépendances |
| --- | --- | --- |
| `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01` | Passer à l'execution ClickUp après plan validé | Ce GO matrice + APPS_PARENT_VALIDATED_PLAN |
| `GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01` | Étendre le pool de workers stricts avec les modèles VERIFIED | Ce GO matrice + strict workers parent |
| `GO_OPENCLAW_OPT_TRADING_CHILD_OPERATOR_BRIDGE_IMPL_V1_01` | Implémenter le premier worker pipeline (signal_router) | Ce GO matrice + full repo surfaces inventory |

### Priorité Moyenne

| GO | Raison | Dépendances |
| --- | --- | --- |
| `GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01` | Ajouter une vue produit/usage au-dessus du Repo KG bundle | Ce GO matrice + Repo KG |
| `GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01` | Matérialiser le bridge Airtable | Ce GO matrice + Airtable parent |
| `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` | Connecter Telegram réel | Ce GO matrice + Botpress parent |

### Priorité Basse (Info/À Différer)

| GO | Raison |
| --- | --- |
| `GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01` | Verrouillage runtime et E2E — après stabilisation des workers |
| `GO_OPT_TRADING_ORCHESTRATOR_CHILD_PROPOSITION_ENGINE_V1_01` | Proposition engine — après validation des moteurs existants |
| `GO_OPT_TRADING_STRICT_WORKERS_CHILD_AIRTABLE_INTEGRATION_01` | Intégration Airtable worker — après bridge Airtable |
| `GO_OPT_TRADING_STRICT_WORKERS_CHILD_CLICKUP_TASK_TRACKER_01` | Worker ClickUp — après execution ClickUp initiale |

## Interdits d'Exécution

- Ne pas ouvrir automatiquement les NEXT_GO — ce sont des recommandations
- Ne pas exécuter de write réel sur les apps (ClickUp, Airtable, Botpress)
- Ne pas lancer d'automatisation trade réelle
- Ne pas modifier les index globaux (GO_INDEX.md, ACTIVE_STREAMS.md, BRANCH_STATE.md, REPRISE.md)
- Ne pas créer de workers pipeline opérationnels — ils sont tous NIVEAU 0
