---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01_JOB_PACKETS_SPEC
doc_type: job_spec
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
status: draft_canonical
lifecycle_stage: spec
topic_keys:
  - opt-trading
  - strict_workers
  - job_packets
  - tasks
  - automation
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - scripts/ai/workers/tasks.index.json
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
---

# 20_JOB_PACKETS_SPEC

## Job Packet : READ_INVENTORY

| Propriété | Valeur |
| --- | --- |
| task_id | READ_INVENTORY |
| autonomie max | A1 |
| inputs autorisés | Chemins de fichiers (glob pattern), surface cible, filtre optionnel |
| denied_inputs | .env, **/.env, **/*secret*, **/*token*, **/*credential*, **/id_rsa, **/id_ed25519, **/*.pem, **/*.key |
| denied_commands | git add, git commit, git push, git rebase, git merge, rm -rf, chmod -R, chown -R |
| output path | reports/ai/workers/<job_id>.md |
| required_sections | 13_ESTABLISHED, 14_HYPOTHESIS, 15_REMAINING_GAP, 16_TODO, FICHIERS_LUS, RISQUES, VERDICT_DRAFT_ONLY |
| preferred_workers | qwen3.5-plus, minimax-m2.5, kimi-k2.5, big-pickle, gpt-5-nano, minimax-m2.5-free, nemotron-3-super-free, deepseek-v4-flash-free, ring-2.6-1t-free, trinity-large-preview-free |
| validation externe | Revue par modèle fort + tests |
| verdict attendu | VERDICT_DRAFT_ONLY avec sections remplies |
| stop conditions | Fichier sensible détecté → stop immédiat. Output vide → rejet. |

## Job Packet : PATCH_DRAFT

| Propriété | Valeur |
| --- | --- |
| task_id | PATCH_DRAFT |
| autonomie max | A2 |
| inputs autorisés | Fichiers sources, objectif du patch, contraintes |
| denied_inputs | .env, **/.env, **/*secret*, **/*token*, **/*credential*, **/id_rsa, **/id_ed25519, **/*.pem, **/*.key |
| denied_commands | git add, git commit, git push, git rebase, git merge, rm -rf, chmod -R, chown -R |
| output path | reports/ai/workers/<job_id>.md |
| required_sections | OBJECTIF_PATCH, FICHIERS_TOUCHES, DIFF_ATTENDU, RISQUES, TESTS_A_EXECUTER, VERDICT_DRAFT_ONLY |
| preferred_workers | glm-5.1, kimi-k2.6, glm-5, qwen3.6-plus, minimax-m2.7, big-pickle |
| validation externe | Modèle fort + tests + git diff réel |
| verdict attendu | VERDICT_DRAFT_ONLY avec diff théorique complet, fichiers touchés listés |
| stop conditions | Patch touche .env ou secret → stop. Diff > 100 lignes → demande approbation. Commandes git write détectées → stop. |

## Job Packet : DOC_DRAFT

