---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
lifecycle_stage: implementation
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: DATA_CENTER_LAYOUT_AND_REGISTRY_INIT
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01
topic_keys:
  - opt-trading
  - data_center
  - registry_storage
  - layout
  - module
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01/20_PRODUCER_INVENTORY.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_CONSUMER_CONTRACTS_01/20_CONSUMER_INVENTORY.md
  - modules/data_center/layout.py
  - modules/data_center/registry/producers.json
  - modules/data_center/registry/consumers.json
  - docs/index/inbox/GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01.md
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Data Center opérationnel : producteurs et consommateurs partagent les mêmes contrats normalisés. *(hérité)*

## 2_INITIAL_PROJECT_DOC

Troisième child GO du parent Data Center. Ce chantier est **implémentation** : il crée le module `modules/data_center/` avec layout initializer, registres JSON canoniques et tests.

## 3_INITIAL_NEED

Les deux premiers child GOs ont produit les contrats producers et consumers sous forme de docs. Ce child matérialise ces contrats en :
- un module Python `modules/data_center/` respectant la convention module du repo ;
- les registres JSON canoniques (`producers.json`, `consumers.json`) sous `modules/data_center/registry/` (committés) ;
- une fonction `ensure_data_center_dirs()` qui initialise le layout runtime `data/data_center/` (gitignored).

Contrainte clé : `data/` est entièrement gitignored (`/data/` + `**/data/` dans `.gitignore`). Les fichiers committés sont sous `modules/data_center/registry/`. Le layout runtime est créé à l'exécution.

## 4_MASTER_PROJECT_PLAN — périmètre child

1. Créer `modules/data_center/__init__.py`.
2. Créer `modules/data_center/layout.py` — `ensure_data_center_dirs()`, `get_producer_dir()`, `load_producers_registry()`, `load_consumers_registry()`.
3. Créer `modules/data_center/registry/producers.json` — registre canonical des 3 producers.
4. Créer `modules/data_center/registry/consumers.json` — registre canonical des 7 consumers.
5. Créer les 4 scripts module convention.
6. Créer `modules/data_center/tests/test_layout.py` — 8 tests couvrant layout, idempotence et chargement registres.

## 7_CANONICAL_STATE

- `data/` gitignored — aucun fichier runtime commitable sous ce path.
- `collectors_core` fournit `ensure_directory`, `atomic_write_json` via `packages/collectors_core`.
- Layout cible `data/data_center/<family>/<producer_id>/` défini dans PRODUCER_INVENTORY.
- Registres JSON spécifiés dans PRODUCER_INVENTORY et CONSUMER_INVENTORY.

## 11_KEY_DECISIONS

- Les registres canoniques vivent sous `modules/data_center/registry/` (committés).
- Le layout runtime (`data/data_center/`) est créé par `ensure_data_center_dirs()` au premier run.
- `modules/data_center/` suit la convention module complète (4 scripts).
- Pas de dépendance à `collectors_core` dans `layout.py` — stdlib seulement (`pathlib`, `json`).

## 12_INVARIANTS

- Aucune modification de `data/` dans git.
- `ensure_data_center_dirs()` est idempotente.
- Les registres JSON ne contiennent pas de secrets ni de chemins absolus.
- Les 4 scripts module convention sont présents.

## 15_REMAINING_GAP

- Migration du path Desk Pro (`data/deskpro/inputs/market_metrics/`) vers Data Center : hors scope.
- Tests de compatibilité contractuelle (smoke) : child suivant `CONTRACT_TESTS_01`.

## 16_TODO

1. Écrire `layout.py`.
2. Écrire `registry/producers.json` et `registry/consumers.json`.
3. Écrire les 4 scripts.
4. Écrire `tests/test_layout.py`.
5. Vérifier `python3 -m pytest modules/data_center/tests/`.

## 17_RESUME_POINT

Prochain child : `GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01` — tests smoke de compatibilité contractuelle.

---

## BUNDLE_TARGET — DATA_CENTER_LAYOUT_AND_REGISTRY_INIT

Fermable quand :
- `modules/data_center/layout.py` présent et fonctionnel ;
- `modules/data_center/registry/producers.json` et `consumers.json` valides ;
- 4 scripts présents ;
- tous les tests passent.
