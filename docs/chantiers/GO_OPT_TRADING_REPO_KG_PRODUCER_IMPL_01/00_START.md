---
doc_id: GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01_00_START
doc_type: chantier/start
repo: opt-trading
branch: go/GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01
go_id: GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01
machine: fantome
status: active
lifecycle_stage: execution
links:
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/07_producer_spec_v1.md
---

# 00_START — Repo KG Producer Implementation

## Objet

Implementer le Producer Repo KG V1 lecture seule qui genere `graph_bundle.json` depuis le repo reel.

## Livrables

- `producer_repo_kg_v1.py` — script de production
- `graph_bundle.json` — bundle graph exporte
- Documentation d execution

## Invariants

- Lecture seule
- Aucun secret scanne
- Aucun runtime modifie

## RISKS

- À qualifier.
