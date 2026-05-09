---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-09
topic_keys:
  - openclaw
  - runtime_security
  - skill_policy_yaml
  - warning_only
  - no_runtime
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01.md
  - configs/openclaw/security/skill_policy.yaml
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01

## 1_MASTER_TARGET

Creer le premier fichier YAML de policy OpenClaw runtime security, encore non connecte au runtime et sans validation bloquante.

## 3_INITIAL_NEED

Le child precedent a defini le schema cible `skill_policy.yaml`.

Besoin courant : poser un premier draft concret pour stabiliser les champs, defaults et enums avant toute integration runtime.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01
```

Fichier YAML ajoute :

```text
configs/openclaw/security/skill_policy.yaml
```

Scope : documentation/config draft uniquement.

## 6_FINAL_TARGET

**FINAL_TARGET : creer un premier fichier `configs/openclaw/security/skill_policy.yaml` declaratif, warning-only, non connecte au runtime, avec defaults securises et sample skill read-only.**

## WHY

Ce child transforme le schema documentaire en artefact concret sans activer l'execution.

Le but est de pouvoir relire, reviewer et stabiliser la policy sous forme YAML avant de brancher un validateur ou un runtime.

## 7_CANONICAL_STATE

Etat valide :

- PR #291 mergee ;
- schema policy documente ;
- branche child dediee creee ;
- YAML draft ajoute ;
- runtime non modifie ;
- validation bloquante non ajoutee ;
- index globaux non modifies.

## 8_VALIDATED_PLAN

- Ajouter `configs/openclaw/security/skill_policy.yaml`.
- Garder `runtime_execution_enabled: false`.
- Garder `warning_only_default: true`.
- Garder `can_fail_ci: false`.
- Ajouter un sample skill read-only.
- Documenter le point de reprise.

## 9_SELECTED_SOLUTION

YAML declaratif version `0.1`, avec :

- `policy_version` ;
- `policy_id` ;
- defaults securises ;
- niveaux L0-L8 ;
- surfaces runtime ;
- confirmation ;
- audit ;
- promotion ;
- static validation warning-only ;
- sample skill `docs_reader`.

## 11_KEY_DECISIONS

- Le YAML est cree sous `configs/openclaw/security/`.
- Le YAML n'est pas connecte au runtime.
- La validation reste warning-only.
- La CI ne peut pas etre bloquee par cette policy.
- Aucun auto-fix.
- Sample skill uniquement read/analyze/plan.

## 12_INVARIANTS

- Aucun runtime.
- Aucun service.
- Aucun secret.
- Aucun index global.
- Aucun auto-fix.
- Pas de validation bloquante.
- `runtime_execution_enabled: false`.
- `warning_only_default: true`.

## 13_ESTABLISHED

Fichier ajoute :

```text
configs/openclaw/security/skill_policy.yaml
```

Defaults poses :

```yaml
runtime_execution_enabled: false
warning_only_default: true
default_mode: "READ_ONLY"
validation_mode: "WARNING_ONLY"
can_fail_ci: false
can_autofix: false
```

## 14_HYPOTHESIS

A valider dans un prochain child :

- besoin d'un schema YAML separe ;
- besoin d'un validateur statique ;
- format des warnings ;
- emplacement final du validateur ;
- rattachement CI non bloquant.

## 15_REMAINING_GAP

- Pas encore de validateur.
- Pas encore de tests YAML.
- Pas encore de schema formel machine-checkable.
- Pas encore de liaison au skill registry.
- Pas encore de lecture runtime.

## 16_TODO

Suite logique :

1. Reviewer le YAML draft.
2. Merge PR du child.
3. Ouvrir un child de validation statique warning-only.
4. Ajouter un validateur qui lit le YAML sans executer d'action.
5. Ajouter des tests non bloquants.

## 17_RESUME_POINT

Reprendre ici :

```text
configs/openclaw/security/skill_policy.yaml
```

Prochain GO logique :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_STATIC_VALIDATOR_01
```

Objectif prochain : ajouter un validateur statique warning-only, sans execution runtime et sans blocage CI.

## 18_TO_DOCUMENT

TAGS :

- OPENCLAW_SKILL_POLICY_YAML
- OPENCLAW_WARNING_ONLY
- OPENCLAW_NO_RUNTIME_EXECUTION
- OPENCLAW_POLICY_DRAFT

## 19_TO_REMEMBER

Memory Bricks candidats projet :

- `configs/openclaw/security/skill_policy.yaml` est le premier draft YAML de policy OpenClaw runtime security.
- Le YAML est declaratif, warning-only et non connecte au runtime.
- Suite logique forte : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_STATIC_VALIDATOR_01`.
