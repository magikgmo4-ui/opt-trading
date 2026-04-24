---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_MASTER_PLAN_FINAL_PRODUCT
doc_type: master_plan
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: cadrage
topic_keys:
  - repo-graph
  - producer-consumer
  - ace-knowledge-graph
  - final-product
search_tags:
  - plan:global
  - graph:system
  - repo:first
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/01_cadrage_parent.md
created_at: 2026-04-24
---

# 05 — Master plan → Final product (Repo Knowledge Graph System)

## 1_MASTER_TARGET

Construire un système complet permettant :

- d'extraire la structure réelle du repo `opt-trading` ;
- de la transformer en knowledge graph structuré ;
- de la visualiser sous plusieurs angles ;
- de permettre une navigation instantanée des chantiers, décisions et états ;
- de rester 100% aligné avec la réalité repo (repo-first).

## 3_INITIAL_NEED

Ton besoin réel :

- comprendre instantanément ton système multi-chantiers ;
- voir dépendances et relations réelles ;
- reprendre un GO sans perte de contexte ;
- détecter contradictions et gaps ;
- créer une couche de navigation supérieure au repo.

## 6_FINAL_TARGET

Produit final attendu :

```text
graph_bundle.json + visualisations multi-angles + méthode consumer Ace KG
```

Capacités finales :

- vue globale du repo ;
- vue GO actifs ;
- vue docs canon ;
- vue modules/runtime ;
- vue branches Git ;
- vue machines ;
- vue reprise (resume points) ;
- vue risques/gaps.

## 4_MASTER_PROJECT_PLAN — PHASES

### PHASE 1 — Cadrage complet (actuelle)

Livrables :
- cadrage parent
- research notes
- gaps + TODO
- master plan

Objectif : figer la vision avant toute implémentation.

---

### PHASE 2 — Schéma Graph V1

Créer :
- `06_graph_schema_v1.md`

Contenu :
- types de nodes
- types de relations
- règles de preuve
- règles de dérivation

---

### PHASE 3 — Producer Spec

Créer :
- `07_producer_spec_v1.md`

Contenu :
- inputs (docs, Git, modules)
- extraction
- transformation
- output JSON

---

### PHASE 4 — Consumer Ace KG

Créer :
- `08_consumer_ace_kg_method_v1.md`

Contenu :
- format import
- prompts standard
- limites Ace KG
- vues exploitables

---

### PHASE 5 — Graph Views

Créer :
- `09_graph_views_v1.md`

Vues :
- GO
- docs
- modules
- machines
- branches
- reprise
- risques

---

### PHASE 6 — Acceptance Tests

Créer :
- `10_acceptance_tests_v1.md`

Tests :
- cohérence graph
- couverture repo
- absence de données sensibles

---

### PHASE 7 — Prototype Producer

Créer :
- module minimal
- export `graph_bundle.demo.json`

---

### PHASE 8 — Visualisation

- test Ace KG
- test Mermaid
- test JSON viewer

---

### PHASE 9 — Closeout

- documentation finale
- session reprise
- validation PASS

## 11_KEY_DECISIONS

- repo = source canonique
- graph = projection
- Producer obligatoire
- Consumer passif
- multi-angles obligatoire

## 12_INVARIANTS

- aucune dépendance forte à Ace KG
- aucun secret exposé
- aucune relation inventée
- graph reconstructible

## 17_RESUME_POINT

Prochaine étape : créer `06_graph_schema_v1.md` (coeur du système).
