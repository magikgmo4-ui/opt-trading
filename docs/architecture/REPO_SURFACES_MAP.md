---
doc_id: OPT_TRADING_REPO_SURFACES_MAP
doc_type: architecture_map
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01
status: reference
lifecycle_stage: architecture
topic_keys:
  - opt-trading
  - surfaces
  - architecture
  - structure
surface: architecture
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Surfaces top-level (lecture canonique)"
updated_at: 2026-04-24
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/REPO_ROOT_POLICY.md
  - registry/README.md
  - registry/meta_index.yaml
  - registry/ui_surfaces_registry.yaml
  - docs/ARCHITECTURE.md
---

# REPO_SURFACES_MAP — opt-trading

## Objet
Fournir une carte humaine de lecture des surfaces du repo, sans remplacer les registres machine-readable.

## Règle de source
- l'etat reel prouve et la carte des surfaces validee par le maitre priment
- source machine-readable : `registry/*`
- cette carte est une lecture humaine de reference pour la continuite, non souveraine hors de son perimetre

## Surfaces top-level (lecture canonique)
- `docs/` : gouvernance, architecture, chantiers et continuité canonique
- `registry/` : registres déclaratifs machine-readable
- `workflow_ai/` : doctrine locale d'execution IA et templates opposables
- `modules/` : modules durables et couches fonctionnelles
- `scripts/` : wrappers et exécution opératoire
- `shared/`, `schemas/`, `adapters/` : briques transverses runtime
- `perf/` : couche performance et persistance associée
- `tools/` : outillage d’appui opératoire
- `deploy_module_multi_machine/` : outillage/continuité déploiement multi-machine
- `packages/` : paquets et workspaces embarqués
- `tradingview/` : surfaces liées à TradingView (support/exécution selon sous-dossiers)
- `state/` : etat runtime léger et checkpoints techniques
- `data/` : sorties, artefacts et sous-produits métier
- `student/` : surface de travail et sous-produits embarqués
- `contracts/` : contrats spécialisés de domaine
- `audit/` : preuves ponctuelles et packs d'audit
- `tests/` : surface top-level de test actuellement faible et partiellement diffuse

## Articulation de référence
- architecture runtime : `docs/ARCHITECTURE.md`
- politique racine : `docs/governance/REPO_ROOT_POLICY.md`
- surfaces déclaratives : `registry/ui_surfaces_registry.yaml`
- index de registres : `registry/meta_index.yaml`

## Limites
- ce document ne duplique pas les entrées détaillées `registry/*`
- ce document n’impose pas de reclassement physique des fichiers

## Surfaces locales / archive
- `_archive/` : archive locale (hors surface active)
- `tmp/` : transit, bundles et essais locaux
- `__pycache__/`, `.ruff_cache/`, `.uv-cache/`, `.uv-python/` : caches et runtimes locaux
- `.secrets/` : support sensible local, non canonique

## Sous-surface documentaire notable
- `docs/ot/trae/trae_pack_texts/README.md` : entree documentaire du support legacy Trae
- `docs/ot/trae/trae_pack_texts/trae_pack/` : archive de lecture legacy, non requise par la continuite canonique

## Ensemble Trae / IDE (lecture de coherence)
- `workflow_ai/` : doctrine d'execution gated et templates opposables
- `modules/validated_prompt_factory/` : outil operateur de generation de prompts structures
- `deploy_module_multi_machine/` : outillage de deploiement multi-machine et de continuite terrain
- `docs/ot/trae/trae_pack_texts/README.md` : synthese repo-native du support legacy Trae
- `docs/ot/trae/trae_pack_texts/trae_pack/` : archive de lecture utile pour l'IDE, non canonique

Règle :
- ces quatre surfaces forment un ensemble pratique de travail Trae/IDE
- en cas de conflit, la couche canonique repo-first prime (`docs/`, `workflow_ai/`, `registry/`, `modules/`)

## REPRISE
- mise à jour continue via `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`

## RISKS

- À qualifier.