| Propriété | Valeur |
| --- | --- |
| task_id | DOC_DRAFT |
| autonomie max | A2 |
| inputs autorisés | Contexte, état initial, changements, validations |
| denied_inputs | .env, **/.env, **/*secret*, **/*token*, **/*credential*, **/id_rsa, **/id_ed25519, **/*.pem, **/*.key |
| denied_commands | git add, git commit, git push, git rebase, git merge, rm -rf, chmod -R, chown -R |
| output path | reports/ai/workers/<job_id>.md (ou draft dans docs/chantiers/** si validé) |
| required_sections | CONTEXTE, ETAT_INITIAL, CHANGEMENTS, VALIDATIONS, LIMITES, POINT_DE_REPRISE, VERDICT_DRAFT_ONLY |
| preferred_workers | qwen3.5-plus, qwen3.6-plus, minimax-m2.5, big-pickle, nemotron-3-super-free |
| validation externe | Revue externe (modèle fort ou humain) |
| verdict attendu | VERDICT_DRAFT_ONLY avec document draft complet |
| stop conditions | Draft écrase un fichier canonique existant → demande approbation. Contient des secrets → stop. |

## Job Packet : TESTPLAN

| Propriété | Valeur |
| --- | --- |
| task_id | TESTPLAN |
| autonomie max | A2 |
| inputs autorisés | Code/fonction à tester, contexte, critères de test |
| denied_inputs | .env, **/.env, **/*secret*, **/*token*, **/*credential*, **/id_rsa, **/id_ed25519, **/*.pem, **/*.key |
| denied_commands | git add, git commit, git push, git rebase, git merge, rm -rf, chmod -R, chown -R, exécution des tests |
| output path | reports/ai/workers/<job_id>.md |
| required_sections | TESTS_UNITAIRES, TESTS_SMOKE, COMMANDES, CRITERES_PASS_FAIL, RISQUES_RESTANTS, VERDICT_DRAFT_ONLY |
| preferred_workers | glm-5.1, qwen3.6-plus, kimi-k2.6, glm-5, minimax-m2.7 |
| validation externe | Modèle fort + tests réels (execution séparée) |
| verdict attendu | VERDICT_DRAFT_ONLY avec plan de test complet et commandes vérifiées |
| stop conditions | Testplan suggère un test destructif → stop. Commandes non valides syntaxiquement → stop. |

## Job Packet : CHERRY_PICK_INVENTORY

| Propriété | Valeur |
| --- | --- |
| task_id | CHERRY_PICK_INVENTORY |
| autonomie max | A2 |
| inputs autorisés | Références de commits, branches source et cible |
| denied_inputs | .env, **/.env, **/*secret*, **/*token*, **/*credential*, **/id_rsa, **/id_ed25519, **/*.pem, **/*.key |
| denied_commands | git add, git commit, git push, git rebase, git merge, cherry-pick, rm -rf, chmod -R, chown -R |
| output path | reports/ai/workers/<job_id>.md |
| required_sections | COMMITS_CANDIDATS, FICHIERS_TOUCHES, DEPENDANCES, RISQUES_CONFLITS, ORDRE_RECOMMANDE, COMMANDES_NON_EXECUTEES, VERDICT_DRAFT_ONLY |
| preferred_workers | kimi-k2.5, kimi-k2.6, glm-5.1, qwen3.6-plus, big-pickle |
| validation externe | Revue externe stricte (modèle fort + humain) |
| verdict attendu | VERDICT_DRAFT_ONLY avec inventaire complet des commits, dépendances et risques |
| stop conditions | Conflit détecté → stop. Force push proposé → stop. Commits inexistants → stop. |

## Job Packet : FAST_TRIAGE

| Propriété | Valeur |
| --- | --- |
| task_id | FAST_TRIAGE |
| autonomie max | A1 |
| inputs autorisés | Liste d'éléments à trier, catégories de classification |
| denied_inputs | .env, **/.env, **/*secret*, **/*token*, **/*credential*, **/id_rsa, **/id_ed25519, **/*.pem, **/*.key |
| denied_commands | git add, git commit, git push, git rebase, git merge, rm -rf, chmod -R, chown -R |
| output path | reports/ai/workers/<job_id>.md |
| required_sections | RESUME, CLASSEMENT, RISQUES, TODO, VERDICT_DRAFT_ONLY |
| preferred_workers | qwen3.5-plus, minimax-m2.5, gpt-5-nano, minimax-m2.5-free, deepseek-v4-flash-free, ring-2.6-1t-free |
| validation externe | Revue par échantillon (modèle fort) |
| verdict attendu | VERDICT_DRAFT_ONLY avec classement complet et résumé |
| stop conditions | Classification incohérente → rejet. TODO vide → demande clarification. |

## Job Packet : ENDPOINT_AUDIT

| Propriété | Valeur |
| --- | --- |
| task_id | ENDPOINT_AUDIT |
| autonomie max | A1 |
| inputs autorisés | Endpoint URL, registry actuel (models.registry.json) |
| denied_inputs | .env, **/.env, **/*secret*, **/*token*, **/*credential*, **/id_rsa, **/id_ed25519, **/*.pem, **/*.key |
| denied_commands | git add, git commit, git push, git rebase, git merge, rm -rf, chmod -R, chown -R |
| output path | reports/ai/workers/<job_id>.md |
| required_sections | ENDPOINT_CONSULTE, MODELES_TROUVES, COMPARAISON_REGISTRY, AJOUTS, RETRAITS, RECOMMANDATIONS, VERDICT_DRAFT_ONLY |
| preferred_workers | qwen3.5-plus, minimax-m2.5, big-pickle |
| validation externe | Test read-only |
| verdict attendu | VERDICT_DRAFT_ONLY avec comparaison endpoint vs registry |
| stop conditions | Endpoint inaccessible → log et stop. Pas de mise à jour automatique du registry. |

## Job Packet : WRITE_GATED

| Propriété | Valeur |
| --- | --- |
| task_id | WRITE_GATED |
| autonomie max | A4 |
| inputs autorisés | Dry-run résultat approuvé, write plan, allowlist cibles |
| denied_inputs | .env, **/.env, **/*secret*, **/*token*, **/*credential*, **/id_rsa, **/id_ed25519, **/*.pem, **/*.key |
| denied_commands | git add, git commit, git push, git rebase, git merge, rm -rf, chmod -R, chown -R |
| output path | docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_*/**, reports/ai/workers/**, scripts/ai/workers/job_packets/** |
| write_allowlist | docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_**/*.md, docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_**/BRANCH_STATE.md, reports/ai/workers/*.md, scripts/ai/workers/job_packets/*.json |
| required_sections | 13_ESTABLISHED, 14_HYPOTHESIS, WRITE_PLAN, WRITE_DIFF_ATTENDU, VALIDATION_EXTERNE, DRY_RUN_RESULT, RISQUES, VERDICT_WRITE_GATED |
| preferred_workers | glm-5.1, qwen3.6-plus, kimi-k2.6, big-pickle |
| validation externe | Approbation écrite explicite + dry-run obligatoire |
| verdict attendu | VERDICT_WRITE_GATED avec dry-run PASS, write plan approuvé |
| stop conditions | Dry-run FAIL → stop. Write hors allowlist → stop. > 50 lignes → stop. Cible interdite (GO_INDEX, BRANCH_STATE, run_task.sh, _validate_job.py, models.registry.json, tasks.index.json) → stop. |
