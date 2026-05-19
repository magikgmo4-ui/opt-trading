---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01_AI_CANDIDATES
doc_type: model_matrix
repo: opt-trading
project: opt-trading
module: matrix
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01
status: draft_canonical
lifecycle_stage: matrix
topic_keys:
  - opt-trading
  - ai_models
  - candidates
  - strict_workers
  - autonomy
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - scripts/ai/workers/models.registry.json
  - scripts/ai/workers/tasks.index.json
---

# 20_AI_CANDIDATES_MATRIX

## Source : MODELS_MATRIX_01.md + models.registry.json (validé 2026-05-14)

Modèles listés ici selon le registry canonique. Statut `VERIFIED` / `VERIFIED_FREE` seulement pour usage possible. Modèles `ABSENT_CURRENT_ENDPOINT`, `RETIRED_CURRENT_ENDPOINT`, `OBSOLETE_REPLACED` exclus ou A0.

## Légende

- **Autonomie max** : A0=DISABLED, A1=READ_ONLY, A2=DRAFT_ONLY, A3=SANDBOX_TEST, A4=WRITE_GATED
- **Statut registry** : VERIFIED (disponible sur endpoint), VERIFIED_FREE (gratuit), ABSENT (absent endpoint), RETIRED (retiré), OBSOLETE (remplacé)

## Matrice Complète

### Modèles VERIFIED (usage possible, A1/A2)

| model_id | config_id OpenCode | Statut | Autonomie max | Rôles autorisés | Tâches autorisées | Tâches interdites | Validation requise | Usage recommandé | Usage à éviter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| glm-5.1 | opencode/glm-5.1 | VERIFIED | A2 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, REVIEW_DRAFT | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | READ_INVENTORY (non listé), FAST_TRIAGE, WRITE_GATED | Modele fort + tests | Raisonnement / patch draft / revue forte intermediaire | Volume masse, tri rapide |
| glm-5 | opencode/glm-5 | VERIFIED | A2 | PATCH_DRAFT, DOC_DRAFT, TESTPLAN | PATCH_DRAFT, DOC_DRAFT, TESTPLAN | READ_INVENTORY (non listé), CHERRY_PICK_INVENTORY, FAST_TRIAGE, WRITE_GATED | Modele fort + tests | Worker raisonnement general / patch draft | Cherry-pick inventory, fast triage |
| kimi-k2.5 | opencode/kimi-k2.5 | VERIFIED | A2 | READ_INVENTORY, PATCH_DRAFT, CHERRY_PICK_INVENTORY | READ_INVENTORY, PATCH_DRAFT, CHERRY_PICK_INVENTORY | FAST_TRIAGE, WRITE_GATED, DOC_DRAFT (non listé) | Revue externe | Long contexte / code reading / inventaire commits | Triage rapide, doc draft volume |
| kimi-k2.6 | opencode/kimi-k2.6 | VERIFIED | A2 | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY | READ_INVENTORY (non listé), FAST_TRIAGE, WRITE_GATED | Revue externe stricte | Patch complexe / cherry-pick inventory | Volume lecture, tri rapide |
| minimax-m2.7 | opencode/minimax-m2.7 | VERIFIED | A2 | READ_INVENTORY, DOC_DRAFT, PATCH_DRAFT, TESTPLAN | READ_INVENTORY, DOC_DRAFT, PATCH_DRAFT (leger), TESTPLAN | FAST_TRIAGE, CHERRY_PICK_INVENTORY, WRITE_GATED | Revue externe | Patch simple / docs / testplan | Cherry-pick complexe, fast triage |
| minimax-m2.5 | opencode/minimax-m2.5 | VERIFIED | A2 | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | PATCH_DRAFT (non listé), CHERRY_PICK_INVENTORY, WRITE_GATED | Revue echantillonnee + diff | Volume / inventaire / docs | Patch complexe, cherry-pick |
| qwen3.6-plus | opencode/qwen3.6-plus | VERIFIED | A2 | DOC_DRAFT, TESTPLAN, PATCH_DRAFT, REVIEW_DRAFT | DOC_DRAFT, TESTPLAN, PATCH_DRAFT (leger), REVIEW_DRAFT | READ_INVENTORY (non listé), FAST_TRIAGE, CHERRY_PICK_INVENTORY, WRITE_GATED | Modele fort + tests | Testplan / doc structuree / patch leger | Volume lecture masse, tri rapide |
| qwen3.5-plus | opencode/qwen3.5-plus | VERIFIED | A2 | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | READ_INVENTORY, DOC_DRAFT, FAST_TRIAGE, CLOSEOUT_DRAFT | PATCH_DRAFT (non listé), CHERRY_PICK_INVENTORY, WRITE_GATED | Revue par echantillon | Haut volume / extraction / docs | Patch complexe, cherry-pick |
| big-pickle | opencode/big-pickle | VERIFIED | A2 | READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN | READ_INVENTORY, PATCH_DRAFT, DOC_DRAFT, TESTPLAN | FAST_TRIAGE, CHERRY_PICK_INVENTORY, WRITE_GATED | Modele fort + tests | Stealth worker pilote / extraction / brouillon | Triage rapide, cherry-pick |
| gpt-5-nano | opencode/gpt-5-nano | VERIFIED | A1 | FAST_TRIAGE, READ_INVENTORY | FAST_TRIAGE, READ_INVENTORY | PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED | Revue externe | Classification / tri tres court / formats courts | Tout ce qui depasse le tri court |

### Modèles VERIFIED_FREE (usage possible, A1 max)

