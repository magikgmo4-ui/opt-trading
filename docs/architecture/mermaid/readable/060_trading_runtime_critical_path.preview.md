# Readable View - Trading Runtime Critical Path

Source canonique :

```text
docs/architecture/mermaid/990_architecture_final.mmd
```

Scope : chemin runtime trading critique de l'alerte jusqu'a la persistence et aux surfaces perf.

```mermaid
flowchart LR
  ext_tradingview["TradingView alert"]

  subgraph ingress_and_guards["Ingress and guards"]
    webhook_server_py["webhook_server.py"]
    modules_auth_webhook_key_py["modules/auth/webhook_key.py"]
    modules_webhook_paper_guards["modules/webhook/paper_guards"]
    modules_risk_calculator["modules/risk_engine/app/risk_calculator.py"]
    modules_risk_engine["modules/risk_engine/app/risk_engine.py"]
  end

  subgraph decision_and_execution["Decision and execution"]
    modules_strategy_logic["modules/decision_engine/app/strategy_logic.py"]
    modules_execution_engine["modules/execution_engine/"]
    modules_trade_executor["modules/trade_executor/app/executor.py"]
    adapters_webhook_to_perf_py["adapters/webhook_to_perf.py"]
  end

  subgraph persistence_and_perf["Persistence and perf"]
    state_root_dir["state/"]
    perf_perf_app_py["perf/perf_app.py"]
    perf_db_sqlite["perf/perf.db WAL probable"]
    registry_cockpit_static_index["registry/cockpit/automation/index.html"]
  end

  ext_tradingview --> webhook_server_py
  webhook_server_py -->|imports| modules_auth_webhook_key_py
  webhook_server_py -->|imports| modules_webhook_paper_guards
  webhook_server_py -->|risk gate| modules_risk_calculator
  modules_risk_calculator -->|imported by| modules_risk_engine
  modules_strategy_logic -.->|signal and rule logic visible| modules_risk_calculator
  webhook_server_py -->|execution path| modules_execution_engine
  modules_trade_executor -->|execution implementation| modules_execution_engine
  webhook_server_py -->|bridge funcs probable| adapters_webhook_to_perf_py
  webhook_server_py -->|writes events probable| state_root_dir
  adapters_webhook_to_perf_py -.->|cross-service adapter probable| perf_perf_app_py
  perf_perf_app_py -->|persists probable| perf_db_sqlite
  perf_perf_app_py -->|mounts desk and perf UI probable| registry_cockpit_static_index
```
