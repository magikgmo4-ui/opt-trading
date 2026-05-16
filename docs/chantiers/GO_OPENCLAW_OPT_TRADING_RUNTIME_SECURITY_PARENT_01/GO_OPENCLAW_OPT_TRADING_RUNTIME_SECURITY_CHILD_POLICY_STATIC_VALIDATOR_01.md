---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_STATIC_VALIDATOR_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_STATIC_VALIDATOR_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - static_validator
  - skill_policy_yaml
  - warning_only
  - no_runtime
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01.md
  - configs/openclaw/security/skill_policy.yaml
  - tools/openclaw/validate_skill_policy_static.py
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_STATIC_VALIDATOR_01

## 1_MASTER_TARGET

Ajouter un validateur statique warning-only pour `configs/openclaw/security/skill_policy.yaml`, sans execution runtime, sans mutation, sans auto-fix et sans blocage CI par defaut.

## 3_INITIAL_NEED

Le child precedent a cree le premier YAML declaratif de policy OpenClaw runtime security.

Besoin courant : verifier statiquement les defaults securises et les champs attendus sans activer de runtime ni imposer une CI bloquante.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_STATIC_VALIDATOR_01
```

Fichier ajoute :

```text
tools/openclaw/validate_skill_policy_static.py
```

## 6_FINAL_TARGET

**FINAL_TARGET : ajouter un validateur statique Python stdlib pour `skill_policy.yaml`, en mode `WARNING_ONLY`, avec sortie rapport texte, sans dependance externe, sans mutation, sans execution runtime, et avec exit code `0` par defaut.**

## WHY

Ce child existe pour rendre la policy YAML relisible et controlable automatiquement sans franchir la ligne vers l'execution.

Le validateur doit detecter les incoherences et defaults dangereux, mais ne doit pas corriger, bloquer, executer ou modifier.

## 7_CANONICAL_STATE

Etat valide :

- PR #413 mergee ;
- `configs/openclaw/security/skill_policy.yaml` existe ;
- branche child dediee creee puis realignee sur `sot/mainline` courant ;
- validateur ajoute sous `tools/openclaw/` ;
- runtime non modifie ;
- CI non modifiee ;
- index globaux non modifies.

## 8_VALIDATED_PLAN

- Lire le YAML comme texte.
- Ne pas ajouter de dependance PyYAML.
- Verifier les cles attendues.
- Verifier les niveaux L0-L8.
- Verifier les surfaces attendues.
- Verifier les defaults securises.
- Produire des warnings.
- Retourner `0` par defaut.

## 9_SELECTED_SOLUTION

Validateur Python autonome :

```text
tools/openclaw/validate_skill_policy_static.py
```

Mode par defaut :

```text
WARNING_ONLY
```

Option disponible mais non recommandee dans cette phase :

```text
--strict-exit
```

## 11_KEY_DECISIONS

- Pas de PyYAML.
- Pas de parsing runtime.
- Pas de mutation.
- Pas d'auto-fix.
- Pas de CI bloquante.
- Exit code `0` par defaut meme avec warnings.
- `--strict-exit` existe seulement pour usage futur explicite.

## 12_INVARIANTS

- Warning-only.
- Aucun runtime.
- Aucun service.
- Aucun secret.
- Aucun index global.
- Aucun auto-fix.
- Aucune execution de skill.
- Aucune mutation de fichier.

## 13_ESTABLISHED

Fichier ajoute :

```text
tools/openclaw/validate_skill_policy_static.py
```

Commande locale prevue :

```bash
python tools/openclaw/validate_skill_policy_static.py
```

La commande retourne `0` par defaut.

## 14_HYPOTHESIS

A valider ensuite :

- besoin de test fixture ;
- besoin d'un job CI non bloquant ;
- besoin de JSON report ;
- besoin d'un parseur YAML strict ;
- besoin d'un schema machine-checkable.

## 15_REMAINING_GAP

- Pas encore de test automatise.
- Pas encore de CI non bloquante.
- Pas encore de rapport JSON.
- Pas encore de validation YAML semantique stricte.
- Pas encore de liaison au skill registry.

## 16_TODO

Suite logique :

1. Reviewer le validateur.
2. Merge PR du child.
3. Ouvrir un child de tests fixtures.
4. Ajouter un test qui confirme le mode warning-only.
5. Ajouter ensuite un job CI non bloquant, si utile.

## 17_RESUME_POINT

Reprendre ici :

```text
tools/openclaw/validate_skill_policy_static.py
```

Prochain GO logique :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_VALIDATOR_TESTS_01
```

Objectif prochain : ajouter des tests fixtures pour prouver que le validateur reste warning-only et non destructif.

## 18_TO_DOCUMENT

TAGS :

- OPENCLAW_STATIC_VALIDATOR
- OPENCLAW_WARNING_ONLY
- OPENCLAW_NO_RUNTIME_EXECUTION
- OPENCLAW_POLICY_VALIDATION

## 19_TO_REMEMBER

Memory Bricks candidats projet :

- `tools/openclaw/validate_skill_policy_static.py` est le premier validateur statique warning-only de la policy OpenClaw runtime security.
- Le validateur retourne `0` par defaut et ne modifie rien.
- Suite logique forte : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_VALIDATOR_TESTS_01`.
