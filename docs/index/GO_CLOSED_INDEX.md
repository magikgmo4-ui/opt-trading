---
doc_id: OPT_TRADING_GO_CLOSED_INDEX
doc_type: reprise
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - go_closed_index
  - continuity
  - governance
surface: continuity
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/index/GO_INDEX.md
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
---

# GO_CLOSED_INDEX — opt-trading

## Objet

Ce document référence les chantiers clos/pass sortis de `docs/index/GO_INDEX.md`.

---

## Règles

- l’index référence et synthétise les chantiers `CLOSED`/`PASS`
- il ne remplace ni le dossier chantier ni le closeout
- lorsqu’un chantier passe en `CLOSED`/`PASS`, sa ligne canonique doit être retirée de `docs/index/GO_INDEX.md` et déplacée ici
- les entrées `REFERENCE` ne sont pas reclassées automatiquement comme `CLOSED`/`PASS`
- les liens doivent pointer vers les artefacts détaillés dès qu’ils existent

---

## Tableau canonique des chantiers clos/pass

Normalisation retenue :

- `PARENT = CHANTIER` si aucun parent explicite n'est prouvé dans le repo
- `SOUS_CHANTIER = —` si aucun sous-chantier explicite n'est prouvé dans le repo
- `STATUT` est normalisé en `OPEN`, `ACTIVE`, `CLOSED`, `REFERENCE`
- `DOSSIER_PRESENT` indique la présence d'un dossier direct sous `docs/chantiers/`

