---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_PRODUCER_SPEC_V1
doc_type: producer_spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: cadrage
topic_keys:
  - producer
  - extraction
  - repo-graph
  - pipeline
search_tags:
  - producer:v1
  - extraction:repo
  - graph:build
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
created_at: 2026-04-24
---

# 07 — PRODUCER_SPEC_V1

## 1_MASTER_TARGET

Définir précisément comment extraire les données du repo `opt-trading` et construire un `graph_bundle.json` conforme au `GRAPH_SCHEMA_V1`.

Le Producer est un module **lecture seule**, reproductible et déterministe.

---

## 3_INITIAL_NEED

Transformer :

- docs gouvernance
- GO_INDEX
- dossiers chantiers
- modules
- état Git

→ en graph structuré fiable.

---

## 4_MASTER_PROJECT_PLAN

Pipeline détaillé :

```text
SCAN SOURCES
  ↓
PARSE
  ↓
NORMALIZE
  ↓
BUILD NODES
  ↓
BUILD EDGES
  ↓
VALIDATE
  ↓
EXPORT
```

---

## 8_VALIDATED_PLAN

### STEP 1 — SCAN

Sources :

- docs/governance/
- docs/index/
- docs/chantiers/
- modules/
- git branches

Sortie : liste fichiers + métadonnées.

---

### STEP 2 — PARSE

Parser :

- frontmatter YAML
- tableaux GO_INDEX
- structure dossiers

Sortie : objets intermédiaires.

---

### STEP 3 — NORMALIZE

Uniformiser :

- IDs
- types
- statuts
- chemins

---

### STEP 4 — BUILD NODES

Créer nodes selon schema :

- GO
- DOC
- MODULE
- BRANCH
- MACHINE (si connu)

---

### STEP 5 — BUILD EDGES

Construire relations :

- DOCUMENTS
- BELONGS_TO
- DEPENDS_ON
- IMPLEMENTS
- RUNS_ON

---

### STEP 6 — VALIDATE

Contrôles :

- node sans source → flag
- edge sans preuve → downgrade confidence
- doublons ID → erreur

---

### STEP 7 — EXPORT

Sorties :

- graph_bundle.json
- nodes.json
- edges.json
- report.md

---

## 10_SELECTED_SETUP

### CLI

```bash
kg scan
kg build
kg validate
kg export
```

---

## 11_KEY_DECISIONS

- parsing simple V1 (pas NLP complexe)
- priorité aux sources canoniques
- fallback → UNKNOWN

---

## 12_INVARIANTS

- lecture seule
- pas de modification repo
- pas de secrets

---

## 15_REMAINING_GAP

- parser GO_INDEX exact
- parser frontmatter robuste
- mapping machine automatisé

---

## 16_TODO

- implémenter parser GO_INDEX
- implémenter parser docs
- implémenter builder nodes/edges
- créer test minimal

---

## 17_RESUME_POINT

Next : `08_consumer_ace_kg_method_v1.md`

---

## 18_TO_DOCUMENT

- consumer spec
- graph views

---

## 19_TO_REMEMBER

TAG: PRODUCER_PIPELINE_V1
Le Producer est un pipeline simple, déterministe, repo-first qui construit un graph fiable sans modifier le repo.

## RISKS

- À qualifier.
