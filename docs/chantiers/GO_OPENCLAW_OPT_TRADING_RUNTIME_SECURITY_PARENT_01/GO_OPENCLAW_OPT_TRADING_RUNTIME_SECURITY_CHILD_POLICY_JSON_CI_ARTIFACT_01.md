---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_CI_ARTIFACT_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_CI_ARTIFACT_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - policy_json_report
  - workflow_artifact
  - github_actions
  - warning_only
  - manual
  - no_runtime
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_REPORT_01.md
  - .github/workflows/openclaw-skill-policy-warning-only.yml
  - tools/openclaw/validate_skill_policy_static.py
  - tests/openclaw/test_validate_skill_policy_static.py
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_CI_ARTIFACT_01

## 1_MASTER_TARGET

Faire produire le rapport JSON du validateur OpenClaw skill policy comme artefact du workflow manuel warning-only, sans rendre la CI bloquante.

## 3_INITIAL_NEED

Le validateur produit deja un rapport JSON machine-readable.

Le besoin courant est de publier ce rapport dans GitHub Actions comme artefact consultable, sans introduire de gate bloquant, sans runtime et sans mutation.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_CI_ARTIFACT_01
```

Fichiers modifies :

```text
.github/workflows/openclaw-skill-policy-warning-only.yml
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_CI_ARTIFACT_01.md
```

## 6_FINAL_TARGET

Ajouter au workflow manuel warning-only une generation du rapport JSON et son upload en artefact, tout en gardant le comportement warning-only et les tests stdlib.

## WHY

Ce child existe pour rendre le rapport JSON exploitable hors du job sans transformer le workflow manuel en garde bloquante.

L'artefact permet la lecture, l'archive et la reprise, mais ne change ni l'exit code warning-only ni la nature non destructive du workflow.

## 7_CANONICAL_STATE

Etat valide :

- PR #453 mergee ;
- rapport JSON du validateur disponible ;
- workflow warning-only manuel disponible ;
- aucun runtime modifie ;
- aucun auto-fix ;
- aucune CI bloquante pour les PR ;
- aucun index global modifie.

## 8_VALIDATED_PLAN

- Garder `workflow_dispatch`.
- Executer le validateur texte.
- Generer le rapport JSON via `--format json`.
- Uploader le JSON comme artefact.
- Conserver les tests `unittest`.
- Ne pas utiliser `--strict-exit` par defaut.

## 9_SELECTED_SOLUTION

Workflow manuel warning-only avec export JSON puis `actions/upload-artifact`.

## 11_KEY_DECISIONS

- Le format texte reste le default.
- Le JSON est publie comme artefact, pas comme gate.
- Le workflow reste manuel.
- Aucun runtime.
- Aucune mutation de fichier.
- Aucun index global.
- Aucune CI bloquante.

## 12_INVARIANTS

- WARNING_ONLY
- aucun runtime
- aucun service
- aucun secret
- aucun auto-fix
- aucun index global
- aucune mutation de fichier
- aucune CI bloquante pour les PR
- aucune execution destructive

## 13_ESTABLISHED

- `python tools/openclaw/validate_skill_policy_static.py --format json` fonctionne.
- Le workflow warning-only existe deja.
- Le prochain pas est la publication de l'artefact JSON.
- Le comportement warning-only doit rester inchange.

## 14_HYPOTHESIS

A valider ensuite :

- nom exact de l'artefact ;
- retention_days ;
- besoin futur d'un consommateur CI ou dashboard.

## 15_REMAINING_GAP

- Pas encore d'artefact JSON publie.
- Pas encore de retention explicite.
- Pas encore de consommateur automatisé de l'artefact.

## 16_TODO

Suite logique :

1. Reviewer le workflow modifie.
2. Merger la PR du child.
3. Eventuellement definir une retention ou un consommateur.

## 17_RESUME_POINT

Reprendre ici :

```text
.github/workflows/openclaw-skill-policy-warning-only.yml
```
