---
doc_id: GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01_00_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: repo_knowledge_graph
go_id: GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01
parent_go: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_GRAPHICAL_STRUCTURING_01/90_CLOSEOUT.md
updated_at: 2026-05-07
topic_keys:
  - opt-trading
  - repo_kg
  - producer
  - graph_bundle
  - views
  - mermaid
links:
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_GRAPHICAL_STRUCTURING_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md
  - producer_repo_kg_v1.py
  - graph_bundle.json
---

# 00_CADRAGE - GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01

## 1_MASTER_TARGET

Faire evoluer `producer_repo_kg_v1.py` et `graph_bundle.json` pour mieux supporter les vues graphiques V1 sans changer le role canonique du repo.

But operatoire :

`repo reel -> Producer -> graph_bundle.json -> vues Mermaid V1 plus fideles`

## 2_INPUT_STATE

Le lot `GO_OPT_TRADING_REPO_KG_CHILD_GRAPHICAL_STRUCTURING_01` est clos en `PASS_LIMITED`.

Limites explicites a traiter dans ce lot :

1. vue apps encore hybride ;
2. vue machines sans cartographie runtime suffisante ;
3. vue branches sans rattachement branche -> GO assez direct ;
4. `HAS_GAP` pas exploite directement dans les cartes ;
5. reprise et `NEXT_GO` pas assez fideles ;
6. statuts GO trop bruyants ou trop plats selon les sources ;
7. `validation.valid=false` precedemment declenche par une heuristique trop agressive autour des credentials.

## 3_OBJECTIF_DE_PROJECTION

Le bundle doit sortir directement ce qu'il faut pour regenerer des vues plus fideles :

1. noeuds `APP` ;
2. relations `RUNS_ON` ;
3. branche -> GO via edge bundle explicite ;
4. edges `HAS_GAP` serialises ;
5. reprise / `NEXT_GO` sans faux positifs ;
6. statuts GO ramenes a un vocabulaire exploitable ;
7. validation sans faux negatif lie au simple mot `credentials`.

## 4_CONTRAINTES

1. repo = source canonique ;
2. `graph_bundle.json` = projection reconstruisible ;
3. ne pas inventer de relations ;
4. ne pas scanner ni exposer de secrets ;
5. ne pas modifier le runtime trading ;
6. ne pas faire d'integration externe dans ce GO.

## 5_ACCEPTANCE

Verdict attendu : `PASS` si les vues Mermaid V1 peuvent etre rejouees avec une meilleure fidelite depuis `graph_bundle.json`.

## 17_RESUME_POINT

```text
producer_repo_kg_v1.py
-> verifier les statuts GO, NEXT_GO, APP, RUNS_ON et branch -> GO
-> regenerer graph_bundle.json
-> rejouer les vues Mermaid V1 du lot
```

## RISKS

- À qualifier.
