---
doc_id: GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01_CADRAGE_PARENT
doc_type: chantier_parent_cadrage
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01
status: open
lifecycle_stage: cadrage
surface: docs/chantiers
topic_keys:
  - opt-trading
  - repo-surfaces
  - cartography
  - governance
  - continuity
source_kind: canonical
reference_canonique_principale: docs/architecture/REPO_SURFACES_MAP.md
point_de_reprise: "Commencer / poursuivre Bloc A, puis Bloc B, Bloc C, Bloc D"
updated_at: 2026-04-24
links:
  - docs/architecture/REPO_SURFACES_MAP.md
  - README.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01 — cadrage parent

## 1_MASTER_TARGET

Produire une cartographie lisible, stable et exploitable des surfaces top-level du repo `opt-trading`, en partant d'une synthèse macro par répertoire puis en déroulant les répertoires par blocs.

## 2_INITIAL_PROJECT_DOC

Document initial figé du chantier parent.

Sources de départ retenues :
- `docs/architecture/REPO_SURFACES_MAP.md`
- `README.md`
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`

État Git retenu au démarrage :
- branche source de lecture : `codex/doc-ops-child-branch-cleanup-01`
- HEAD source : `f4f78d32b436aa1fbc7401f9c0ee8e1a7aeaa8c0`
- branche parent dédiée créée : `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01`
- base canonique de comparaison : `sot/mainline`
- état comparatif observé : branche source en divergence avec `sot/mainline` (`ahead 1`, `behind 1`)

## 3_INITIAL_NEED

Ouvrir un chantier parent et une branche dédiée, fixer intégralement le plan de lecture des surfaces repo comme chantier, puis commencer la passe détaillée.

## 4_MASTER_PROJECT_PLAN

### Plan figé

- Bloc A: surfaces canoniques de pilotage et de continuité (`docs`, `registry`, `workflow_ai`)
- Bloc B: surfaces runtime et opératoires (`modules`, `scripts`, `shared`, `adapters`, `schemas`, `perf`, `tools`, `packages`, `deploy_module_multi_machine`)
- Bloc C: surfaces produit, données et état (`data`, `state`, `student`, `tests`, `tradingview`, `contracts`, `audit`)
- Bloc D: surfaces support, archive et local-only (`_archive`, `tmp`, `__pycache__`, `.ruff_cache`, `.uv-cache`, `.uv-python`, `.secrets`)

### Synthèse macro par répertoire

| Répertoire | Rôle synthétique | Statut |
| --- | --- | --- |
| `docs/` | gouvernance, architecture, chantiers, continuité canonique | canonique |
| `modules/` | cœur fonctionnel du repo, familles métier et modules durables | actif |
| `scripts/` | wrappers, menus, exécution opératoire et vérification | actif |
| `registry/` | registre déclaratif machine-readable des surfaces/modules/wrappers | canonique |
| `workflow_ai/` | doctrine d’exécution IA, gates, templates | canonique |
| `deploy_module_multi_machine/` | outillage validé de déploiement multi-machine | actif |
| `shared/` | briques transverses légères réutilisées | support runtime |
| `adapters/` | adaptateurs ciblés entre couches | support runtime |
| `schemas/` | schémas de validation ponctuels | support runtime |
| `perf/` | surface applicative Perf | actif ciblé |
| `tools/` | utilitaires opératoires ponctuels | support actif |
| `packages/` | package embarqué / code mutualisé | support actif |
| `tradingview/` | compatibilité et support côté TradingView | support produit |
| `data/` | stockage de sorties et sous-produits métier par domaine | actif, à qualifier finement |
| `state/` | état persistant léger et configs runtime | actif |
| `student/` | surface machine/student, exports, validations, scripts | actif contextuel |
| `tests/` | surface de test très légère actuellement | faible couverture |
| `contracts/` | contrats / schémas métier spécialisés | support |
| `audit/` | audits datés et preuves historiques | lecture / archive active |
| `_archive/` | archives locales assumées | archive |
| `tmp/` | temporaires locaux et bundles de travail | local-only |
| `__pycache__/` | cache Python | cache |
| `.ruff_cache/` | cache linter | cache |
| `.uv-cache/` | cache gestionnaire Python `uv` | cache |
| `.uv-python/` | runtimes/interpréteurs `uv` locaux | cache local |
| `.secrets/` | exemples/support secrets locaux | support local |

### Ordre recommandé des passes détaillées

1. Commencer par le Bloc A, parce qu’il fixe le vocabulaire et la source de vérité du reste.
2. Enchaîner avec le Bloc B, parce qu’il décrit les vraies surfaces d’exécution.
3. Puis Bloc C, pour séparer clairement données métier, état runtime et surfaces machine.
4. Finir par Bloc D, qui relève surtout d’hygiène repo et de statut local.

## 5_GO_PLAN

- `GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01` : chantier parent de cartographie.
- Première passe enfant logique : Bloc A.
- Passes suivantes : Bloc B, Bloc C, Bloc D.

## 6_FINAL_TARGET

Livrable attendu : dossier chantier parent contenant :
- plan figé intégral ;
- synthèse top-level validable ;
- lectures détaillées par bloc ;
- écarts, hypothèses et gaps restants séparés ;
- point de reprise indépendant de la session.

## 7_CANONICAL_STATE

État initial validé :
- `docs/architecture/REPO_SURFACES_MAP.md` donne la carte humaine de référence des surfaces top-level.
- `README.md` expose l'entrée repo minimale : quickstart, environnement et vérification.
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md` gouverne l'arbitrage documentaire, le placement, les GO, le frontmatter, la propagation et le support Git.

