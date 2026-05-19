---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_VALIDATOR_TESTS_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_VALIDATOR_TESTS_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - policy_validator_tests
  - warning_only
  - unittest
  - no_runtime
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_STATIC_VALIDATOR_01.md
  - tools/openclaw/validate_skill_policy_static.py
  - tests/openclaw/test_validate_skill_policy_static.py
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_VALIDATOR_TESTS_01

## 1_MASTER_TARGET

Ajouter des tests fixtures pour prouver que le validateur statique OpenClaw skill policy reste warning-only, non destructif et sans dependance externe.

## 3_INITIAL_NEED

Le child precedent a ajoute `tools/openclaw/validate_skill_policy_static.py`.

Besoin courant : prouver le comportement attendu du validateur sans connecter de runtime, sans modifier les fichiers projet et sans ajouter de CI bloquante.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_VALIDATOR_TESTS_01
```

Fichier test ajoute :

```text
tests/openclaw/test_validate_skill_policy_static.py
```

## 6_FINAL_TARGET

**FINAL_TARGET : ajouter un test `unittest` stdlib qui verifie que le validateur retourne `0` par defaut, produit un rapport `WARNING_ONLY`, detecte les defaults dangereux et ne mute pas les fixtures.**

## WHY

Ce child existe pour eviter que le validateur statique devienne implicitement bloquant ou destructif.

Les tests servent a figer le comportement securise : signaler les problemes, mais ne pas executer, ne pas modifier et ne pas bloquer par defaut.

## 7_CANONICAL_STATE

Etat valide :

- PR #446 mergee ;
- validateur statique disponible ;
- branche child dediee creee ;
- tests stdlib ajoutes ;
- runtime non modifie ;
- CI non modifiee ;
- index globaux non modifies.

## 8_VALIDATED_PLAN

- Utiliser `unittest` standard library.
- Importer le validateur depuis son chemin fichier.
- Tester le YAML reel.
- Tester policy manquante en mode warning-only.
- Tester `--strict-exit` seulement comme option future explicite.
- Tester la detection de defaults dangereux.
- Verifier l'absence de mutation de fixture temporaire.

## 9_SELECTED_SOLUTION

Test autonome :

```text
tests/openclaw/test_validate_skill_policy_static.py
```

Commande locale :

```bash
python -m unittest tests.openclaw.test_validate_skill_policy_static
```

## 11_KEY_DECISIONS

- Pas de pytest requis.
- Pas de dependance externe.
- Pas de CI change.
- Pas d'execution runtime.
- Pas de mutation projet.
- `--strict-exit` teste seulement comme comportement optionnel.

## 12_INVARIANTS

- Warning-only par defaut.
- Aucun runtime.
- Aucun service.
- Aucun secret.
- Aucun index global.
- Aucun auto-fix.
- Aucune mutation de fichier projet.
- Aucune CI bloquante dans ce child.

## 13_ESTABLISHED

Fichier ajoute :

```text
tests/openclaw/test_validate_skill_policy_static.py
```

Tests couverts :

- policy reelle retourne `0` ;
- rapport contient `WARNING_ONLY` ;
- policy manquante retourne `0` par defaut ;
- `--strict-exit` retourne `1` si findings ;
- defaults dangereux detectes ;
- fixture temporaire non supprimee par le validateur.

## 14_HYPOTHESIS

A valider ensuite :

- besoin d'un job CI non bloquant ;
- besoin d'un rapport JSON ;
- besoin de fixtures multiples ;
- besoin de parsing YAML strict.

## 15_REMAINING_GAP

- Pas de CI non bloquante.
- Pas de rapport JSON.
- Pas de schema machine-checkable.
- Pas de tests sur policies multiples.
- Pas de lien skill registry.

## 16_TODO

Suite logique :

1. Reviewer tests.
2. Merge PR du child.
3. Ouvrir un child CI non bloquant si utile.
4. Ajouter un job manuel ou non bloquant qui lance les tests.

## 17_RESUME_POINT

Reprendre ici :

```text
tests/openclaw/test_validate_skill_policy_static.py
```

Prochain GO logique :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_NON_BLOCKING_CI_01
```

Objectif prochain : ajouter une execution CI non bloquante ou manuelle pour le validateur, sans transformer les warnings en blocage.

## 18_TO_DOCUMENT

TAGS :

- OPENCLAW_VALIDATOR_TESTS
- OPENCLAW_WARNING_ONLY
- OPENCLAW_UNITTEST
- OPENCLAW_NO_RUNTIME_EXECUTION

## 19_TO_REMEMBER

Memory Bricks candidats projet :

- `tests/openclaw/test_validate_skill_policy_static.py` prouve le mode warning-only du validateur de policy OpenClaw.
- Les tests utilisent uniquement `unittest` et ne changent pas la CI.
- Suite logique forte : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_NON_BLOCKING_CI_01`.
