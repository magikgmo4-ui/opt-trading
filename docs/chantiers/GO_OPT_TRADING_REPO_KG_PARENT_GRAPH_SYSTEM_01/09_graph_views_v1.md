---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_GRAPH_VIEWS_V1
doc_type: graph_views_spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: cadrage
topic_keys:
  - repo-graph
  - graph-views
  - visualization
  - continuity
  - opt-trading
search_tags:
  - graph:views_v1
  - visualization:multi_angle
  - consumer:ace_kg
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/06_graph_schema_v1.md
point_de_reprise: "Créer ensuite 10_acceptance_tests_v1.md"
created_at: 2026-04-24
---

# 09 — GRAPH_VIEWS_V1

## 1_MASTER_TARGET

Définir les vues graphiques V1 nécessaires pour visualiser `opt-trading` sous tous les angles utiles à ton usage : gouvernance, reprise, modules, machines, branches, risques, Producer/Consumer et final product.

Le but n'est pas seulement de dessiner un graph. Le but est de pouvoir répondre vite à ces questions :

- Où en est le repo ?
- Quel GO reprendre ?
- Quelle branche porte quel chantier ?
- Quel module existe vraiment ?
- Quelle machine exécute quoi ?
- Quel document est canonique ?
- Où sont les gaps ?
- Qu'est-ce qui est établi vs hypothèse ?

---

## 7_CANONICAL_STATE

Le graph reste une projection.

Sources souveraines :

1. état Git réel ;
2. `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` ;
3. `docs/index/GO_INDEX.md` ;
4. `docs/chantiers/<GO_...>/` ;
5. `docs/index/BRANCH_STATE.md` pour la surface branches ;
6. modules et scripts réels du repo.

---

# 8_VALIDATED_PLAN — vues obligatoires

## Vue 1 — `GO_MAP`

### Objectif

Visualiser la structure des chantiers.

### Nodes requis

- `GO`
- `DOC`
- `RESUME_POINT`
- `TODO`
- `GAP`

### Edges requis

- `BELONGS_TO`
- `HAS_DOC`
- `RESUMES_AT`
- `HAS_TODO`
- `HAS_GAP`

### Questions couvertes

- Quels GO sont ouverts ?
- Quels GO sont actifs ?
- Quel parent contient quel sous-GO ?
- Où reprendre ?

### Filtre par défaut

```text
node.type in [GO, DOC, RESUME_POINT, TODO, GAP]
status in [OPEN, ACTIVE, REFERENCE]
```

---

## Vue 2 — `DOC_CANON_MAP`

### Objectif

Voir les documents qui gouvernent réellement le repo.

### Nodes requis

- `GOVERNANCE`
- `INDEX`
- `DOC`
- `GO`

### Edges requis

- `REFERENCES`
- `DOCUMENTS`
- `DERIVED_FROM`

### Questions couvertes

- Quel document est source canonique ?
- Quel document est une annexe ?
- Quel document ne doit pas gouverner ?
- Quels docs servent un GO ?

### Filtre par défaut

```text
source_kind in [canonical, reference]
```

---

## Vue 3 — `MODULE_SURFACE_MAP`

### Objectif

Visualiser les modules réels et leurs surfaces opératoires.

### Nodes requis

- `MODULE`
- `SCRIPT`
- `TEST`
- `DOC`
- `GO`

### Edges requis

- `IMPLEMENTS`
- `VALIDATES`
- `DOCUMENTS`
- `HAS_DOC`

### Questions couvertes

- Quels modules existent vraiment ?
- Quels modules ont `cmd.sh`, `menu.sh`, `sanity_check.sh` ?
- Quels modules sont documentés ?
- Quel GO justifie quel module ?

### Filtre par défaut

```text
node.type in [MODULE, SCRIPT, TEST, DOC, GO]
```

---

## Vue 4 — `MACHINE_RUNTIME_MAP`

### Objectif

Relier les composants à tes machines réelles.

### Machines V1

- `admin-trading`
- `student`
- `db-layer`
- `cursor-ai`

### Nodes requis

- `MACHINE`
- `MODULE`
- `SERVICE`
- `DOC`
- `GO`

### Edges requis

- `RUNS_ON`
- `DOCUMENTS`
- `DEPENDS_ON`

