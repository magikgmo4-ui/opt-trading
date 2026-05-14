# GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01

**Statut** : DRAFT
**Dépend de** : GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_PROVIDER_SMOKE_CANONICAL_01 (PASS)

## Objectif

Empêcher la saturation des sessions agent local Ollama sur Student.

## Problème

- n_ctx=4096 sur le modèle qwen2.5:0.5b-instruct
- System prompt ~3500 tokens
- Session historique non bornée → overflow → timeout >300s

## Solution documentée

- Rotation de session après 10 runs ou 7 jours
- Purge automatique des sessions avec PROMPT_ERROR
- Détection overflow avec seuils

## Documents

- `docs/chantiers/.../SESSION_RETENTION_POLICY_01.md`
- `docs/chantiers/.../RUNBOOK_SESSION_ROTATION_01.md`
- `docs/chantiers/.../CHECKPOINT.md`

## Prochaine action

Valider la politique, tester rotation manuelle, décider automation.
