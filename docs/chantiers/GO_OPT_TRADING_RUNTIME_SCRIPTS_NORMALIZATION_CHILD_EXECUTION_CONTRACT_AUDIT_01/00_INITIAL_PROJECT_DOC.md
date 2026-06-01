---
doc_id: RUNTIME_SCRIPTS_NORMALIZATION_EXECUTION_CONTRACT_AUDIT_00
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
module: runtime_scripts_normalization
go_id: GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01
status: open
lifecycle_stage: audit_doc_only
topic_keys:
  - opt-trading
  - runtime
  - scripts
  - jobs
  - registry
  - execution_contract
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-31
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md
  - docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_IMPL_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01/10_REGISTRY_SOURCE_MAP.md
  - registry/modules_registry.yaml
  - registry/wrappers_registry.yaml
  - registry/machines_registry.yaml
  - config/machine_runtime_map.yml
---

# 00_INITIAL_PROJECT_DOC

## GO_HEADER

```yaml
GO_ID: GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: null
MASTER_TARGET_ID: null
MASTER_PROJECT_PLAN_ID: null
PARENT_GO_ID: GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_IMPL_01
NEXT_ATTACH_TARGET: null
6_FINAL_TARGET: "Audit doc-only ouvrant le contrat execution runtimes/scripts/jobs"
BUNDLE_TARGET: "patch doc-only du chantier"
TRANSPORT_MODE: patch_only
CLOSE_GATE_MASTER_TARGET: not_applicable
```

## 1_MASTER_TARGET

Ouvrir un child GO doc-only qui relie l'execution runtime, les scripts, les jobs et la sante runtime aux sources existantes du repo, sans creer un second systeme de normalisation.

## 2_INITIAL_PROJECT_DOC

Ce fichier est le document initial canonique du chantier.

## 3_INITIAL_NEED

Le repo contient deja des registres centraux, des registres Markdown, une map runtime operationnelle et un module `runtime_health`. Le gap restant n'est pas l'absence de registry, mais l'absence d'un contrat execution machine-readable qui relie explicitement :

- module registry;
- code registry;
- jobs registry;
- wrappers registry;
- machines registry;
- runtime map;
- runtime health.

## 4_MASTER_PROJECT_PLAN

1. Lire les regles de gouvernance et confirmer le mode `patch_only`.
2. Lire les registries centrales et les registres Markdown existants.
3. Documenter le modele source-of-truth reel.
4. Proposer le draft de `registry/runtime_execution_contracts.yaml`.
5. Classer les gaps modules, wrappers, machines et tests.
6. Produire un plan d'implementation suivant, sans mutation runtime.

## 6_FINAL_TARGET

Un chantier local complet avec six livrables doc-only et un patch de transport, utilisable pour lancer ensuite une implementation bornee :

- creation future de `registry/runtime_execution_contracts.yaml`;
- creation future de `docs/registry/RUNTIME_EXECUTION_CONTRACTS.md` comme vue derivee;
- creation future de `scripts/validate_runtime_execution_contracts.py`;
- branchement CI futur dans `gh-actions-registry-validation.yml`;
- integration runtime health future, progressive et diagnostic-only.

## 7_CANONICAL_STATE

Etat etabli par lecture locale du repo le 2026-05-31 :

| Surface | Etat observe |
| --- | --- |
| `registry/modules_registry.yaml` | present, 49 entrees |
| `registry/wrappers_registry.yaml` | present, 56 wrappers |
| `registry/machines_registry.yaml` | present, 5 machines |
| `registry/ui_surfaces_registry.yaml` | present, 22 surfaces |
| `registry/meta_index.yaml` | present, 4 registries centrales |
| `config/machine_runtime_map.yml` | present, 5 cles machines runtime |
| `docs/registry/CODE_REGISTRY.md` | present, registre code canonique v1 |
| `docs/registry/JOBS_REGISTRY.md` | present, registre jobs canonique v1 |
| `.github/workflows/*.yml` | 7 workflows |
| `modules/runtime_health/` | present, diagnostic-only, lit `machine_runtime_map.yml` |

Constat structurant : `registry/*.yaml` reste la source centrale, et `config/machine_runtime_map.yml` doit etre traite comme projection operationnelle runtime, pas comme registry concurrente.

## 8_SELECTED_SOLUTION

La solution retenue est une couche pont :

```text
registry source-of-truth
-> runtime execution contract
-> wrapper coverage
-> runtime health integration
-> CI validation
-> migration progressive
```

Le futur contrat ne remplace ni `modules_registry.yaml`, ni `wrappers_registry.yaml`, ni `machines_registry.yaml`, ni `CODE_REGISTRY.md`, ni `JOBS_REGISTRY.md`.

## 12_INVARIANTS

- doc-only dans ce lot;
- pas de modification runtime;
- pas de deplacement ou renommage de scripts;
- pas de mutation de `registry/*.yaml`;
- pas de mutation de `config/machine_runtime_map.yml`;
- pas de modification des index globaux;
- pas de fermeture du parent;
- pas d'auto-heal runtime;
- pas d'execution de trading reel;
- pas d'ajout de secrets.

## 15_REMAINING_GAP

Le gap central est un contrat execution canonique reliant module, code, job, wrapper, machine, entrypoint, inputs, outputs, effets de bord, healthcheck, tests, risk et status.

Les gaps secondaires sont :

- couverture module registry incomplete par rapport aux dossiers physiques;
- couverture wrapper incomplete par rapport aux `wrappers_expected`;
- divergence entre identifiants machines snake_case et cles runtime hyphen-case;
- autorite exacte de `machine_runtime_map.yml` a formaliser comme projection operationnelle;
- hygiene de decouverte pytest et artefacts Python generes a traiter dans un lot dedie.

## 16_TODO

- [x] Verifier l'etat Git.
- [x] Lire la gouvernance obligatoire utile.
- [x] Lire les registries et registres imposes.
- [x] Creer les documents de chantier.
- [ ] Produire le patch final.
- [ ] Lancer un GO d'implementation separe pour le YAML, le validateur et la CI.

## 17_RESUME_POINT

Repartir des sources existantes : `registry/*.yaml`, `docs/registry/CODE_REGISTRY.md`, `docs/registry/JOBS_REGISTRY.md`, `config/machine_runtime_map.yml` et `modules/runtime_health/`.

Ne pas creer une normalisation parallele. Ajouter d'abord un pont `runtime_execution_contracts.yaml`, puis valider par CI avant toute migration de scripts ou integration runtime.
