---
doc_id: GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01_DECISION_GRID
doc_type: chantier_policy
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_MODULE_CANONICAL_CONSOLIDATION_01
status: complete
lifecycle_stage: policy
topic_keys:
  - opt-trading
  - modules
  - canonical
  - archive
  - decision-grid
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - _archive/legacy_modules
  - _archive/root_backups
---

# Grille de decision

## Etats autorises

### 1. `canonique`
Surface proprietaire de la capacite.

Criteres :
- callers identifies
- docs courantes pointent dessus
- wrappers et registre pointent dessus
- usage runtime ou operatoire prouve utile

Action :
- garder active
- consolider les callers vers elle

### 2. `utile_prouve`
Surface active utile, mais pas encore proprietaire unique de sa categorie.

Criteres :
- role reel prouve
- pas encore assez de preuve pour eliminer ou fusionner

Action :
- garder active provisoirement
- requalifier plus tard en `canonique` ou `compat`

### 3. `compat_temporaire`
Surface gardee seulement pour transition.

Criteres :
- ancien nom, ancien wrapper ou ancienne facade encore appeles
- successeur canonique deja designe

Action :
- garder pour une duree borne
- retirer des flux actifs des que callers migres
- exiger une date ou condition de retrait

### 4. `legacy_fige`
Surface depassee, gardee en lecture seulement.

Criteres :
- plus de caller critique
- plus de role proprietaire
- utilite limitee a la relecture ou au forensic

Action :
- retirer des wrappers et de la doc courante
- preparer bascule vers archive

### 5. `archive_backup`
Surface sortie du runtime et des flux actifs.

Criteres :
- aucun caller critique
- aucune raison de la garder active dans `modules/`
- conservation voulue uniquement pour trace ou secours

Action :
- deplacer vers `_archive/legacy_modules`
- ajouter `DEPRECATED.md` si utile
- couper liens actifs depuis docs/registry/wrappers

## Destinations

### Runtime/module legacy
Destination preferee :
- `_archive/legacy_modules/<module_name>`

Si la famille contient plusieurs variantes :
- `_archive/legacy_modules/<family>/<module_name>`

### Backup de surface racine ou artefact unique
Destination preferee :
- `_archive/root_backups/<name>_<date>`

## Tests de bascule vers archive
Avant tout move vers archive :
1. verifier callers repo
2. verifier registre wrappers et modules
3. verifier docs actives
4. verifier scripts d'install et entrypoints globaux
5. preparer rollback simple

## Regles d'interdiction
- ne pas archiver un module encore cible par un wrapper global actif
- ne pas garder en actif deux modules qui portent exactement la meme capacite proprietaire
- ne pas laisser un `step`, `fix`, `patch`, `v2` actif sans raison explicite

## Regle de nommage canonique
Quand une famille doit converger vers un module unique, le nom canonique final doit reprendre le nom de famille stable.

Exemple attendu :
- famille `reseau_ssh*` -> module canonique final `reseau_ssh`

Consequence :
- un nom suffixe `step`, `fix`, `patch`, `v2` peut servir de base d'absorption
- mais il ne doit pas rester le nom canonique final si le nom de famille racine peut etre recupere proprement

## Target
1 module canonique par famille.
