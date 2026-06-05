---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01_40_VERIFICATION
doc_type: chantier/verification
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
---

# 40_VERIFICATION

## Verifications post-maintenance

### Check 1 — Fichiers presents

- [ ] `bundles/claude-artifacts/CHECKLIST_EXECUTION.md` existe.
- [ ] `bundles/claude-artifacts/bundle_meta/manifest.json` existe.
- [ ] `bundles/claude-artifacts/` contient maintenant 6 fichiers.
- [ ] `bundles/README.md` contient les nouvelles entrees.

### Check 2 — Manifest valide

```powershell
$manifest = Get-Content "bundles/claude-artifacts/bundle_meta/manifest.json" -Raw | ConvertFrom-Json
# Verifier schema
if ($manifest.schema -eq "opt_trading_bundle_manifest_v1") { "PASS: schema" }
# Verifier machine
if ($manifest.machine -eq "cursor-ai") { "PASS: machine" }
# Verifier invariants
if ($manifest.invariants.doc_only) { "PASS: doc_only" }
if ($manifest.invariants.no_runtime) { "PASS: no_runtime" }
if ($manifest.invariants.no_secrets) { "PASS: no_secrets" }
if ($manifest.invariants.no_admin_trading) { "PASS: no_admin_trading" }
# Verifier fichiers references
$manifest.files | ForEach-Object { "  file: $($_.path) -> $($_.role)" }
```

### Check 3 — Diff propre

```bash
git diff --stat
git diff --name-only | grep -vE "^(bundles/)"  # doit etre vide
```

### Check 4 — Aucun secret

```bash
git diff | grep -iE "(password|secret|token|key=|api_key|\.env)"  # doit etre vide
```

### Check 5 — Manifest JSON valide

```bash
python -m json.tool bundles/claude-artifacts/bundle_meta/manifest.json > $null && echo "PASS: valid JSON" || echo "FAIL: invalid JSON"
```

## Verdict attendu

Tous les checks PASS. Aucun fichier hors `bundles/`. Aucun secret.

## RISKS

- À qualifier.