| model_id | config_id OpenCode | Statut | Autonomie max | Rôles autorisés | Tâches autorisées | Tâches interdites | Validation requise | Usage recommandé | Usage à éviter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| minimax-m2.5-free | opencode/minimax-m2.5-free | VERIFIED_FREE | A1 | READ_INVENTORY, FAST_TRIAGE | READ_INVENTORY, FAST_TRIAGE | PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED | Revue externe | Volume gratuit / tri non sensible | Tout write, tout draft |
| nemotron-3-super-free | opencode/nemotron-3-super-free | VERIFIED_FREE | A1 | READ_INVENTORY, DOC_DRAFT | READ_INVENTORY, DOC_DRAFT | PATCH_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, FAST_TRIAGE, WRITE_GATED | Revue externe | Brouillon general non sensible | Patch, testplan, cherry-pick |
| deepseek-v4-flash-free | opencode/deepseek-v4-flash-free | VERIFIED_FREE | A1 | READ_INVENTORY, FAST_TRIAGE | READ_INVENTORY, FAST_TRIAGE | PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED | Revue externe | Tri rapide non sensible / lecture | Tout draft, tout write |
| ring-2.6-1t-free | opencode/ring-2.6-1t-free | VERIFIED_FREE | A1 | READ_INVENTORY, FAST_TRIAGE | READ_INVENTORY, FAST_TRIAGE | PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED | Revue externe | Tri rapide / lecture (successeur ling-2.6) | Tout write, tout draft |
| trinity-large-preview-free | opencode/trinity-large-preview-free | VERIFIED_FREE | A1 | READ_INVENTORY | READ_INVENTORY | FAST_TRIAGE, PATCH_DRAFT, DOC_DRAFT, TESTPLAN, CHERRY_PICK_INVENTORY, WRITE_GATED | Revue externe | Lecture conservative uniquement | Tout sauf lecture |

### Modèles ABSENT_CURRENT_ENDPOINT (A0 — exclus tant qu'absents)

| model_id | config_id | Statut | Autonomie max | Note |
| --- | --- | --- | --- | --- |
| mimo-v2-pro | null | ABSENT_CURRENT_ENDPOINT | A0 | Absent de l'endpoint au 2026-05-14 |
| mimo-v2-omni | null | ABSENT_CURRENT_ENDPOINT | A0 | Absent de l'endpoint au 2026-05-14 |
| mimo-v2.5-pro | null | ABSENT_CURRENT_ENDPOINT | A0 | Absent de l'endpoint au 2026-05-14 |
| mimo-v2.5 | null | ABSENT_CURRENT_ENDPOINT | A0 | Absent de l'endpoint au 2026-05-14 |
| deepseek-v4-pro | null | ABSENT_CURRENT_ENDPOINT | A0 | Toujours absent. deepseek-v4-flash-free present (version free) |

### Modèles RETIRED / OBSOLETE (A0 — exclus)

| model_id | config_id | Statut | Autonomie max | Note |
| --- | --- | --- | --- | --- |
| hy3-preview-free | opencode/hy3-preview-free | RETIRED_CURRENT_ENDPOINT | A0 | Retire de l'endpoint au 2026-05-14. Etait VERIFIED_FREE |
| ling-2.6-flash-free | opencode/ling-2.6-flash-free | RETIRED_CURRENT_ENDPOINT | A0 | Retire de l'endpoint au 2026-05-14. Successeur: ring-2.6-1t-free |
| deepseek-v4-flash | null | OBSOLETE_REPLACED | A0 | Remplace par deepseek-v4-flash-free dans le registry |

## Sélection par Tâche

### READ_INVENTORY
Qwen3.5 Plus, MiniMax M2.5, Kimi K2.5, Big Pickle, GPT-5 Nano, MiniMax M2.5 Free, Nemotron 3 Super Free, DeepSeek V4 Flash Free, Ring 2.6 1T Free, Trinity Large Preview Free

### PATCH_DRAFT
GLM-5.1, Kimi K2.6, GLM-5, Qwen3.6 Plus, MiniMax M2.7, Big Pickle

### DOC_DRAFT / CLOSEOUT_DRAFT
Qwen3.5 Plus, Qwen3.6 Plus, MiniMax M2.5, Nemotron 3 Super Free, Big Pickle

### TESTPLAN
GLM-5.1, Qwen3.6 Plus, Kimi K2.6, GLM-5, MiniMax M2.7

### CHERRY_PICK_INVENTORY
Kimi K2.5, Kimi K2.6, GLM-5.1, Qwen3.6 Plus, Big Pickle

### FAST_TRIAGE
Qwen3.5 Plus, MiniMax M2.5, GPT-5 Nano, MiniMax M2.5 Free, Nemotron 3 Super Free, DeepSeek V4 Flash Free, Ring 2.6 1T Free

### ENDPOINT_AUDIT
Qwen3.5 Plus, MiniMax M2.5, Big Pickle

### WRITE_GATED
GLM-5.1, Qwen3.6 Plus, Kimi K2.6, Big Pickle (uniquement avec dry-run + approbation explicite)

## Résumé des Statuts

| Statut | Nombre | Usage |
| --- | ---: | --- |
| VERIFIED | 10 | Usage possible A1/A2 |
| VERIFIED_FREE | 5 | Usage possible A1 max |
| ABSENT_CURRENT_ENDPOINT | 5 | Exclus (A0) |
| RETIRED_CURRENT_ENDPOINT | 2 | Exclus (A0) |
| OBSOLETE_REPLACED | 1 | Exclus (A0) |
| **Total** | **23** | |

## Règle de Promotion

Aucun modèle n'est promu décideur final. Aucun modèle n'est A4 sans preuve explicite documentée. La promotion A2→A3→A4 nécessite :
1. Test READ_ONLY PASS (3-5 fichiers non sensibles)
2. Test PATCH_DRAFT PASS (patch minimal théorique)
3. Consolidation : revue modele fort/humain + git diff + tests réels