| PARENT | CHANTIER | SOUS_CHANTIER | STATUT | DOSSIER_PRESENT | SOURCE |
| --- | --- | --- | --- | --- | --- |
| GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01 | GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/90_closeout.md`<br>`docs/governance/MATRICE_GOUVERNANTE_V2.md` |
| GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01 | GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01/00_cadrage.md` |
| GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01 | GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01/90_closeout.md` |
| GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01 | GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md` |
| GO_UNIFORM_CONTINUITY_HARDENING_01 | GO_UNIFORM_CONTINUITY_HARDENING_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00B_parent_scope_and_structure.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/90_closeout.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01 | CLOSED | non | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/01_branch_trunk_cross_audit.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | GO_OPT_TRADING_MODULE_FAMILY_CONSOLIDATION_AUDIT_01 | CLOSED | non | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_module_family_consolidation_audit.md` |
| github_park_inventory_audit_consolidation | GO_GITHUB_PARK_AUDIT_EXPANSION_01 | GO_GITHUB_PARK_FILE_ROLE_CARTOGRAPHY_01 | CLOSED | non | `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/00_cadrage.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_file_role_cartography.md` |
| GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01 | GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01 | — | CLOSED | non | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_journal_technique.md`<br>`docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_decisions.md` |
| GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01 | GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/00_cadrage.md`<br>`docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/90_closeout.md` |
| GO_INTEG_TRADING_DUAL_STACK_DOC_ONLY_INTEGRATION_01 | GO_INTEG_TRADING_DUAL_STACK_DOC_ONLY_INTEGRATION_01 | — | CLOSED | non | `docs/index/GO_INDEX.md`<br>`docs/trading/02_ETABLI_TRADING_DUAL_STACK_V1_0.txt`<br>`docs/trading/03_KANBAN_TRADING_DUAL_STACK_V1_0.txt`<br>`docs/trading/04_REPRISE_TRADING_DUAL_STACK_V1_0.txt`<br>`docs/trading/TRADING_DUAL_STACK_V1_0_CLARIFIED.md` |
| GO_RANGE_STRATEGY_V1_STRUCT_01 | GO_RANGE_STRATEGY_V1_STRUCT_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_RANGE_STRATEGY_V1_STRUCT_01/90_closeout.md` |
| GO_STRATEGY_KERNEL_SHARED_LAYER_01 | GO_STRATEGY_KERNEL_SHARED_LAYER_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_STRATEGY_KERNEL_SHARED_LAYER_01/90_closeout.md` |
| UNIFORM_CONTINUITY_HARDENING | GO_UNIFORM_CONTINUITY_HARDENING_02 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md` |
| GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01 | GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/00_cadrage.md`<br>`docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/90_closeout.md` |
| UNIFORM_CONTINUITY_HARDENING | GO_UNIFORM_CONTINUITY_HARDENING_02 | GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01 | CLOSED | oui | `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md`<br>`docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/90_closeout.md` |
| GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02 | GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02 | — | CLOSED | oui | `docs/index/GO_INDEX.md`<br>`docs/chantiers/GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02/00_cadrage.md` |
| GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS | GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS | — | CLOSED | oui | `docs/chantiers/GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS/00_cadrage.md`<br>`docs/chantiers/GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS/90_closeout.md` |
| GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01 | GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/90_closeout.md` |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01/02_go_map.md`<br>`docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01/90_closeout.md` |
| GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01 | GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/90_closeout.md` |
| GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/10_closeout.md`<br>`docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md` |
| GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md`<br>`registry/README.md` |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/03_decisions.md`<br>`docs/ot/trae/trae_pack_texts/README.md` |
| GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/90_closeout.md`<br>`docs/index/GO_INDEX.md` |
| GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/90_closeout.md`<br>`docs/architecture/REPO_SURFACES_MAP.md` |
| GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/03_decisions.md`<br>`docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/90_closeout.md`<br>`docs/governance/REPO_ROOT_POLICY.md` |
| GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md`<br>`docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/90_closeout.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01/90_closeout.md`<br>`modules/naming_normalizer/README.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/00_cadrage.md`<br>`docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/90_closeout.md`<br>`modules/naming_normalizer/output/naming_audit_report.md` |
| GO_OPT_TRADING_PARENT_NAMING_CANON_01 | GO_OPT_TRADING_PARENT_NAMING_CANON_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/90_closeout.md`<br>`docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_CLOSEOUT_01/90_closeout.md` |
| GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md`<br>`docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/90_closeout.md`<br>`docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_CLOSEOUT_01/90_closeout.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01/00_INITIAL_PROJECT_DOC.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01/01_TMUX_OPERATOR_PROTOCOL.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01/RUNTIME_LOG.md`<br>`docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md` |
| GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_PROMPT_01 | GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/00_GO_OPEN.md`<br>`docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/90_CLOSEOUT.md`<br>`docs/index/inbox/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01.md` |
| GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01 | GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md`<br>`docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_PARENT_CHECKPOINT.md` |
| GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01 | GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_REVIEW_REALIGN_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_REVIEW_REALIGN_01/00_REALIGN_PLAN.md` |
| GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01 | GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01/CHECKPOINT.md` |
| GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01 | GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01/CHECKPOINT.md` |
| GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_FIRST_CONTROLLED_CONSUMER_01 | GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_FIRST_CONTROLLED_CONSUMER_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_FIRST_CONTROLLED_CONSUMER_01/CHECKPOINT.md` |
| GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01 | GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01/CHECKPOINT.md` |
| GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01 | GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01/CHECKPOINT.md` |
| GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01 | GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01/CHECKPOINT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_RUNTIME_SYNC_AFTER_PAPER_GUARDS_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_RUNTIME_SYNC_AFTER_PAPER_GUARDS_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PAPER_POSITION_CLOSE_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_POSITION_CLOSE_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_CYCLE_CLOSEOUT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_CYCLE_CLOSEOUT_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PAPER_VALIDATION_GLOBAL_CLOSEOUT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_VALIDATION_GLOBAL_CLOSEOUT_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_READINESS_CONDITIONS_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_READINESS_CONDITIONS_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_IMPL_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_IMPL_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_AND_SECRETS_AUDIT_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_AND_SECRETS_AUDIT_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01 | GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_PNL_ALERT_THRESHOLDS_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_PNL_ALERT_THRESHOLDS_01/90_CLOSEOUT.md` |
| GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01 | GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01/CLOSE_GATE.md`<br>`docs/index/GO_INDEX.md`<br>`docs/index/GO_CLOSED_INDEX.md` |
| GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01 | GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_ENRICH_01 | — | CLOSED | oui | `docs/chantiers/GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_ENRICH_01/90_CLOSEOUT.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01 | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01/20_ACCEPTANCE_REVIEW.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01 | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_DRY_RUN_LOCALCMS_GATE_01/00_INITIAL_PROJECT_DOC.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01 | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_REQUIREMENTS_REQUESTS_FIX_01/90_REPRISE_POINT.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01 | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_LIVE_DRY_RUN_POST_GATE_01/90_REPRISE_POINT.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01 | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_REPORT_BUNDLE_01/90_REPRISE_POINT.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01 | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_PARENT_FINAL_ACCEPTANCE_REVIEW_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_PARENT_FINAL_ACCEPTANCE_REVIEW_01/20_FINAL_ACCEPTANCE_REPORT.md` |
| GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_ACCEPTANCE_REVIEW_01 | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01 | — | CLOSED | oui | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_E2E_ARTIFACT_REGISTRY_01/90_REPRISE_POINT.md` — PR #851 — 63/63 registry + 282/282 e2e PASS |
| GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01 | GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01 | — | CLOSED | oui | `docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_MARKET_METRICS_CONSUMER_01/20_MARKET_METRICS_CONSUMER_TARGET.md` — PR #817 — 21/21 consumer PASS / 134/134 google_sheets PASS |

