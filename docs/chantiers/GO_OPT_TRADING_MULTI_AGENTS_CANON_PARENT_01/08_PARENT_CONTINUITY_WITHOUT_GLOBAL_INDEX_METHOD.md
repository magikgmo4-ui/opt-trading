---
doc_id: OPT_TRADING_MULTI_AGENTS_PARENT_CONTINUITY_WITHOUT_GLOBAL_INDEX_METHOD_01
doc_type: method
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: method
topic_keys:
  - opt-trading
  - multi_agents
  - parent_continuity
  - indexation
  - go_index
  - active_streams
  - next_go_candidates
  - reprise
  - git_friction
  - aggregation
topic_primary: parent_continuity
search_tags:
  - surface:chantier
  - doc_role:method
  - governance:parent_continuity
  - governance:indexation
  - git:friction_reduction
  - index:local_first
  - index:global_aggregation
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 9 - Méthode retenue recommandée"
updated_at: 2026-04-26
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/07_TRANSITIONAL_GLOBAL_INDEXATION_METHOD.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/GAP_INDEXATION.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
---

# 08_PARENT_CONTINUITY_WITHOUT_GLOBAL_INDEX_METHOD

## 1. Problème à résoudre

Les index globaux assurent la continuité du repo, mais leur modification systématique crée une friction structurelle :

- tous les chantiers finissent par toucher `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md` et `REPRISE.md` ;
- les fichiers deviennent volumineux ;
- les branches concurrentes produisent des conflits récurrents ;
- les connecteurs ou outils distants peuvent tronquer le contenu ;
- une petite ouverture de chantier entraîne une modification de fichiers globaux sans valeur ajoutée immédiate.

## 2. Objectif

Garder la continuité complète au niveau du parent sans modifier systématiquement les index globaux.

La continuité doit rester lisible depuis le dossier parent, puis être propagée vers les index globaux seulement par batch ou par nécessité forte.

## 3. Solutions possibles

### Solution A — Parent-local continuity pack

Chaque parent porte sa propre continuité complète dans son dossier :

```text
docs/chantiers/<GO_ID>/
  00_INITIAL_PROJECT_DOC.md
  PARENT_STATE.md
  NEXT.md
  ACTIVE.md
  DECISIONS.md
  INDEX_PATCH.md
  BRANCH_STATE.md
  90_CLOSEOUT.md
```

Rôle : les index globaux n'ont plus besoin d'être modifiés à chaque micro-étape. Le parent devient autosuffisant pour la reprise.

Avantages :

- faible friction Git ;
- continuité proche du travail réel ;
- reprise plus claire ;
- compatible multi-agents ;
- facile à transporter en bundle.

Limite :

- les index globaux peuvent être temporairement en retard.

### Solution B — Global index inbox

Créer une zone légère d'entrées atomiques :

```text
docs/index/inbox/<GO_ID>.md
```

Chaque chantier crée un fichier court dans `docs/index/inbox/` au lieu de modifier les index globaux.

Un lot agrégateur lit ensuite les fichiers inbox et met à jour les grands index.

Avantages :

- pas de conflit sur les gros fichiers ;
- un fichier par chantier ;
- facile à scanner ;
- compatible avec automatisation.

Limite :

- nécessite une convention de nettoyage après agrégation.

### Solution C — Registry YAML machine-readable

Créer une registry légère :

```text
registry/go_continuity/<GO_ID>.yaml
```

Chaque chantier ajoute son état sous forme structurée :

```yaml
go_id:
parent:
status:
priority:
branch:
refs:
next_action:
last_established:
gap:
```

Les index globaux deviennent des vues générées ou semi-générées.

Avantages :

- très bon pour tooling ;
- évite les gros diffs Markdown ;
- prêt pour extraction / dashboard / LocalCMS / graph.

Limite :

- ajoute une couche technique ;
- nécessite discipline de génération ou de validation.

### Solution D — Batch-only global index update

Règle simple : aucun chantier ne touche les index globaux directement.

Seuls des GO dédiés, par exemple :

```text
GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_01
```

appliquent les mises à jour globales.

Avantages :

- très robuste Git ;
- évite les conflits ;
- responsabilise l'agrégation.

Limite :

- les index globaux peuvent être décalés entre deux batchs.

### Solution E — Hybrid parent-local + inbox + batch

Combiner :

1. continuité complète dans le parent ;
2. entrée courte dans `docs/index/inbox/<GO_ID>.md` ;
3. batch périodique qui agrège vers les index globaux.

C'est la solution la plus équilibrée.

## 4. Méthode recommandée

La méthode recommandée est la Solution E.

```text
Parent continuity first
→ index inbox atomique
→ batch d'agrégation
→ index globaux
```

## 5. Structure parent recommandée

Pour chaque parent actif :

```text
docs/chantiers/<GO_ID>/
  00_INITIAL_PROJECT_DOC.md
  01_...
  PARENT_STATE.md
  NEXT.md
  ACTIVE.md
  DECISIONS.md
  INDEX_PATCH.md
  BRANCH_STATE.md
  GAP_INDEXATION.md si nécessaire
  90_CLOSEOUT.md
```

### 5.1 PARENT_STATE.md

Contient l'état canonique du parent :

