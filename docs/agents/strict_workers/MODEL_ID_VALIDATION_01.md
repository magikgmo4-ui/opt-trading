---
doc_id: STRICT_WORKERS_MODEL_ID_VALIDATION_01
doc_type: agent_model_id_validation
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: draft_canonical
lifecycle_stage: validation
topic_keys:
  - strict_workers
  - opencode_zen
  - model_ids
  - validation
surface: docs/agents
source_kind: canonical
reference_canonique_principale: docs/agents/strict_workers/MODEL_ID_VALIDATION_01.md
point_de_reprise: "Utiliser uniquement les IDs VERIFIED dans le task index jusqu'à nouvelle vérification"
updated_at: 2026-04-26
links:
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
---

# MODEL_ID_VALIDATION_01 — OpenCode Zen strict workers

## 1. Objet

Valider les IDs réels utilisables pour les `strict_workers / auto_workers` à partir de l'endpoint OpenCode Zen courant.

## 2. Source vérifiée

Endpoint consulté :

```text
https://opencode.ai/zen/v1/models
```

Date de validation documentaire :

```text
2026-04-26
```

## 3. IDs confirmés pour la liste utilisateur

| Modèle utilisateur | ID endpoint OpenCode | ID de config OpenCode | Statut |
| --- | --- | --- | --- |
| GLM-5.1 | `glm-5.1` | `opencode/glm-5.1` | VERIFIED |
| GLM-5 | `glm-5` | `opencode/glm-5` | VERIFIED |
| Kimi K2.5 | `kimi-k2.5` | `opencode/kimi-k2.5` | VERIFIED |
| Kimi K2.6 | `kimi-k2.6` | `opencode/kimi-k2.6` | VERIFIED |
| MiniMax M2.7 | `minimax-m2.7` | `opencode/minimax-m2.7` | VERIFIED |
| MiniMax M2.5 | `minimax-m2.5` | `opencode/minimax-m2.5` | VERIFIED |
| MiniMax M2.5 Free | `minimax-m2.5-free` | `opencode/minimax-m2.5-free` | VERIFIED |
| Qwen3.6 Plus | `qwen3.6-plus` | `opencode/qwen3.6-plus` | VERIFIED |
| Qwen3.5 Plus | `qwen3.5-plus` | `opencode/qwen3.5-plus` | VERIFIED |
| Big Pickle | `big-pickle` | `opencode/big-pickle` | VERIFIED |
| Hy3 Preview | `hy3-preview-free` | `opencode/hy3-preview-free` | VERIFIED_FREE |
| Ling 2.6 Flash | `ling-2.6-flash-free` | `opencode/ling-2.6-flash-free` | VERIFIED_FREE |
| Nemotron 3 Super | `nemotron-3-super-free` | `opencode/nemotron-3-super-free` | VERIFIED_FREE |
| GPT-5 Nano | `gpt-5-nano` | `opencode/gpt-5-nano` | VERIFIED |

## 4. IDs absents du endpoint courant

Ces modèles sont présents dans la liste ou l'image utilisateur, mais absents du endpoint OpenCode Zen au moment de validation :

| Modèle utilisateur | ID supposé précédent | Statut courant | Conséquence |
| --- | --- | --- | --- |
| MiMo-V2-Pro | `mimo-v2-pro`, `mimo-v2-pro-free` | ABSENT_CURRENT_ENDPOINT | ne pas router |
| MiMo-V2-Omni | `mimo-v2-omni`, `mimo-v2-omni-free` | ABSENT_CURRENT_ENDPOINT | ne pas router |
| MiMo-V2.5-Pro | `mimo-v2.5-pro` | ABSENT_CURRENT_ENDPOINT | ne pas router |
| MiMo-V2.5 | `mimo-v2.5` | ABSENT_CURRENT_ENDPOINT | ne pas router |
| DeepSeek V4 Pro | `deepseek-v4-pro` | ABSENT_CURRENT_ENDPOINT | ne pas router |
| DeepSeek V4 Flash | `deepseek-v4-flash` | ABSENT_CURRENT_ENDPOINT | ne pas router |

## 5. Autres IDs utiles visibles dans l'endpoint

Le endpoint expose aussi des familles utiles pour comparaison ou consolidation future :

```text
claude-opus-4-7
claude-opus-4-6
claude-opus-4-5
claude-opus-4-1
claude-sonnet-4-6
claude-sonnet-4-5
claude-sonnet-4
claude-3-5-haiku
claude-haiku-4-5
gemini-3.1-pro
gemini-3-pro
gemini-3-flash
gpt-5.5
gpt-5.5-pro
gpt-5.4
gpt-5.4-pro
gpt-5.4-mini
gpt-5.4-nano
gpt-5.3-codex-spark
gpt-5.3-codex
gpt-5.2
gpt-5.2-codex
gpt-5.1
gpt-5.1-codex-max
gpt-5.1-codex
gpt-5.1-codex-mini
gpt-5
gpt-5-codex
trinity-large-preview-free
```

Ces modèles ne sont pas intégrés au pool strict_workers initial sauf décision explicite.

## 6. Règle d'exécution immédiate

Jusqu'à nouvelle vérification :

```text
- seuls les modèles VERIFIED / VERIFIED_FREE peuvent être placés dans preferred_workers
- les modèles ABSENT_CURRENT_ENDPOINT restent documentés mais non routables
- les quotas utilisateur restent utiles comme indication, mais ne prouvent pas la disponibilité courante
```

## 7. Décision de routage

Pour le task index courant :

```text
Retirer des preferred_workers :
- deepseek-v4-pro
- deepseek-v4-flash
- mimo-v2.5
- mimo-v2-pro
- mimo-v2-omni
- mimo-v2.5-pro
```

Ajouter ou confirmer :

```text
- hy3-preview-free
- ling-2.6-flash-free
- nemotron-3-super-free
- minimax-m2.5-free
- gpt-5-nano
```

## 8. Point de reprise

```text
Prochaine étape : créer un premier runner ou des commandes OpenCode qui ne consomment que scripts/ai/workers/models.registry.json et scripts/ai/workers/tasks.index.json.
```

## RISKS

- À qualifier.
