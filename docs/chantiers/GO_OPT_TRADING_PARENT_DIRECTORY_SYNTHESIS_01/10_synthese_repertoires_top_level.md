---
doc_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01_TOP_LEVEL
doc_type: chantier_synthese
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01
status: active
lifecycle_stage: analyse
topic_keys:
  - opt-trading
  - directory
  - synthesis
  - top_level
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_PARENT_DIRECTORY_SYNTHESIS_01/01_cadrage_parent.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - README.md
---

# Synthese top-level par repertoire

## Regle
Ce document donne une vue macro par repertoire top-level.
Il ne remplace pas les syntheses detaillees par bloc.

## Tableau top-level

| Repertoire | Role synthétique | Statut retenu |
| --- | --- | --- |
| `docs/` | gouvernance, architecture, chantiers, continuité canonique | canonique |
| `modules/` | coeur fonctionnel du repo, familles metier et modules durables | actif |
| `scripts/` | wrappers, menus, execution operatoire et verification | actif |
| `registry/` | registre declaratif machine-readable des surfaces/modules/wrappers | canonique |
| `workflow_ai/` | doctrine d’execution IA, gates, templates | canonique |
| `deploy_module_multi_machine/` | outillage valide de deploiement multi-machine | actif |
| `shared/` | briques transverses legeres reutilisees | support runtime |
| `adapters/` | adaptateurs cibles entre couches | support runtime |
| `schemas/` | schemas de validation ponctuels | support runtime |
| `perf/` | surface applicative Perf | actif cible |
| `tools/` | utilitaires operatoires ponctuels | support actif |
| `packages/` | package embarque / code mutualise | support actif |
| `tradingview/` | compatibilite et support cote TradingView | support produit |
| `data/` | stockage de sorties et sous-produits metier par domaine | actif, a qualifier finement |
| `state/` | etat persistant leger et configs runtime | actif |
| `student/` | surface machine/student, exports, validations, scripts | actif contextuel |
| `tests/` | surface de test legere | faible couverture |
| `contracts/` | contrats / schemas metier specialises | support |
| `audit/` | audits dates et preuves historiques | lecture / archive active |
| `_archive/` | archives locales assumees | archive |
| `tmp/` | temporaires locaux et bundles de travail | local-only |
| `__pycache__/` | cache Python | cache |
| `.ruff_cache/` | cache linter | cache |
| `.uv-cache/` | cache `uv` | cache |
| `.uv-python/` | runtimes / interpreteurs `uv` locaux | cache local |
| `.secrets/` | exemples / support secrets locaux | support local |

## Hors perimetre de ce tableau
Les fichiers racine (`README.md`, `requirements.txt`, `webhook_server.py`, `bitget_bridge.py`, etc.) ne sont pas des repertoires top-level.
Ils pourront etre resumes a part si necessaire, mais ne font pas partie de la presente synthese par repertoire.

## Point de reprise
- detail en cours : Bloc A (`docs/`, `registry/`, `workflow_ai/`)
