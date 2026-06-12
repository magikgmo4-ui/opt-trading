---
doc_id: OPENCODE_ZEN_MODEL_ID_AUDIT_01
doc_type: external_model_id_audit
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_PARENT_01
status: draft_canonical
lifecycle_stage: validation
topic_keys:
  - opencode_zen
  - model_ids
  - strict_workers
  - audit
surface: docs/agents
source_kind: canonical
reference_canonique_principale: docs/agents/strict_workers/OPENCODE_ZEN_MODEL_ID_AUDIT_01.md
point_de_reprise: "Corriger la matrice et le task index selon les IDs confirmés"
updated_at: 2026-04-26
links:
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - scripts/ai/workers/tasks.index.json
  - https://opencode.ai/docs/zen/
---

# OPENCODE_ZEN_MODEL_ID_AUDIT_01

## 1. Objet

Valider les IDs OpenCode Zen utilisés dans la matrice `strict_workers`.

## 2. Source externe consultée

Source officielle :

```text
https://opencode.ai/docs/zen/
```

État observé :

```text
Last updated: Apr 26, 2026
```

## 3. Règle OpenCode

La doc OpenCode Zen indique que le modèle dans la configuration OpenCode utilise le format :

```text
opencode/<model-id>
```

Exemple :

```text
opencode/gpt-5.5
```

## 4. IDs confirmés dans la doc officielle

| Modèle | Model ID officiel | ID OpenCode config |
| --- | --- | --- |
| GPT 5.5 | `gpt-5.5` | `opencode/gpt-5.5` |
| GPT 5.5 Pro | `gpt-5.5-pro` | `opencode/gpt-5.5-pro` |
| GPT 5.4 | `gpt-5.4` | `opencode/gpt-5.4` |
| GPT 5.4 Pro | `gpt-5.4-pro` | `opencode/gpt-5.4-pro` |
| GPT 5.4 Mini | `gpt-5.4-mini` | `opencode/gpt-5.4-mini` |
| GPT 5.4 Nano | `gpt-5.4-nano` | `opencode/gpt-5.4-nano` |
| GPT 5 Nano | `gpt-5-nano` | `opencode/gpt-5-nano` |
| Qwen3.6 Plus | `qwen3.6-plus` | `opencode/qwen3.6-plus` |
| Qwen3.5 Plus | `qwen3.5-plus` | `opencode/qwen3.5-plus` |
| MiniMax M2.7 | `minimax-m2.7` | `opencode/minimax-m2.7` |
| MiniMax M2.5 | `minimax-m2.5` | `opencode/minimax-m2.5` |
| MiniMax M2.5 Free | `minimax-m2.5-free` | `opencode/minimax-m2.5-free` |
| GLM 5.1 | `glm-5.1` | `opencode/glm-5.1` |
| GLM 5 | `glm-5` | `opencode/glm-5` |
| Kimi K2.5 | `kimi-k2.5` | `opencode/kimi-k2.5` |
| Kimi K2.6 | `kimi-k2.6` | `opencode/kimi-k2.6` |
| Big Pickle | `big-pickle` | `opencode/big-pickle` |
| Ling 2.6 Flash | `ling-2.6-flash` | `opencode/ling-2.6-flash` |
| Hy3 Preview Free | `hy3-preview-free` | `opencode/hy3-preview-free` |
| Nemotron 3 Super Free | `nemotron-3-super-free` | `opencode/nemotron-3-super-free` |

## 5. Écarts observés contre la matrice initiale

### 5.1 À corriger

| Entrée matrice initiale | Correction |
| --- | --- |
| `opencode/ling-2.6-flash-free` | utiliser `opencode/ling-2.6-flash` |
| `Hy3 Preview` / `A_VERIFIER` | utiliser `opencode/hy3-preview-free` |
| `Nemotron 3 Super Free` déjà probable | confirmé : `opencode/nemotron-3-super-free` |
| `GPT-5 Nano` incertain | confirmé : `opencode/gpt-5-nano` |
| `MiniMax M2.5 Free` absent de matrice principale | ajouter comme worker volume gratuit distinct si nécessaire |

### 5.2 Toujours non confirmés dans la source officielle consultée

| Modèle utilisateur | Statut |
| --- | --- |
| MiMo-V2-Pro | non trouvé dans la doc officielle consultée |
| MiMo-V2-Omni | non trouvé dans la doc officielle consultée |
| MiMo-V2.5-Pro | non trouvé dans la doc officielle consultée |
| MiMo-V2.5 | non trouvé dans la doc officielle consultée |
| DeepSeek V4 Pro | non trouvé dans la doc officielle consultée |
| DeepSeek V4 Flash | non trouvé dans la doc officielle consultée |

Ces modèles peuvent exister dans ton interface, dans un endpoint spécifique, ou dans une liste non visible dans la page docs. Ils doivent rester `A_VERIFIER` tant qu'un test `/models` ou endpoint `/zen/v1/models` ne confirme pas l'ID exact.

## 6. Notes de prix / sécurité observées

La doc officielle indique :

- OpenCode Zen est en beta ;
- les admins peuvent activer/désactiver des modèles dans le workspace ;
- certains modèles free sont temporaires ;
- Big Pickle, MiniMax M2.5 Free, Ling 2.6 Flash Free, Hy3 Preview Free peuvent collecter des données pendant la période gratuite ;
- Nemotron 3 Super Free est sous conditions NVIDIA trial et ne doit pas recevoir de données personnelles ou confidentielles ;
- OpenAI / Anthropic peuvent avoir une rétention de 30 jours selon les politiques applicables.

## 7. Décision

La matrice strict workers doit distinguer :

```text
CONFIRMED_OFFICIAL_DOC
CONFIRMED_BY_USER_UI_ONLY
A_VERIFIER_ENDPOINT
DISABLED_UNTIL_VERIFIED
```

## 8. Prochaine action

Corriger :

```text
docs/agents/strict_workers/MODELS_MATRIX_01.md
scripts/ai/workers/tasks.index.json
```

puis lancer seulement un test `READ_INVENTORY` sur un modèle confirmé et non sensible.

## RISKS

- À qualifier.
