---
doc_id: GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01_MVP_SPEC
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
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/01_architecture_cible.md
  - docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md
---

# 01_MVP_SPEC — AI Team MVP

## Perimetre

Le MVP AI Team est un setup minimal prouvant que le contrat d'integration Strict Workers fonctionne avec 3 workers qualifies sur 1 tache reelle doc-only.

### Inclus

- 3 workers : Observer, Documenter, Gatekeeper
- 1 tache : READ_INVENTORY (doc-only, read-only)
- Runner Python minimal (stdlib only)
- Task packet `read_inventory.json` compatible Strict Workers
- Smoke READ_INVENTORY obligatoire
- Sortie DRAFT_ONLY au format `13_ESTABLISHED..VERDICT_DRAFT_ONLY`
- Bundle reuse map documentant les 4 artefacts REUSE_FOR_MVP

### Exclus

- Orchestrator / Supervisor (deferre au MVP suivant)
- Analyzer / Reasoner (deferre)
- PATCH_DRAFT / DOC_DRAFT (deferre, tache read-only only)
- Sandbox Docker
- Framework d'orchestration (LangGraph, CrewAI, etc.)
- Git write ops
- ClickUp

## Architecture MVP

```
modules/ai_team_mvp/
  runner.py                    # Runner securise read-only
  tasks/
    read_inventory.json        # Task packet Strict Workers
  README.md                    # Documentation operateur
```

## Flux d'execution

1. Operateur humain lance `runner.py` avec la tache `read_inventory`.
2. Le runner charge le task packet et verifie qu'il est autorise.
3. Le runner verifie qu'aucun denied_input n'est touche.
4. Le runner execute la tache (lecture docs/chantiers/ + GO_INDEX.md).
5. Le runner produit une sortie au format DRAFT_ONLY.
6. Le runner verifie qu'aucun git write n'a ete fait.
7. Le Gatekeeper (humain) valide la sortie avant toute suite.

## Contrat Strict Workers applique

```text
no_secrets: true
no_env_files: true
no_git_write_ops: true
no_runtime_write_by_default: true
requires_external_validation: true
output_status: DRAFT_ONLY
only_verified_models: true
```

### Denied inputs

```
.env, **/.env, **/*secret*, **/*token*, **/*credential*,
**/id_rsa, **/id_ed25519, **/*.pem, **/*.key
```

### Denied commands

```
git add, git commit, git push, git rebase, git merge,
rm -rf, chmod -R, chown -R
```

## Cible de sortie (format required_sections)

```
13_ESTABLISHED
14_HYPOTHESIS
15_REMAINING_GAP
16_TODO
VERDICT_DRAFT_ONLY
```
