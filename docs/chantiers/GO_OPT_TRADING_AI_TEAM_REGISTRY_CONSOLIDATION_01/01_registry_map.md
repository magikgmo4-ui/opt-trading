---
doc_id: GO_OPT_TRADING_AI_TEAM_REGISTRY_CONSOLIDATION_01_REGISTRY_MAP
doc_type: registry_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_REGISTRY_CONSOLIDATION_01
status: open
lifecycle_stage: registry
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 01_REGISTRY_MAP — Mapping des registres AI Team

## Structure des registres

```
modules/ai_team_mvp/registry/
  workers.registry.json    — 5 roles Architecture Canon
  tasks.registry.json      — 4 task types implementes
  outputs.registry.json    — 3 outputs + smoke trace
```

## Mapping workers → tasks

| Worker | Task Type | Packet | Output | Smoke |
|:-------|:----------|:-------|:-------|:------|
| observer | READ_INVENTORY | `tasks/read_inventory.json` | `.observer_output_last.txt` | 6/6 PASS |
| analyzer | ANALYZE_INVENTORY | `tasks/analyze_inventory.json` | `analyzer_*.md` | 8/8 PASS |
| documenter | DOC_DRAFT | `tasks/observer_doc_draft.json` | `documenter_*.md` | 6/6 PASS |
| orchestrator | ORCHESTRATOR_CHAIN | `tasks/orchestrator_chain_v2.json` | (delegue aux sous-taches) | 7/7 PASS |
| gatekeeper | GATEKEEPER_VALIDATE | (humain) | (humain) | HITL |

## Chaine MVP v2

```
observer          analyzer         documenter        gatekeeper
(READ_INVENTORY)  (ANALYZE_INV)    (DOC_DRAFT)       (HITL)
     │                 │                │                │
     ▼                 ▼                ▼                ▼
.observer_output  analyzer_*.md    documenter_*.md   validation
(last.txt)                                          humaine
     │                 │                │
     └─────────┬───────┘                │
               │                        │
         orchestrator (ORCHESTRATOR_CHAIN)
               │
         chaine les 3 etapes, arret au 1er echec
```

## Contrat Strict Workers (commun a tous)

| Regle | Valeur |
|:------|:------|
| no_secrets | true |
| no_env_files | true |
| no_git_write_ops | true |
| no_runtime_write_by_default | true |
| requires_external_validation | true |
| output_status | DRAFT_ONLY |
| only_verified_models | true |
| model | opencode-go/deepseek-v4-pro |

### Denied inputs (communs)

```
.env, **/.env, **/*secret*, **/*token*, **/*credential*,
**/id_rsa, **/id_ed25519, **/*.pem, **/*.key
```

### Denied commands (communs)

```
git add, git commit, git push, git rebase, git merge,
rm -rf, chmod -R, chown -R
```

## Zones d'ecriture

| Zone | Workers autorises |
|:-----|:------------------|
| `modules/ai_team_mvp/drafts/` | analyzer, documenter |
| Aucune (read-only) | observer, orchestrator, gatekeeper |

## Gaps

- Gatekeeper non automatise (HITL uniquement).
- Pas de PATCH_DRAFT (ecriture hors drafts/).
- Pas de sandbox Docker.
- Pas de modele alternatif teste (1 seul modele VERIFIED).
- Pas de parallelisme dans la chaine (sequentiel uniquement).

## Prochaine extension

Ajout de `PATCH_DRAFT` : un 5e task type avec ecriture controlee sur un fichier non sensible hors drafts/.
