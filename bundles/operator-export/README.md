---
doc_id: BUNDLE_OPERATOR_EXPORT_01
doc_type: bundle/operator_export
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: operator_export
links:
  - bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md
  - bundles/claude-artifacts/README.md
---

# Operator Export — cursor-ai

Point d'entree pour un nouvel operateur cursor-ai.

## Resume de l'etat

- **Machine** : cursor-ai.
- **Sequence** : positions 1-4 terminees + Options A, B, C.
- **Admin-trading** : ferme.
- **Runtime** : non modifie.

## Ordre de lecture

1. `bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md` — reprise rapide.
2. `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` — bloc CURSOR_AI.
3. `bundles/claude-artifacts/README.md` — pack operateur.
4. `bundles/ACTIVE_WORKFLOW.md` — workflow Bundles.
5. `bundles/operator-export/EXPORT_MANIFEST.json` — inventaire complet.

## Actions possibles

- Lire `50_NEXT_GO_OPTIONS.md` pour les suites.
- Option D : nettoyage branches.
- Option E : admin-trading (ferme, phrase requise).
- Ou tout nouveau GO cursor-ai.

## A ne pas faire

- Ouvrir admin-trading sans la phrase d'activation.
- Modifier le runtime.
- Committer des secrets.
- Fermer alert_webhook ou Bundles produit.
