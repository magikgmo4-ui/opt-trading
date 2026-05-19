---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_TEST_PY314_COMPAT_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_TEST_PY314_COMPAT_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - unittest
  - py314
  - compatibility
  - warning_only
  - no_runtime
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_VALIDATOR_TESTS_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_NON_BLOCKING_CI_01.md
  - tests/openclaw/test_validate_skill_policy_static.py
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_TEST_PY314_COMPAT_01

## 1_MASTER_TARGET

Corriger la compatibilite locale Python 3.14 du test du validateur OpenClaw skill policy, sans modifier le comportement du validateur ni le workflow CI.

## 3_INITIAL_NEED

Le workflow warning-only est deja merge et cible Python 3.11 sur GitHub Actions.

Le besoin courant est de rendre le test local portable sous Python 3.14, car le chargement dynamique du module peut echouer si le module n'est pas enregistre dans `sys.modules` avant `exec_module`.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_TEST_PY314_COMPAT_01
```

Fichier cible :

```text
tests/openclaw/test_validate_skill_policy_static.py
```

## 6_FINAL_TARGET

Corriger la compatibilite Python 3.14 du test local sans changer la logique du validateur ni le workflow CI.

## WHY

Ce child existe pour supprimer une dette locale mineure de portabilite des tests.

Le but est de conserver un test warning-only stable sur les environnements locaux tout en laissant intact le comportement de la policy OpenClaw et du workflow GitHub Actions.

## 7_CANONICAL_STATE

Etat valide :

- PR #450 mergee ;
- workflow warning-only deja en place ;
- validateur statique deja stable ;
- test local Python 3.14 documente comme gap technique mineur ;
- aucun runtime modifie ;
- aucun workflow CI modifie ici ;
- aucun index global modifie.

## 8_VALIDATED_PLAN

- Ajouter `import sys`.
- Inserer le module dans `sys.modules` avant `exec_module`.
- Conserver le comportement du validateur.
- Ne pas modifier le workflow CI.
- Valider avec `git diff --check`.
- Valider avec le validateur direct.
- Valider avec `python -m unittest tests.openclaw.test_validate_skill_policy_static`.

## 9_SELECTED_SOLUTION

Patch minimal dans `load_validator_module()` :

```python
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
return module
```

## 11_KEY_DECISIONS

- Corriger le test, pas le validateur.
- Garder le workflow warning-only tel quel.
- Ne pas activer de runtime.
- Ne pas utiliser d'auto-fix.
- Ne pas changer les index globaux.
- Ne pas introduire de dette CI nouvelle.

## 12_INVARIANTS

- warning-only
- no runtime
- no service
- no secret
- no auto-fix
- no index global
- no workflow change
- no validator behavior change
- no file mutation outside the test file

## 13_ESTABLISHED

- `tests/openclaw/test_validate_skill_policy_static.py` existe ;
- le validateur statique OpenClaw existe ;
- le workflow warning-only est merge ;
- le test local Python 3.14 a un gap connu ;
- la cause probable est le chargement dynamique sans insertion préalable dans `sys.modules` ;
- la correction attendue est minimale et locale.

## 15_REMAINING_GAP

- Le comportement Python 3.14 local doit etre confirme apres patch.
- Le gap technique `GAP_LOCAL_PY314_DYNAMIC_IMPORT_01` doit etre ferme par validation locale.

## 16_TODO

Suite logique :

1. Appliquer le patch minimal au test.
2. Lancer le validateur direct.
3. Lancer `unittest`.
4. Ouvrir la PR de correction locale.

## 17_RESUME_POINT

Reprendre ici :

```text
tests/openclaw/test_validate_skill_policy_static.py
```

Prochain GO logique :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_TEST_PY314_COMPAT_01
```

Objectif prochain : valider la correction locale Python 3.14 puis merger le patch si les checks restent warning-only.
