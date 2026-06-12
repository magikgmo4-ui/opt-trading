---
doc_id: RUNTIME_EXECUTION_CONTRACTS_REGISTRY_V1
doc_type: runtime_execution_contracts_registry_view
repo: opt-trading
project: opt-trading
module: runtime_execution_contracts
status: open
version: v1
updated_at: 2026-06-02
source_kind: derived_view
source_of_truth:
  - registry/runtime_execution_contracts.yaml
links:
  - registry/modules_registry.yaml
  - registry/wrappers_registry.yaml
  - registry/machines_registry.yaml
  - config/machine_runtime_map.yml
  - docs/registry/CODE_REGISTRY.md
  - docs/registry/JOBS_REGISTRY.md
---

# RUNTIME_EXECUTION_CONTRACTS — v1 (vue dérivée)

**Source de vérité** : `registry/runtime_execution_contracts.yaml`

## Contrats enregistrés

| contract_id | module_name | machine_target | runtime_map_key | wrapper_ids | execution_mode | risk | status |
|---|---|---|---|---|---|---|---|
| `desk_pro_runner_runtime` | `desk_pro_runner` | `admin_trading` | `admin-trading` | `cmd-desk_pro_runner` | `on_demand` | `medium` | `active` |
