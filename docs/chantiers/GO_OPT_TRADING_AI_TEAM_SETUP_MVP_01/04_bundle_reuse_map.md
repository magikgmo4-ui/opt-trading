---
doc_id: GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01_BUNDLE_REUSE_MAP
doc_type: spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01
status: open
lifecycle_stage: spec
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_BUNDLES_REUSE_AUDIT_01/
---

# 04_BUNDLE_REUSE_MAP — Mapping des artefacts reutilises

## Artefacts REUSE_FOR_MVP

| Artefact | Statut | Utilisation dans le MVP | Preuve |
|:---------|:-------|:------------------------|:-------|
| **Strict Workers** (remote `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01`) | REUSE | Couche securite/execution : denied_inputs, denied_commands, required_sections, no_git_write, DRAFT_ONLY, smoke READ_INVENTORY | Architecture Canon Axes 7-8 |
| **Architecture Canon** (`docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/`) | REUSE | Structure cible : 3 couches, 5 roles, contrat d'integration, next GO | 01_architecture_cible.md, 02_decisions.md |
| **validated_prompt_factory** (`modules/validated_prompt_factory/`) | REUSE | Utilitaire : generation prompts structures, mode bundle_transfer disponible | README, cmd.sh, 4 modes operatoires |
| **Multi-Agents Canon Parent** (remote `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`) | REUSE | Doctrine multi-agent : BUNDLE_EXECUTION_PROMPT, EXECUTION_BUNDLE_PLAN, gap indexation | 8 docs dans le chantier |

## Mapping fonctionnel

```
                       Architecture Canon
                       (structure cible)
                              |
          +-------------------+-------------------+
          |                   |                   |
   Strict Workers      validated_prompt     Multi-Agents
   (securite+exec)     (std prompts)        (doctrine)
          |                   |                   |
     denied_inputs      bundle_transfer    BUNDLE_EXECUTION
     denied_commands    prompt templates   EXECUTION_BUNDLE
     required_sections                      GAP_INDEXATION
     smoke READ_INV
          |
     Runner MVP
     tasks/read_inventory.json
```

## Ce qui n'a PAS ete recreé

- Aucun nouveau format de bundle (reutilise `validated_prompt_factory/bundle_transfer`)
- Aucune nouvelle politique de securite (reutilise Strict Workers)
- Aucun nouveau cadre d'architecture (reutilise Architecture Canon)
- Aucune nouvelle doctrine agent (reutilise Multi-Agents Canon Parent)
- Aucun nouveau systeme de tasks index (reutilise le format Strict Workers)

## Ce qui a ete cree (net nouveau)

- `modules/ai_team_mvp/runner.py` : runner read-only minimal
- `modules/ai_team_mvp/tasks/read_inventory.json` : premier task packet MVP
- `docs/chantiers/GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01/` : chantier setup documentaire
