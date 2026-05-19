---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01_40_VERIFICATION_CHECKLIST
doc_type: chantier/verification_checklist
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/operator-export/CHECKLIST_VERIFICATION.md
---

# 40_VERIFICATION_CHECKLIST

Checklist de verification de l'export operateur.

La checklist complete est dans `bundles/operator-export/CHECKLIST_VERIFICATION.md`.

## Verifications export

- [ ] `bundles/operator-export/README.md` existe et presente le point d'entree.
- [ ] `bundles/operator-export/EXPORT_MANIFEST.json` existe et liste tous les bundles/GO.
- [ ] `bundles/operator-export/HANDOFF.md` donne les instructions de handoff.
- [ ] `bundles/operator-export/CHECKLIST_VERIFICATION.md` existe.
- [ ] Tous les bundles references dans le manifest existent dans le repo.
- [ ] Aucune reference admin-trading dans l'export.
- [ ] Aucun secret, token, .env dans l'export.
- [ ] L'export est autonome (un operateur peut reprendre sans la conversation).

## Verifications diff

```bash
git diff --stat
git diff --name-only | grep -vE "^(bundles/|docs/)"  # doit etre vide
```

## Verdict

PASS si toutes les verifications sont OK.
