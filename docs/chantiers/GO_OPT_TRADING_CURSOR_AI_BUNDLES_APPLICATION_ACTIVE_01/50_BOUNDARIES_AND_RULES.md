---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01_50_BOUNDARIES_AND_RULES
doc_type: chantier/boundaries_and_rules
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 50_BOUNDARIES_AND_RULES — Limites Bundles cursor-ai

Les regles completes sont dans `bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md`.

## Pas de runtime

Interdictions :
- Pas de modification de code dans `modules/`
- Pas de scripts runtime dans `scripts/`
- Pas de systemd units (`.service`, `.timer`)
- Pas de configuration webhook serveur
- Pas de configuration risk engine
- Pas de fichiers de deploiement runtime

## Pas de secrets

Interdictions :
- Pas de cles API, mots de passe, credentials
- Pas de `.env`, `.env.local`, `.env.production`
- Pas de tokens (GitHub, MCP, Claude, API)
- Pas d'outputs live sensibles
- Pas de captures d'alertes reelles
- Pas de logs runtime avec donnees sensibles
- Pas de payloads TradingView reels
- Pas de chemins prives non anonymises

## Pas d'admin-trading sans demande explicite

- Aucun bundle cursor-ai ne touche admin-trading.
- Le bundle admin-trading gate reste FERME.
- Conformite avec `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`.

## Pas de fermeture produit intempestive

- `alert_webhook` reste `ACTIVE_CONTINUITY`.
- `Bundles produit` reste `APPLICATION_DOCUMENTED`, non ferme.
- Les bundles sont un workflow, pas un produit termine.

## Verification pre-commit

```bash
# Fichiers hors docs/ et bundles/
git diff --cached --name-only | grep -vE "^(docs/|bundles/)"

# Secrets
git diff --cached | grep -iE "(password|secret|token|key=|api_key|\.env)"

# Runtime
git diff --cached --name-only | grep -iE "(systemd|webhook|risk)"
```

## RISKS

- À qualifier.
