# GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01

## Verdict
**PASS**

## Resume
Le system prompt OpenClaw a ete reduit de ~30K chars (24 tools) a ~12.8K chars (1 tool) via :
- `tools.profile = minimal` (1 tool au lieu de 24)
- Reduction des fichiers workspace (AGENTS.md 7874→150 chars, etc.)
- Timeout augmente a 300s

qwen2.5:3b-instruct repond maintenant en 12-75s sans timeout. Modele/provider inchanges.

## Actions
- Config : `tools.profile = minimal`, `idleTimeoutSeconds = 300`, `timeoutSeconds = 300`
- Workspace : tous les fichiers .md reduits a 22-150 chars chacun
- Agent smoke : 3/3 tests PASS (latence 12s-75s)
- Backup complet : `/home/openclaw-lab/openclaw_lab_backups/workspace_slim_01/`

## Chantier
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01/`

## RISKS

- À qualifier.
