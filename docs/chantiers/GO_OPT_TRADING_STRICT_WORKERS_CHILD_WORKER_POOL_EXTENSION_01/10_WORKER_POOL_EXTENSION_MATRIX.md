---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01_WORKER_POOL_MATRIX
doc_type: model_matrix
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01
status: draft_canonical
lifecycle_stage: matrix
topic_keys:
  - opt-trading
  - strict_workers
  - worker_pool
  - verified_models
  - autonomy
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/tasks.index.json
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
---

# 10_WORKER_POOL_EXTENSION_MATRIX

## Source

`models.registry.json` (validé 2026-05-14) — seuls les modèles VERIFIED / VERIFIED_FREE sont listés ici.
Les modèles ABSENT_CURRENT_ENDPOINT, RETIRED_CURRENT_ENDPOINT, OBSOLETE_REPLACED sont exclus (classés A0).

## Modèles VERIFIED (10)

| worker_id | config_id | Autonomie max | Rôles autorisés | Tâches autorisées | Interdits | Validation requise | Usage recommandé | Limites |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| glm-5.1 | opencode/glm-5.1 | A2 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, REVIEW_DRAFT | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | READ_INVENTORY (non listé), FAST_TRIAGE, WRITE_GATED, .env, tokens, git write | Modèle fort + tests | Raisonnement / patch draft / revue forte intermédiaire | Pas de volume lecture, pas de tri rapide |
| glm-5 | opencode/glm-5 | A2 | PATCH_DRAFT, DOC_DRAFT, TESTPLAN | PATCH_DRAFT, DOC_DRAFT, TESTPLAN | READ_INVENTORY (non listé), CHERRY_PICK_INVENTORY, FAST_TRIAGE, WRITE_GATED, .env, tokens, git write | Modèle fort + tests | Worker raisonnement général / patch draft | Pas de cherry-pick, pas de fast triage |
| kimi-k2.5 | opencode/kimi-k2.5 | A2 | READ_INVENTORY, PATCH_DRAFT, CHERRY_PICK_INVENTORY | READ_INVENTORY, PATCH_DRAFT, CHERRY_PICK_INVENTORY | FAST_TRIAGE, WRITE_GATED, DOC_DRAFT, .env, tokens, git write | Revue externe | Long contexte / code reading / inventaire commits | Pas de tri rapide, pas de doc draft volume |
| kimi-k2.6 | opencode/kimi-k2.6 | A2 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | READ_INVENTORY (non listé), FAST_TRIAGE, WRITE_GATED, .env, tokens, git write | Revue externe stricte | Patch complexe / cherry-pick inventory | Pas de volume lecture, pas de tri rapide |
| minimax-m2.7 | opencode/minimax-m2.7 | A2 | READ_INVENTORY, DOC_DRAFT, PATCH_DRAFT, TESTPLAN | READ_INVENTORY, DOC_DRAFT, PATCH_DRAFT (léger), TESTPLAN | FAST_TRIAGE, CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Revue externe | Patch simple / docs / testplan | Pas de cherry-pick complexe, pas de fast triage |
| minimax-m2.5 | opencode/minimax-m2.5 | A2 | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | PATCH_DRAFT (non listé), CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Revue échantillonnée + diff | Volume / inventaire / docs | Pas de patch complexe, pas de cherry-pick |
| qwen3.6-plus | opencode/qwen3.6-plus | A2 | DOC_DRAFT, TESTPLAN, PATCH_DRAFT, REVIEW_DRAFT | DOC_DRAFT, TESTPLAN, PATCH_DRAFT (léger), REVIEW_DRAFT | READ_INVENTORY (non listé), FAST_TRIAGE, CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Modèle fort + tests | Testplan / doc structurée / patch léger | Pas de volume lecture masse, pas de tri rapide |
| qwen3.5-plus | opencode/qwen3.5-plus | A2 | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | PATCH_DRAFT (non listé), CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Revue par échantillon | Haut volume / extraction / docs | Pas de patch complexe, pas de cherry-pick |
| big-pickle | opencode/big-pickle | A2 | READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN | READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN | FAST_TRIAGE, CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Modèle fort + tests | Stealth worker pilote / extraction / brouillon | Pas de tri rapide, pas de cherry-pick |
| gpt-5-nano | opencode/gpt-5-nano | A1 | FAST_TRIAGE, READ_INVENTORY | FAST_TRIAGE, READ_INVENTORY | PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Revue externe | Classification / tri très court / formats courts | Tout ce qui dépasse le tri court |

