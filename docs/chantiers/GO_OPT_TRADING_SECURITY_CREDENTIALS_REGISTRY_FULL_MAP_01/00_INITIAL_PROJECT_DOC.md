---
doc_id: GO_OPT_TRADING_SECURITY_CREDENTIALS_REGISTRY_FULL_MAP_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_SECURITY_CREDENTIALS_REGISTRY_FULL_MAP_01
parent_go: GO_OPT_TRADING_OPENCLAW_GOVERNANCE_CHILD_SECURITY_CREDENTIALS_METHOD_01
status: impl
created_at: 2026-06-03
---

# GO_OPT_TRADING_SECURITY_CREDENTIALS_REGISTRY_FULL_MAP_01

## Objectif

Compléter le registre canonique credentials/roles/machines avec toutes les apps
utilisées dans le repo — y compris celles absentes de l'inventaire initial.

## Apps ajoutées

| App | Credentials | Rôle | Statut |
|-----|-------------|------|--------|
| TradingView (webhook_server.py) | TV_WEBHOOK_KEY, OPS_ADMIN_KEY | webhook_receiver (complété) | ACTIVE |
| Airtable | AIRTABLE_API_KEY, AIRTABLE_BASE_ID | airtable_user (nouveau) | CONFIGURED |
| DeskPro | DESKPRO_API_KEY, DESKPRO_API_URL | deskpro_user (complété) | CONFIGURED |
| ClickUp | CLICKUP_TOKEN | clickup_user (nouveau) | CONFIGURED |
| Figma | FIGMA_TOKEN, FIGMA_FILE_KEY | figma_designer (nouveau) | FUTURE — phase 2 |
| Infrastructure SSH/SSHFS/WG | IDENTITY_FILE, WG_PRIVATE_KEY, termux key | infrastructure (nouveau) | ACTIVE système |

## KG Repo

`producer_repo_kg_v1.py` écrit dans `graph_bundle.json` localement.
Aucune credential externe requise — accès git uniquement (rôle git_dev).

## Règle multi-machine

Tous les rôles actifs sur `admin-trading` doivent être déployables sur `fantome`
sur demande via la procédure de sync SSH (voir 60_ROTATION_RUNBOOK.md du parent GO).

## Fichiers modifiés

```
configs/env/registry/credentials.yaml   — 12 nouvelles entrées
configs/env/registry/roles.yaml         — 4 nouveaux rôles, 2 complétés
configs/env/registry/machines.yaml      — mapping complet 5 machines
configs/env/roles/webhook_receiver.env.example   — TV_WEBHOOK_KEY + OPS_ADMIN_KEY ajoutés
configs/env/roles/airtable_user.env.example      — nouveau
configs/env/roles/clickup_user.env.example       — nouveau
configs/env/roles/figma_designer.env.example     — nouveau (future)
configs/env/roles/infrastructure.env.example     — nouveau
```
