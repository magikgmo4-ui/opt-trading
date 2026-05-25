---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_SCOPE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
go_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_SCOPE_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
MASTER_TARGET: github_actions_openclaw
status: open
lifecycle_stage: implementation
surface: github_actions
transport_mode: bundle_patch_zip
---

# 00_INITIAL_PROJECT_DOC — GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_SCOPE_01

## 1_MASTER_TARGET

`github_actions_openclaw`

## 3_INITIAL_NEED

Ajouter la couche de protection PR avant OpenClaw opérationnel :

- `.github/workflows/gated-pr.yml`
- `FILE_SCOPE.txt` par GO
- blocage des fichiers hors scope
- blocage des chevauchements de scope entre GO
- documentation des required checks GitHub

## 4_MASTER_PROJECT_PLAN

```text
master plan github_actions_openclaw
-> registry GitHub Actions
-> validation registry
-> bridge OpenClaw GitHub Actions
-> dry-run positif PASS
-> gated PR / FILE_SCOPE / no-overlap
-> orchestration OpenClaw opérationnelle
```

## 6_FINAL_TARGET

Une PR est bloquée si elle ne respecte pas son scope GO ou si elle modifie un fichier revendiqué par un autre GO.

## 12_INVARIANTS

- `origin/sot/mainline` est canonique.
- Pas de push direct sur `sot/mainline`.
- Pas de `reset --hard` sans backup explicite.
- Push forcé seulement avec `--force-with-lease`.
- OpenClaw orchestre, mais ne contourne jamais GitHub Actions.
- OpenClaw ne merge pas seul.
- Chaque GO doit déclarer son `FILE_SCOPE.txt`.

## 17_RESUME_POINT

Après merge : configurer les required checks côté GitHub puis ouvrir le GO d'orchestration opérationnelle.
