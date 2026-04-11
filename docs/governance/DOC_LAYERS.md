---
doc_id: OPT_TRADING_DOC_LAYERS
doc_type: workflow_rule
repo: opt-trading
project: opt-trading
module:
go_id:
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - doc_layers
  - governance
  - continuity
  - memory_bricks
surface: governance
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/governance/REPO_ROLE.md
---

# DOC_LAYERS — opt-trading

## Objet

Ce document fixe les couches documentaires utilisées dans `opt-trading` dans le cadre de la méthode uniforme de continuité.

Il sert à distinguer les fonctions documentaires et à éviter :
- les doublons de source de vérité
- les mélanges entre doc longue, chantier, continuité et compaction
- les dérivations implicites non tracées

---

## 1. Vue d’ensemble

Les couches documentaires retenues sont :

- gouvernance
- chantier
- continuité
- compaction
- couche humaine à préciser séparément

Chaque couche a une fonction propre.

---

## 2. Couche gouvernance

### But
Définir les règles stables du repo.

### Contenu type
- rôle du repo
- conventions locales
- règles de dérivation
- règles de structure des documents

### Artefacts typiques
- `REPO_ROLE.md`
- `DOC_LAYERS.md`
- `MEMORY_BRICKS_MAPPING.md`

---

## 3. Couche chantier

### But
Porter un lot de travail borné.

### Structure canonique
- `00_cadrage.md`
- `01_plan.md`
- `02_journal_technique.md`
- `03_decisions.md`
- `90_closeout.md`

### Fonction
- cadrer
- exécuter
- valider
- clore
- reprendre

---

## 4. Couche continuité

### But
Rendre visible l’état courant et les suites naturelles.

### Artefacts typiques
- `docs/index/GO_INDEX.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/REPRISE.md`
- `docs/next/NEXT_GO_CANDIDATES.md`
- `docs/opportunities/OPPORTUNITY_LOG.md`

### Fonction
- suivi des GO connus
- suivi des flux actifs
- reprise rapide
- visibilité des prochains GO candidats
- conservation des opportunités non encore ouvertes

---

## 5. Couche compaction

### But
Fournir une forme compacte, structurée et navigable.

### Artefact principal
- `memory_bricks`

### Règle
La compaction dérive de documents stabilisés.
Elle ne remplace ni les closeouts ni la doc de chantier.

---

## 6. Couche humaine

### Statut actuel
Cette couche est reconnue comme nécessaire, mais son rôle exact n’est pas fixé dans ce document.

### Règle actuelle
La matière humaine et contextuelle doit être relue et stabilisée avant d’alimenter les couches canoniques.

Ce document ne tranche pas encore :
- le lieu exact final de cette matière
- son niveau de duplication autorisé
- son mapping détaillé vers les autres couches

---

## 7. Règles anti-mélange

### 7.1 La gouvernance ne remplace pas le chantier
Un document de gouvernance n’est pas un dossier chantier.

### 7.2 Le chantier ne remplace pas la continuité transverse
Un dossier chantier ne remplace ni un index, ni un `REPRISE.md`, ni un `NEXT_GO_CANDIDATES.md`.

### 7.3 La compaction ne remplace pas le détail
`memory_bricks` ne remplace pas la documentation longue.

### 7.4 La continuité ne remplace pas le closeout
Les index et fichiers de reprise pointent vers les closeouts, ils ne les absorbent pas.

---

## 8. Pipeline local cible

Le pipeline local cible est :

contexte utile / matière stabilisée
-> chantier borné
-> closeout / reprise / next
-> compaction `memory_bricks`

La continuité locale doit rester cohérente avec ce pipeline.

---

## 9. Statut

Statut :
- document de référence locale
- à maintenir cohérent avec la méthode uniforme globale
