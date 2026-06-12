---
doc_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01_GRAPH_SCHEMA_V1
doc_type: graph_schema
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: OPEN
lifecycle_stage: cadrage
topic_keys:
  - repo-graph
  - schema
  - nodes
  - edges
  - producer
  - consumer
search_tags:
  - graph:schema_v1
  - producer:contract
  - consumer:ace_kg
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/05_master_plan_final_product.md
created_at: 2026-04-24
---

# 06 — GRAPH_SCHEMA_V1

## 1_MASTER_TARGET

Définir le contrat de graph V1 pour transformer le repo `opt-trading` en projection knowledge graph exploitable par :

- un Producer lecture seule ;
- des renderers JSON / Markdown / Mermaid / CSV ;
- un Consumer externe comme Ace Knowledge Graph ;
- une future couche d'agents ou d'audit automatisé.

Le graph est une **projection reconstruisible**, jamais une source canonique.

---

## 3_INITIAL_NEED

Le repo contient plusieurs couches :

- gouvernance ;
- GO actifs / ouverts / références / clos ;
- docs chantier ;
- modules runtime ;
- branches Git ;
- machines ;
- décisions ;
- invariants ;
- points de reprise ;
- gaps et risques.

Le schéma doit permettre de visualiser ces couches sans les confondre.

---

## 7_CANONICAL_STATE

Sources canon V1 :

| Source | Rôle |
|---|---|
| `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` | autorité documentaire maître |
| `docs/index/GO_INDEX.md` | vérité locale de liste des GO non clos |
| `docs/index/GO_CLOSED_INDEX.md` | vérité locale des GO clos si présent |
| `docs/index/REPRISE.md` | support de reprise opératoire |
| `docs/index/BRANCH_STATE.md` | état branches si présent |
| `docs/chantiers/<GO_...>/` | surface chantier canonique |
| `modules/` | surface modules/runtime |
| Git refs | branches / commits / support réel |

---

# 8_VALIDATED_PLAN — structure du bundle

## 8.1 Bundle racine

```json
{
  "schema_version": "repo_kg.v1",
  "meta": {},
  "nodes": [],
  "edges": [],
  "views": [],
  "validation": {},
  "provenance": {}
}
```

## 8.2 Champs meta obligatoires

```json
{
  "repo": "opt-trading",
  "repository_full_name": "magikgmo4-ui/opt-trading",
  "base_branch": "sot/mainline",
  "producer_version": "0.1.0",
  "generated_at": "ISO-8601",
  "source_commit": "<sha>",
  "mode": "read_only"
}
```

---

# 9_SELECTED_SOLUTION — Nodes V1

## 9.1 Format node minimal

```json
{
  "id": "stable_unique_id",
  "type": "GO",
  "label": "Human label",
  "status": "OPEN",
  "source_path": "docs/...",
  "source_ref": "sot/mainline",
  "confidence": "ESTABLISHED",
  "tags": [],
  "properties": {}
}
```

## 9.2 Types de nodes autorisés V1

| Type | Description | Source typique |
|---|---|---|
| `REPO` | repo canonique | GitHub repo metadata |
| `BRANCH` | branche Git | Git refs |
| `COMMIT` | commit Git si pertinent | Git history |
| `GO` | chantier / GO / sous-GO | `GO_INDEX.md`, `docs/chantiers/` |
| `DOC` | document canonique ou support | `docs/**` |
| `GOVERNANCE` | matrice / règle stable | `docs/governance/**` |
| `INDEX` | index opératoire | `docs/index/**` |
| `MODULE` | module durable | `modules/<name>/` |
| `SCRIPT` | wrapper ou script opératoire | `cmd.sh`, `menu.sh`, `sanity_check.sh`, scripts |
| `TEST` | test ou sanity | `tests/`, `sanity_check.sh` |
| `MACHINE` | machine connue | docs / config / mémoire canonique |
| `SERVICE` | service runtime | docs runtime, systemd refs |
| `DECISION` | décision validée | `03_decisions.md`, closeout |
| `INVARIANT` | règle à ne pas rouvrir | cadrage, closeout, governance |
| `RESUME_POINT` | point de reprise | `SESSION_REPRISE.txt`, `REPRISE.md` |
| `RISK` | risque établi | docs, audit, validation |
| `GAP` | manque restant | `15_REMAINING_GAP`, audit |
| `TODO` | action prochaine | `16_TODO`, reprise |
| `VIEW` | vue graphique prédéfinie | spec graph views |
| `CONSUMER` | app consommatrice | Ace KG, Mermaid, Cytoscape |
| `PRODUCER` | module producteur | futur `modules/repo_knowledge_graph` |

---

## 9.3 Champs properties par type

### GO

