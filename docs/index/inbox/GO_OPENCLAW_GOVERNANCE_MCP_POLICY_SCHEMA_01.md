---
doc_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01_INBOX
doc_type: index_inbox
repo: opt-trading
project: opt-trading
module: governance_openclaw_mcp_policy_schema
go_id: GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01
status: inbox_local
lifecycle_stage: doc_only_spec
surface: docs/index/inbox
source_kind: local_continuity
updated_at: 2026-05-13
---

# GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01

## 1_MASTER_TARGET

Schema canonique de policy MCP pour OpenClaw.

## 2_INITIAL_PROJECT_DOC

Chantier :

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/
```

## 3_INITIAL_NEED

Transformer MCP Boundary, Human Review Gates et Agent Trace/Evals en policy schema conceptuel, sans runtime.

## 4_MASTER_PROJECT_PLAN

Livrables locaux :

- principes ;
- fields ;
- classes ;
- gates ;
- traces/evals ;
- strict workers ;
- Ollama Lab ;
- deny-by-default ;
- validations ;
- examples draft ;
- closeout.

## 6_FINAL_TARGET

Verdict attendu :

```text
PASS_DOC_ONLY
```

## 7_CANONICAL_STATE

Etat local :

```text
branche: go/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01
scope: docs-only
runtime: none
trade: none
secret: none
global indexes: not modified
```

## 8_VALIDATED_PLAN

Cette inbox est une continuite locale. Elle ne remplace pas `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE`, `BRANCH_STATE` ni `MACHINE_WORK_SPLIT_ANTI_CONFLICT_01`.

## 9_SELECTED_SOLUTION

Utiliser le dossier chantier comme source de detail, cette inbox comme pointeur court.

## 12_INVARIANTS

- Aucun runtime.
- Aucun trade.
- Aucun sudo.
- Aucun secret.
- Aucun shell libre.
- Aucun merge.
- Aucun push force.
- Aucun cleanup.
- Aucun index global modifie.

## 13_ESTABLISHED

Le schema relie :

```text
capability class -> human gate -> trace family -> eval profile -> strict worker role -> Governor decision
```

## 14_HYPOTHESIS

Le prochain GO pourra traduire ce schema en YAML/JSON non executable.

## 15_REMAINING_GAP

Pas de policy runtime, pas de validator, pas de eval runner.

## 16_TODO

NEXT_GO recommande :

```text
GO_OPENCLAW_GOVERNANCE_MCP_POLICY_YAML_DRAFT_01
```

## 17_RESUME_POINT

Reprendre par :

```text
docs/chantiers/GO_OPENCLAW_GOVERNANCE_MCP_POLICY_SCHEMA_01/90_CLOSEOUT.md
```

## 18_TO_DOCUMENT

Agregation index globale seulement via batch ou GO explicite.

## 19_TO_REMEMBER

Memoire projet candidate :

```text
OpenClaw MCP policy schema is doc-only and deny-by-default; global indexes were intentionally not touched.
```
