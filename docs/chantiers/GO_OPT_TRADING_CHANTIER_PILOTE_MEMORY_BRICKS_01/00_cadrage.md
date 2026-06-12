---
doc_id: GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: memory_bricks
module: memory_bricks
go_id: GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - memory_bricks
  - continuity
  - pilot
surface: memory
source_kind: canonical
updated_at: 2026-04-11
links:
  - docs/governance/MEMORY_BRICKS_MAPPING.md
  - modules/memory_bricks/docs/SPEC_MEMORY_BRICKS_API_V2_READONLY.md
  - docs/chantiers/GO_OPT_TRADING_LOCAL_CONTINUITY_BOOTSTRAP_01/90_closeout.md
---

# 00_cadrage — GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01

## Identité
- GO : GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01
- Repo : opt-trading
- Branche : sot/mainline
- Statut : active
- Type de travail : module durable / chantier pilote memory_bricks

## État de départ retenu
- état repo retenu : socle documentaire local posé et premier chantier pilote de bootstrap déjà clos en PASS
- artefacts existants retenus : `MEMORY_BRICKS_MAPPING.md`, spec API V2 read-only, module `memory_bricks` existant
- limites connues : absence encore d’un chantier pilote canonique directement centré sur un cas réel `memory_bricks`
- dépendances : cohérence avec le schéma réel `memory_bricks` et sa consommation par `localcms`

## Objectif du lot
- objectif principal : produire un premier chantier canonique directement aligné sur `memory_bricks`
- résultat attendu : un dossier chantier complet montrant comment un sujet `memory_bricks` se cadre, se décide, se clôt et se relie à la compaction

## Non-objectifs
- refondre le module `memory_bricks`
- modifier le contrat API V2 read-only à ce stade

## Contexte utile
- source humaine / contexte : migration uniforme désormais assez stabilisée pour tester un cas directement relié au compact canonique
- artefacts de référence : mapping local `memory_bricks`, spec API V2, closeout du bootstrap local

## Critères PASS / FAIL
- PASS si : le chantier pilote produit un dossier canonique cohérent et utile comme référence de cas `memory_bricks`
- FAIL si : il reste trop abstrait, déconnecté du schéma réel du module, ou inutilisable comme exemple

## Point de vigilance
- risque principal : rester au niveau méthode sans ancrage suffisant dans le composant réel `memory_bricks`
- point d’arrêt acceptable : cadrage + plan + décisions stabilisées si le factuel détaillé doit être enrichi ensuite

## RISKS

- À qualifier.
