# Readable View - Interfaces And Entrypoints

Source canonique :

```text
docs/architecture/mermaid/990_architecture_final.mmd
```

Scope : HTTP, CLI et surfaces statiques. Fichiers generes exclus visuellement.

```mermaid
flowchart LR
  subgraph http_surfaces["HTTP and static surfaces"]
    webhook_server_py["webhook_server.py"]
    perf_perf_app_py["perf/perf_app.py"]
    modules_localcms_main["modules/localcms/app/main.py"]
    modules_signal_router_server["modules/signal_router/app/server.py"]
    modules_signal_router_route["modules/signal_router/app/router.py route(raw)"]
    modules_memory_bricks_api_v2["modules/memory_bricks/app/api_v2_server.py"]
    modules_hf_mcp_public_app["modules/hf_free_platform/spaces/mcp_public/app.py"]
    modules_hf_tools_private_app["modules/hf_free_platform/spaces/tools_private/app.py"]
    modules_hf_portal_static_index["modules/hf_free_platform/spaces/portal_static/index.html"]
    registry_cockpit_static_index["registry/cockpit/automation/index.html"]
    modules_perf_app_candidate["modules/perf/app.py UNKNOWN candidate"]
  end

  subgraph cli_surfaces["CLI surfaces"]
    cli_collector_binance_spot["modules/collector_binance_spot/src/collector_binance_spot/cli.py"]
    cli_collector_coingecko["modules/collector_coingecko/src/collector_coingecko/cli.py"]
    cli_governance_validator["modules/governance/openclaw_mcp_policy_validator/cli.py"]
    cli_governance_validator_main["modules/governance/openclaw_mcp_policy_validator/__main__.py"]
    cli_kil_v1["modules/kil_v1/src/kil_v1/cli.py"]
    cli_memory_bricks_v1["modules/memory_bricks/src/memory_bricks_v1/cli.py"]
    cli_naming_normalizer["modules/naming_normalizer/app/cli.py"]
    cli_proposition_engine_main["modules/proposition_engine/app/__main__.py"]
    cli_signal_router_main["modules/signal_router/app/__main__.py"]
    cli_notification_dispatcher_main["modules/notification_dispatcher/app/__main__.py"]
    cli_openclaw_operator_bridge_main["modules/openclaw_operator_bridge/app/__main__.py"]
  end

  perf_perf_app_py -->|mounts desk and perf UI probable| registry_cockpit_static_index
  modules_localcms_main -->|local ops cockpit| registry_cockpit_static_index
  modules_signal_router_server -->|imports route| modules_signal_router_route
  cli_signal_router_main -->|imports run| modules_signal_router_server
  cli_proposition_engine_main -->|cli entrypoint| modules_signal_router_route
  modules_hf_portal_static_index -.->|static entrypoint visible only| modules_hf_mcp_public_app
  modules_hf_tools_private_app -.->|spaces runtime probable| modules_hf_mcp_public_app
  modules_perf_app_candidate -.->|entrypoint candidate UNKNOWN| perf_perf_app_py

  cli_governance_validator_main -->|python module entrypoint| cli_governance_validator
  cli_memory_bricks_v1 -.->|CLI family visible in tree| modules_memory_bricks_api_v2
  cli_kil_v1 -.->|standalone cli visible in tree| cli_notification_dispatcher_main
  cli_naming_normalizer -.->|standalone cli visible in tree| cli_openclaw_operator_bridge_main
```
