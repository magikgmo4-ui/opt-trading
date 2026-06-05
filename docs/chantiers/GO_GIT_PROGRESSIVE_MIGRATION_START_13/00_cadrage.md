---
doc_id: GO_GIT_PROGRESSIVE_MIGRATION_START_13_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_GIT_PROGRESSIVE_MIGRATION_START_13
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - migration
  - git
  - governance
  - documentation
surface: governance
source_kind: canonical
updated_at: 2026-04-16
links:
  - docs/index/GO_INDEX.md
  - docs/governance/REPO_ROLE.md
  - docs/governance/DOC_LAYERS.md
  - docs/governance/MEMORY_BRICKS_MAPPING.md
  - docs/index/REPRISE.md
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
---

# 00_cadrage — GO_GIT_PROGRESSIVE_MIGRATION_START_13

## Objet

Ouvrir un dossier chantier dédié minimal pour `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, déjà référencé dans `docs/index/GO_INDEX.md` mais non rattaché jusque-là à un dossier `docs/chantiers/` dédié.

---

## Besoin initial

Donner un point d’ancrage chantier explicite au démarrage de la migration Git progressive, afin de ne pas laisser ce GO uniquement porté par l’index et par les documents de gouvernance locale.

---

## Intention

Stabiliser la trajectoire documentaire de migration progressive dans le repo canonique, en conservant le lien entre gouvernance locale, dérivation documentaire et reprise, sans reconstruire artificiellement des lots non déjà établis.

---

## Produits finaux voulus / objectifs du chantier

- un dossier chantier dédié minimal pour ce GO
- un rattachement propre aux documents fondateurs de la gouvernance locale
- une base de reprise claire pour la poursuite de la migration documentaire
- une séparation explicite entre ce qui est déjà posé et ce qui reste à migrer

---

## Cible finale

Disposer d’un dossier `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/` qui matérialise ce GO comme point d’entrée chantier de la migration Git progressive sur `opt-trading`.

---

## Plan validé

1. constater la présence du GO dans `GO_INDEX.md`
2. constater l’absence de dossier chantier dédié
3. ouvrir un `00_cadrage.md` minimal
4. préserver le statut connu `active`
5. renvoyer aux documents fondateurs déjà canoniques du repo

---

## ETABLI

- `GO_GIT_PROGRESSIVE_MIGRATION_START_13` est référencé dans `docs/index/GO_INDEX.md`
- l’index indique :
  - type : migration documentaire
  - statut : `active`
  - titre court : démarrage de la migration Git progressive
  - dernier état connu : gouvernance locale initiale créée sur `sot/mainline`
- les liens utiles déjà portés par l’index sont :
  - `docs/governance/REPO_ROLE.md`
  - `docs/governance/DOC_LAYERS.md`
  - `docs/governance/MEMORY_BRICKS_MAPPING.md`
- aucun dossier chantier dédié n’a été observé sous `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/` avant la présente ouverture

---

## Gap restant

- détailler, si nécessaire plus tard, les lots de migration encore ouverts
- rattacher explicitement les suites actives si la migration progressive doit être rejouée ou auditée comme chantier autonome

---

## Rôles séparés

### Rôle repo / produit
- `opt-trading` porte la migration documentaire Git progressive comme trajectoire de structuration locale

### Rôle IA / IDE
- ouvrir le rattachement chantier minimal
- préserver la séparation entre fondations déjà posées et suites encore actives

### Rôle machine
- aucun runtime engagé
- chantier documentaire uniquement

---

## Next GO

À expliciter dans une suite dédiée seulement si la migration progressive doit être poursuivie comme chantier autonome distinct.

À ce stade, le présent dossier sert d’ancrage minimal et de point de reprise.

---

## REPRISE

### Reprise globale
- `docs/index/REPRISE.md`

### Point de reprise local
- `docs/chantiers/GO_GIT_PROGRESSIVE_MIGRATION_START_13/00_cadrage.md`

---

## Statut

**ACTIVE — dossier chantier dédié minimal désormais ouvert pour un GO déjà actif dans l’index**

## RISKS

- À qualifier.