## 8_VALIDATED_PLAN

Procéder par lecture repo-first, sans reclassement physique immédiat :
1. relire les sources canoniques ;
2. figer le plan parent ;
3. documenter Bloc A ;
4. poursuivre Bloc B / C / D ;
5. clôturer avec gaps, décisions et point de reprise.

## 9_SELECTED_SOLUTION

Solution retenue : chantier parent documentaire sur branche dédiée, sans patch runtime.

## 10_SELECTED_SETUP

- Branche : `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01`
- Dossier : `docs/chantiers/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01/`
- Mode : documentation canonique / cartographie / continuité.

## 11_KEY_DECISIONS

- Le plan utilisateur est figé intégralement dans ce cadrage.
- La passe commence par Bloc A.
- Le chantier ne modifie pas physiquement les surfaces du repo à ce stade.
- La divergence avec `sot/mainline` est explicitement conservée comme état réel, non masquée.

## 12_INVARIANTS

- Ne pas transformer `registry/*` en source souveraine au-dessus de `docs/governance/*`.
- Ne pas remplacer `REPO_SURFACES_MAP.md` par une table opportuniste.
- Ne pas reclasser physiquement des répertoires sans GO séparé.
- Ne pas interpréter les caches et surfaces local-only comme surfaces produit.
- Ne pas ouvrir de sous-GO technique avant qualification documentaire.

## 13_ESTABLISHED

- Connecteur GitHub actif.
- Repo `magikgmo4-ui/opt-trading` accessible avec droits d'écriture.
- Branche source `codex/doc-ops-child-branch-cleanup-01` existante.
- Branche parent dédiée créée depuis `f4f78d32b436aa1fbc7401f9c0ee8e1a7aeaa8c0`.

## 14_HYPOTHESIS

- Certains répertoires listés dans le plan utilisateur (`data`, `state`, `contracts`, `audit`, `tmp`, caches, `.secrets`) peuvent ne pas être tous représentés dans `REPO_SURFACES_MAP.md` au même niveau de détail ; ils devront être qualifiés par preuve repo lors des blocs C/D.

## 15_REMAINING_GAP

- Bloc A à compléter par lecture détaillée.
- Bloc B/C/D non encore déroulés.
- Propagation éventuelle dans `GO_INDEX.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `REPRISE.md` non appliquée dans ce premier commit de cadrage.

## 16_TODO

- Finaliser `01_bloc_A_surfaces_canoniques.md`.
- Préparer `02_bloc_B_surfaces_runtime_operatoires.md`.
- Préparer `03_bloc_C_surfaces_produit_donnees_etat.md`.
- Préparer `04_bloc_D_support_archive_local_only.md`.
- Produire `90_closeout.md` en fin de passe.

## 17_RESUME_POINT

Reprendre depuis :
- branche : `go/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01`
- dossier : `docs/chantiers/GO_OPT_TRADING_REPO_SURFACES_PARENT_CARTOGRAPHY_01/`
- prochaine action : poursuivre Bloc A, puis dérouler les Blocs B, C et D selon l'ordre figé.
