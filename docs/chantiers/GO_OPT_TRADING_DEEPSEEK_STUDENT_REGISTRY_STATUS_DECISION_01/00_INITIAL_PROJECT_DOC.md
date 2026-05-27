---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_REGISTRY_STATUS_DECISION_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Decider le sort registry central de `deepseek_student` sans melanger ce lot avec le raffinement global de `machine_target`.

## 3_INITIAL_NEED
`deepseek_student` est deja qualifie comme legacy/transitoire dans les decisions famille, mais reste hors registries centrales. Il faut maintenant trancher entre ajout central `legacy`/`transitional` ou priorite a une fermeture physique/runtime d'abord.

## 6_FINAL_TARGET
Une decision explicite, doc-only, sur la politique centrale a tenir pour `deepseek_student` et le prochain GO d'execution qui en decoule.

## 12_INVARIANTS
- doc-only
- no runtime mutation
- no registry mutation
- no global index mutation
- no `secrets/`

## 16_TODO
- [x] Lire les preuves famille/registry/runtime pertinentes
- [x] Trancher la politique registry centrale
- [ ] Verifier le scope doc-only

## 17_RESUME_POINT
Trancher si `deepseek_student` entre maintenant avec un statut central, ou reste hors registries jusqu'a fermeture de la frontiere `modules/deepseek_student/` / `scripts/student/` / `student/scripts/`.
