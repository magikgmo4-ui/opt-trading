---
doc_id: OPENCLAW_LIBRARY_INDEX
doc_type: master_index
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
---

# docs/openclaw — Master Cross-Surface Registry

Bibliothèque opérateur OpenClaw. Source : cartographie des 77 sources du parent
`GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01`.

## Surfaces

| Surface | Count | Index |
| --- | --- | --- |
| Modules runtime | 9 | [modules/INDEX.md](modules/INDEX.md) |
| Chantiers GO | 130+ | [chantiers/INDEX.md](chantiers/INDEX.md) |
| Hermes bridge | 10 | [hermes/INDEX.md](hermes/INDEX.md) |
| Governance / targets | 2 | [governance/INDEX.md](governance/INDEX.md) |
| Branches git | 37 | voir chantiers/INDEX.md section branches |
| **Loop contract** | **5 formats** | [loop_contract/INDEX.md](loop_contract/INDEX.md) |
| **Fleet matrix** | **6 machines** | [fleet/INDEX.md](fleet/INDEX.md) |
| **Student lab** | E2E prouvé / non opérationnel | [student_lab/INDEX.md](student_lab/INDEX.md) |

## Architecture OpenClaw dans opt-trading

```
ChatGPT (conversationnel / gouvernance)
  └─> OpenClaw (orchestrateur)
        ├─> IDE / agents / tools / MCP / jobs
        ├─> gateway_openclaw (tmux openclaw-gateway, 127.0.0.1:18789)
        └─> retour structuré → validation humaine → relance
```

## Runtime actif

```
user:       openclaw
gateway:    127.0.0.1:18789
tmux:       openclaw-gateway
host:       db-layer (hôte prioritaire)
```

## Axes canoniques (DO NOT MIX)

| Axe | État |
| --- | --- |
| Docs / Research Library | Parent open — child extraction en cours |
| Runtime db-layer | Gateway prouvé, tmux actif |
| Gouvernance / méthode | Noyau posé — PR gated, no auto-merge |
| Orchestration GitHub Actions | Principe validé — file-scope encore fragile |

## Références parent

```
docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/00_CADRAGE_PARENT.md
docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/01_SOURCE_CARTOGRAPHY.md
```
