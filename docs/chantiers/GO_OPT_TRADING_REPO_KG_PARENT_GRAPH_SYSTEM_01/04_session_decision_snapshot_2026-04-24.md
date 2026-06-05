---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_DECISION_SNAPSHOT_2026_04_24
doc_type: decision_snapshot
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: cadrage
topic_keys:
  - ace-knowledge-graph
  - repo-graph
  - producer-consumer
  - opt-trading
search_tags:
  - graph:consumer
  - producer:required
  - source:session
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/01_cadrage_parent.md
created_at: 2026-04-24
---

# 04 — Session decision snapshot — 2026-04-24

## 7_CANONICAL_STATE

- Branche dédiée : `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
- Dossier chantier : `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/`
- Docs déjà créés dans ce chantier :
  - `01_cadrage_parent.md`
  - `02_research_notes_ace_kg_and_repo_graph.md`
  - `03_remaining_gap_todo.md`
- Source canonique : repo `opt-trading`, branche de base `sot/mainline`, matrice maître et index GO.

## 13_ESTABLISHED

### Nature de Ace Knowledge Graph

Ace Knowledge Graph est retenu comme **consumer visuel intelligent**, pas comme backend de vérité et pas comme outil Git natif.

Capacités utiles :
- transformer un document ou sujet structuré en knowledge graph interactif ;
- explorer nodes et relations ;
- produire une vue lisible d'un système complexe.

Limites retenues :
- pas de preuve de scan Git natif ;
- pas de preuve de sync GitHub ;
- pas de preuve d'écriture contrôlée dans `opt-trading` ;
- format d'import exact encore inconnu.

## 11_KEY_DECISIONS

1. Ace KG consomme une projection, il ne gouverne pas le repo.
2. Le repo `opt-trading` reste la source canonique absolue.
3. Un module Producer est obligatoire pour rendre Ace KG utile dans ton contexte.
4. Le graph doit être reconstruit depuis les sources repo, pas maintenu manuellement comme vérité.
5. Les relations critiques doivent être sourcées : doc, Git, module, branch, machine ou closeout.
6. Toute relation non prouvée reste `HYPOTHESIS`.

## 15_REMAINING_GAP — version session

### GAP STRUCTURE

- Schéma nodes/edges non figé.
- Mapping GO ↔ doc ↔ module ↔ machine ↔ branche encore à définir.
- Modèle des décisions, invariants et resume points à spécifier.

### GAP EXTRACTION

- Parser `GO_INDEX.md` proprement.
- Parser `docs/chantiers/*` proprement.
- Relier Git aux docs sans inventer.
- Définir mapping machines/runtime.

### GAP CONSUMER

- Format d'entrée Ace KG inconnu.
- Limites de taille inconnues.
- Persistance inconnue.
- Sync incrémentale non confirmée.

### GAP VISUALISATION

- Vues multi-angles non normalisées.
- Filtrage `ACTIVE` / `OPEN` / `REFERENCE` / `CLOSED` à définir.
- Rendu Mermaid/Cytoscape/JSON/Markdown à arbitrer.

## 16_TODO — version session

### P0

- Créer `05_master_plan_final_product.md` avant code.
- Créer `06_graph_schema_v1.md`.
- Créer `07_producer_spec_v1.md`.
- Créer `08_consumer_ace_kg_method_v1.md`.

### P1

- Créer `09_graph_views_v1.md`.
- Créer `10_acceptance_tests_v1.md`.
- Créer `11_security_and_no_secret_policy.md`.

### P2

- Implémenter ensuite seulement un Producer minimal lecture seule.
- Générer `graph_bundle.demo.json`.
- Tester import manuel ou prompt structuré dans Ace KG.

## 17_RESUME_POINT

Reprise immédiate : documenter d'abord le plan complet jusqu'au final product dans `05_master_plan_final_product.md`, puis seulement après ouvrir les specs de schéma, Producer et Consumer.

## RISKS

- À qualifier.
