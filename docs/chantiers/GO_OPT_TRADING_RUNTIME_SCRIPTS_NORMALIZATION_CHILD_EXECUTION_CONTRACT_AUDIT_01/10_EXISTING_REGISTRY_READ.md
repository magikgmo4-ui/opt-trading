---
doc_id: RUNTIME_SCRIPTS_NORMALIZATION_EXECUTION_CONTRACT_AUDIT_10
doc_type: EXISTING_REGISTRY_READ
repo: opt-trading
project: opt-trading
module: runtime_scripts_normalization
go_id: GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01
status: open
lifecycle_stage: audit_doc_only
topic_keys:
  - opt-trading
  - registry
  - source_of_truth
  - runtime_map
  - code_registry
  - jobs_registry
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-31
links:
  - registry/README.md
  - registry/modules_registry.yaml
  - registry/wrappers_registry.yaml
  - registry/machines_registry.yaml
  - registry/ui_surfaces_registry.yaml
  - registry/meta_index.yaml
  - config/machine_runtime_map.yml
  - docs/registry/CODE_REGISTRY.md
  - docs/registry/JOBS_REGISTRY.md
  - modules/runtime_health/README.md
---

# 10_EXISTING_REGISTRY_READ

## Read scope

Sources lues pour ce child GO :

| Source | Role observe | Autorite dans ce lot |
| --- | --- | --- |
| `registry/README.md` | declare `registry/` comme source de verite versionnee repo | reference de cadrage |
| `registry/modules_registry.yaml` | catalogue canonique des modules fonctionnels | source centrale |
| `registry/wrappers_registry.yaml` | catalogue des wrappers `menu`, `cmd`, `sanity` | source centrale |
| `registry/machines_registry.yaml` | identite machines et hostnames | source centrale identite |
| `registry/ui_surfaces_registry.yaml` | surfaces UI et actions operateur/systeme | source centrale surface |
| `registry/meta_index.yaml` | index des registries centrales | source centrale meta |
| `config/machine_runtime_map.yml` | services, timers, ports, paths, env, forbidden services par machine | projection runtime operationnelle |
| `docs/registry/CODE_REGISTRY.md` | `code_id`, path, role, entrypoint, tests, risk | registre canonique Markdown |
| `docs/registry/JOBS_REGISTRY.md` | `job_id`, workflows, workers, scripts operateurs | registre canonique Markdown |
| `.github/workflows/*.yml` | workflows reels GitHub Actions | realite execution CI |
| `modules/runtime_health/*` | diagnostic runtime, machine map, forbidden services | consumer runtime |

## Source-of-truth model

Le modele existant est deja suffisant pour eviter un second registre concurrent :

```text
registry/*.yaml
  -> sources centrales machine-readable

docs/registry/CODE_REGISTRY.md
docs/registry/JOBS_REGISTRY.md
  -> vues canoniques documentaires code/jobs

config/machine_runtime_map.yml
  -> projection operationnelle runtime consommee par runtime_health

modules/runtime_health/*
  -> verification diagnostic-only du scope runtime courant
```

La future couche `runtime_execution_contracts.yaml` doit seulement relier ces surfaces.

## Registry central readout

| Registry | Count local | Champs structurants observes |
| --- | ---: | --- |
| modules | 49 | `module_name`, `domain`, `machine_target`, `wrappers_expected`, `status`, `priority`, `dependencies` |
| wrappers | 56 | `wrapper_name`, `wrapper_family`, `target_module`, `target_script`, `install_location`, `audience`, `status` |
| machines | 5 | `machine_id`, `hostname`, `role`, `primary_use`, `ui_priority` |
| ui_surfaces | 22 | `surface_name`, `source_module`, `machine_target`, `actions`, `status`, `priority` |
| meta_index | 4 | `registry_name`, `registry_file`, `purpose`, `primary_consumer`, `scope`, `status` |

## Code registry readout

`docs/registry/CODE_REGISTRY.md` couvre deja les familles utiles au contrat execution :

- services FastAPI et entrees production;
- moteurs runtime;
- Trading Lab / Realtime V1;
- Desk Pro / Vision;
- collecteurs;
- OpenClaw / agents;
- validateurs et schemas;
- infra / fleet / sante;
- registry readers;
- GitHub Actions workflows;
- entrees blocked et delete candidates.

Champs utiles pour le futur contrat :

| Champ CODE_REGISTRY | Usage dans execution contract |
| --- | --- |
| `code_id` | liaison stable vers le code |
| `path` | verification entrypoint/path |
| `role` | classification runtime/cli/validator/orchestrator |
| `status` | filtre actif/candidat/experimental |
| `entrypoint` | preuve d'executabilite |
| `tests` | test references |
| `risk` | niveau de risque initial |
| `next_action` | suite de qualification |

## Jobs registry readout

`docs/registry/JOBS_REGISTRY.md` couvre :

- 7 workflows GitHub Actions;
- entry points AI workers;
- job packets;
- scripts Python workers;
- scripts operateurs OpenClaw;
- scripts operateurs racine cles;
- anomalies a traiter.

Champs utiles pour le futur contrat :

| Champ JOBS_REGISTRY | Usage dans execution contract |
| --- | --- |
| `job_id` | liaison vers job ou workflow |
| `path` | verification existence |
| `type` | gha/shell/python/config |
| `trigger` | scheduled/manual/pr/runtime |
| `owner_surface` | domaine proprietaire |
| `inputs` / `outputs` | contrat I/O |
| `status` | filtre actif/candidat |
| `risk` | priorisation validation |

## Runtime health readout

`modules/runtime_health/healthcheck.py` integre deja `MachineMap` :

- `--map` permet de choisir une map runtime;
- `MachineMap.load()` charge `config/machine_runtime_map.yml`;
- `scope_for_current_host()` resout machine/alias;
- `build_config_from_scope()` construit les checks services/timers/venvs/ports/paths/env/logs;
- `check_forbidden_services()` ajoute un bloc de securite;
- `MACHINE_IDENTITY` documente la resolution machine.

Le contrat execution futur doit donc rester compatible avec l'approche diagnostic-only existante.

## Authority decision

Decision de ce GO :

```text
registry/machines_registry.yaml = identite machine canonique
config/machine_runtime_map.yml = projection runtime operationnelle
runtime_execution_contracts.yaml = pont execution entre registries, code, jobs, wrappers et runtime health
```

Cette decision interdit de corriger les divergences par renommage opportuniste dans ce lot.