- objectif ;
- statut ;
- branche ;
- dernier point établi ;
- gap restant ;
- décision courante ;
- prochain geste ;
- liens internes.

### 5.2 NEXT.md

Contient uniquement le prochain geste du parent :

- next action ;
- next GO si nécessaire ;
- dépendances ;
- critère de passage ;
- blocages.

### 5.3 ACTIVE.md

Contient la lecture locale du flux actif :

- actif / bloqué / en attente ;
- preuve disponible ;
- surface touchée ;
- owner logique ;
- machine si pertinent.

### 5.4 DECISIONS.md

Contient les décisions stabilisées du parent :

- décisions retenues ;
- décisions refusées ;
- hypothèses non validées ;
- invariants.

### 5.5 INDEX_PATCH.md

Contient les entrées prêtes à propager vers :

- `GO_INDEX.md` ;
- `ACTIVE_STREAMS.md` ;
- `NEXT_GO_CANDIDATES.md` ;
- `REPRISE.md`.

## 6. Index inbox proposé

Créer :

```text
docs/index/inbox/<GO_ID>.md
```

Contenu minimal :

```yaml
go_id:
status:
priority:
branch:
parent_ref:
last_established:
next_action:
index_patch_ref:
updated_at:
```

Ce fichier est court, atomique, et réduit les conflits.

## 7. Rôle des index globaux après transition

### GO_INDEX.md

Devient la vue consolidée officielle, pas le lieu de travail quotidien.

### ACTIVE_STREAMS.md

Devient la vue consolidée des flux actifs, mise à jour par batch.

### NEXT_GO_CANDIDATES.md

Devient la vue consolidée des prochains GO primaires, pas le fichier de décision local.

### REPRISE.md

Devient la vue synthétique de reprise globale. Le détail de reprise vit dans le parent.

## 8. Conditions de modification directe des index globaux

Modification directe autorisée seulement si :

- correction critique de continuité ;
- fichier complet disponible localement ;
- aucun conflit de branche probable ;
- diff minimal contrôlé ;
- closeout ou note de propagation ;
- pas de troncature par connecteur.

Sinon : utiliser `PARENT_STATE.md`, `INDEX_PATCH.md` et `docs/index/inbox/<GO_ID>.md`.

## 9. Méthode retenue recommandée

Adopter pour les nouveaux parents :

```text
1. Ouvrir dossier parent.
2. Créer 00_INITIAL_PROJECT_DOC.md.
3. Créer PARENT_STATE.md.
4. Créer NEXT.md.
5. Créer ACTIVE.md si flux actif.
6. Créer INDEX_PATCH.md.
7. Créer docs/index/inbox/<GO_ID>.md si la méthode inbox est acceptée.
8. Ne pas toucher les quatre index globaux sauf nécessité forte.
9. Agréger par GO dédié périodique.
```

## 10. Application au chantier courant

Pour `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`, les fichiers existants couvrent déjà une partie de cette méthode :

- `00_INITIAL_PROJECT_DOC.md` ;
- `BRANCH_STATE.md` ;
- `GAP_INDEXATION.md` ;
- `07_TRANSITIONAL_GLOBAL_INDEXATION_METHOD.md`.

Fichiers à ajouter si la méthode est validée :

- `PARENT_STATE.md` ;
- `NEXT.md` ;
- `ACTIVE.md` ;
- `DECISIONS.md` ;
- `INDEX_PATCH.md` ;
- éventuellement `docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md`.

## 11. Avantages attendus

- réduction des conflits Git ;
- meilleure autonomie de chaque parent ;
- reprise locale complète ;
- meilleure compatibilité avec connecteurs ;
- meilleure compatibilité multi-agents ;
- possibilité d'agrégation contrôlée ;
- meilleure future compatibilité avec LocalCMS, graph, dashboard ou extraction YAML.

## 12. Risques et garde-fous

### Risque

Les index globaux peuvent être en retard.

### Garde-fou

Chaque parent doit avoir `INDEX_PATCH.md` et un statut de propagation.

### Risque

Le parent devient une source concurrente permanente.

### Garde-fou

Le parent-local est source de travail et reprise locale. Les index globaux restent vues consolidées officielles.

### Risque

Accumulation d'inbox non agrégées.

### Garde-fou

Créer un rituel `GO_OPT_TRADING_INDEX_AGGREGATION_BATCH_XX`.

## 13. Proposition de canonisation future

Créer un chantier dédié :

```text
GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01
```

Objectif : promouvoir cette méthode dans la matrice gouvernante ou dans une annexe gouvernance, puis appliquer un premier pilote.

## 14. Verdict proposé

Méthode recommandée :

```text
PARENT_STATE + NEXT + ACTIVE + INDEX_PATCH local
+ docs/index/inbox/<GO_ID>.md optionnel
+ batch d'agrégation vers index globaux
```

Ne pas modifier systématiquement les quatre index globaux à chaque chantier.

## 15. Point de reprise

Si validé, créer dans ce chantier :

- `PARENT_STATE.md` ;
- `NEXT.md` ;
- `ACTIVE.md` ;
- `DECISIONS.md` ;
- `INDEX_PATCH.md`.

Puis ouvrir ou proposer :

```text
GO_OPT_TRADING_PARENT_CONTINUITY_INDEX_INBOX_METHOD_01
```
