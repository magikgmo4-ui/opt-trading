---
doc_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01_CARTOGRAPHY
doc_type: source_cartography
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: open
updated_at: 2026-05-06
---

# 01_SOURCE_CARTOGRAPHY — OpenClaw Ecosystem

## CLASS 1 — MODULES RUNTIME (9)

| Module | Path | Role |
| --- | --- | --- |
| configure_openclaw | `modules/configure_openclaw/` | Configuration runtime OpenClaw |
| doctor_openclaw | `modules/doctor_openclaw/` | Diagnostic et health check |
| evidence_openclaw | `modules/evidence_openclaw/` | Preuves et traces d execution |
| gateway_openclaw | `modules/gateway_openclaw/` | Pilotage tmux gateway |
| install_module_openclaw | `modules/install_module_openclaw/` | Installation modules |
| menu_openclaw | `modules/menu_openclaw/` | Menu operateur interactif |
| model_provider_openclaw | `modules/model_provider_openclaw/` | Provider LLM, policy, alignment |
| openclaw_config_modulaire | `modules/openclaw_config_modulaire/` | Configuration modulaire |
| tradingview_observer_openclaw | `modules/tradingview_observer_openclaw/` | Observer TradingView |

## CLASS 2 — CHANTIERS (19)

### A. Orchestration parent (1)

| Chantier | Contenu |
| --- | --- |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | Parent orchestration OpenClaw → opt-trading |

### B. Gateway/TMUX (4)

| Chantier | Surface |
| --- | --- |
| `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01` | Gateway supervision tmux |
| `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01` | Closeout gateway tmux |
| `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` | Runtime log gateway |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | Runtime tmux opencode |

### C. State dir / reclass (3)

| Chantier | Surface |
| --- | --- |
| `GO_GIT_OPENCLAW_STATE_DIR_REPAIR_10_CLASSIFICATION_01` | Repair state dir |
| `GO_GIT_OPENCLAW_STATE_DIR_READ_09_CLASSIFICATION_01` | Read state dir |
| `GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01` | Absorbed sublot reclass |

### D. Family consolidation (1)

| Chantier | Contenu |
| --- | --- |
| `GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01` | Cartographie suite, wrappers, duplications, closeout |

### E. AI Team SSH chains (7)

| Chantier | Phase |
| --- | --- |
| `...OPENCLAW_SSH_OPENCODE_ORCHESTRATION_PLAN_01` | Orchestration plan |
| `...OPENCLAW_SSH_OPENCODE_PHASE_0_IMPL_01` | Phase 0 checks |
| `...OPENCLAW_SSH_OPENCODE_PHASE_1_READONLY_01` | Phase 1 read-only |
| `...OPENCLAW_SSH_PYTHON_RUNNER_PHASE_2_ANALYZE_DOC_01` | Phase 2 analyze doc |
| `...OPENCLAW_SSH_PYTHON_RUNNER_PHASE_3_PATCH_DRAFT_01` | Phase 3 patch draft |
| `...OPENCLAW_SSH_PYTHON_RUNNER_PHASE_4_FULL_CHAIN_01` | Phase 4 full chain |
| `...OPENCLAW_SSH_PYTHON_RUNNER_REMOTE_PHASE_CLOSEOUT_01` | Phase closeout |

### F. Botpress OpenClaw (2)

| Chantier | Surface |
| --- | --- |
| `GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01` | Adapter spec |
| `GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01` | Adapter impl |

### G. DB Layer research (1)

| Chantier | Surface |
| --- | --- |
| `GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01` | Ce document |

## CLASS 3 — HERMES BRIDGE (10 docs)

| Document | Surface |
| --- | --- |
| `03_bridge_openclaw.md` | Integration bridge |
| `GO_HERMES_OPENCLAW_BRIDGE_05*.md` | GO bridge execution |
| `HERMES_OPENCLAW_BRIDGE_RUNBOOK_V1.md` | Runbook bridge |
| `HERMES_OPENCLAW_BRIDGE_CASE_01_*.txt/.md` | Case studies et resultats |

## CLASS 4 — GOVERNANCE & TARGETS (2)

| Document | Surface |
| --- | --- |
| `docs/product_targets/OPENCLAW_TARGET_CANON.md` | Cible canonique OpenClaw |
| `docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md` | Project card OpenClaw |

## CLASS 5 — GIT BRANCHES (37)

37 branches contenant "openclaw" dans leur nom. Couvrent:
- Gateway supervision (5)
- Ollama student lab (7)
- AI team orchestration (7)
- Family consolidation (3)
- State dir repair/reclass (5)
- Botpress adapter (3)
- Divers (7)

## BILAN

| Classe | Count |
| --- | --- |
| MODULES | 9 |
| CHANTIERS | 19 |
| HERMES | 10 |
| GOVERNANCE | 2 |
| BRANCHES | 37 |
| **TOTAL sources** | **77** |

## GAPS IDENTIFIES

1. `docs/openclaw/` (research, wiki, registries, security) absent du repo — present dans le bundle sandbox inaccessible
2. Pas de vue unifiee cross-surfaces
3. Doublons potentiels entre consolidation famille et orchestration parent
4. Hermes bridge potentiellement obsolete (non maintenu)
