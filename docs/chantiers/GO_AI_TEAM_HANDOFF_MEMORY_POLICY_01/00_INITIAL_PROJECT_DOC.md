---
doc_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-21
links:
  - docs/agents/strict_workers/MODELS_MATRIX_01.md
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
  - scripts/ai/workers/tasks.index.json
  - scripts/ai/workers/models.registry.json
  - modules/model_provider_openclaw/config/agent_model_matrix.yaml
  - config/machine_runtime_map.yml
---

# GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01

## Objectif

Rendre l'équipe AI concrète : rôles, handoff protocol, mémoire partagée, task router, validation humaine (GAP_03 du parent).

## Périmètre

- Manager agent défini (rôle, responsabilités, modèle)
- Spécialistes définis (raisonnement, volume, long contexte, flash/tri)
- Handoff packet protocol (structure, validation, rejet)
- Memory broker (stockage partagé, rotation, recovery)
- Task router (affectation, file, priorité)
- Human validation gate
- Scénario multi-agent dry-run non destructif

## Preuve concrète pour l'ouverture

- `agent_model_matrix.yaml` : 4 agents OpenClaw (orchestrateur, builder, reviewer, lab) existent, sans handoff protocol ni mémoire
- `machine_runtime_map.yml` : sessions tmux openclaw définies sur admin-trading, gateway 18789 déclarée
- Le parent team AI existe mais l'architecture concrète n'est pas livrée

## Livrables

- Diagramme actor/role/handoff
- Protocole de handoff (packet JSON)
- Policy mémoire (scope, durée, rotation)
- Registry rôles
- Failure modes
- Preuve dry-run multi-agent

## Exclusions

- Implémentation des bridges apps externes
- Déploiement runtime machine-side
