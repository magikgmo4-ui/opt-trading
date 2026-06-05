# 00_START — GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01

## Contexte
- GO precedent : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01` — verdict FAIL controle
- Root cause : system prompt OpenClaw (~30K chars / 24 tools) trop lourd pour qwen2.5:3b-instruct sur CPU student
- Timeout 60s → 300s n'a pas suffi — le modele ne peut pas evaluer 30K chars de prompt en <300s
- Cette GO est le next GO recommande par le closeout precedent

## Objectif
Reduire le system prompt / tools / workspace OpenClaw pour permettre a qwen2.5:3b-instruct de repondre sans timeout sur student.

## Regles strictes
- Agir seulement sur student
- reduire tools : 3-5 max, pas d'exposition reseau inutile
- reduire workspace / system prompt
- garder qwen2.5:3b-instruct comme modele cible
- garder gateway local-only
- backup obligatoire avant modification
- rollback si health KO, listener LAN, config invalide, agent instable

## Branche
- `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01` depuis `origin/sot/mainline`

## RISKS

- À qualifier.
