---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01_40_VALIDATION_MATRIX
doc_type: chantier/validation_matrix
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/20_PRE_ADMIN_GATE_REQUIREMENTS.md
---

# 40_VALIDATION_MATRIX

Matrice de validation avant toute ouverture admin-trading pour alert_webhook.

| # | Check | Commande / Inspection | Attendu | PASS/FAIL | Bloque ouverture |
| --- | --- | --- | --- | --- | --- |
| 1 | Fichiers modifies hors docs/ bundles/ | `git diff --name-only | grep -vE "^(docs/|bundles/)"` | Aucun | PASS si vide | OUI |
| 2 | Secrets dans le diff | `git diff | grep -iE "(password|secret|token|key=|api_key|\.env)"` | Aucun | PASS si vide | OUI |
| 3 | `trade_allowed` modifie | `git diff -- modules/ | grep "trade_allowed.*true"` | Aucun | PASS si vide | OUI |
| 4 | `admin_trading_runtime` modifie | `git diff -- modules/ | grep "admin_trading_runtime.*true"` | Aucun | PASS si vide | OUI |
| 5 | webhook_server.py modifie | `git diff --name-only | grep webhook_server.py` | Aucun | PASS si vide | OUI |
| 6 | systemd touche | `git diff --name-only | grep -i systemd` | Aucun | PASS si vide | OUI |
| 7 | risk engine touche | `git diff --name-only | grep -i risk` | Aucun | PASS si vide | OUI |
| 8 | URL webhook reelle dans diff | `git diff | grep -iE "https?://[^/]+/webhook" | grep -v "127.0.0.1\|localhost"` | Aucune | PASS si vide | OUI |
| 9 | Demande explicite "chantiers pour admin-trading" | Verification manuelle | Phrase prononcee | PASS si oui | OUI |
| 10 | alert_webhook non ferme | Inspection `ACTIVE_CONTINUITY` | Statut preserve | PASS | NON (doc-only) |
| 11 | Bundles produit non ferme | Inspection `APPLICATION_DOCUMENTED` | Statut preserve | PASS | NON (doc-only) |
| 12 | Commit doc-only | `git diff --stat` | Seulement `docs/`, `bundles/` | PASS | NON si doc-only |

## Commande de verification combinee

```bash
# Check 1-8 en une seule commande
echo "=== Check 1: non-doc files ==="
git diff --name-only --diff-filter=ACMR | grep -vE "^(docs/|bundles/)" || echo "PASS: no non-doc files"

echo "=== Check 2: secrets ==="
git diff | grep -iE "(password|secret|token|key=|api_key|\.env)" && echo "FAIL: secrets found" || echo "PASS: no secrets"

echo "=== Check 3: trade_allowed ==="
git diff -- modules/ | grep "trade_allowed.*true" && echo "FAIL: trade_allowed=true" || echo "PASS: trade_allowed safe"

echo "=== Check 4: admin_trading_runtime ==="
git diff -- modules/ | grep "admin_trading_runtime.*true" && echo "FAIL: admin_trading_runtime=true" || echo "PASS: admin_trading_runtime safe"

echo "=== Check 5: webhook_server ==="
git diff --name-only | grep webhook_server.py && echo "FAIL: webhook_server modified" || echo "PASS: webhook_server untouched"

echo "=== Check 6: systemd ==="
git diff --name-only | grep -i systemd && echo "FAIL: systemd touched" || echo "PASS: systemd untouched"

echo "=== Check 7: risk engine ==="
git diff --name-only | grep -i risk && echo "FAIL: risk engine touched" || echo "PASS: risk engine untouched"

echo "=== Check 8: real webhook URLs ==="
git diff | grep -iE "https?://[^/]+/webhook" | grep -v "127.0.0.1\|localhost" && echo "FAIL: real webhook URL found" || echo "PASS: no real webhook URLs"
```

## Interpretation

- Tout `FAIL` sur les checks 1-9 = **bloque ouverture admin-trading**.
- Checks 10-12 = non bloquants (doc-only status).
- Aucune ouverture sans tous les checks 1-9 PASS.
