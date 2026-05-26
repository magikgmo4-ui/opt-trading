# Readable View - Quality Contracts Docs

Source canonique :

```text
docs/architecture/mermaid/990_architecture_final.mmd
```

Scope : evidence, documentation, tests, contracts et sorties de support.

```mermaid
flowchart LR
  subgraph documentation_and_evidence["Documentation and evidence"]
    docs_architecture_evidence["docs/architecture/evidence/"]
    docs_architecture_mermaid["docs/architecture/mermaid/"]
    docs_chantiers["docs/chantiers/"]
  end

  subgraph quality_surfaces["Quality surfaces"]
    tests_root["tests/"]
    module_tests["modules/*/tests/"]
    scripts_ai_tests["scripts/ai/tests/"]
    contracts_marketdata["contracts/schemas_marketdata/v1/"]
    schemas_webhook_event_v1_json["schemas/webhook_event_v1.json"]
  end

  subgraph support_outputs["Support and output surfaces"]
    reports_dir["reports/"]
    bundles_dir["bundles/"]
    archive_dir["_archive/"]
    tmp_dir["tmp/ UNKNOWN usage boundary"]
    notes_open_questions["08_notes_open_questions.md TODO"]
    bot_vision_package_json["modules/bot_vision/headless_capture/package.json"]
  end

  webhook_server_py["webhook_server.py"]
  perf_perf_app_py["perf/perf_app.py"]
  modules_data_center["modules/data_center/"]
  modules_proposition_engine["modules/proposition_engine/app/engine.py"]
  modules_trade_executor["modules/trade_executor/app/executor.py"]
  scripts_ai_workers["scripts/ai/workers/"]
  ext_hf_spaces_runtime["Hugging Face Spaces runtime probable"]

  docs_architecture_evidence -->|source of truth for map| docs_architecture_mermaid
  docs_chantiers -->|tracks chantier decisions| docs_architecture_mermaid

  tests_root -.->|repo-wide validation| webhook_server_py
  tests_root -.->|repo-wide validation| perf_perf_app_py
  module_tests -.->|module validation| modules_data_center
  module_tests -.->|module validation| modules_proposition_engine
  module_tests -.->|module validation| modules_trade_executor
  scripts_ai_tests -.->|worker contract validation| scripts_ai_workers
  contracts_marketdata -.->|market data contract probable| modules_data_center
  schemas_webhook_event_v1_json -.->|webhook contract| webhook_server_py

  reports_dir -.->|outputs and diagnostics probable| scripts_ai_workers
  bundles_dir -.->|packaged outputs probable| docs_architecture_mermaid
  archive_dir -.->|historical surfaces visible only| docs_architecture_mermaid
  tmp_dir -.->|unknown support boundary| docs_architecture_mermaid
  notes_open_questions -.->|remaining unknowns| docs_architecture_mermaid
  bot_vision_package_json -.->|node runtime dependency evidence| ext_hf_spaces_runtime
```
