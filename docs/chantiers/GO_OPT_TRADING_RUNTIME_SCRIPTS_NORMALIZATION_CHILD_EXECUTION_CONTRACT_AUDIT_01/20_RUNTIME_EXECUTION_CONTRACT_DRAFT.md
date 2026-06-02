---
doc_id: RUNTIME_SCRIPTS_NORMALIZATION_EXECUTION_CONTRACT_AUDIT_20
doc_type: RUNTIME_EXECUTION_CONTRACT_DRAFT
repo: opt-trading
project: opt-trading
module: runtime_scripts_normalization
go_id: GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01
status: open
lifecycle_stage: audit_doc_only
topic_keys:
  - opt-trading
  - runtime_execution_contract
  - validator_draft
  - registry
  - ci
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-31
links:
  - registry/modules_registry.yaml
  - registry/wrappers_registry.yaml
  - registry/machines_registry.yaml
  - config/machine_runtime_map.yml
  - docs/registry/CODE_REGISTRY.md
  - docs/registry/JOBS_REGISTRY.md
---

# 20_RUNTIME_EXECUTION_CONTRACT_DRAFT

## Decision

Ajouter plus tard une source machine-readable :

```text
registry/runtime_execution_contracts.yaml
```

Elle ne doit pas etre creee dans ce lot doc-only. Ce document fige seulement le draft.

## Role du contrat

Le contrat execution relie des objets deja existants :

```text
module_name  -> registry/modules_registry.yaml
code_id      -> docs/registry/CODE_REGISTRY.md
job_id       -> docs/registry/JOBS_REGISTRY.md
wrapper_ids  -> registry/wrappers_registry.yaml
machine      -> registry/machines_registry.yaml + config/machine_runtime_map.yml
healthcheck  -> modules/runtime_health/*
```

Il doit repondre a une question operationnelle simple :

```text
Ce module/job/script est-il operable, sur quelle machine, via quel wrapper, avec quels effets, quels tests et quelle garde runtime ?
```

## Schema draft

```yaml
schema_version: "0.1.0"
contracts:
  - contract_id: desk_pro_runner_runtime
    module_name: desk_pro_runner
    code_id: desk_pro_runner
    job_id: null
    wrapper_ids:
      - cmd-desk_pro_runner
    machine_target: admin_trading
    runtime_map_key: admin-trading
    execution_mode: on_demand
    entrypoint: modules/desk_pro_runner/app/desk_pro_runner.py
    command: cmd-desk_pro_runner run

    inputs:
      - desk_snapshot
      - visual_context
      - market_metrics

    outputs:
      - desk_snapshot.v1
      - visual_context.v1
      - runtime_log

    side_effects:
      - writes_artifacts
      - no_live_trade

    healthcheck:
      type: runtime_health
      required: true
      blocks:
        - MACHINE_IDENTITY
        - FORBIDDEN_SERVICES

    tests:
      - tests/test_desk_pro_health_classification.py

    risk: medium
    status: active
```

## Required root fields

| Field | Required | Source / validation |
| --- | --- | --- |
| `schema_version` | yes | explicit string |
| `contracts` | yes | non-empty list |

## Required contract fields

| Field | Required | Rule |
| --- | --- | --- |
| `contract_id` | yes | unique, stable, snake_case |
| `module_name` | yes | must exist in `registry/modules_registry.yaml` unless status is `external` |
| `code_id` | yes or null | should exist in `CODE_REGISTRY.md` when executable code is identified |
| `job_id` | yes or null | should exist in `JOBS_REGISTRY.md` when a job/workflow drives execution |
| `wrapper_ids` | yes | every wrapper must exist in `registry/wrappers_registry.yaml` or be explicitly marked missing in audit |
| `machine_target` | yes | canonical `machine_id` from `registry/machines_registry.yaml` |
| `runtime_map_key` | yes or null | key from `config/machine_runtime_map.yml` or documented alias |
| `execution_mode` | yes | allowed values below |
| `entrypoint` | yes or null | repo-relative path, must exist when not null |
| `command` | yes or null | operator command or workflow command |
| `inputs` | yes | list, empty allowed only with justification |
| `outputs` | yes | list, empty allowed only with justification |
| `side_effects` | yes | list from controlled vocabulary |
| `healthcheck` | yes | required object |
| `tests` | yes | list of repo-relative tests or empty with reason |
| `risk` | yes | `low`, `medium`, `high`, `critical` |
| `status` | yes | `active`, `candidate`, `experimental`, `legacy`, `blocked`, `deprecated` |

## Controlled values draft

`execution_mode`:

- `on_demand`
- `scheduled`
- `service`
- `timer`
- `ci`
- `worker`
- `library`
- `diagnostic_only`

`side_effects`:

- `read_only`
- `writes_artifacts`
- `writes_logs`
- `writes_registry`
- `writes_runtime_state`
- `network_call`
- `external_api`
- `requires_secret`
- `no_live_trade`
- `live_trade_possible`
- `service_start_stop`

`healthcheck.type`:

- `none`
- `runtime_health`
- `ci`
- `custom`

## Machine identity draft

Le contrat doit separer trois noms :

| Nom | Exemple | Role |
| --- | --- | --- |
| `machine_target` | `admin_trading` | identite canonique registry |
| `hostname` | `admin-trading` | hostname ou nom systeme |
| `runtime_map_key` | `admin-trading` | cle operationnelle dans `machine_runtime_map.yml` |

Un futur champ `machine_aliases` peut etre ajoute dans `registry/machines_registry.yaml`, mais pas dans ce lot.

## Validator draft

Futur fichier propose :

```text
scripts/validate_runtime_execution_contracts.py
```

Checks minimaux :

1. charger `registry/runtime_execution_contracts.yaml`;
2. charger les index sources : modules, wrappers, machines, runtime map, code registry, jobs registry;
3. verifier l'unicite de `contract_id`;
4. verifier que `module_name` existe ou est explicitement `external`;
5. verifier que `wrapper_ids` existent;
6. verifier que `machine_target` existe;
7. verifier que `runtime_map_key` existe ou est resolu par alias documente;
8. verifier que `entrypoint` existe si non null;
9. verifier que chaque test reference existe si non null;
10. verifier valeurs autorisees de `risk`, `status`, `execution_mode`;
11. refuser tout chemin absolu non autorise, sauf ceux provenant explicitement de `machine_runtime_map.yml`;
12. scanner les champs string pour patterns de secrets evidents;
13. produire un rapport fail-closed lisible par CI.

## CI binding draft

Futur branchement :

```text
.github/workflows/gh-actions-registry-validation.yml
```

Ajouts attendus :

- inclure `registry/runtime_execution_contracts.yaml` dans les `paths`;
- inclure `scripts/validate_runtime_execution_contracts.py` dans les `paths`;
- lancer le validateur apres `validate_gh_actions_registries.py`;
- garder `permissions: contents: read`;
- aucune variable secrete requise.

## Derived Markdown draft

Futur fichier :

```text
docs/registry/RUNTIME_EXECUTION_CONTRACTS.md
```

Regle : ce Markdown doit etre une vue derivee et lisible, pas la source principale.

La source principale doit rester :

```text
registry/runtime_execution_contracts.yaml
```
