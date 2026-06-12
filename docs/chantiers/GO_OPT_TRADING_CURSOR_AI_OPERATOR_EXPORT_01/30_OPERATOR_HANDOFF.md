---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01_30_OPERATOR_HANDOFF
doc_type: chantier/operator_handoff
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/operator-export/HANDOFF.md
---

# 30_OPERATOR_HANDOFF

Instructions de handoff pour un nouvel operateur cursor-ai.

Le handoff complet est dans `bundles/operator-export/HANDOFF.md`.

## Resume

```text
Nouvel operateur cursor-ai :

1. git clone ou git pull sot/mainline.
2. Lire bundles/operator-export/README.md.
3. Consulter bundles/operator-export/EXPORT_MANIFEST.json pour l'inventaire.
4. Suivre l'ordre de lecture dans 20_EXPORT_CONTENTS.md.
5. Utiliser bundles/claude-artifacts/PROMPT_TEMPLATES.md pour les actions.
6. Respecter bundles/claude-artifacts/NO_COMMIT_RULES.md pour la securite.
7. Admin-trading = FERME. Phrase "chantier pour admin-trading" requise.
8. Suite : 50_NEXT_GO_OPTIONS.md dans le packet de reprise.
```

## Etat des continuites

- alert_webhook = ACTIVE_CONTINUITY (ne pas fermer).
- Bundles = workflow actif, produit non ferme.
- Admin-trading = gate fermee.
- Runtime = non modifie.

## Commandes de demarrage

```bash
git fetch origin --prune
git checkout sot/mainline
git pull --rebase origin sot/mainline
git log --oneline -5
```

## RISKS

- À qualifier.
