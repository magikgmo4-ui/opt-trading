---
doc_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01_MATRIX
doc_type: audit_matrix
repo: opt-trading
project: opt-trading
module:
  go_id: GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01
status: active
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - branch_audit
  - matrix
  - go_branches
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Tableau principal"
updated_at: 2026-04-28
links:
  - docs/chantiers/GO_OPT_TRADING_REMAINING_GO_BRANCHES_MATRIX_AUDIT_01/raw_branch_scan.json
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
---

# Branch Matrix Audit

| branch | go_id_extracted | remote_present | local_present | ahead_behind_vs_sot | in_GO_INDEX | in_BRANCH_STATE | chantier_dir_present | frontmatter_go_id_match | closeout_present | matrix_status | decision_candidate | evidence |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---|
| `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | yes | no | `behind 139 / ahead 10` | yes | yes | no | no | no | `BRANCH_DOC_MISMATCH` | `TRANSPORT_DOCS_THEN_DELETE` | GO present in `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE` and `BRANCH_STATE`; canonical dossier absent on `sot/mainline`; remote diff is 8 docs-only files adding `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/`. |
| `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | `GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` | yes | no | `behind 139 / ahead 19` | no | no | no | no | no | `BRANCH_ONLY` | `NEEDS_DEEP_AUDIT` | No canonical index or chantier proof on `sot/mainline`; remote diff adds 10 chantier docs, 4 bundle files under `bundles/`, and a `BRANCH_STATE.md` edit. |
| `go/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` | `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` | yes | no | `behind 139 / ahead 18` | no | no | no | no | no | `BRANCH_ONLY` | `NEEDS_DEEP_AUDIT` | No matrix or index presence; remote diff adds bundle payload files, chantier docs, and a custom index entry file outside `GO_INDEX.md`. |
| `go/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | `GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | yes | no | `behind 47 / ahead 3` | no | no | no | no | no | `BRANCH_ONLY` | `NEEDS_DEEP_AUDIT` | Small docs-only branch with 3 added chantier files, but no parent proof in `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE`, or `BRANCH_STATE`. |
| `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` | yes | no | `behind 139 / ahead 12` | no | no | no | no | no | `BRANCH_ONLY` | `NEEDS_DEEP_AUDIT` | Branch-only doc pack with txt/csv payload under `CLICKUP_IMPLEMENTATION_BUNDLE_V1`; no canonical GO entry or chantier on `sot/mainline`. |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` | `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01` | yes | yes | `behind 54 / ahead 6` | no | no | yes | yes | yes | `CLOSED_BUT_BRANCH_EXISTS` | `NEEDS_DEEP_AUDIT` | Local closeout marks the GO `closed`; branch diff still touches 124 files including `_archive/`, `modules/`, and `scripts/`; closeout explicitly says the polluting branch must not serve PR. |
| `go/GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_ISOLATED` | `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01_ISOLATED` | yes | yes | `behind 48 / ahead 0` | no | no | no | no | no | `STALE_REFERENCE` | `DELETE_AFTER_CONFIRMATION` | No canonical GO with this isolated name; zero unique file delta versus `sot/mainline`; only referenced from the closeout of `GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01`. |
| `go/GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01` | `GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01` | yes | yes | `behind 14 / ahead 0` | no | no | yes | yes | yes | `CLOSED_BUT_BRANCH_EXISTS` | `DELETE_AFTER_CONFIRMATION` | `90_CLOSEOUT.md` marks status `pass`; no unique file delta versus `sot/mainline`; branch remains local and remote after absorption of index patches. |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | yes | no | `behind 139 / ahead 11` | no | no | no | no | no | `BRANCH_ONLY` | `NEEDS_DEEP_AUDIT` | Remote branch adds 9 chantier docs plus custom index/branch files, but no canonical proof exists on `sot/mainline`. |
| `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` | `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` | yes | yes | `behind 86 / ahead 2` | yes | yes | yes | yes | no | `OPEN_PARENT_BRANCH_OK` | `KEEP_ACTIVE` | Parent is explicitly open in the matrix and `GO_INDEX`; canonical dossier exists with matching `go_id`; branch support is named in `01_cadrage_parent.md`; delta is doc-only on governance surfaces. |
| `go/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_ALIGNMENT_01` | `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01_ALIGNMENT_01` | yes | yes | `behind 86 / ahead 1` | no | yes | no | no | no | `BRANCH_DOC_MISMATCH` | `TRANSPORT_DOCS_THEN_DELETE` | Alignment support branch is tracked in `BRANCH_STATE` but not canonized in `GO_INDEX`; no direct chantier dir on `sot/mainline`; doc-only delta overlaps the same surfaces already owned by the parent branch. |
| `go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | yes | yes | `behind 20 / ahead 4` | yes | no | yes | yes | yes | `BRANCH_DOC_MISMATCH` | `KEEP_ACTIVE` | Parent is open in `GO_INDEX`, `ACTIVE_STREAMS`, and `REPRISE`; `PARENT_STATE.md` names the dedicated branch and keeps the parent open; branch is missing from `BRANCH_STATE`; remaining delta is 4 docs-only files. |
| `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LIVE_ARTIFACTS_01` | `GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LIVE_ARTIFACTS_01` | yes | no | `behind 47 / ahead 0` | no | no | no | no | no | `STALE_REFERENCE` | `DELETE_AFTER_CONFIRMATION` | Remote branch has zero unique file delta versus `sot/mainline` and no canonical proof in index or chantier surfaces. |
| `go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01` | `GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01` | yes | no | `behind 83 / ahead 4` | no | no | no | no | no | `BRANCH_ONLY` | `NEEDS_DEEP_AUDIT` | Small docs-only parent pack with no matrix/index presence and no chantier dir on `sot/mainline`. |
| `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | `GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` | yes | no | `behind 68 / ahead 18` | no | no | no | no | no | `BRANCH_ONLY` | `NEEDS_DEEP_AUDIT` | Large docs-only branch with `ide_bundle/` payload and 18 added files, but no canonical GO line, no chantier dir on `sot/mainline`, and no branch-state classification. |
| `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` | `GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` | yes | no | `behind 68 / ahead 1` | no | no | no | no | no | `BRANCH_ONLY` | `NEEDS_DEEP_AUDIT` | Single added parent cadrage file, but no explicit proof in `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE`, or `BRANCH_STATE`. |
| `go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | yes | yes | `behind 10 / ahead 15` | no | no | no | no | no | `BRANCH_ONLY` | `NEEDS_DEEP_AUDIT` | Branch adds chantier docs plus non-doc payload under `scripts/ai/workers/` and `reports/ai/workers/`; absent from all canonical GO/index surfaces. |

## Notes de lecture

- `BRANCH_ONLY` signifie que la branche existe mais ne suffit pas a prouver un parent ou un GO canonique.
- `BRANCH_DOC_MISMATCH` signifie qu'une partie de la preuve canonique existe, mais qu'un maillon manque entre branche, dossier chantier, index, ou surface branches.
- `CLOSED_BUT_BRANCH_EXISTS` signifie que le GO local est clos ou `pass`, alors que le support Git reste present.