## Modèles VERIFIED_FREE (5)

| worker_id | config_id | Autonomie max | Rôles autorisés | Tâches autorisées | Interdits | Validation requise | Usage recommandé | Limites |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| minimax-m2.5-free | opencode/minimax-m2.5-free | A1 | READ_INVENTORY, FAST_TRIAGE | READ_INVENTORY, FAST_TRIAGE | PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Revue externe | Volume gratuit / tri non sensible | Pas de draft, pas de write |
| nemotron-3-super-free | opencode/nemotron-3-super-free | A1 | READ_INVENTORY, DOC_DRAFT | READ_INVENTORY, DOC_DRAFT | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, FAST_TRIAGE, WRITE_GATED, .env, tokens, git write | Revue externe | Brouillon général non sensible | Pas de patch, testplan, cherry-pick |
| deepseek-v4-flash-free | opencode/deepseek-v4-flash-free | A1 | READ_INVENTORY, FAST_TRIAGE | READ_INVENTORY, FAST_TRIAGE | PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Revue externe | Tri rapide non sensible / lecture | Pas de draft, pas de write |
| ring-2.6-1t-free | opencode/ring-2.6-1t-free | A1 | READ_INVENTORY, FAST_TRIAGE | READ_INVENTORY, FAST_TRIAGE | PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Revue externe | Tri rapide / lecture (successeur ling-2.6) | Pas de write, pas de draft |
| trinity-large-preview-free | opencode/trinity-large-preview-free | A1 | READ_INVENTORY | READ_INVENTORY | FAST_TRIAGE, PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED, .env, tokens, git write | Revue externe | Lecture conservative uniquement | Tout sauf lecture |

## Modèles Exclus (A0)

| model_id | Raison |
| --- | --- |
| mimo-v2-pro | ABSENT_CURRENT_ENDPOINT |
| mimo-v2-omni | ABSENT_CURRENT_ENDPOINT |
| mimo-v2.5-pro | ABSENT_CURRENT_ENDPOINT |
| mimo-v2.5 | ABSENT_CURRENT_ENDPOINT |
| deepseek-v4-pro | ABSENT_CURRENT_ENDPOINT |
| hy3-preview-free | RETIRED_CURRENT_ENDPOINT |
| ling-2.6-flash-free | RETIRED_CURRENT_ENDPOINT |
| deepseek-v4-flash | OBSOLETE_REPLACED |

## Mapping Tâche → Workers préférés

| Tâche | Workers VERIFIED | Workers VERIFIED_FREE |
| --- | --- | --- |
| READ_INVENTORY | qwen3.5-plus, minimax-m2.5, kimi-k2.5, big-pickle, gpt-5-nano | minimax-m2.5-free, nemotron-3-super-free, deepseek-v4-flash-free, ring-2.6-1t-free, trinity-large-preview-free |
| PATCH_DRAFT | glm-5.1, kimi-k2.6, glm-5, qwen3.6-plus, minimax-m2.7, big-pickle | — (aucun VERIFIED_FREE autorisé) |
| DOC_DRAFT | qwen3.5-plus, qwen3.6-plus, minimax-m2.5, big-pickle | nemotron-3-super-free |
| TESTPLAN | glm-5.1, qwen3.6-plus, kimi-k2.6, glm-5, minimax-m2.7 | — (aucun VERIFIED_FREE autorisé) |
| CHERRY_PICK_INVENTORY | kimi-k2.5, kimi-k2.6, glm-5.1, qwen3.6-plus, big-pickle | — (aucun VERIFIED_FREE autorisé) |
| FAST_TRIAGE | qwen3.5-plus, minimax-m2.5, gpt-5-nano | minimax-m2.5-free, deepseek-v4-flash-free, ring-2.6-1t-free |
| ENDPOINT_AUDIT | qwen3.5-plus, minimax-m2.5, big-pickle | — (aucun VERIFIED_FREE autorisé) |
| WRITE_GATED | glm-5.1, qwen3.6-plus, kimi-k2.6, big-pickle | — (aucun VERIFIED_FREE autorisé) |

## Règle de Promotion

Aucun modèle promu décideur final. Promotion A2→A3→A4 nécessite :
1. Test READ_ONLY PASS (3-5 fichiers non sensibles)
2. Test PATCH_DRAFT PASS (patch minimal théorique)
3. Consolidation : revue modèle fort/humain + git diff + tests réels
