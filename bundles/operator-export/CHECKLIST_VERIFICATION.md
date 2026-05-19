# CHECKLIST_VERIFICATION — Operator Export

Checklist de verification de l'integrite de l'export operateur cursor-ai.

## Verifications export

- [ ] `bundles/operator-export/README.md` existe.
- [ ] `bundles/operator-export/EXPORT_MANIFEST.json` existe et est un JSON valide.
- [ ] `bundles/operator-export/HANDOFF.md` existe.
- [ ] `bundles/operator-export/CHECKLIST_VERIFICATION.md` existe (ce fichier).

## Verifications bundles references

- [ ] `bundles/claude-artifacts/README.md` existe.
- [ ] `bundles/ACTIVE_WORKFLOW.md` existe.
- [ ] `bundles/BUNDLE_TYPES.md` existe.
- [ ] `bundles/OPERATOR_FLOW.md` existe.
- [ ] `bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md` existe.
- [ ] `bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md` existe.

## Verifications GO references

- [ ] Tous les dossiers `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_*/` references existent.

## Verifications continuites

- [ ] `alert_webhook` n'est pas marque comme ferme.
- [ ] `Bundles produit` n'est pas marque comme ferme.
- [ ] Aucune reference admin-trading ouverte.

## Verifications securite

- [ ] Aucun secret dans l'export.
- [ ] Aucun `.env` dans l'export.
- [ ] Aucun token dans l'export.
- [ ] Aucun endpoint de production dans l'export.

## Commande de verification

```bash
# Verifier que tous les fichiers references existent
for f in bundles/operator-export/* bundles/claude-artifacts/README.md bundles/ACTIVE_WORKFLOW.md bundles/BUNDLE_TYPES.md bundles/OPERATOR_FLOW.md bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md; do
  if [ -f "$f" ]; then echo "PASS: $f"; else echo "FAIL: $f"; fi
done

# Verifier l'absence de secrets
grep -riE "(password|secret|token|api_key)" bundles/operator-export/ && echo "FAIL: possible secret" || echo "PASS: no secrets"
```
