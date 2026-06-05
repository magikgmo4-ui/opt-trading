---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_CADRAGE_PARENT
doc_type: cadrage_parent
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - knowledge-graph
  - repo-graph
  - producer-consumer
  - ace-knowledge-graph
search_tags:
  - surface:docs/chantiers
  - doc_role:cadrage_parent
  - graph:projection
  - producer:repo
  - consumer:ace_kg
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
created_at: 2026-04-24
---

# GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01 — Cadrage parent

## 1_MASTER_TARGET

Créer un chantier parent pour concevoir un système **repo → knowledge graph** permettant de visualiser `opt-trading` sous plusieurs angles : GO, docs, modules, branches, machines, décisions, dépendances, reprises et risques.

## 3_INITIAL_NEED

Le connecteur ACE Knowledge Graph peut servir de couche de visualisation et de navigation, mais il ne doit pas devenir source canonique. Pour le rendre fonctionnel, le repo doit produire une projection exploitable via un module **Producer**, puis une méthode **Consumer** doit décrire comment l'app graph consomme cette projection.

## 4_MASTER_PROJECT_PLAN

Pipeline cible :

```text
Repo opt-trading
  ↓
Module Producer lecture seule
  ↓
Graph bundle standardisé
  ↓
ACE Knowledge Graph / app consumer
  ↓
Visualisation multi-angles du repo
```

## 5_GO_PLAN

GO parent :

```text
GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
```

GO enfants proposés :

| GO | Rôle |
|---|---|
| `GO_OPT_TRADING_REPO_KG_PRODUCER_CONSUMER_CADRAGE_01` | cadrer schéma + Producer + Consumer |
| `GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01` | créer extracteur lecture seule |
| `GO_OPT_TRADING_REPO_KG_SCHEMA_VALIDATE_01` | valider nodes/edges |
| `GO_OPT_TRADING_REPO_KG_CONSUMER_METHOD_01` | documenter méthode ACE KG |
| `GO_OPT_TRADING_REPO_KG_VISUAL_REPORTS_01` | produire vues graphiques |
| `GO_OPT_TRADING_REPO_KG_CLOSEOUT_01` | fermer avec tests et reprise |

## 6_FINAL_TARGET

Livrable cible principal :

```text
graph_bundle.json
```

Ce bundle doit contenir :

```json
{
  "meta": {},
  "nodes": [],
  "edges": [],
  "views": [],
  "validation": {}
}
```

## 7_CANONICAL_STATE

- Repo canonique : `magikgmo4-ui/opt-trading`
- Branche de base : `sot/mainline`
- Branche dédiée ouverte : `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01`
- Graph externe : projection consommable, non source de vérité
- Source canonique : GitHub repo + docs + Git state réel

## 8_VALIDATED_PLAN

1. Ouvrir le chantier parent sur branche dédiée.
2. Documenter le cadrage complet Producer/Consumer.
3. Séparer les gaps restants et TODO opératoires.
4. Préparer le GO enfant d'implémentation, sans coder le module dans ce lot.

## 11_KEY_DECISIONS

1. `opt-trading` reste la source canonique.
2. ACE KG ou autre app graph consomme une projection.
3. Le Producer doit être lecture seule au départ.
4. La visualisation doit être multi-angles.
5. Les relations critiques doivent être sourcées par docs ou Git, non inventées.

## 12_INVARIANTS

- Ne pas faire du graph externe la source canonique.
- Ne pas scanner secrets, `.env`, tokens, clés API.
- Ne pas refactorer le repo pendant ce cadrage.
- Ne pas créer de relation critique sans preuve documentaire ou Git.
- Toute hypothèse reste marquée `HYPOTHESIS`.

## 17_RESUME_POINT

Reprendre ici :

```text
docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/
```

Lire dans l'ordre :

1. `01_cadrage_parent.md`
2. `02_integrale_plan_producteur_consommateur.md`
3. `03_remaining_gap_todo.md`
4. `SESSION_REPRISE.txt`

## RISKS

- À qualifier.
