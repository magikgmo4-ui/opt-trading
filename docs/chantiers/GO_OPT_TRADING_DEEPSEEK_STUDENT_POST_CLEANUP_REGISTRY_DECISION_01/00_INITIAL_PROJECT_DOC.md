---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_POST_CLEANUP_REGISTRY_DECISION_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Finaliser la decision registry centrale pour `deepseek_student` apres fermeture runtime boundary et cleanup compat wrappers.

## 3_INITIAL_NEED
Les lots precedents ont retire l'ambiguite de frontiere: `student/scripts/` est maintenant la surface canonique, `scripts/student/` un shim legacy, et `modules/deepseek_student/` un scaffold non-runtime. Il faut donc re-evaluer si un objet registry central `deepseek_student` a encore un sens.

## 6_FINAL_TARGET
Une decision doc-only sur le maintien hors registries centrales ou, si justifie, la preparation d'une entree future `legacy` ou `transitional` ciblee sur le bon objet post-cleanup.

## 12_INVARIANTS
- doc-only
- no registry mutation
- no runtime mutation
- no global index mutation
- no `secrets/`

## 16_TODO
- [x] Relire les decisions pre-cleanup et le contrat registry
- [x] Evaluer l'objet post-cleanup representable
- [ ] Verifier le scope doc-only

## 17_RESUME_POINT
Trancher si `deepseek_student` reste exclu des registries centrales apres cleanup, ou si une mutation registry dediee devient maintenant justifiee.
