---
go_id: GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Stabiliser le contrat source-of-truth registry apres `P2_MODULE_FAMILY_CLOSEOUT`.

## 2_INITIAL_PROJECT_DOC
This document.

## 3_INITIAL_NEED
P2 a clarifie plusieurs stacks et applique plusieurs realignements registry, mais le contrat transverse reste implicite: priorite des registres centraux, statut des vues derivees, fallbacks locaux toleres, gestion des divergences, et vocabulaire minimal de statut/machine.

## 4_MASTER_PROJECT_PLAN
1. Formaliser quelles registries centrales sont sources de verite.
2. Classer readers, facade, seeds, exports et copies comme derives ou fallbacks.
3. Definir les regles de divergence et les conditions d'autorisation de fallback local.
4. Poser un modele minimal de `status` et de `machine_target`.
5. Produire la liste des prochains GO d'implementation.

## 6_FINAL_TARGET
Un contrat de gouvernance registry doc-only, exploitable par les futurs GOs d'implementation, sans mutation runtime ni mutation des registries centrales dans ce lot.

## 7_CANONICAL_STATE
- `registry/modules_registry.yaml`, `registry/machines_registry.yaml`, `registry/wrappers_registry.yaml`, `registry/ui_surfaces_registry.yaml`, `registry/meta_index.yaml` existent.
- les readers canoniques lisent deja directement les YAML centraux.
- `ui_registry_msi` possede encore un seed local JSON en fallback.
- des vues derivees/export JSON existent deja sous `modules/*/output/`.

## 12_INVARIANTS
- doc-only
- no runtime mutation
- no registry mutation
- no global index mutation
- no `secrets/`

## 16_TODO
- [x] Lire les sources imposees et la surface des readers
- [x] Rediger le contrat source-of-truth registry
- [x] Verifier le scope doc-only
- [ ] Commit, push, ouvrir PR

## 17_RESUME_POINT
Formaliser la priorite des `registry/*.yaml`, encadrer les fallbacks locaux, et preparer les GOs d'implementation `source-of-truth`, `deepseek_student`, et `machine_target`.
