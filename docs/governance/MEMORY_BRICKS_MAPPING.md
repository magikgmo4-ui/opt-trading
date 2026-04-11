---
doc_id: OPT_TRADING_MEMORY_BRICKS_MAPPING
doc_type: workflow_rule
repo: opt-trading
project: memory_bricks
module: memory_bricks
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - memory_bricks
  - mapping
  - governance
  - continuity
surface: memory
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
---

# MEMORY_BRICKS_MAPPING — opt-trading

## Objet

Ce document fixe le principe de dérivation documentaire vers `memory_bricks` dans `opt-trading`.

Il sert à éviter :
- l’écriture de briques comme seconde narration libre
- les contradictions entre doc longue et compaction
- la perte de traçabilité entre documents stabilisés et forme compacte

---

## 1. Principe

`memory_bricks` est une forme compacte dérivée.

La brique ne remplace pas :
- la documentation de chantier
- le closeout
- les décisions détaillées
- la continuité locale

Elle résume, relie et prépare la reprise compacte.

---

## 2. Sources amont prioritaires

Les champs d’une brique doivent dériver en priorité de documents stabilisés, notamment :

- `00_cadrage.md`
- `03_decisions.md`
- `90_closeout.md`
- `docs/index/REPRISE.md` si utile
- `docs/next/NEXT_GO_CANDIDATES.md` si utile

Les sources brutes non stabilisées ne sont pas privilégiées.

---

## 3. Champs principaux

### 3.1 Identité
- `id`
- `title`
- `type`

### 3.2 Statut et périmètre
- `status`
- `project`
- `module`
- `repo`
- `branch`

### 3.3 Résumé compact
- `summary_short`
- `resume_point`

### 3.4 Décisions et suites
- `decisions`
- `todo`

### 3.5 Références
- `tags`
- `links`
- `path`
- `canonical_ref`
- `real_state_ref`
- `source_ref`

### 3.6 Métadonnées complémentaires
- `machine`
- `surface`
- `timezone`
- `validated_by`
- `date`

Ces champs complémentaires ne sont utilisés que si leur valeur de reprise est réelle.

---

## 4. Règles de dérivation

### 4.1 Une brique résume
Elle ne remplace pas la documentation détaillée.

### 4.2 Pas de champ sans source
Chaque champ doit pouvoir être rattaché à une source amont identifiable.

### 4.3 Priorité aux documents stabilisés
La compaction se fait prioritairement depuis des documents stabilisés, pas depuis du brut si cela peut être évité.

### 4.4 `todo` actionnable
Le champ `todo` ne doit contenir que des suites utiles et actionnables.

### 4.5 Traçabilité
La brique doit permettre de remonter au contexte détaillé par ses références.

---

## 5. Lien avec la couche humaine

La matière humaine n’alimente pas directement la brique sous forme brute.

Chemin visé :

matière humaine
-> extraction validée
-> documentation stabilisée
-> `memory_bricks`

---

## 6. Lien avec la continuité locale

Les briques peuvent compléter les index et points de reprise locaux, mais :
- elles ne remplacent pas `GO_INDEX.md`
- elles ne remplacent pas `ACTIVE_STREAMS.md`
- elles ne remplacent pas `REPRISE.md`

Les fonctions sont voisines mais distinctes.

---

## 7. Limites

Ce document ne fixe pas encore :
- le template exact de chaque type de brique
- les règles d’automatisation éventuelle
- les exceptions repo par repo hors `opt-trading`

---

## 8. Statut

Statut :
- document de référence locale
- à maintenir cohérent avec le schéma réel de `memory_bricks`
