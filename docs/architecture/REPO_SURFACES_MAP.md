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
updated_at: 2026-04-18
links:
  - registry/README.md
  - registry/meta_index.yaml
  - registry/ui_surfaces_registry.yaml
  - docs/ARCHITECTURE.md
---

# REPO_SURFACES_MAP — opt-trading

## Objet
Fournir une carte humaine de lecture des surfaces du repo, sans remplacer les registres machine-readable.

## Règle de source
- source machine-readable : `registry/*`
- cette carte est une lecture humaine de référence pour la continuité

## Surfaces top-level (lecture canonique)
- `docs/` : gouvernance, architecture, chantiers et continuité canonique
- `modules/` : modules durables et couches fonctionnelles
- `scripts/` : wrappers et exécution opératoire
- `registry/` : registres déclaratifs machine-readable
- `perf/` : couche performance et persistance associée
- `shared/`, `schemas/`, `adapters/` : briques transverses runtime
- `tools/` : outillage d’appui opératoire
- `student/` : surface de travail et sous-produits embarqués
- `workflow_ai/` : doctrine et outillage IA embarqués
- `infra_context_sanitized/` : contexte infra sanitizé (support, continuité)
- `deploy_module_multi_machine/` : outillage/continuité déploiement multi-machine
- `packages/` : paquets et workspaces embarqués
- `tradingview/` : surfaces liées à TradingView (support/exécution selon sous-dossiers)
- `journal.md`, `journal/` : brut vivant, index dérivés, archives de lecture

## Articulation de référence
- architecture runtime : `docs/ARCHITECTURE.md`
- surfaces déclaratives : `registry/ui_surfaces_registry.yaml`
- index de registres : `registry/meta_index.yaml`

## Limites
- ce document ne duplique pas les entrées détaillées `registry/*`
- ce document n’impose pas de reclassement physique des fichiers

## Surfaces secondaires / archive
- `_archive/` : archive locale (hors surface active)
- `trae_pack_texts/` : bibliothèque locale de textes Trae (support)

## REPRISE
- mise à jour continue via `GO_OPT_TRADING_CANON_STRUCTURE_REALIGNMENT_01`
