# STRICT WORKER REPORT — ENDPOINT_AUDIT

## ENDPOINT_CONSULTE

https://opencode.ai/zen/v1/models → 40 modeles retournes (2026-05-19)

## MODELES_TROUVES

| ID Endpoint | Provider | Note |
|---|---|---|
| claude-opus-4-7 | Anthropic | Nouveau |
| claude-opus-4-6 | Anthropic | Nouveau |
| claude-opus-4-5 | Anthropic | Nouveau |
| claude-opus-4-1 | Anthropic | Nouveau |
| claude-sonnet-4-6 | Anthropic | Nouveau |
| claude-sonnet-4-5 | Anthropic | Nouveau |
| claude-sonnet-4 | Anthropic | Nouveau |
| claude-haiku-4-5 | Anthropic | Nouveau |
| gemini-3.1-pro | Google | Nouveau |
| gemini-3-flash | Google | Nouveau |
| gpt-5.5 | OpenAI | Nouveau |
| gpt-5.5-pro | OpenAI | Nouveau |
| gpt-5.4 | OpenAI | Nouveau |
| gpt-5.4-pro | OpenAI | Nouveau |
| gpt-5.4-mini | OpenAI | Nouveau |
| gpt-5.4-nano | OpenAI | Nouveau |
| gpt-5.3-codex-spark | OpenAI | Nouveau |
| gpt-5.3-codex | OpenAI | Nouveau |
| gpt-5.2 | OpenAI | Nouveau |
| gpt-5.2-codex | OpenAI | Nouveau |
| gpt-5.1 | OpenAI | Nouveau |
| gpt-5.1-codex-max | OpenAI | Nouveau |
| gpt-5.1-codex | OpenAI | Nouveau |
| gpt-5.1-codex-mini | OpenAI | Nouveau |
| gpt-5 | OpenAI | Nouveau |
| gpt-5-codex | OpenAI | Nouveau |
| gpt-5-nano | OpenAI | Present dans registry |
| glm-5.1 | Zhipu | Present dans registry |
| glm-5 | Zhipu | Present dans registry |
| minimax-m2.7 | MiniMax | Present dans registry |
| minimax-m2.5 | MiniMax | Present dans registry |
| minimax-m2.5-free | MiniMax | Present dans registry |
| kimi-k2.6 | Moonshot | Present dans registry |
| kimi-k2.5 | Moonshot | Present dans registry |
| qwen3.6-plus | Alibaba | Present dans registry |
| qwen3.6-plus-free | Alibaba | Nouveau |
| qwen3.5-plus | Alibaba | Present dans registry |
| big-pickle | Big-Pickle | Present dans registry |
| deepseek-v4-flash-free | DeepSeek | Present dans registry |
| nemotron-3-super-free | NVIDIA | Present dans registry |

## COMPARAISON_REGISTRY

Registry actuel: scripts/ai/workers/models.registry.json (valide le 2026-05-14)

### Modeles ENDPOINT presents dans REGISTRY (13)

glm-5.1, glm-5, kimi-k2.5, kimi-k2.6, minimax-m2.7, minimax-m2.5, minimax-m2.5-free, qwen3.6-plus, qwen3.5-plus, big-pickle, gpt-5-nano, deepseek-v4-flash-free, nemotron-3-super-free

### Modeles REGISTRY ABSENTS de l ENDPOINT (2)

| Registry Key | Status Registry | Note |
|---|---|---|
| ring-2.6-1t-free | VERIFIED_FREE | RETIRE de l endpoint (etait nouveau au 2026-05-14) |
| trinity-large-preview-free | VERIFIED_FREE | RETIRE de l endpoint (etait nouveau au 2026-05-14) |

## AJOUTS

27 nouveaux modeles dans l endpoint absents du registry:

- Claude: opus-4-7, opus-4-6, opus-4-5, opus-4-1, sonnet-4-6, sonnet-4-5, sonnet-4, haiku-4-5 (8)
- Gemini: 3.1-pro, 3-flash (2)
- GPT-5.x: 5.5, 5.5-pro, 5.4, 5.4-pro, 5.4-mini, 5.4-nano, 5.3-codex-spark, 5.3-codex, 5.2, 5.2-codex, 5.1, 5.1-codex-max, 5.1-codex, 5.1-codex-mini, 5, 5-codex (16)
- Free: qwen3.6-plus-free (1)

## RETRAITS

- ring-2.6-1t-free (etait VERIFIED_FREE depuis 2026-05-14)
- trinity-large-preview-free (etait VERIFIED_FREE depuis 2026-05-14)

## RECOMMANDATIONS

1. Mettre a jour models.registry.json: passer ring-2.6-1t-free et trinity-large-preview-free de VERIFIED_FREE a RETIRED_CURRENT_ENDPOINT
2. Ajouter les 27 nouveaux modeles en statut ABSENT_CURRENT_ENDPOINT (ou DRAFT si on veut les evaluer)
3. Les modeles Claude/GPT-5.x sont des ajouts majeurs — evaluer autonomie_max et roles avant de les promouvoir en VERIFIED
4. Mettre a jour validated_at: "2026-05-19"
5. Le champ validation_source est correct (https://opencode.ai/zen/v1/models)

## RISQUES

- R1: ring-2.6-1t-free est reference dans 4 job packets (READ_INVENTORY_MATRIX_01, FAST_TRIAGE_MATRIX_01, POOL_SMOKE_RING_2_6_1T_FREE, POOL_SMOKE_TRINITY) — la CI/CD qui utilise l endpoint reel echouera si ces modeles ne sont pas disponibles
- R2: trinity-large-preview-free est le seul modele reference dans POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE.json — ce job packet devient non executable
- R3: L endpoint a change significativement en 5 jours (2026-05-14 → 2026-05-19) — 27 ajouts, 2 retraits. La cadence de validation du registry devrait etre hebdomadaire

## VERDICT_DRAFT_ONLY
