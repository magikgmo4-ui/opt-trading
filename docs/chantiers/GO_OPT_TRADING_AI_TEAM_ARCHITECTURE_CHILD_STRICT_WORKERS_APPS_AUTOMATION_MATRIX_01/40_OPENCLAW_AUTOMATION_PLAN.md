---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01_AUTOMATION_PLAN
doc_type: automation_plan
repo: opt-trading
project: opt-trading
module: matrix
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01
status: draft_canonical
lifecycle_stage: plan
topic_keys:
  - opt-trading
  - openclaw
  - automation
  - strict_workers
  - tasks
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - scripts/ai/workers/tasks.index.json
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/05_OPERATIONAL_RUNTIME_PLAN.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/04_api_contract_openclaw_gateway.md
---

# 40_OPENCLAW_AUTOMATION_PLAN

## Niveaux d'Automatisation

| Code | Niveau | Description |
| --- | --- | --- |
| MANUAL_ONLY | Manuel uniquement | Aucune automatisation, tout est fait à la main |
| SEMI_AUTOMATED_DRAFT | Semi-automatisé (brouillon) | Worker prépare un draft, humain consolide |
| AUTOMATED_READONLY | Automatisé read-only | Worker lit et rapporte, aucun write |
| AUTOMATED_GATED_WRITE | Automatisé avec garde-fous | Worker écrit via runner verrouillé + validation externe |

## Plan d'Automatisation par Tâche/Job

### 1. READ_INVENTORY

| Propriété | Valeur |
| --- | --- |
| Trigger | Prompts utilisateur ou tâche planifiée |
| Input attendu | Chemins de fichiers, surface cible, filtre |
| Worker IA recommandé | Qwen3.5 Plus, MiniMax M2.5, Kimi K2.5, Big Pickle |
| Appel | OpenClaw runner strict worker (run_task.sh READ_INVENTORY) |
| Sortie attendue | Rapport structuré (ETABLI/HYPOTHESE/TODO/FICHIERS_LUS/RISQUES/VERDICT_DRAFT_ONLY) |
| Stockage attendu | reports/ai/workers/<task_id>.md |
| Validation externe | Revue par modèle fort + tests |
| Action interdite | Write fichier source, modification arborescence |
| Rollback / stop condition | Si fichier sensible détecté (.env, token) → stop immédiat |
| Niveau automatisation | AUTOMATED_READONLY |
| Healthcheck requis | Vérifier que run_task.sh répond, que le rapport est généré |

### 2. PATCH_DRAFT

| Propriété | Valeur |
| --- | --- |
| Trigger | Demande de modification documentée |
| Input attendu | Fichiers sources, objectif du patch, contraintes |
| Worker IA recommandé | GLM-5.1, Kimi K2.6, GLM-5, Qwen3.6 Plus, Big Pickle |
| Appel | OpenClaw runner strict worker (run_task.sh PATCH_DRAFT) |
| Sortie attendue | OBJECTIF_PATCH, FICHIERS_TOUCHES, DIFF_ATTENDU, RISQUES, TESTS_A_EXECUTER, VERDICT_DRAFT_ONLY |
| Stockage attendu | reports/ai/workers/<task_id>.md |
| Validation externe | Modèle fort + tests + git diff réel |
| Action interdite | Application du patch, git add/commit/push |
| Rollback / stop condition | Si patch touche .env ou secret → stop, si diff > 100 lignes → demande approbation |
| Niveau automatisation | SEMI_AUTOMATED_DRAFT |
| Healthcheck requis | Vérifier que le diff proposé est cohérent et ne contient pas de secrets |

### 3. DOC_DRAFT

