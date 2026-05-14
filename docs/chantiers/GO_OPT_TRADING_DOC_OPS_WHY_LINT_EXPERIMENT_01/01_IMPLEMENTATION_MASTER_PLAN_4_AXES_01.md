---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01_MASTER_PLAN
doc_type: chantier_master_plan
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: opening
topic_keys:
  - why_lint
  - master_plan
  - governance
  - runtime_security
  - why_runtime_graph
  - openclaw_central
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_CONSOLIDATION_MAP_01.md
---

# 01_IMPLEMENTATION_MASTER_PLAN_4_AXES_01

## Plan documentaire complet

Ce plan couvre les 4 axes documentaires de controle + la cible produit OpenClaw central.

### Axe 1 — Gouvernance

- **Etat existant** : MATRICE_DOC_OPS_MASTER_MATRIX_01.md est le canon maitre souverain. Les regles stables, le nommage, le frontmatter, l'indexation, les branches, la continuite produit sont fixes.
- **Sources deja validees** : `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, `MATRICE_GOUVERNANTE_V2.md`, `MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`, `PRODUCT_CONTINUITY_HIERARCHY_01.md`, `REPO_ROLE.md`, `REPO_ROOT_POLICY.md`, `GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`, `SESSION_DOCUMENTATION_GATE.md`, `DOC_LAYERS.md`, `REPO_SURFACES_MAP.md`.
- **Gaps restants** : alignement/deduplication/reclassement des surfaces proches (reporte au lot suivant de la matrice maitre).
- **Action de ce chantier** : referencer, ne pas reecrire.

### Axe 2 — Runtime Security

- **Etat existant** : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01` est ouvert avec SPEC parent, child permission matrix, child policy schema. Le modele L0-L8 est defini.
- **Sources deja validees** : `SPEC_RUNTIME_SECURITY_PARENT_01.md`, `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md`, `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01.md`.
- **Gaps restants** : skill registry futur, integration Telegram/Gateway/tmux, tests de non-destruction, integration avec modules existants.
- **Action de ce chantier** : referencer, ne pas reecrire.

### Axe 3 — WHY / WHY-runtime graph

- **Etat existant** : `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_VIEW_REAL_01` est ouvert avec 15 fichiers de cadrage. Le scope local view, inputs, outputs, overlays, gates, architecture synthesis sont definis.
- **Sources deja validees** : `00_INITIAL_PROJECT_DOC.md`, `10_LOCAL_VIEW_SCOPE.md`, `20_LOCAL_VIEW_INPUTS.md`, `30_LOCAL_EXECUTION_CONSTRAINTS.md`, `40_LOCAL_VIEW_OUTPUTS.md`, `50_LOCAL_VIEW_OVERLAYS.md`, `60_LOCAL_VIEW_MULTI_MACHINE_CONTEXT.md`, `70_LOCAL_VIEW_OBSERVABILITY_ALIGNMENT.md`, `80_LOCAL_VIEW_HUMAN_REVIEW_GATES.md`, `90_LOCAL_VIEW_RENDER_PIPELINE.md`, `100_LOCAL_VIEW_JSON_EXPORT_ALIGNMENT.md`, `110_LOCAL_VIEW_GOVERNANCE_SNAPSHOTS.md`, `120_LOCAL_VIEW_IMPLEMENTATION_GATES.md`, `130_LOCAL_VIEW_ARCHITECTURE_SYNTHESIS.md`, `140_CLOSEOUT.md`.
- **Gaps restants** : premier render graph local reel non encore execute.
- **Action de ce chantier** : referencer, ne pas reecrire.

### Axe 4 — WHY lint (present chantier)

- **Etat existant** : nouveau chantier parent, ouverture doc-only.
- **Sources deja validees** : aucun fichier de WHY lint n'existe encore. Ce chantier est la premiere pose.
- **Gaps restants** : tout le modele de warnings, la matrice de non-duplication, le graphe de dependances, les bindings de gates, le roadmap d'implementation.
- **Action de ce chantier** : ecrire maintenant comme consolidation warning-only.

### Axe 5 — OpenClaw central (cible produit)

- **Etat existant** : references eparses dans les chantiers (runtime security, db-layer orchestrator, infra baseline, policy YAML draft).
- **Sources existantes** : `GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01/` (dossier vide), `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` (branche db-layer), `GO_OPENCLAW_INFRA_BASELINE_01` (branche db-layer).
- **Gaps restants** : pas encore de SPEC canonique unifiee OpenClaw central pour opt-trading.
- **Action de ce chantier** : stabiliser ensuite comme cible produit, sans autorisation runtime.

### Ordre d'implementation documentaire

1. Gouvernance : referencer, ne pas reecrire.
2. WHY : referencer, ne pas reecrire.
3. WHY lint : ecrire maintenant comme consolidation warning-only.
4. OpenClaw central : stabiliser ensuite comme cible produit.

### Futures phases separees

- Le WHY lint restera un chantier separe, potentiellement sous-GO du parent `GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`.
- L'implementation eventuelle d'un linter statique (Python/Rust) serait un child GO futur, toujours doc-only en phase de specification.
- L'integration CI (can_fail_ci: false) est explicitement exclue du scope WHY lint.
