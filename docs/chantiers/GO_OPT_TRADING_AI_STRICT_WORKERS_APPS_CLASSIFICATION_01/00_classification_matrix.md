# Matrice de Classification des GOs : Architecture AI / Strict Workers / Apps

**Objectif:** Découper et classer proprement les surfaces de travail pour permettre une reprise organisée sans interférence avec les PRs déjà mergées.

---

**Proposition de Matrice de Classification des GOs:**

**1. GO_STRICT_WORKERS_ORCHESTRATION_ET_DEPLOIEMENT**
    *   **Description:** Mise en place et gestion de l'infrastructure fondamentale pour le fonctionnement des workers stricts, incluant l'orchestration via `systemd` et `fleet`, ainsi que le mapping des runtimes machines.
    *   **Blocs Candidats:**
        *   `.github/workflows/strict-workers-smoke.yml` (tests de fumée)
        *   `.github/workflows/strict-workers-validate.yml` (validation CI)
        *   `deploy/systemd/*` (services, timers, et fichiers d'override pour `fantome`, `student`)
        *   `config/machine_runtime_map.yml` (mapping runtime/machines)
        *   Modules spécifiques avec `systemd` (ex: `modules/bot_vision/headless_capture/systemd/*`, `modules/desk_pro/systemd/*`)

**2. GO_STRICT_WORKERS_PLANIFICATION_ET_GESTION_DES_TACHES**
    *   **Description:** Définition et optimisation des mécanismes de CI/CD et de planification pour les workers stricts, incluant la gestion et la promotion des paquets de tâches (`job packets`).
    *   **Blocs Candidats:**
        *   `.github/workflows/strict-workers-schedule.yml` (gestion du cron hebdomadaire)
        *   PRs récentes liées à la planification et aux paquets de tâches (ex: PR #612, #608, #606)

**3. GO_STRATEGIE_FRAMEWORK_ET_REGISTRE_CENTRAL**
    *   **Description:** Développement et validation du framework central de stratégie, y compris le registre des stratégies, les adaptateurs et les outils de validation.
    *   **Blocs Candidats:**
        *   `modules/strategy/*` (adapter, `__init__.py`, `README.md`, registry, types)
        *   `tools/strategy/validate_strategy_registry.py` (validation du registre des stratégies)
        *   PRs récentes liées aux nouvelles stratégies (ex: PR #616, #615)

**4. GO_INTEGRATIONS_EXTERNES_AIRTABLE_BRIDGE**
    *   **Description:** Conception, implémentation et maintenance du pont d'intégration avec Airtable, en se concentrant sur la fiabilité des flux de données avec des mécanismes `fail-open`/`write-gated`.
    *   **Blocs Candidats:**
        *   `modules/airtable_bridge/*` (client, payloads, scripts, fichiers de configuration comme `.env.example`, `README.md`)

**5. GO_OPENCLAW_GOUVERNANCE_ET_MOTEUR_DE_POLITIQUES**
    *   **Description:** Définition, implémentation et gestion des politiques de sécurité et d'exécution pour OpenClaw, incluant les schémas de politiques et les validateurs statiques.
    *   **Blocs Candidats:**
        *   Tous les documents de chantier sous `docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_*` (ex: `SCHEMA`, `STATIC_VALIDATOR`, `YAML_DRAFT`)
        *   `modules/model_provider_openclaw/docs/GO_OPENCLAW_POLICY_RUNTIME_ALIGNMENT_05.md`
        *   `modules/model_provider_openclaw/docs/GO_OPENCLAW_PROVIDER_POLICY_04.md`

**6. GO_OPENCLAW_COEUR_DBLAYER_ET_OPERATIONS_RUNTIME**
    *   **Description:** Implémentation directe du cœur d'OpenClaw et ses interactions avec la couche d'accès aux données (DBLayer) et les processus d'exécution runtime.
    *   **Blocs Candidats:**
        *   Documents de chantier sous `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/*`
        *   Documents de chantier sous `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_*`
        *   Documents de chantier sous `docs/chantiers/GO_OPT_TRADING_CHILD_DBLAYER_ORCHESTRATOR_*`
        *   `modules/evidence_openclaw/docs/*`, `modules/menu_openclaw/docs/*`, `modules/model_provider_openclaw/docs/GO_OPENCLAW_ALIGNMENT_*`
        *   Documents de chantier sous `docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_*`

**7. GO_ARCHITECTURES_AI_ET_INTEGRATION_APPLICATIVE**
    *   **Description:** Conception de l'architecture générale AI et intégration des workers stricts dans les applications, y compris l'orchestration des modèles et les interactions avec des plateformes externes (ex: Ollama, Botpress).
    *   **Blocs Candidats:**
        *   Documents de chantier sous `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_*`
        *   Documents de chantier sous `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_CLI_LOCAL_DRYRUN_INVOCATION_01/*`
        *   `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_STRICT_WORKERS_APPS_AUTOMATION_MATRIX_01/40_OPENCLAW_AUTOMATION_PLAN.md`
        *   `modules/decision_engine/app/strategy_logic.py`
        *   Documents de chantier sous `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_*` (intégration Ollama)
        *   Documents de chantier sous `docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_*` (intégration Botpress)