---

## Entrées closes/pass

Ces entrées détaillées sont sorties de `docs/index/GO_INDEX.md`.

### GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01
- repo : opt-trading
- type : gouvernance / doc-only / canonisation
- statut : pass
- titre court : promotion canonique de la matrice gouvernante V2
- dernier état connu : la matrice V2 issue du bundle clos a été promue dans `docs/governance/` avec maintien de `GO_INDEX.md` comme vérité de liste, `REPRISE.md` comme surface opératoire seulement, `BRANCH_STATE.md` comme surface branches, et limite AI team conservée comme report borné
- lien utile : `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_CANONIZATION_01/90_closeout.md`, `docs/governance/MATRICE_GOUVERNANTE_V2.md`

### GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01
- repo : opt-trading
- type : gouvernance / continuité produit
- statut : pass
- titre court : hiérarchie produit multi-chantier canonisée
- dernier état connu : structuration Couche 0 / Anneau A / Anneau B posée comme source canonique de continuité produit
- lien utile : `docs/chantiers/GO_CONTINUITE_PRODUIT_MULTI_CHANTIER_CANON_01/00_cadrage.md`, `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`, `docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md`

### GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01
- repo : opt-trading
- type : continuité locale / bootstrap
- statut : pass
- titre court : socle documentaire local posé
- dernier état connu : closeout PASS avec gouvernance locale, index et reprise locale en place
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01/90_closeout.md`, `docs/index/REPRISE.md`

### GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01
- repo : opt-trading
- type : chantier pilote / memory_bricks
- statut : pass
- titre court : pilote canonique `memory_bricks`
- dernier état connu : closeout PASS posé comme second pilote local directement ancré sur `memory_bricks`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md`, `docs/governance/MEMORY_BRICKS_MAPPING.md`

