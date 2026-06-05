---
doc_id: GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02_IDE_PACK
doc_type: workflow_rule
repo: opt-trading
project: opt-trading
module:
go_id: GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02
status: active
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - continuity
  - ide
  - execution_pack
  - hardening
surface: chantier
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/chantiers/GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02/00_cadrage.md
  - docs/chantiers/GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02/01_plan.md
---

# IDE_EXECUTION_PACK — GO_UNIFORM_CONTINUITY_IDE_EXECUTION_PACK_02

## Objet

Ce document dit exactement à l’IDE quoi faire pour terminer le hardening restant et continuer le plan, sans modifier les fichiers GO déjà ouverts dans cette session sauf si la tâche le demande explicitement à la toute fin.

---

## 1. Règle générale

L’IDE travaille en Git natif.
Il peut modifier des fichiers existants.
Il ne doit pas ouvrir de nouveau chantier métier.
Il doit d’abord finir le hardening documentaire déjà identifié.

---

## 2. Repo 1 — opt-trading

### Branche
- `sot/mainline`

### Fichiers à mettre à jour
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/REPRISE.md`
- `docs/next/NEXT_GO_CANDIDATES.md`

### Objectif exact
Faire refléter dans les index l’état réel suivant :
- `GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01` = PASS
- `GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01` = PASS
- `GO_UNIFORM_CONTINUITY_HARDENING_01` = actif tant que les updates ne sont pas effectivement appliqués
- prochain point de reprise local = finir le hardening puis ouvrir le prochain lot métier réel

### Règles d’édition
- ne pas casser le frontmatter existant
- conserver le style court, opératoire et lisible
- ne pas réécrire inutilement les sections stables
- mettre à jour uniquement les parties devenues obsolètes

### Validation attendue
- lecture des 4 fichiers mis à jour
- cohérence avec les closeouts PASS déjà présents
- commit Git propre sur `sot/mainline`

---

## 3. Repo 2 — localcms

### Branche
- `main` comme support réel observable retenu pour ce lot

### Fichiers à mettre à jour
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/REPRISE.md`
- `docs/next/NEXT_GO_CANDIDATES.md`

### Objectif exact
Faire refléter dans les index l’état réel suivant :
- `GO_LOCALCMS_UNIFORM_CONTINUITY_ALIGNMENT_01` = actif ou stabilisé selon l’état retenu par les fichiers créés
- `GO_LOCALCMS_MEMORY_BRICKS_CONSUMER_PILOT_01` = PASS
- prochain point de reprise local = enrichissement index + normalisation historique utile ou suite transverse utile

### Règles d’édition
- conserver le rôle consumer du repo
- ne pas faire de `localcms` une source maîtresse de `memory_bricks`
- garder les textes courts et actionnables

### Validation attendue
- lecture des 4 fichiers mis à jour
- cohérence avec le pilote consumer PASS
- commit Git propre sur `main`

---

## 4. Repo 3 — llm_wiki_minimal

### Action
Pas de hardening obligatoire immédiat.

### Option courte
Ajouter éventuellement :
- `docs/index/ACTIVE_STREAMS.md`
- et/ou `docs/next/NEXT_GO_CANDIDATES.md`

### Condition
Seulement si l’IDE juge que cela améliore vraiment la reprise sans créer de bruit documentaire.

---

## 5. Repo 4 — hf_trading

### Action
Pas de modification immédiate requise.

### Suite logique
Attendre un vrai lot métier avant d’ouvrir un chantier canonique.

---

## 6. Fermeture du hardening

Une fois `opt-trading` et `localcms` réellement mis à jour, l’IDE peut :
- mettre à jour le verdict du chantier `GO_UNIFORM_CONTINUITY_HARDENING_01`
- ou écrire un court addendum de clôture si modifier `90_closeout.md` est jugé préférable à ce moment-là

### Condition stricte
Ne basculer le hardening en PASS que si les fichiers existants ont vraiment été corrigés et commités.

---

## 7. Suite du plan après hardening

Une fois le hardening réellement terminé, la suite logique est :
- soit normalisation historique ciblée de 1 à 2 anciens chantiers utiles
- soit premier vrai chantier métier dans `hf_trading`

### Recommandation par défaut
Prendre un remapping historique court avant d’ouvrir trop vite un nouveau chantier métier.

---

## 8. Sortie attendue de l’IDE

L’IDE doit produire au minimum :
- liste exacte des fichiers modifiés
- commit(s) réalisés
- vérification de cohérence courte
- point de reprise suivant

## RISKS

- À qualifier.
