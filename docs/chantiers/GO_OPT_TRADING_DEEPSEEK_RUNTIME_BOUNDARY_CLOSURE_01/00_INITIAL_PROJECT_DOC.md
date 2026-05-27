---
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_BOUNDARY_CLOSURE_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Fermer la frontiere runtime `deepseek_student` entre `modules/deepseek_student/`, `scripts/student/`, et `student/scripts/`.

## 3_INITIAL_NEED
Le GO precedent a decide de garder `deepseek_student` hors registries centrales tant que la frontiere physique/runtime n'est pas close. Ce lot doit donc designer la surface survivante reelle, classifier les deux autres surfaces, et preparer le GO d'execution suivant si un cleanup physique reste a faire.

## 6_FINAL_TARGET
Une decision explicite sur:
- la surface runtime survivante
- la surface legacy compat a conserver temporairement
- la surface module non-runtime a laisser hors verite centrale

## 12_INVARIANTS
- doc-only
- no runtime mutation
- no registry mutation
- no global index mutation
- no `secrets/`

## 16_TODO
- [x] Lire les surfaces et callers actifs
- [x] Trancher la surface survivante
- [ ] Verifier le scope doc-only

## 17_RESUME_POINT
Fixer `student/scripts/` comme survivant canonique si les preuves runtime convergent, puis releguer `scripts/student/` en compat et `modules/deepseek_student/` hors runtime.