| Propriété | Valeur |
| --- | --- |
| Trigger | Besoin documentaire (nouveau GO, closeout, décision) |
| Input attendu | Contexte, état initial, changements, validations |
| Worker IA recommandé | Qwen3.5 Plus, Qwen3.6 Plus, MiniMax M2.5, Big Pickle, Nemotron 3 Super Free |
| Appel | OpenClaw runner strict worker (run_task.sh DOC_DRAFT) |
| Sortie attendue | CONTEXTE, ETAT_INITIAL, CHANGEMENTS, VALIDATIONS, LIMITES, POINT_DE_REPRISE, VERDICT_DRAFT_ONLY |
| Stockage attendu | reports/ai/workers/<task_id>.md ou docs/chantiers/** draft |
| Validation externe | Revue externe (modèle fort ou humain) |
| Action interdite | Remplacement de doc canonique, suppression de contenu existant |
| Rollback / stop condition | Si le draft écrase un fichier existant → demande approbation |
| Niveau automatisation | SEMI_AUTOMATED_DRAFT |
| Healthcheck requis | Vérifier que les sections requises sont toutes présentes |

### 4. TESTPLAN

| Propriété | Valeur |
| --- | --- |
| Trigger | Nouveau module, nouvelle fonctionnalité, closeout |
| Input attendu | Code/fonction à tester, contexte, critères |
| Worker IA recommandé | GLM-5.1, Qwen3.6 Plus, Kimi K2.6, GLM-5, MiniMax M2.7 |
| Appel | OpenClaw runner strict worker (run_task.sh TESTPLAN) |
| Sortie attendue | TESTS_UNITAIRES, TESTS_SMOKE, COMMANDES, CRITERES_PASS_FAIL, RISQUES_RESTANTS, VERDICT_DRAFT_ONLY |
| Stockage attendu | reports/ai/workers/<task_id>.md |
| Validation externe | Modèle fort + tests réels (execution) |
| Action interdite | Exécution des tests, modification des scripts de test |
| Rollback / stop condition | Si testplan suggère un test destructif → stop |
| Niveau automatisation | SEMI_AUTOMATED_DRAFT |
| Healthcheck requis | Vérifier que les commandes de test sont syntaxiquement valides |

### 5. CHERRY_PICK_INVENTORY

| Propriété | Valeur |
| --- | --- |
| Trigger | Préparation de merge, closeout de branche |
| Input attendu | Références de commits, branches source et cible |
| Worker IA recommandé | Kimi K2.5, Kimi K2.6, GLM-5.1, Qwen3.6 Plus, Big Pickle |
| Appel | OpenClaw runner strict worker (run_task.sh CHERRY_PICK_INVENTORY) |
| Sortie attendue | COMMITS_CANDIDATS, FICHIERS_TOUCHES, DEPENDANCES, RISQUES_CONFLITS, ORDRE_RECOMMANDE, COMMANDES_NON_EXECUTEES, VERDICT_DRAFT_ONLY |
| Stockage attendu | reports/ai/workers/<task_id>.md |
| Validation externe | Revue externe stricte (modèle fort + humain) |
| Action interdite | Exécution du cherry-pick, git rebase/merge |
| Rollback / stop condition | Si conflit détecté → stop, ne pas proposer de force push |
| Niveau automatisation | SEMI_AUTOMATED_DRAFT |
| Healthcheck requis | Vérifier que les commits existent bien dans le log Git |

### 6. FAST_TRIAGE

| Propriété | Valeur |
| --- | --- |
| Trigger | Lot de fichiers/commits/issues à classifier |
| Input attendu | Liste d'éléments à trier, catégories de classification |
| Worker IA recommandé | Qwen3.5 Plus, MiniMax M2.5, GPT-5 Nano, MiniMax M2.5 Free, DeepSeek V4 Flash Free |
| Appel | OpenClaw runner strict worker (run_task.sh FAST_TRIAGE) |
| Sortie attendue | RESUME, CLASSEMENT, RISQUES, TODO, VERDICT_DRAFT_ONLY |
| Stockage attendu | reports/ai/workers/<task_id>.md |
| Validation externe | Revue par échantillon (modèle fort) |
| Action interdite | Reclassification automatique sans validation, déplacement de fichiers |
| Rollback / stop condition | Si classification incohérente → rejet et nouveau tri |
| Niveau automatisation | AUTOMATED_READONLY |
| Healthcheck requis | Vérifier que le classement est non vide et cohérent |

### 7. ENDPOINT_AUDIT

| Propriété | Valeur |
| --- | --- |
| Trigger | Vérification périodique des modèles disponibles |
| Input attendu | Endpoint URL, registry actuel |
| Worker IA recommandé | Qwen3.5 Plus, MiniMax M2.5, Big Pickle |
| Appel | OpenClaw runner strict worker (run_task.sh ENDPOINT_AUDIT) |
| Sortie attendue | ENDPOINT_CONSULTE, MODELES_TROUVES, COMPARAISON_REGISTRY, AJOUTS, RETRAITS, RECOMMANDATIONS, VERDICT_DRAFT_ONLY |
| Stockage attendu | reports/ai/workers/<task_id>.md |
| Validation externe | Test read-only |
| Action interdite | Mise à jour automatique du registry |
| Rollback / stop condition | Si l'endpoint est inaccessible → log et stop |
| Niveau automatisation | AUTOMATED_READONLY |
| Healthcheck requis | Vérifier que l'endpoint répond |

### 8. WRITE_GATED

| Propriété | Valeur |
| --- | --- |
| Trigger | Approbation humaine explicite après dry-run |
| Input attendu | Dry-run résultat, write plan approuvé |
| Worker IA recommandé | GLM-5.1, Qwen3.6 Plus, Kimi K2.6, Big Pickle |
| Appel | OpenClaw runner strict worker (run_task.sh WRITE_GATED) |
| Sortie attendue | 13_ESTABLISHED, 14_HYPOTHESIS, WRITE_PLAN, WRITE_DIFF_ATTENDU, VALIDATION_EXTERNE, DRY_RUN_RESULT, RISQUES, VERDICT_WRITE_GATED |
| Stockage attendu | docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_*/**, reports/ai/workers/**, scripts/ai/workers/job_packets/** |
| Validation externe | Approbation écrite explicite + dry-run obligatoire |
| Action interdite | Write hors allowlist, dépassement 50 lignes, write sur GO_INDEX/BRANCH_STATE/run_task.sh/_validate_job.py/models.registry.json/tasks.index.json |
| Rollback / stop condition | Dry-run FAIL → stop, write hors périmètre → stop |
| Niveau automatisation | AUTOMATED_GATED_WRITE |
| Healthcheck requis | Vérifier que le write plan est cohérent, que le dry-run est PASS |

### 9. Jobs Pipeline (à produire — workers NIVEAU 0)

| Job | Automatisation proposée | Worker IA | Appel OpenClaw | Dépendances avant activation |
| --- | --- | --- | --- | --- |
| signal_router | AUTOMATED_GATED_WRITE | Kimi K2.5 (contexte long) | Gateway API → builder | market_scanner OK, collector_binance OK |
| proposition_engine | SEMI_AUTOMATED_DRAFT | GLM-5.1 (raisonnement) | Gateway API → builder | decision_engine, opportunity_ranker OK |
| validation_gate | AUTOMATED_GATED_WRITE | GLM-5.1 (raisonnement) + humain | Gateway API + HITL | risk_engine, kil_v1 OK |
| trade_executor | AUTOMATED_GATED_WRITE | Aucun IA (exécution mécanique) | Runner dédié | validation_gate OK, simex_bitget_bridge OK |
| result_tracker | AUTOMATED_READONLY | MiniMax M2.5 (volume) | Gateway API | position_engine, portfolio_engine OK |
| datasheet_writer | SEMI_AUTOMATED_DRAFT | Qwen3.5 Plus (volume) | Gateway API → Airtable/Sheets | result_tracker OK, journal_engine OK |
| learning_feeder | AUTOMATED_GATED_WRITE | Big Pickle (pilote) | Gateway API → memory_bricks | result_tracker OK, memory_bricks OK |
| notification_dispatcher | AUTOMATED_GATED_WRITE | GPT-5 Nano (format court) | Gateway API → Telegram API | Telegram API OK |
| task_tracker | SEMI_AUTOMATED_DRAFT | MiniMax M2.7 (patch simple) | Gateway API → ClickUp API | ClickUp OK |

## Interdits Permanents (Tous Niveaux)

- Aucune automatisation trade réel (toute exécution réelle nécessite validation humaine explicite)
- Aucun write sur GO_INDEX.md, BRANCH_STATE.md, REPRISE.md, ACTIVE_STREAMS.md
- Aucun write sur les fichiers registry (models.registry.json, tasks.index.json)
- Aucun write sur les runners (run_task.sh, _validate_job.py)
- Aucun write hors allowlist définie dans tasks.index.json
- Aucun commit/push/rebase/merge automatisé
- Aucune modification des fichiers .env, tokens, clés, credentials
