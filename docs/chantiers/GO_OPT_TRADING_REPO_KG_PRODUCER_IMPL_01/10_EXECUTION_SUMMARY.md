---
doc_id: GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01_10_EXECUTION_SUMMARY
doc_type: chantier/execution_summary
repo: opt-trading
branch: go/GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01
go_id: GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01
machine: fantome
status: pass
lifecycle_stage: execution
links:
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/07_producer_spec_v1.md
---

# 10_EXECUTION_SUMMARY — Repo KG Producer V1

## Resultat

**PASS** — Producer lecture seule operationnel.

## Pipeline

```
SCAN repos reel → PARSE frontmatter + GO_INDEX → BUILD nodes + edges → VALIDATE schema → EXPORT graph_bundle.json
```

## Output

| Metrique | Valeur |
| --- | --- |
| Nodes | 1450 |
| Edges | 957 |
| GOs | 188 |
| Modules | 88 |
| Branches | 107 |
| Docs | 877 |
| Scripts | 38 |
| GAPs | 58 |
| Validation errors | 0 |

## Node types

| Type | Count |
| --- | --- |
| BRANCH | 107 |
| DOC | 877 |
| GAP | 58 |
| GO | 188 |
| GOVERNANCE | 54 |
| INDEX | 32 |
| MACHINE | 5 |
| MODULE | 88 |
| PRODUCER | 1 |
| REPO | 1 |
| RESUME_POINT | 1 |
| SCRIPT | 38 |

## Edge types

| Type | Count |
| --- | --- |
| BELONGS_TO | 140 |
| DOCUMENTS | 689 |
| HAS_BRANCH | 115 |
| PRODUCES | 1 |
| RESUMES_AT | 1 |
| VALIDATES | 11 |

## Schema

`repo_kg.v1` — conforme a `06_graph_schema_v1.md`

## Secrets

Aucun secret scanne. `.env`, tokens, cles exclus.

## Fichiers

- `producer_repo_kg_v1.py`
- `graph_bundle.json`

## RISKS

- À qualifier.
