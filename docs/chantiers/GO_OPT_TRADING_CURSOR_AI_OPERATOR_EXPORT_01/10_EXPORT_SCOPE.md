---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01_10_EXPORT_SCOPE
doc_type: chantier/export_scope
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/README.md
---

# 10_EXPORT_SCOPE

## Perimetre de l'export

L'export couvre l'integralite de l'etat cursor-ai valide apres Options A et B.

### Inclus

| Categorie | Contenu |
| --- | --- |
| Bundles cursor-ai | `bundles/claude-artifacts/`, `bundles/operator-export/`, fichiers workflow |
| Docs operationnelles | `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/` |
| Docs sequence | `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01/` |
| Docs sequence | `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_BUNDLES_APPLICATION_ACTIVE_01/` |
| Docs sequence | `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/` |
| Docs sequence | `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01/` |
| Docs sequence | `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01/` |
| Docs sequence | `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01/` |
| Routage machine | `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` |
| Reprise rapide | `bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md` |
| Inbox | `docs/index/inbox/` (GO cursor-ai) |

### Exclus

| Categorie | Raison |
| --- | --- |
| Admin-trading | Ferme, non inclus dans l'export cursor-ai |
| Runtime code | Hors perimetre doc-only |
| Secrets, .env, tokens | Interdits |
| Packs student | Machine separee |
| Branches Git | Referencees mais non exportees (Git = source) |

## Type d'export

- **Format** : documentation structuree + manifest JSON.
- **Transport** : le repo Git est la source canonique. L'export est un point d'entree lisible pour un nouvel operateur.
- **Autonomie** : un operateur peut lire `bundles/operator-export/README.md` et comprendre l'etat cursor-ai sans lire toute la conversation.
