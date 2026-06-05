---
doc_id: OPT_TRADING_REPO_ROOT_POLICY
doc_type: governance_policy
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - governance
  - root
  - policy
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section Fichiers racine legitimes observes"
updated_at: 2026-04-29
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt
  - docs/governance/REPO_ROLE.md
  - docs/INDEX.md
---

# REPO_ROOT_POLICY — opt-trading

## Objet
Fixer la politique canonique de la racine interne du repo.

Cette politique est subordonnée à l'état réel prouvé puis à `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`.
Elle fixe seulement l'application locale à la racine de `opt-trading`.

## Portée
- ce document traite ce qui reste à la racine **dans le repo**
- la frontière repo/hors-repo reste portée par `docs/ot/trae/06_REPO_BOUNDARY_POLICY_V1.txt`

## Articulation avec la carte des surfaces
- la carte complete des repertoires top-level est portee par `docs/architecture/REPO_SURFACES_MAP.md`
- le present document fixe d'abord la discipline de la racine minimale, des fichiers top-level et des exceptions explicites

## Règles racine
- ne laisser à la racine que les éléments ayant une valeur d’entrée, d’exécution ou de compatibilité explicite
- rattacher tout objet racine à une catégorie documentée (runtime, support, legacy, ou en attente d’arbitrage)
- éviter les dépôts opportunistes non qualifiés à la racine
- aucune nouvelle documentation de support, preuve ponctuelle, export machine, pack legacy ou helper contextuel ne doit remonter à la racine

## Classes d’objets racine
- **Entrée produit/runtime** : artefacts d’accès immédiat à l’exécution
- **Support opératoire** : fichiers de support temporairement conservés avec justification
- **Legacy toléré** : éléments conservés pour compatibilité, explicitement marqués
- **Arbitrage ouvert** : objets à reclasser dans un chantier dédié ultérieur

## Fichiers racine legitimes observes au 2026-04-24
- `README.md` : point d'entree repo minimal (quickstart / verification)
- `.gitignore` : metadata Git canonique du repo
- `.gitattributes` : metadata Git canonique du repo
- `requirements.txt` : dependances Python repo-first
- `.env.example` : exemple minimal de configuration locale
- `webhook_server.py` : entrypoint runtime historique et toujours actif, encore reference par la doc canonique et les scripts de verification
- `bitget_bridge.py` : shim legacy de compatibilite vers `modules/simex_bitget_bridge/app/simex_bitget_bridge.py`, conserve explicitement en racine comme point d'entree historique secondaire

## Surfaces top-level explicitement tolerees par la politique racine
- `workflow_ai/` : doctrine locale d'execution IA et templates opposables
- `deploy_module_multi_machine/` : outillage valide de deploiement multi-machine
- `_archive/` : archive locale assumee, hors surface active

## Exception racine de compatibilite explicite
- `bitget_bridge.py` : shim legacy minimal, conserve en racine comme alias de compatibilite explicite ; aucun caller repo direct n'est prouve, mais `modules/simex_bitget_bridge/README.md` confirme que le shim reste disponible et les wrappers actifs pointent deja vers le module canonique

## Garde-fou local-only
- `_archive/`, `tmp/`, `__pycache__/`, `.ruff_cache/`, `.uv-cache/`, `.uv-python/`, `.secrets/` ne sont ni des sources de verite ni des prerequis de lecture canonique
- ces surfaces ne doivent jamais etre promues comme justification pour remonter d'autres artefacts a la racine
- les bundles locaux ignores a la racine (par exemple `GO_*_BUNDLE*` et les `.zip` de travail) restent des artefacts de transit non canoniques ; ils ne reouvrent pas la politique racine

## Lot de retrait applique
- `journal.md` : supprime comme surface de continuite locale obsolete
- `journal/` : supprime ; les resultats extraits utiles sont conserves sous forme documentaire dans `docs/governance/HUMAN_*`
- `modules/journal_de_bord/` : supprime comme outillage operatoire obsolete
- `tools/journal_from_paste.py` : supprime avec l'abandon de la journalisation repo

## Lot de reclassement racine applique
- `Readme` -> `README.md`
- `TOOLBOX.txt` : contenu fusionne dans `docs/admin_trading_desk_pro_quick_reference.md`, copie legacy archivee sous `_archive/root_backups/TOOLBOX_root_legacy_2026-04-24.txt`
- `UI_URLS.md` : contenu fusionne dans `docs/desk_pro_multi_machine_quick_reference.md`, copie legacy archivee sous `_archive/root_backups/UI_URLS_root_legacy_2026-04-24.md`
- `smartmoney.txt` : copie racine archivee sous `_archive/root_backups/smartmoney_root_legacy_2026-04-24.txt` ; surface active retenue = `tradingview/smartmoney_webhook_server_compat.pine`
- `strategy_logic.py` : reclassé vers `modules/decision_engine/app/strategy_logic.py`
- `validated_prompt_factory_role_preface.patch` : archive sous `_archive/root_backups/validated_prompt_factory_role_preface_2026-04-01.patch`
- `.gitignore.bak*` : aucun artefact present en racine ; backup observe sous `_archive/root_backups/.gitignore.bak2.20260219_111605`
- `trae_pack_texts/` : deplace hors racine vers `docs/ot/trae/trae_pack_texts/`

## Ensemble Trae/IDE (lecture de coherence)
- `workflow_ai/` : doctrine gated, GO/STOP, templates opposables
- `modules/validated_prompt_factory/` : generation de prompts structures pour session, patch, module et transfert
- `deploy_module_multi_machine/` : propagation multi-machine depuis `admin-trading`
- `docs/ot/trae/trae_pack_texts/README.md` : entree documentaire du support legacy Trae
- `docs/ot/trae/trae_pack_texts/trae_pack/` : archive de lecture gardee pour compatibilite documentaire

Regle retenue :
- l'ensemble est coherent comme pack de travail Trae/IDE, mais seule la couche repo-first canonique prime en cas de conflit
- `docs/ot/trae/trae_pack_texts/trae_pack/` ne doit pas redevenir une source de continuite opposable

## Limites
- ce document ne déplace aucun fichier à lui seul
- ce document ne remplace pas les chantiers de reclassement physique

## REPRISE
- closeout porte par `docs/chantiers/GO_OPT_TRADING_ROOT_POLICY_AND_RECLASS_01/90_closeout.md`
- lot dedie `GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01` deja clos

## RISKS

- À qualifier.