### Questions couvertes

- Qu'est-ce qui tourne sur `admin-trading` ?
- Quelle machine sert au dev ?
- Quelle machine sert au runtime ?
- Quelle machine sert à la DB / ingestion ?
- Où sont les gaps de runtime ?

### Règle de confiance

Toute relation machine non prouvée doit être `HYPOTHESIS`.

---

## Vue 5 — `BRANCH_WORK_MAP`

### Objectif

Voir le support Git réel des chantiers.

### Nodes requis

- `BRANCH`
- `GO`
- `DOC`
- `COMMIT`

### Edges requis

- `HAS_BRANCH`
- `DOCUMENTS`
- `REFERENCES`

### Questions couvertes

- Quelle branche porte quel GO ?
- Quelle branche est active ?
- Quelle branche est seulement référence ?
- Quelle branche doit être closeout / merge / revue ?

### Source prioritaire

- Git refs réels
- `docs/index/BRANCH_STATE.md`

---

## Vue 6 — `RESUME_MAP`

### Objectif

Reprendre une session sans perdre le fil.

### Nodes requis

- `GO`
- `RESUME_POINT`
- `TODO`
- `DOC`
- `GAP`

### Edges requis

- `RESUMES_AT`
- `HAS_TODO`
- `HAS_GAP`
- `DOCUMENTS`

### Questions couvertes

- Où reprendre maintenant ?
- Quel fichier lire d'abord ?
- Quelle action suit ?
- Qu'est-ce qui manque encore ?

### Sortie minimale attendue

Chaque GO ouvert doit pouvoir produire :

```text
GO_ID
status
branch
folder
read_first
next_action
blocking_gap
```

---

## Vue 7 — `RISK_GAP_MAP`

### Objectif

Voir ce qui peut casser la continuité ou provoquer une fausse lecture.

### Nodes requis

- `RISK`
- `GAP`
- `GO`
- `DOC`
- `INVARIANT`
- `DECISION`

### Edges requis

- `HAS_GAP`
- `BLOCKS`
- `HAS_INVARIANT`
- `HAS_DECISION`

### Questions couvertes

- Quels gaps restent ?
- Quels risques bloquent ?
- Quelle hypothèse ne doit pas être traitée comme établie ?
- Quels invariants protègent le repo ?

---

## Vue 8 — `PRODUCER_CONSUMER_MAP`

### Objectif

Visualiser le système Repo KG lui-même.

### Nodes requis

- `PRODUCER`
- `CONSUMER`
- `DOC`
- `GO`
- `VIEW`

### Edges requis

- `PRODUCES`
- `CONSUMES`
- `DOCUMENTS`
- `DERIVED_FROM`

### Questions couvertes

- Que produit le Producer ?
- Que consomme Ace KG ?
- Quelle vue vient de quel bundle ?
- Quelle documentation gouverne le flux ?

---

# 9_SELECTED_SOLUTION — formats de rendu par vue

| Vue | JSON | Markdown | Mermaid | Ace KG |
|---|---:|---:|---:|---:|
| `GO_MAP` | oui | oui | oui | oui |
| `DOC_CANON_MAP` | oui | oui | oui | oui |
| `MODULE_SURFACE_MAP` | oui | oui | oui | oui |
| `MACHINE_RUNTIME_MAP` | oui | oui | oui | oui |
| `BRANCH_WORK_MAP` | oui | oui | oui | oui |
| `RESUME_MAP` | oui | oui | optionnel | oui |
| `RISK_GAP_MAP` | oui | oui | oui | oui |
| `PRODUCER_CONSUMER_MAP` | oui | oui | oui | oui |

---

# 10_SELECTED_SETUP — rendu Markdown pour Ace KG

Chaque vue doit pouvoir être rendue sous cette forme :

```markdown
# VIEW: GO_MAP

## NODES
- GO | GO_X | status=OPEN | confidence=ESTABLISHED
- DOC | docs/chantiers/GO_X/01_cadrage_parent.md | source_kind=canonical

## EDGES
- GO_X HAS_DOC docs/chantiers/GO_X/01_cadrage_parent.md | confidence=ESTABLISHED
- GO_X RESUMES_AT SESSION_REPRISE | confidence=ESTABLISHED

## QUESTIONS
- Quels GO sont ouverts ?
- Quel fichier lire d'abord ?
```

