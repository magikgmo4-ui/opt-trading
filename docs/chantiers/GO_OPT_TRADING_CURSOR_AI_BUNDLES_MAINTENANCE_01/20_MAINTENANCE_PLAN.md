---
doc_id: GO_OPT_TRADING_CURSOR_AI_BUNDLES_MAINTENANCE_01_20_MAINTENANCE_PLAN
doc_type: chantier/maintenance_plan
repo: opt-trading
machine: cursor-ai
status: active
---

# 20_MAINTENANCE_PLAN

## Actions

### 1. Creer CHECKLIST_EXECUTION.md

Checklist d'execution standard pour operateur cursor-ai :
- Avant tout commit (branche, diff, secrets, flags)
- Avant tout push (message, nommage, force-add)
- Avant toute PR (diff, inbox, closeout)
- Apres merge (sync, reprise)
- Commande de verification rapide

### 2. Creer bundle_meta/manifest.json

Metadata structuree du pack :
- Schema, bundle_id, bundle_type, machine, version
- Liste des fichiers
- Dependances
- Invariants

### 3. Mettre a jour bundles/README.md

Ajouter a l'index :
- `claude-artifacts/` (ACTIVE)
- `CURSOR_AI_OPERATOR_REPRISE_PACKET.md` (ACTIVE)
- `ACTIVE_WORKFLOW.md` (ACTIVE)
- `BUNDLE_TYPES.md` (ACTIVE)
- `OPERATOR_FLOW.md` (ACTIVE)
- `NO_RUNTIME_NO_SENSITIVE_RULES.md` (ACTIVE)

Mettre a jour le statut de `GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01` de ACTIVE a REFERENCE (historique).

## Modifications

- 2 nouveaux fichiers.
- 1 fichier modifie (`bundles/README.md`).
- Aucun fichier hors `bundles/`.
- Doc-only.

## RISKS

- À qualifier.
