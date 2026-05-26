# Readable View - Ops Governance

Source canonique :

```text
docs/architecture/mermaid/990_architecture_final.mmd
```

Scope : orchestration, governance, registries, workers et control plane OpenClaw.

```mermaid
flowchart LR
  subgraph workers_and_checks["Workers and checks"]
    scripts_verify_all_sh["scripts/verify_all.sh"]
    scripts_ai_workers["scripts/ai/workers/"]
    scripts_tmux["scripts/tmux/"]
    github_workflows[".github/workflows/"]
    modules_runtime_health["modules/runtime_health/"]
    modules_validation_gate["modules/validation_gate/app/"]
    deploy_systemd["deploy/systemd/"]
  end

  subgraph openclaw_control_plane["OpenClaw control plane"]
    modules_gateway_openclaw_scripts["modules/gateway_openclaw/scripts/"]
    modules_openclaw_config_modulaire["modules/openclaw_config_modulaire/app/"]
    modules_openclaw_operator_bridge["modules/openclaw_operator_bridge/app/bridge.py + client.py + schema.py"]
    modules_model_provider_openclaw_config["modules/model_provider_openclaw/config/"]
  end

  subgraph registries_and_policy["Registries and policy"]
    config_machine_runtime_map_yml["config/machine_runtime_map.yml"]
    configs_openclaw_skill_policy_yaml["configs/openclaw/security/skill_policy.yaml"]
    registry_machines_yaml["registry/machines_registry.yaml"]
    registry_meta_index_yaml["registry/meta_index.yaml"]
    registry_modules_yaml["registry/modules_registry.yaml"]
    registry_ui_surfaces_yaml["registry/ui_surfaces_registry.yaml"]
    registry_wrappers_yaml["registry/wrappers_registry.yaml"]
  end

  ext_openclaw_gateway["OpenClaw gateway probable"]

  github_workflows -.->|validation and scheduled workers probable| scripts_ai_workers
  github_workflows -.->|policy validation probable| configs_openclaw_skill_policy_yaml
  scripts_ai_workers -->|job runtime| modules_validation_gate
  scripts_tmux -.->|health and mobile smoke probable| modules_runtime_health
  deploy_systemd -.->|schedules runtime health probable| modules_runtime_health
  modules_runtime_health -.->|configured by| config_machine_runtime_map_yml
  scripts_verify_all_sh -.->|verification boundary| modules_runtime_health

  config_machine_runtime_map_yml --> registry_machines_yaml
  registry_modules_yaml -->|registry inputs| modules_openclaw_config_modulaire
  registry_meta_index_yaml -->|registry inputs| modules_openclaw_config_modulaire
  registry_ui_surfaces_yaml -->|registry inputs| modules_openclaw_config_modulaire
  registry_wrappers_yaml -->|registry inputs| modules_openclaw_config_modulaire

  modules_model_provider_openclaw_config -.->|model routing probable| modules_openclaw_operator_bridge
  modules_gateway_openclaw_scripts -.->|gateway control| ext_openclaw_gateway
  modules_openclaw_operator_bridge -.->|gateway call probable| ext_openclaw_gateway
```
