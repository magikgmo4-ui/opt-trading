# 00_START

## Contexte post provider switch PASS
- switch apply : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_APPLY_01`
- commit switch apply : `38f1f4d`
- verdict switch apply : `PASS`
- `defaultModel` : `ollama/deepseek-r1:1.5b`
- `models.json` hash : `65066bdc...` inchange

## Objectif
Prouver le chemin E2E minimal :
```
OpenClaw lab local → provider ollama → Ollama 127.0.0.1:11434 → deepseek-r1:1.5b → reponse
```

## Regles strictes
- Aucun changement db-layer / admin-trading
- Aucun trading reel / orchestrator
- Aucun listener LAN
- Aucun telechargement de modele
- Aucun changement models.json
- Aucun secret expose
- Aucun prompt long
- Si E2E inaccessible sans secret, produire GAP documente
