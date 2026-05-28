---
doc_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01_TEST_LOCK_AND_VALIDATION
doc_type: validation_plan
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: validation_design
topic_keys:
  - tests
  - validation
  - smoke
  - regression_lock
  - code_ops
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 60_TEST_LOCK_AND_VALIDATION

## Objectif

Définir le verrouillage minimal avant refactor.

## Règle

On ne refactorise pas un comportement non verrouillé.

## Niveaux de validation

| Niveau | But | Exemple de preuve |
|---|---|---|
| `syntax` | fichier parseable | compilation ou parse local |
| `unit` | fonction verrouillée | test ciblé |
| `cli_smoke` | commande exécutable | aide CLI ou dry-run documenté |
| `json_contract` | sortie JSON parseable | parse strict documenté |
| `doc_command` | runbook exécutable | commandes copiables validées |
| `compat` | OS/shell validé | Bash et PowerShell si concernés |

## Validation registre future

Validateur candidat :

- chemin proposé : `tools/code_ops/validate_code_registry.py`
- entrée proposée : registre Markdown ou JSON défini dans `20_CODE_REGISTRY_SPEC.md`
- sortie attendue : statut, nombre d'entrées, erreurs, avertissements

## Tests à ajouter avant refactor

| Cas | Test attendu |
|---|---|
| CLI sans test | aide CLI ou smoke minimal |
| JSON output | parse et clés obligatoires |
| helper extrait | test unitaire de l'ancien comportement |
| suppression candidate | test du remplaçant |
| migration chemin | test import + runbook mis à jour |

## Critères de PASS batch

Un batch passe si :

- diff limité ;
- aucun code hors scope ;
- tests ciblés OK ;
- contrôle whitespace OK ;
- contrat CLI/JSON conservé ou migration documentée ;
- rollback simple ;
- compatibilité non régressée.

## Critères BLOCKED

Bloquer si :

- consommateur inconnu ;
- test absent sur zone critique ;
- sortie JSON non verrouillée ;
- différence Bash/PowerShell non comprise ;
- changement dépasse le batch ;
- dépendance externe non maîtrisée.

## Rapport de validation attendu

Chaque batch doit produire :

- scope ;
- fichiers changés ;
- validations exécutées ;
- résultats ;
- limites connues ;
- décision `PASS`, `REWORK` ou `BLOCKED` ;
- prochaine étape.

## Invariants

- `PASS` sans commande exécutée doit être justifié comme `DOC_ONLY_PASS`, pas `RUNTIME_PASS`.
- Un test manquant n'est pas un échec, mais bloque certains refactors.
- Les validations doc-only ne prouvent pas la compatibilité runtime.
