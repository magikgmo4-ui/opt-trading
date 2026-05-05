---
doc_id: BUNDLE_CLAUDE_ARTIFACTS_NO_COMMIT_RULES
doc_type: bundle/no_commit_rules
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: operator_pack
links:
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
  - bundles/claude-artifacts/REPRISE_TEMPLATE.md
---

# NO_COMMIT_RULES — Claude Artifacts Operator Pack

Regles strictes de ce qui ne doit **jamais** etre committe dans le repo.

## Interdictions absolues

| Categorie | Exemples | Raison |
| --- | --- | --- |
| Secrets | cles API, mots de passe, credentials | Securite |
| .env | fichiers .env, .env.local, .env.production | Contiennent souvent des secrets |
| Tokens | tokens GitHub, tokens MCP, tokens Claude | Acces non autorise |
| Outputs live | captures d'alerte reelles, logs runtime, payloads TradingView | Donnees sensibles ou live |
| Captures sensibles | screenshots avec donnees personnelles, logs avec IP | Vie privee / securite |
| Payloads reels | JSON de transactions, signaux trading reels | Donnees financieres sensibles |
| Chemins locaux prives | chemins absolus avec `C:\Users\<nom>\` non anonymises | Vie privee |

## Chemins acceptables

| Acceptable | Exemple |
| --- | --- |
| Chemins anonymises | `C:\Users\<user>\opt-trading` |
| Chemins relatifs | `./docs/chantiers/`, `./bundles/` |
| Variables | `$REPO_ROOT`, `$WORKSPACE` |

## Verification avant commit

```bash
# Verifier qu'aucun secret n'est present dans le diff
git diff --cached | grep -iE "(password|secret|token|key=|api_key|\.env)" && echo "WARNING: possible secret" || echo "OK"

# Verifier qu'aucun chemin prive n'est present
git diff --cached | grep -oP "C:\\\\Users\\\\[^\\\\]+" | sort -u
# Si des chemins apparaissent, les anonymiser avant commit
```

## Sanctions

Tout commit contenant un element interdit doit etre :
1. Revert immediat.
2. Token rotation si applicable.
3. Documentation de l'incident.