```json
{
  "go_id": "GO_...",
  "parent_go_id": "GO_... or null",
  "status": "OPEN|ACTIVE|REFERENCE|CLOSED|PASS|UNKNOWN",
  "priority": "P0|P1|P2|null",
  "has_chantier_folder": true,
  "source_table": "GO_INDEX",
  "resume_point": "path or null"
}
```

### DOC

```json
{
  "path": "docs/...",
  "doc_id": "frontmatter doc_id or null",
  "doc_type": "frontmatter doc_type or unknown",
  "go_id": "frontmatter go_id or null",
  "source_kind": "canonical|derived|reference|unknown",
  "updated_at": "YYYY-MM-DD or null"
}
```

### MODULE

```json
{
  "path": "modules/<name>",
  "has_cmd": true,
  "has_menu": true,
  "has_sanity": true,
  "has_readme": true,
  "runtime_role": "producer|consumer|runtime|tooling|unknown"
}
```

### MACHINE

```json
{
  "name": "admin-trading|student|db-layer|cursor-ai",
  "role": "runtime|dev|db|windows_gui|unknown",
  "confidence": "ESTABLISHED|HYPOTHESIS"
}
```

### DECISION

```json
{
  "decision_id": "D-XX or stable generated id",
  "text": "decision summary",
  "source_path": "docs/.../03_decisions.md",
  "scope": "GO|MODULE|REPO|GOVERNANCE"
}
```

### INVARIANT

```json
{
  "invariant_id": "INV-XX or stable generated id",
  "text": "invariant summary",
  "source_path": "docs/...",
  "do_not_reopen_without": "explicit reason|new proof|new GO"
}
```

---

# 10_SELECTED_SETUP — Edges V1

## 10.1 Format edge minimal

```json
{
  "id": "edge_stable_id",
  "source": "node_id_a",
  "target": "node_id_b",
  "type": "DOCUMENTS",
  "confidence": "ESTABLISHED",
  "source_path": "docs/...",
  "evidence": "short evidence text",
  "properties": {}
}
```

## 10.2 Types de edges autorisés V1

| Edge | Sens | Exemple |
|---|---|---|
| `HAS_BRANCH` | repo → branch | repo has branch |
| `HAS_GO` | repo/index → GO | GO_INDEX lists GO |
| `HAS_DOC` | GO → DOC | chantier contains doc |
| `DOCUMENTS` | DOC → GO/MODULE | doc documents object |
| `BELONGS_TO` | child → parent | sous-GO belongs parent |
| `DEPENDS_ON` | A → B | module/GO depends on object |
| `IMPLEMENTS` | MODULE → GO | module implements GO target |
| `RUNS_ON` | MODULE/SERVICE → MACHINE | runtime placement |
| `VALIDATES` | TEST/SCRIPT → MODULE/GO | sanity validates surface |
| `HAS_DECISION` | GO/DOC → DECISION | decisions document |
| `HAS_INVARIANT` | GO/DOC → INVARIANT | invariant documented |
| `HAS_GAP` | GO/DOC → GAP | gap documented |
| `HAS_TODO` | GO/DOC → TODO | TODO documented |
| `RESUMES_AT` | GO → RESUME_POINT | reprise point |
| `SUPERSEDES` | DOC → DOC | newer doc supersedes old |
| `REFERENCES` | DOC → DOC/GO | generic reference |
| `CONSUMES` | CONSUMER → bundle/view | Ace KG consumes projection |
| `PRODUCES` | PRODUCER → bundle/view | Producer generates graph |
| `BLOCKS` | RISK/GAP → GO | risk blocks chantier |
| `DERIVED_FROM` | projection → source | graph derived from repo doc |

---

## 10.3 Sens de lecture strict

- `DOCUMENTS`: le document documente l'objet.
- `BELONGS_TO`: l'enfant pointe vers le parent.
- `DEPENDS_ON`: le consommateur pointe vers la dépendance.
- `RUNS_ON`: l'objet runtime pointe vers la machine.
- `VALIDATES`: la preuve/test pointe vers ce qu'elle valide.
- `DERIVED_FROM`: la projection pointe vers la source.

---

# 11_KEY_DECISIONS — règles de preuve

## 11.1 Niveaux de confiance

| Confidence | Usage |
|---|---|
| `ESTABLISHED` | preuve directe dans repo, doc ou Git |
| `INFERRED` | relation dérivée par règle stable documentée |
| `HYPOTHESIS` | relation possible non validée |
| `CONTRADICTION` | conflit entre sources |
| `UNKNOWN` | donnée absente ou non parsée |

## 11.2 Règles de preuve minimale

Une relation `ESTABLISHED` exige au moins une source :

- ligne `GO_INDEX.md` ;
- frontmatter doc ;
- chemin de fichier ;
- Git ref ;
- fichier de décisions ;
- closeout ;
- script réel ;
- sanity/test réel.

## 11.3 Règles de dérivation autorisées