### GO_UNIFORM_CONTINUITY_HARDENING_01
- repo : opt-trading
- type : hardening documentaire
- statut : pass
- titre court : réalignement final des index locaux
- dernier état connu : hardening appliqué sur les index `opt-trading` ; `localcms` hors-scope dans ce flux ; closeout PASS
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_01/90_closeout.md`, `docs/index/ACTIVE_STREAMS.md`

### GO_GITHUB_PARK_AUDIT_EXPANSION_01
- repo : opt-trading
- type : audit / parc GitHub
- statut : pass
- titre court : expansion de l’audit du parc GitHub
- dernier état connu : cible finale atteinte ; cross-audit consolidé et intégrité canonique `GO_INDEX ↔ 04_branch_trunk_cross_audit_target.md` rétablie sur `sot/mainline`
- lien utile : `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/90_closeout.md`, `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_branch_trunk_cross_audit_target.md`

### GO_GITHUB_PARK_AUDIT_EXPANSION_ISOLATE_01
- repo : opt-trading
- type : patch local / doc-only
- statut : pass
- titre court : isolation des modifications locales audit GitHub Park
- dernier état connu : les 2 docs locaux du chantier GitHub Park ont été isolés sur branche dédiée avec commit `a4ce731` et worktree propre
- lien utile : `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_journal_technique.md`, `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/03_decisions.md`

### GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01
- repo : opt-trading
- type : gouvernance / git / branches
- statut : pass
- titre court : méthode canonique de ménage des branches Git
- dernier état connu : méthode récurrente figée sur base `origin/sot/mainline`, avec tri standard `DELETE_NOW / KEEP / REVIEW`, revue manuelle obligatoire pour les familles sensibles, et extraction Skill explicitement postérieure à la doc canonique
- lien utile : `docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/00_cadrage.md`, `docs/chantiers/GO_GIT_BRANCH_HOUSEKEEPING_METHOD_01/90_closeout.md`, `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`, `docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/04_branch_trunk_cross_audit_target.md`

### GO_INTEG_TRADING_DUAL_STACK_DOC_ONLY_INTEGRATION_01
- repo : opt-trading
- type : intégration doc-only
- statut : pass
- titre court : intégration bornée du pack trading dual stack
- dernier état connu : intégration via checkout borné sur `docs/trading/*` sans merge global, commit `5d46981`, worktree propre
- lien utile : `docs/trading/02_ETABLI_TRADING_DUAL_STACK_V1_0.txt`, `docs/trading/03_KANBAN_TRADING_DUAL_STACK_V1_0.txt`, `docs/trading/04_REPRISE_TRADING_DUAL_STACK_V1_0.txt`, `docs/trading/TRADING_DUAL_STACK_V1_0_CLARIFIED.md`

### GO_RANGE_STRATEGY_V1_STRUCT_01
- repo : opt-trading
- type : trading / stratégie range
- statut : pass
- titre court : cadrage stratégie range v1
- dernier état connu : chantier documentaire range strategy v1 aligné sur la gate de session avec ancrage métier trading créé
- lien utile : `docs/chantiers/GO_RANGE_STRATEGY_V1_STRUCT_01/90_closeout.md`

### GO_STRATEGY_KERNEL_SHARED_LAYER_01
- repo : opt-trading
- type : trading / noyau stratégie
- statut : pass
- titre court : cadrage noyau stratégie partagé
- dernier état connu : sujet désormais couvert par un chantier canonique propre, aligné sur l’intention figée et l’état réel du repo
- lien utile : `docs/chantiers/GO_STRATEGY_KERNEL_SHARED_LAYER_01/90_closeout.md`

### GO_UNIFORM_CONTINUITY_HARDENING_02
- repo : opt-trading
- type : hardening documentaire
- statut : pass
- titre court : normalisation des headings workflow / mémoire / documentation
- dernier état connu : cadrage canonique posé + lot patchable appliqué en docs-only ; closeout PASS
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/00_cadrage.md`, `docs/chantiers/GO_UNIFORM_CONTINUITY_HARDENING_02/90_closeout.md`

### GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01
- repo : opt-trading
- type : exécution doc-only (lot fermé)
- statut : pass
- titre court : application normalisation headings (workflow / mémoire / documentation)
- dernier état connu : closeout PASS ; patch headings-only limité au lot fermé, sans réécriture de fond
- lien utile : `docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/00_cadrage.md`, `docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/02_journal_technique.md`, `docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/03_decisions.md`, `docs/chantiers/GO_APPLY_UNIFORM_WORKFLOW_MEMORY_DOCUMENTATION_01/90_closeout.md`

### GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02
- repo : opt-trading
- type : pack IDE / transmission
- statut : pass
- titre court : pack d’exécution IDE pour le hardening
- dernier état connu : chantier documentaire de transmission complet et immédiatement exploitable par l’IDE
- lien utile : `docs/chantiers/GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02/IDE_EXECUTION_PACK.md`

### GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS
- repo : opt-trading
- type : collectors / lifecycle compatibility
- statut : pass
- titre court : séquence lifecycle compat collectors canonisée en lot fermé
- dernier état connu : séquence baseline -> scope -> spec -> closeout canonisée sous une forme close `_CLOS` ; closeout historique conservé ; aucun next GO ouvert automatiquement
- lien utile : `docs/chantiers/GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS/00_cadrage.md`, `docs/chantiers/GO_COLLECTORS_LIFECYCLE_COMPAT_CLOS/90_closeout.md`, `docs/COLLECTORS_LIFECYCLE_COMPAT_CLOSEOUT_01.md`

### GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01
- repo : opt-trading
- type : sous-lot d'execution / suite modules / openclaw
- statut : pass
- titre court : consolidation bornee de la suite OpenClaw
- dernier état connu : sous-lot ferme en doc-only apres cartographie de suite, matrice des wrappers, runbook unique, conventions de famille et audit de duplication ; aucun patch shell transverse publie
- lien utile : `docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/03_step_01_matrice_wrappers.md`, `docs/chantiers/GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01/04_step_02_runbook_de_suite.md`

### GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_01
- repo : opt-trading
- type : gouvernance / chantier parent / orchestration de reprise repo-first
- statut : pass
- titre court : parent canonique de reprise avant structuration project/machine
- dernier état connu : closeout dedie publie le 2026-04-29 ; sequence enfant complete, `admin-trading` et `db-layer` conformes, `student` et `fantome` differes, `localcms` fusionne
- lien utile : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_DOC_OPS_PARENT_PROJECT_MACHINE_SPLIT_CLOSEOUT_01/02_final_state.md`

### GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01
- repo : opt-trading
- type : doc-only / sous-go d'audit final des parents ouverts
- statut : pass
- titre court : audit final de conformite des parents ouverts
- dernier état connu : `90_closeout.md` en `pass` ; conformite finale des parents audites et propagation de continuite corrigee
- lien utile : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_DOC_OPS_CHILD_PARENT_CONFORMITY_AUDIT_01/01_conformity_matrix.md`

### GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01
- repo : opt-trading
- type : gouvernance / metadata derivee / doc-only
- statut : closed
- titre court : doctrine legere de derivation post-matrice
- dernier état connu : `10_closeout.md` ferme la sequence documentaire et recommande le gel ; reouverture seulement sous condition explicite
- lien utile : `docs/chantiers/GO_OPT_TRADING_MATRICE_GOUVERNANTE_METADATA_DERIVATION_01/10_closeout.md`, `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`

### GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : closed
- titre court : réalignement scope registry
- dernier état connu : `registry/README.md` clarifie le périmètre, la limite repo/package et les exceptions sans créer de doctrine parallèle
- lien utile : `registry/README.md`, `docs/chantiers/GO_OPT_TRADING_REGISTRY_SCOPE_REALIGNMENT_01/03_decisions.md`

### GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01
- repo : opt-trading
- type : patch local / doc-only / reclassement documentaire
- statut : closed
- titre court : révision et relocalisation documentaire de `trae_pack_texts`
- dernier état connu : `docs/ot/trae/trae_pack_texts/README.md` est l'entrée vivante, `trae_pack/` est archive de lecture et le pack n'est plus opposable face au canon repo-first
- lien utile : `docs/ot/trae/trae_pack_texts/README.md`, `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/03_decisions.md`

### GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01
- repo : opt-trading
- type : Claude Cowork / Attention Center / real run / doc-only
- statut : pass
- titre court : premier run reel du prompt `OPT_TRADING_ATTENTION_CENTER_01`
- dernier etat connu : PR #274 mergee dans `sot/mainline` avec verdict PASS ; sortie P0/P1/P2 capturee ; aucun gap bloqueur prouve ; prochain GO recommande `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`
- reserve de reprise : machine cible a verifier avant execution ; OpenClaw hors scope pour cette suite
- lien utile : `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/90_CLOSEOUT.md`, `docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01/30_CLAUDE_OUTPUT_CAPTURE.md`, `docs/index/inbox/GO_OPT_TRADING_CLAUDE_COWORK_CHILD_ATTENTION_CENTER_REAL_RUN_01.md`

### GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : closed
- titre court : realignement continuite index
- dernier état connu : la couche `docs/index/*` est coherente, `docs/next/NEXT_GO_CANDIDATES.md` est declassé, et les anciennes surfaces `journal*` ne sont plus actives dans le repo
- lien utile : `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/90_closeout.md`, `docs/index/GO_INDEX.md`, `docs/next/NEXT_GO_CANDIDATES.md`

### GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01
- repo : opt-trading
- type : patch local / doc-only
- statut : closed
- titre court : carte canonique des surfaces du repo
- dernier état connu : `docs/architecture/REPO_SURFACES_MAP.md` est la carte humaine de reference et `docs/INDEX.md` / `docs/ARCHITECTURE.md` sont alignes sans duplication de `registry/*`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01/90_closeout.md`, `docs/architecture/REPO_SURFACES_MAP.md`, `docs/ARCHITECTURE.md`

### GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
- repo : opt-trading
- type : patch local / doc-only
- statut : closed
- titre court : politique racine canonique interne du repo
- dernier état connu : `REPO_ROOT_POLICY.md` qualifie desormais la racine reelle, y compris le shim `bitget_bridge.py` comme exception legacy de compatibilite explicite, sans arbitrage ouvert residuel
- lien utile : `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/90_closeout.md`, `docs/governance/REPO_ROOT_POLICY.md`

### GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01
- repo : opt-trading
- type : audit / qualification / préparation reclassement physique
- statut : closed
- titre court : audit obsolete / archive / legacy / sous arbitrage
- dernier état connu : la matrice d'audit est jugee suffisante, les lots executes sont documentes et aucun move/delete/archive supplementaire n'est requis pour le closeout
- lien utile : `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_OBSOLETE_RECLASS_ARCHIVE_AUDIT_01/02_journal_technique.md`

### GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01
- repo : opt-trading
- type : module durable audit-only
- statut : closed
- titre court : module naming_normalizer
- dernier état connu : le module audit-only est livre avec README, wrappers shell, moteur Python et configuration declarative, sans apply automatique du repo
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_NORMALIZER_01/90_closeout.md`, `modules/naming_normalizer/README.md`

### GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01
- repo : opt-trading
- type : audit repo-first
- statut : closed
- titre court : inventaire des ecarts de nommage
- dernier état connu : inventaire repo-first produit sur `docs/chantiers/`, `docs/governance/`, `modules/`, scripts et branches locales, avec classification `CANON / LEGACY_TOLERE / A_CORRIGER_PLUS_TARD / REVIEW_REQUIRED / REFERENCE_ONLY`
- lien utile : `docs/chantiers/GO_OPT_TRADING_CHILD_NAMING_INVENTORY_01/90_closeout.md`, `modules/naming_normalizer/output/naming_audit_report.md`, `modules/naming_normalizer/output/naming_audit_report.json`

### GO_OPT_TRADING_PARENT_NAMING_CANON_01
- repo : opt-trading
- type : gouvernance / nommage / chantier parent
- statut : closed
- titre court : parent canonique naming
- dernier état connu : politique par surface stable, module audit-only livre, inventaire repo-first prouve et aucune application reelle requise pour le closeout parent
- lien utile : `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_PARENT_NAMING_CANON_CLOSEOUT_01/90_closeout.md`, `docs/governance/NAMING_CANON_POLICY_01.md`

### GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
- repo : opt-trading
- type : gouvernance / chantier parent / doc-only
- statut : closed
- titre court : matrice maitre doc ops
- dernier état connu : matrice maitre finale publiee et souveraine ; les closeouts de gouvernance necessaires sont executes ; aucun lot complementaire propre au parent ne bloque sa fermeture
- lien utile : `docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/90_closeout.md`, `docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_CLOSEOUT_01/90_closeout.md`, `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`

### GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01
- repo : opt-trading
- type : protocole tmux / db-layer / child OpenClaw
- statut : closed
- titre court : protocole de supervision tmux OpenClaw sur db-layer
- dernier état connu : cadrage et protocole doc-only merges dans `sot/mainline` ; phase child closee avant runtime PASS
- lien utile : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01/00_INITIAL_PROJECT_DOC.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01/01_TMUX_OPERATOR_PROTOCOL.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md`

### GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01
- repo : opt-trading
- type : runtime execution / tmux / db-layer
- statut : closed
- titre court : runtime tmux OpenClaw start/status/stop sur db-layer
- dernier état connu : runtime `PASS` merge via PR #221 ; `RUNTIME_LOG.md` en `status: closed` ; bind `127.0.0.1:18789`, `/health` live, stop OK, aucun zombie
- lien utile : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01/RUNTIME_LOG.md`, `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md`

### GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01
- repo : opt-trading
- type : closeout / tmux / db-layer / OpenClaw
- statut : pass
- titre court : closeout de la chaine OpenClaw parent -> tmux -> runtime sur db-layer
- dernier état connu : closeout merge via PR #222 ; chaine parent -> child -> runtime declaree `CLOSED` ; aucun `NEXT_GO` requis
- lien utile : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md`

### GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
- repo : opt-trading
- type : chantier parent machine / doc-only / Ollama local
- statut : closed
- titre court : parent Local Ollama pour student
- dernier état connu : closeout PASS dans `90_CLOSEOUT.md` ; parent valide, student rattache comme machine Ollama sur preuve runtime reelle ; OpenClaw lab differe ; aucun merge aveugle de la branche autorise ; gap d'indexation declare au checkpoint puis resolu dans le lot de reparation
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md`, `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_PARENT_CHECKPOINT.md`, `docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01.md`

### GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_REVIEW_REALIGN_01
- repo : opt-trading
- type : realignement doc-only / child parent
- statut : closed
- titre court : realignement du parent Local Ollama
- dernier état connu : PR #251 merged ; realignement student Local Ollama parent complete
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_REVIEW_REALIGN_01/00_REALIGN_PLAN.md`

### GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01
- repo : opt-trading
- type : standardisation agent / doc-only
- statut : closed
- titre court : adoption baseline runtime Student/Ollama
- dernier état connu : FULL_PASS ; chaine Student/Ollama complete ; provider local CPU, smoke canonique, politique retention, enforcement, baseline adoption fixes ; ferme dans le cadre de Student/Ollama FULLY_CLOSED
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01/CHECKPOINT.md`

### GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01
- repo : opt-trading
- type : gouvernance agent / doc-only
- statut : closed
- titre court : gate capacite et fallback pour Student/Ollama
- dernier état connu : livrables produits (capability gate, model task boundary, runbook escalation) ; 0.5B = probe pipeline, pas worker decisionnel ; ferme apres merge dans le cadre Student/Ollama FULLY_CLOSED
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01/CHECKPOINT.md`

### GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_FIRST_CONTROLLED_CONSUMER_01
- repo : opt-trading
- type : execution controlee / doc-only
- statut : closed
- titre court : premier consommateur controle Student/Ollama
- dernier état connu : FIRST_CONSUMER_PASS ; pipeline agent fonctionnel ; modele 0.5B ne suit pas instructions exactes ; pas de trading/worker ; ferme dans le cadre Student/Ollama FULLY_CLOSED
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_FIRST_CONTROLLED_CONSUMER_01/CHECKPOINT.md`

### GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01
- repo : opt-trading
- type : runbook / doc-only
- statut : closed
- titre court : runbook usage controle Student/Ollama
- dernier état connu : baseline runtime ADOPTED ; runbook usage controle DRAFT ; ferme apres merge ; baseline Student/Ollama complete : validation -> politique -> enforcement -> baseline adoption -> usage runbook
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01/CHECKPOINT.md`

### GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01
- repo : opt-trading
- type : politique / doc-only
- statut : closed
- titre court : politique de retention de session Student/Ollama
- dernier état connu : politique documentee ; runbook rotation documente ; ferme dans le cadre Student/Ollama FULLY_CLOSED
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01/CHECKPOINT.md`

### GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01
- repo : opt-trading
- type : enforcement / scripts
- statut : closed
- titre court : enforcement retention de session Student/Ollama
- dernier état connu : plan d'enforcement, script diagnostic, script purge produits ; ferme dans le cadre Student/Ollama FULLY_CLOSED
- lien utile : `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01/CHECKPOINT.md`


### GO_DB_LAYER_REPRISE_AUDIT_01
- repo : opt-trading
- type : audit / housekeeping / doc-only
- statut : closed
- titre court : audit et nettoyage parc branches db-layer post-PR #517
- dernier état connu : ~45 branches db-layer supprimées (local + remote) ; squash-orphelins CHILD_GATEWAY_SUPERVISION_TMUX confirmés ; A_VERIFIER finaux audités et droppés ; BRANCH_STATE.md et MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md réconciliés ; PASS
- lien utile : `docs/chantiers/GO_DB_LAYER_REPRISE_AUDIT_01/90_CLOSEOUT.md`

---

### GO_OPT_TRADING_ADMIN_TRADING_RUNTIME_SYNC_AFTER_PAPER_GUARDS_01
- repo : opt-trading
- type : runtime sync / verification
- statut : closed
- titre court : sync runtime admin-trading + verification guards PAPER_TEST
- dernier etat connu : runtime synchronise sur `sot/mainline @ 50df15c3` ; `GET /api/paper/guards` retourne 200 avec guards correctement bloquants
- verdict : PASS_SYNC_BLOCKING_GUARDS
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_RUNTIME_SYNC_AFTER_PAPER_GUARDS_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01
- repo : opt-trading
- type : configuration / paper flags
- statut : closed
- titre court : configurer flags paper pour guards ok:true
- dernier etat connu : flags configurés sur admin-trading ; `GET /api/paper/guards` retourne `ok: true` avec tous les guards PASS
- verdict : PASS_CONFIG
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_FLAGS_CONFIG_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01
- repo : opt-trading
- type : execution / PAPER_TEST
- statut : closed
- titre court : exécution PAPER_TEST contrôlée via paper adapter
- dernier etat connu : PAPER_TEST envoyé et exécuté ; position BTC/USDT ouverte en simulation ; guards ok:true avant et après
- verdict : PASS_PAPER_TEST_EXECUTED
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_RETRY_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_POSITION_CLOSE_01
- repo : opt-trading
- type : position close / paper
- statut : closed
- titre court : fermer position paper BTC/USDT du retry
- dernier etat connu : position BTC/USDT BUY 0.1 @ 65000.0 fermée ; positions préexistantes inchangées ; guards ok:true
- verdict : PASS_POSITION_CLOSED
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_POSITION_CLOSE_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_CYCLE_CLOSEOUT_01
- repo : opt-trading
- type : cycle closeout / PAPER_TEST
- statut : closed
- titre court : closeout cycle PAPER_TEST complet
- dernier etat connu : cycle complet validé (guards → exec → tracking → close) ; aucun trade réel ; guards ok:true
- verdict : PASS_CYCLE_COMPLETE
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_TEST_CYCLE_CLOSEOUT_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01
- repo : opt-trading
- type : paper scenarios / expansion
- statut : closed
- titre court : scénarios paper additionnels (SELL, invalid, guard fail, ledger)
- dernier etat connu : 5/5 scénarios PASS ; positions nettoyées ; guards ok:true
- verdict : PASS_ALL_SCENARIOS
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_SCENARIOS_EXPANSION_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PAPER_VALIDATION_GLOBAL_CLOSEOUT_01
- repo : opt-trading
- type : global closeout / paper validation
- statut : closed
- titre court : closeout global validation paper admin-trading
- dernier etat connu : 10 PRs/GOs consolidés ; preuves collectées ; conditions production définies ; production non ouverte
- verdict : PASS_GLOBAL_PAPER_VALIDATION
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PAPER_VALIDATION_GLOBAL_CLOSEOUT_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_READINESS_CONDITIONS_01
- repo : opt-trading
- type : production readiness / conditions
- statut : closed
- titre court : conditions production readiness admin-trading
- dernier etat connu : 7 conditions évaluées (0 SATISFIED, 2 PARTIAL, 4 MISSING, 1 BLOCKED) ; production non ouverte
- verdict : PASS_CONDITIONS_DEFINED
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_READINESS_CONDITIONS_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01
- repo : opt-trading
- type : production readiness / risk limits + kill switch
- statut : closed
- titre court : spécification risk limits et kill switch production
- dernier etat connu : risk limits et kill switch spécifiés ; rollback plan documenté ; validation gates définis ; production non ouverte
- verdict : PARTIAL (spécifié, non implémenté)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_IMPL_01
- repo : opt-trading
- type : implementation / risk limits + kill switch
- statut : closed
- titre court : implémentation risk limits et kill switch
- dernier etat connu : risk limits et kill switch implémentés et testés ; endpoints fonctionnels ; production non ouverte
- verdict : PASS_IMPLEMENTED
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_RISK_LIMITS_AND_KILL_SWITCH_IMPL_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_AND_SECRETS_AUDIT_01
- repo : opt-trading
- type : production readiness / monitoring + secrets audit
- statut : closed
- titre court : audit monitoring et secrets admin-trading
- dernier etat connu : monitoring PARTIAL (services actifs, P&L manquant) ; secrets PARTIAL (TV_WEBHOOK_KEY non défini) ; production non ouverte
- verdict : PARTIAL
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_AND_SECRETS_AUDIT_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_PNL_ALERT_THRESHOLDS_01
- repo : opt-trading
- type : production readiness / monitoring spec
- statut : closed
- titre court : spécification P&L tracking et alert thresholds
- dernier etat connu : P&L tracking et alert thresholds spécifiés ; monitoring reste PARTIAL ; production non ouverte
- verdict : PARTIAL (spécifié, non implémenté)
- lien utile : `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PRODUCTION_MONITORING_PNL_ALERT_THRESHOLDS_01/90_CLOSEOUT.md`

### GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
- repo : opt-trading
- type : master project plan / github actions / openclaw
- statut : closed
- titre court : master target github_actions_openclaw
- dernier état connu : close gate master consolidee avec preuve live reelle (run `26486400740`) ; close gate PASS ; 10 conditions de fermeture validees ; aucun gap bloqueur residuel ; chantier clos
- lien utile : `docs/chantiers/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01/CLOSE_GATE.md`, `docs/index/GO_INDEX.md`, `docs/index/GO_CLOSED_INDEX.md`

### GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_ENRICH_01
- repo : opt-trading
- type : enrichissement module / read-only operator
- statut : closed
- titre court : enrichissement openclaw_tmux_operator — session-logs SSH, health-aggregate multi-machines
- dernier état connu : cmd.sh enrichi, health_aggregate.py ajouté, 45/45 tests PASS, post-merge smoke PASS ; branche supprimée
- verdict : PASS
- lien utile : `docs/chantiers/GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_ENRICH_01/90_CLOSEOUT.md`
