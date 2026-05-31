---
doc_id: OPENCLAW_CHANTIERS_INDEX
doc_type: chantiers_index
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
---

# docs/openclaw/chantiers — Index des 19 chantiers GO

Source : `01_SOURCE_CARTOGRAPHY.md` CLASS 2.

## A. Orchestration parent (1)

| GO_ID | Rôle |
| --- | --- |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | Parent orchestration OpenClaw → opt-trading |

## B. Gateway / TMUX (4)

| GO_ID | Surface |
| --- | --- |
| `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01` | Gateway supervision tmux |
| `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01` | Closeout gateway tmux |
| `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` | Runtime log gateway |
| `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` | Runtime tmux opencode |

## C. State dir / reclass (3)

| GO_ID | Surface |
| --- | --- |
| `GO_GIT_OPENCLAW_STATE_DIR_REPAIR_10_CLASSIFICATION_01` | Repair state dir |
| `GO_GIT_OPENCLAW_STATE_DIR_READ_09_CLASSIFICATION_01` | Read state dir |
| `GO_GIT_OPENCLAW_ABSORBED_SUBLOT_RECLASS_01` | Absorbed sublot reclass |

## D. Family consolidation (1)

| GO_ID | Contenu |
| --- | --- |
| `GO_OPT_TRADING_OPENCLAW_FAMILY_CONSOLIDATION_01` | Cartographie suite, wrappers, duplications, closeout |

## E. AI Team SSH chains (7)

| GO_ID | Phase |
| --- | --- |
| `...OPENCLAW_SSH_OPENCODE_ORCHESTRATION_PLAN_01` | Orchestration plan |
| `...OPENCLAW_SSH_OPENCODE_PHASE_0_IMPL_01` | Phase 0 checks |
| `...OPENCLAW_SSH_OPENCODE_PHASE_1_READONLY_01` | Phase 1 read-only |
| `...OPENCLAW_SSH_PYTHON_RUNNER_PHASE_2_ANALYZE_DOC_01` | Phase 2 analyze doc |
| `...OPENCLAW_SSH_PYTHON_RUNNER_PHASE_3_PATCH_DRAFT_01` | Phase 3 patch draft |
| `...OPENCLAW_SSH_PYTHON_RUNNER_PHASE_4_FULL_CHAIN_01` | Phase 4 full chain |
| `...OPENCLAW_SSH_PYTHON_RUNNER_REMOTE_PHASE_CLOSEOUT_01` | Phase closeout |

## F. Botpress OpenClaw (2)

| GO_ID | Surface |
| --- | --- |
| `GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_SPEC_01` | Adapter spec |
| `GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01` | Adapter impl |

## G. DB Layer research (1)

| GO_ID | Surface |
| --- | --- |
| `GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01` | Parent research library (ce child) |

## Branches git OpenClaw (37)

37 branches contenant "openclaw". Clusters :

| Cluster | Count |
| --- | --- |
| Gateway supervision | 5 |
| Ollama student lab | 7 |
| AI team orchestration | 7 |
| Family consolidation | 3 |
| State dir repair/reclass | 5 |
| Botpress adapter | 3 |
| Divers | 7 |

```bash
# Lister toutes les branches openclaw
git branch -a | grep -i openclaw | sort
```
