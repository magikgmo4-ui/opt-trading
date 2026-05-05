---
doc_id: BUNDLES_NO_RUNTIME_NO_SENSITIVE_RULES_01
doc_type: bundle/boundary_rules
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: workflow_active
links:
  - bundles/ACTIVE_WORKFLOW.md
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# NO_RUNTIME_NO_SENSITIVE_RULES — Regles Bundles cursor-ai

## Regles absolues

### Pas de runtime

Un bundle cursor-ai ne contient jamais :
- Modification de code dans `modules/`
- Modification de scripts dans `scripts/` (sauf scripts doc-only)
- Systemd units (`.service`, `.timer`)
- Configuration de webhook serveur
- Configuration de risk engine
- Fichiers de deploiement runtime

### Pas de secrets

Un bundle cursor-ai ne contient jamais :
- Cles API, mots de passe, credentials
- Fichiers `.env`, `.env.local`, `.env.production`
- Tokens (GitHub, MCP, Claude, API)
- Outputs live sensibles
- Captures d'alertes reelles
- Logs runtime avec donnees sensibles
- Payloads TradingView reels
- Chemins prives non anonymises

### Pas d'admin-trading sans demande

- Aucun bundle cursor-ai ne touche admin-trading sans demande explicite.
- Le bundle admin-trading gate (`BUNDLE_TYPES.md` #7) reste FERME.
- Toute violation = rollback.

### Pas de fermeture produit

- `alert_webhook` ne doit pas etre marque comme ferme.
- `Bundles produit` ne doit pas etre marque comme ferme.
- Les bundles sont un workflow actif, pas un produit termine.

## Verification pre-commit

```bash
# Verifier qu'aucun fichier runtime n'est touche
git diff --cached --name-only | grep -vE "^(docs/|bundles/)" && echo "WARNING: non-doc file" || echo "OK"

# Verifier qu'aucun secret n'est present
git diff --cached | grep -iE "(password|secret|token|key=|api_key|\.env)" && echo "WARNING: possible secret" || echo "OK"

# Verifier qu'aucun systemd/webhook/risk n'est touche
git diff --cached --name-only | grep -iE "(systemd|webhook|risk)" && echo "WARNING: runtime file" || echo "OK"
```

## Conformite machine

Les bundles cursor-ai respectent le routage machine defini dans `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` :
- Cursor-ai : preparation, documentation, packaging, gate.
- Admin-trading : runtime, services, execution (non ouvert sans demande).
- Aucune collision machine.