---

# 11_KEY_DECISIONS

1. Les vues sont des projections filtrées du même `graph_bundle.json`.
2. Une vue ne doit jamais modifier le graph source.
3. Une vue ne doit jamais masquer les `HYPOTHESIS`.
4. Les vues doivent servir ton usage opératoire, pas seulement être jolies.
5. `RESUME_MAP` et `RISK_GAP_MAP` sont prioritaires pour la continuité.

---

# 12_INVARIANTS

- Aucune vue ne remplace `GO_INDEX.md`.
- Aucune vue ne remplace `BRANCH_STATE.md`.
- Aucune vue ne remplace `REPRISE.md`.
- Les vues doivent afficher la confiance (`ESTABLISHED`, `HYPOTHESIS`, etc.).
- Toute vue doit pouvoir être reconstruite depuis le bundle.
- Les données sensibles restent hors export.

---

# 13_ESTABLISHED

Les vues V1 nécessaires à ton usage sont :

1. `GO_MAP`
2. `DOC_CANON_MAP`
3. `MODULE_SURFACE_MAP`
4. `MACHINE_RUNTIME_MAP`
5. `BRANCH_WORK_MAP`
6. `RESUME_MAP`
7. `RISK_GAP_MAP`
8. `PRODUCER_CONSUMER_MAP`

---

# 14_HYPOTHESIS

À valider lors du prototype :

- Ace KG accepte un rendu Markdown multi-vues.
- Une vue complète ne dépasse pas les limites de taille de l'app.
- Les sous-graphes par vue sont plus lisibles qu'un graph global unique.
- Mermaid reste utile pour une vue rapide mais Ace KG est plus adapté à l'exploration.

---

# 15_REMAINING_GAP

- Définir les seuils de taille d'une vue.
- Définir le tri des nodes dans chaque vue.
- Définir les priorités visuelles : statut, type, confiance.
- Définir l'export `view_<name>.md`.
- Définir l'export `view_<name>.mmd`.
- Définir les tests d'acceptation par vue.

---

# 16_TODO

## P0

1. Créer `10_acceptance_tests_v1.md`.
2. Créer `11_security_and_no_secret_policy.md`.
3. Créer `SESSION_REPRISE.md` ou mettre à jour `SESSION_REPRISE.txt`.

## P1

1. Définir renderer Markdown par vue.
2. Définir renderer Mermaid pour les vues simples.
3. Définir prompts Ace KG par vue.

## P2

1. Implémenter `kg render --view GO_MAP --format md`.
2. Implémenter `kg render --view RESUME_MAP --format md`.
3. Tester import Ace KG.

---

# 17_RESUME_POINT

Reprise immédiate :

```text
GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
→ lire 06_graph_schema_v1.md
→ lire 07_producer_spec_v1.md
→ lire 08_consumer_ace_kg_method_v1.md
→ lire 09_graph_views_v1.md
→ créer 10_acceptance_tests_v1.md
```

---

# 18_TO_DOCUMENT

À documenter ensuite :

- `10_acceptance_tests_v1.md`
- `11_security_and_no_secret_policy.md`
- `SESSION_REPRISE.txt`

---

# 19_TO_REMEMBER

Memory Bricks projet :

```text
TAG: REPO_KG_VIEWS_V1
Les vues graph V1 pour opt-trading sont : GO_MAP, DOC_CANON_MAP, MODULE_SURFACE_MAP, MACHINE_RUNTIME_MAP, BRANCH_WORK_MAP, RESUME_MAP, RISK_GAP_MAP, PRODUCER_CONSUMER_MAP.

TAG: GRAPH_VIEW_IS_FILTER
Une vue graph est un filtre/re rendu du graph bundle. Elle ne remplace jamais une surface canonique comme GO_INDEX, BRANCH_STATE ou REPRISE.

TAG: RESUME_AND_RISK_FIRST
Pour l'usage quotidien du projet, RESUME_MAP et RISK_GAP_MAP sont prioritaires parce qu'elles accélèrent la reprise et empêchent les fausses lectures.
```

## RISKS

- À qualifier.