| Dérivation | Condition |
|---|---|
| doc → GO | `go_id` frontmatter ou chemin chantier clair |
| GO → folder | dossier `docs/chantiers/<GO_ID>/` existe |
| module → script | script présent dans module |
| repo → branch | branche présente Git |
| GO → parent | ligne `GO_INDEX.md` ou document parent explicite |
| doc → governance | chemin `docs/governance/` + doc_type governance |

## 11.4 Dérivations interdites

- déduire un parent depuis le seul nom d'une branche ;
- déduire une machine depuis une mémoire non sourcée sans marquer `HYPOTHESIS` ;
- déduire un module actif sans script ou doc ;
- déduire un statut `PASS` sans closeout ou index clos ;
- créer une relation Ace KG → repo comme écriture réelle.

---

# 12_INVARIANTS

- Le graph est une projection, pas une vérité.
- Le repo est prioritaire sur toute visualisation.
- Ace KG est consumer, pas producer canonique.
- Le Producer V1 est lecture seule.
- Aucun secret ne doit être lu, exporté ou indexé.
- Les `.env`, tokens, clés, credentials sont hors périmètre.
- Les relations critiques doivent être sourcées.
- Les hypothèses doivent rester visibles comme hypothèses.
- Le graph doit pouvoir être supprimé et régénéré sans perte canonique.

---

# 13_ESTABLISHED — statuts normalisés

## GO status V1

| Statut | Sens |
|---|---|
| `OPEN` | ouvert mais pas forcément actif immédiatement |
| `ACTIVE` | actif dans l'opératoire courant |
| `REFERENCE` | référence utile mais pas chantier actif |
| `CLOSED` | clos |
| `PASS` | clos avec validation positive |
| `FAIL` | clos ou arrêté avec échec |
| `UNKNOWN` | non déterminé |

## Document status V1

| Statut | Sens |
|---|---|
| `canonical` | source canonique |
| `reference` | référence stable |
| `draft` | brouillon |
| `deprecated` | déclassé |
| `unknown` | non déterminé |

---

# 14_HYPOTHESIS

À valider au Producer :

- `GO_INDEX.md` est assez structuré pour parser le tableau canonique automatiquement.
- Les dossiers `docs/chantiers/<GO_ID>/` peuvent être mappés sans collision.
- Les frontmatters sont assez réguliers pour extraire `doc_id`, `doc_type`, `go_id`, `status`.
- Ace KG peut consommer soit JSON, soit Markdown structuré généré depuis JSON.

---

# 15_REMAINING_GAP

- Définir exactement l'ordre de priorité des sources en cas de conflit.
- Définir le format stable d'ID pour chaque node.
- Définir la stratégie d'export compatible Ace KG.
- Définir si les commits sont inclus en V1 ou repoussés V2.
- Définir les limites de profondeur de scan modules.
- Définir comment intégrer les machines sans exposer d'informations sensibles.

---

# 16_TODO

## P0 — avant implémentation

1. Créer `07_producer_spec_v1.md`.
2. Créer `08_consumer_ace_kg_method_v1.md`.
3. Créer `09_graph_views_v1.md`.
4. Créer `10_acceptance_tests_v1.md`.
5. Créer `11_security_and_no_secret_policy.md`.

## P1 — prototype

1. Créer module `modules/repo_knowledge_graph/`.
2. Ajouter `cmd.sh`, `menu.sh`, `sanity_check.sh`.
3. Générer `graph_bundle.demo.json`.
4. Générer `graph_bundle.demo.md` pour Ace KG.

## P2 — validation

1. Valider coverage GO_INDEX.
2. Valider absence secrets.
3. Valider vues multi-angles.
4. Produire closeout.

---

# 17_RESUME_POINT

Reprise immédiate :

```text
GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
→ lire 05_master_plan_final_product.md
→ lire 06_graph_schema_v1.md
→ créer 07_producer_spec_v1.md
```

---

# 18_TO_DOCUMENT

À produire ensuite :

- `07_producer_spec_v1.md`
- `08_consumer_ace_kg_method_v1.md`
- `09_graph_views_v1.md`
- `10_acceptance_tests_v1.md`
- `11_security_and_no_secret_policy.md`

---

# 19_TO_REMEMBER

Memory Bricks projet :

```text
TAG: REPO_KG_SCHEMA_V1
Le graph V1 de opt-trading est une projection reconstruisible avec nodes typés, edges typées, confiance explicite et preuves source. Il ne remplace jamais le repo canonique.

TAG: ACE_KG_CONSUMER_ONLY
Ace Knowledge Graph est utilisé comme consumer visuel interactif. Le Producer repo reste nécessaire pour produire les données structurées.

TAG: GRAPH_PROOF_DISCIPLINE
Toute relation critique dans le graph doit être sourcée. Les hypothèses restent marquées HYPOTHESIS.
```

## RISKS

- À qualifier.
