---
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_COMPAT_WRAPPERS_CLEANUP_01
doc_type: INITIAL_PROJECT_DOC
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET
Faire converger la couche legacy `scripts/student/` vers la surface canonique `student/scripts/` sans retirer encore la compatibilite.

## 3_INITIAL_NEED
La frontiere runtime est closee au niveau decisionnel, mais plusieurs wrappers legacy existent encore dans `scripts/student/`, dont un `student_cmd.sh` recursif. Ce lot doit transformer la couche legacy en shim de compatibilite explicite vers `student/scripts/`.

## 6_FINAL_TARGET
Les entrypoints legacy `student` et `deepseek_student` deleguent vers les wrappers canoniques `student/scripts/`, et les controles minimaux verrouillent l'absence de recursion legacy.

## 12_INVARIANTS
- pas de suppression de `scripts/student/`
- pas de mutation registry
- pas de mutation runtime lourde
- pas de `secrets/`

## 16_TODO
- [x] Auditer les wrappers legacy et canoniques
- [x] Remplacer les wrappers legacy par des shims de compatibilite
- [x] Ajouter verification ciblee
- [x] Verifier le lot

## 17_RESUME_POINT
Conserver `scripts/student/` uniquement comme facade de compatibilite vers `student/scripts/`, sans maintenir de logique divergente locale.
