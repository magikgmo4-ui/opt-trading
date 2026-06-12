---
doc_id: GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01_01_PRODUCER_DELTA
doc_type: implementation_delta
repo: opt-trading
project: opt-trading
module: repo_knowledge_graph
go_id: GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01
parent_go: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: open
lifecycle_stage: implementation
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/00_CADRAGE.md
updated_at: 2026-05-07
links:
  - producer_repo_kg_v1.py
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/07_producer_spec_v1.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md
  - graph_bundle.json
---

# 01_PRODUCER_DELTA - GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01

## 1_DELTA_APPLIQUE

Le Producer est aligne sur les besoins des vues V1 selon trois axes.

### 1.1 Statuts GO

1. les statuts GO sont ramenes a un vocabulaire borne (`OPEN`, `ACTIVE`, `REFERENCE`, `CLOSED`, `PASS`, `PASS_LIMITED`, `PARTIAL`, `BLOCKED`, `FAIL`, `UNKNOWN`) ;
2. les surfaces canoniques `GO_INDEX`, `GO_CLOSED_INDEX`, `REPRISE`, `ACTIVE_STREAMS`, `NEXT_GO_CANDIDATES` priment sur les statuts de documents individuels ;
3. les frontmatters de documents ne fuient plus vers des statuts GO parasites comme `CLOSING`, `VERDICT` ou `READY_FOR_REVIEW` ;
4. un verdict de closeout n'est utilise qu'en fallback quand les surfaces d'index ne parlent pas deja du GO.

### 1.2 Reprise / NEXT_GO

1. `NEXT_GO` extrait maintenant le premier token `GO_...` au lieu de serialiser toute la ligne comme identifiant ;
2. la ligne brute est conservee comme note (`next_go_note`) quand elle apporte un contexte utile ;
3. les auto-transitions terminales du type `GO_X -> CLOSED (PASS)` ne sont plus traitees comme un vrai `next_go_primary`.

### 1.3 Projection views-first

1. les noeuds `APP` restent projetes dans le bundle et sont maintenant ancres sur des docs GO deja presentes sur la base canonique ;
2. les edges `RUNS_ON`, `HAS_GAP`, `RESUMES_AT`, `HAS_TODO`, `PRODUCES` et branche -> GO (`REFERENCES`) sont exploitables directement ;
3. la validation du bundle refuse maintenant tout statut GO hors vocabulaire attendu ;
4. le bundle projette maintenant des types/relations conformes aux besoins des vues V1 (`APP`, `RUNS_ON`, `REFERENCES` depuis `BRANCH` et `TODO`).

## 2_NON_OBJECTIFS

1. aucune relation nouvelle non prouvee n'est introduite ;
2. aucune source externe n'est consultee ;
3. aucun runtime trading n'est modifie.

## 17_RESUME_POINT

```text
graph_bundle.json
-> verifier validation.valid=true
-> verifier APP / RUNS_ON / HAS_GAP / REFERENCES branche -> GO / RESUMES_AT / HAS_TODO
-> rejouer les cartes Mermaid V1
```

## RISKS

- À qualifier.
