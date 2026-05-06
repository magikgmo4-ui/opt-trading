---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_CONSUMER_ACE_KG_METHOD_V1
doc_type: consumer_spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: cadrage
topic_keys:
  - consumer
  - ace-knowledge-graph
  - graph-visualization
  - usage
search_tags:
  - consumer:v1
  - ace_kg
  - visualization
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
created_at: 2026-04-24
---

# 08 — CONSUMER_ACE_KG_METHOD_V1

## 1_MASTER_TARGET

Définir une méthode robuste pour utiliser Ace Knowledge Graph comme **consumer visuel interactif** du graph produit par le Producer.

Le consumer ne modifie jamais la source canonique (repo), il sert uniquement à explorer et comprendre.

---

## 3_INITIAL_NEED

Permettre :

- visualisation multi-angles du repo
- exploration interactive des GO / docs / modules
- compréhension rapide des dépendances
- reprise instantanée des chantiers

---

## 7_CANONICAL_STATE

Selon la matrice gouvernante :

- le repo est la source de vérité ;
- le graph est une projection ;
- Ace KG est une surface de lecture ;
- aucune donnée du graph ne remplace le canon.

---

## 9_SELECTED_SOLUTION

### Mode d'utilisation

Ace KG est utilisé via **prompt structuré**.

Input = document structuré dérivé du `graph_bundle.json`.

---

## 10_SELECTED_SETUP

### Format d'entrée recommandé

Transformer `graph_bundle.json` en Markdown lisible :

```text
PROJECT: opt-trading
SOURCE: repo canonical

NODES:
- GO: ...
- DOC: ...
- MODULE: ...

EDGES:
- GO_A BELONGS_TO GO_B
- DOC_X DOCUMENTS GO_A
```

---

## 11_KEY_DECISIONS

- ne pas injecter JSON brut si Ace KG ne le supporte pas
- privilégier Markdown structuré
- garder IDs lisibles
- conserver types explicites

---

## 12_INVARIANTS

- ne jamais modifier repo via Ace KG
- ne jamais considérer Ace KG comme source
- toujours pouvoir reconstruire depuis repo

---

## 5_GO_PLAN — usage concret

### Étape 1 — générer bundle

```bash
kg export
```

### Étape 2 — générer Markdown

```bash
kg render --format md
```

### Étape 3 — envoyer à Ace KG

Prompt :

```text
Create an interactive knowledge graph from this repository structure.
Respect node types and relationships.
Do not infer missing relations.
Highlight ACTIVE GO, dependencies and resume points.
```

---

## 9_SELECTED_SOLUTION — vues recommandées

### Vue GO
- parents / enfants
- dépendances

### Vue Docs
- doc → GO

### Vue Modules
- module → scripts → machine

### Vue Reprise
- GO → resume_point → TODO

### Vue Risque
- GO → GAP / RISK

---

## 15_REMAINING_GAP

- vérifier capacité Ace KG à gérer grands graphes
- vérifier limite de tokens
- tester granularité optimale

---

## 16_TODO

- créer renderer Markdown optimisé
- tester prompts multiples
- tester découpage graph en sous-graphes

---

## 17_RESUME_POINT

Consumer prêt.
Next : `09_graph_views_v1.md`

---

## 18_TO_DOCUMENT

- graph views
- acceptance tests

---

## 19_TO_REMEMBER

TAG: ACE_KG_USAGE_METHOD_V1
Ace KG est utilisé via transformation Markdown du graph et exploration interactive.
