---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_50_NO_COMMIT_RULES
doc_type: chantier/no_commit_rules
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
---

# 50_NO_COMMIT_RULES

Regles strictes de non-commit applicables a tout operateur cursor-ai.

Les regles completes sont dans `bundles/claude-artifacts/NO_COMMIT_RULES.md`.

## Resume des interdictions

| Categorie | Ne jamais committer |
| --- | --- |
| Secrets | cles API, mots de passe, credentials |
| .env | .env, .env.local, .env.production |
| Tokens | tokens GitHub, MCP, Claude, API |
| Outputs live | captures d'alerte reelles, logs runtime, payloads TradingView |
| Captures sensibles | screenshots avec donnees personnelles, logs avec IP |
| Payloads reels | JSON de transactions, signaux trading reels |
| Chemins prives | chemins absolus non anonymises |

## Commande de verification pre-commit

```bash
# Verifier secrets
git diff --cached | grep -iE "(password|secret|token|key=|api_key|\.env)" && echo "WARNING" || echo "OK"

# Verifier chemins prives
git diff --cached | grep -oP "C:\\\\Users\\\\[^\\\\]+" | sort -u
```

## Sanctions en cas de violation

1. Revert immediat du commit.
2. Rotation des tokens si applicable.
3. Documentation de l'incident dans le GO courant.

## RISKS

- À qualifier.
