---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_RESEARCH_NOTES
doc_type: research_notes
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: research
topic_keys:
  - ace-knowledge-graph
  - chatgpt-apps
  - repo-graph
  - graph-consumer
search_tags:
  - app:ace_knowledge_graph
  - source:web_research
  - graph:consumer
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/01_cadrage_parent.md
created_at: 2026-04-24
---

# 02 — Research notes : Ace Knowledge Graph + repo graph

## 13_ESTABLISHED

### Ace Knowledge Graph — capacité publique observée

La fiche app ChatGPT publique décrit Ace Knowledge Graph comme une app destinée à transformer des documents et sujets en graphes interactifs.

Capacités indiquées publiquement :

- visualiser des fichiers et sujets avec des knowledge graphs interactifs ;
- transformer des documents en réseaux structurés ;
- cliquer sur des nodes pour expliquer des concepts ;
- cliquer sur des relations pour clarifier les liens ;
- app classée avec capacités `Interactive` et `Writes` ;
- développeur indiqué : `Sider AI` ;
- cas d'usage publics : recherche, apprentissage, analyse de relations complexes.

### OpenAI Apps / Connectors — cadre général

Les apps/connectors ChatGPT servent à connecter ChatGPT à des outils et informations externes. Selon les capacités exposées par l'app, elles peuvent permettre recherche, référence, interaction et parfois actions.

### Limite critique pour notre usage

Ace Knowledge Graph n'est pas documenté publiquement comme outil natif de lecture Git, de scan GitHub, de commit ou de synchronisation repo.

Donc, pour `opt-trading`, il faut traiter Ace KG comme **consumer graph interactif**, pas comme producteur de vérité repo.

## 7_CANONICAL_STATE

Pour `opt-trading`, le canon existant impose :

- réalité prouvée du repo avant reconstruction documentaire ;
- matrice maître comme autorité documentaire ;
- `GO_INDEX.md` comme vérité locale de liste GO ;
- `docs/chantiers/<GO_...>/` comme surface chantier ;
- branche Git comme support, non source produit ;
- surfaces dérivées et registry comme projections, non souveraines.

## 11_KEY_DECISIONS

1. Ace KG consomme une projection, il ne gouverne pas le repo.
2. Le Producer doit vivre côté repo ou outil adjacent contrôlé.
3. Le bundle graph doit être reconstruisible depuis `opt-trading`.
4. Les nodes/edges doivent pointer vers des sources repo vérifiables.
5. Toute relation non prouvée reste `HYPOTHESIS`.

## 14_HYPOTHESIS

À valider dans l'app Ace KG :

- accepte-t-elle un import JSON brut ?
- accepte-t-elle un document Markdown contenant nodes/edges ?
- accepte-t-elle un prompt long structuré comme source de graph ?
- conserve-t-elle les graphes entre sessions ?
- expose-t-elle une API d'update ou seulement une génération interactive ?
- permet-elle plusieurs graphes/vues pour un même projet ?

## 15_REMAINING_GAP

- Format d'import exact Ace KG inconnu.
- Limite de taille des documents inconnue.
- Granularité nodes/edges réellement exploitable inconnue.
- Export depuis Ace KG vers JSON/CSV non confirmé.
- Différentiel d'update non confirmé.

## 16_TODO

### Test Consumer manuel minimal

Créer un document source compact :

```text
Projet: opt-trading
Source canonique: repo GitHub + docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
Noeuds: GO, DOC, MODULE, BRANCH, MACHINE, DECISION, INVARIANT, RESUME_POINT, RISK
Relations: DOCUMENTS, DEPENDS_ON, BELONGS_TO, RUNS_ON, VALIDATES, RESUMES_AT, HAS_INVARIANT
Objectif: visualiser la gouvernance repo et la reprise multi-chantiers.
```

Puis demander à Ace KG :

```text
@Ace Knowledge Graph Create an interactive knowledge graph from this structured repo map. Keep repo as source of truth. Show GO, docs, modules, machines, branches and resume points as typed nodes. Show typed relationships and isolate unvalidated hypotheses.
```

### Test Producer minimal

Avant implémentation complète, produire un bundle `graph_bundle.demo.json` limité à :

- `GO_INDEX.md`
- `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- le chantier parent courant
- branches Git parent/enfant connues

## 17_RESUME_POINT

Prochaine reprise : créer `04_graph_schema_v1.md`, puis `05_producer_spec_v1.md`, puis `06_consumer_ace_kg_method_v1.md`.

## RISKS

- À qualifier.
