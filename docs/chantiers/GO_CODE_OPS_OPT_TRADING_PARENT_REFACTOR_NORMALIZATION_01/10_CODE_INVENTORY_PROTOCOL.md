---
doc_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01_CODE_INVENTORY_PROTOCOL
doc_type: audit_protocol
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: audit
topic_keys: [code_inventory, code_ops, audit_first, no_mutation]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 10_CODE_INVENTORY_PROTOCOL

## Objectif

Définir l'inventaire initial du code avant tout refactor.

L'inventaire doit prouver :

- quels fichiers existent réellement ;
- quel rôle chaque fichier joue ;
- quels fichiers sont exécutables ;
- quels fichiers sont importés ;
- quels fichiers sont testés ;
- quels fichiers sont potentiellement redondants ;
- quelles surfaces sont sensibles.

## Règle centrale

```text
Aucun refactor sans inventaire.
Aucune suppression sans preuve.
Aucun renommage sans liste de consommateurs.
```

## Périmètre à scanner

| Surface | Inclure | But |
|---|---:|---|
| `tools/` | oui | scripts CLI, validateurs, helpers opératoires |
| `modules/` | oui | runtime et logique durable |
| `tests/` | oui | couverture et points de verrouillage |
| `docs/` | partiel | runbooks exécutables, contrats, index locaux |
| `.github/workflows/` | oui | compatibilité CI |
| `scripts/` | oui si présent | wrappers et tâches d'environnement |
| `config/` | oui si présent | schémas, mappings, paramètres |
| `data/` | non par défaut | données lourdes hors refactor, sauf contrats |
| `artifacts/` | non | sorties générées, sauf exemples de contrat |

## Tables d'inventaire attendues

### Table A — fichiers de code

| path | role | surface | executable | imported_by | tests | status | risk |
|---|---|---|---:|---|---|---|---|
| à remplir | cli/module/validator/adapter/schema/helper | tools/modules/tests | oui/non | à remplir | à remplir | active/candidate/deprecated | low/medium/high |

### Table B — entrypoints CLI

| command | path | args | output | json_parseable | docs | tests |
|---|---|---|---|---:|---|---|
| à remplir | à remplir | à remplir | stdout/file | oui/non | lien | lien |

### Table C — validateurs

| validator_id | path | validates | input | output | blocking | tests | duplicate_suspect |
|---|---|---|---|---|---:|---|---|

### Table D — schémas / contrats

| contract_id | path | format | consumers | producers | validation |
|---|---|---|---|---|---|

## Méthode d'audit

### 1. Lire l'état Git

```bash
git status --short --branch
git branch --show-current
git remote -v
git fetch --prune origin
git rev-parse HEAD
git rev-parse origin/sot/mainline
```

### 2. Lister les fichiers candidats

```bash
git ls-files 'tools/*' 'modules/*' 'tests/*' '.github/workflows/*' 'scripts/*' 'config/*'
```

### 3. Identifier les exécutables

```bash
git grep -n "if __name__ == .__main__." -- '*.py'
git grep -n "argparse\|click\|typer" -- '*.py'
```

### 4. Identifier les sorties JSON

```bash
git grep -n "json.dump\|json.dumps\|\.json" -- '*.py' '*.md'
```

### 5. Identifier les imports transverses

```bash
git grep -n "^from \|^import " -- '*.py'
```

## Critères de classification

| Rôle | Définition |
|---|---|
| `runtime` | exécuté dans le flux produit réel |
| `cli` | appelé directement par opérateur, CI ou wrapper |
| `validator` | vérifie un contrat, schéma, sécurité ou registre |
| `adapter` | convertit une source vers un format interne |
| `schema` | définit une structure attendue |
| `helper` | utilitaire partagé |
| `test` | verrou de comportement |
| `doc_runbook` | documentation contenant des commandes exécutables |

## Niveaux de risque

| Niveau | Définition |
|---|---|
| `low` | fichier isolé, testé, sans consommateur externe connu |
| `medium` | fichier utilisé par un runbook ou un autre module |
| `high` | entrypoint CLI, CI, runtime, stratégie, sécurité, ou ingestion |
| `blocked` | consommateur inconnu ou risque de casse non borné |

## Sortie attendue du premier sous-GO

```text
docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01/
  00_INITIAL_PROJECT_DOC.md
  10_FILE_INVENTORY.md
  20_ENTRYPOINTS.md
  30_VALIDATORS_AND_SCHEMAS.md
  40_RISK_MAP.md
  50_NEXT_REGISTRY_INPUT.md
```

## Invariants

- Ne pas éditer le code.
- Ne pas déplacer les fichiers.
- Ne pas supprimer les fichiers.
- Ne pas modifier les index globaux.
- Ne pas conclure `deprecated` sans preuve.
- Marquer `unknown` plutôt que deviner.

## Verdict attendu

```text
PASS_INVENTORY_READY
ou
BLOCKED_WITH_REASON
```
