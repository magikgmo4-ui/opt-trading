---
doc_id: RUNTIME_SCRIPTS_NORMALIZATION_EXECUTION_CONTRACT_AUDIT_50
doc_type: NEXT_IMPL_PATCH_PLAN
repo: opt-trading
project: opt-trading
module: runtime_scripts_normalization
go_id: GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01
status: open
lifecycle_stage: audit_doc_only
topic_keys:
  - opt-trading
  - next_go
  - implementation_plan
  - runtime_execution_contract
  - ci
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-31
links:
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01/20_RUNTIME_EXECUTION_CONTRACT_DRAFT.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01/30_GAPS_MODULES_WRAPPERS_MACHINES.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01/40_TEST_DISCOVERY_HYGIENE.md
---

# 50_NEXT_IMPL_PATCH_PLAN

## Purpose

Ce fichier decrit le patch d'implementation suivant. Il ne l'applique pas.

## Proposed next GO

```text
GO_OPT_TRADING_RUNTIME_EXECUTION_CONTRACTS_REGISTRY_IMPL_01
```

Role propose :

```text
GO_CHILD_ATTACHED_TO_PARENT
```

Parent propose :

```text
GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_IMPL_01
```

## Implementation scope

### 1. Add machine-readable contract

Creer :

```text
registry/runtime_execution_contracts.yaml
```

Contenu initial recommande :

- schema version;
- quelques contrats seed a faible risque;
- pas de couverture exhaustive forcee;
- statut `candidate` lorsque wrapper, job ou test est incomplet.

Contrats seed candidats :

| contract_id | Raison |
| --- | --- |
| `runtime_health_healthcheck_diagnostic` | existe, diagnostic-only, tests existants |
| `gha_registry_validation_ci` | workflow et script existants, read-only |
| `desk_pro_runner_runtime_candidate` | surface critique, mais wrapper coverage a confirmer |

### 2. Add derived Markdown view

Creer :

```text
docs/registry/RUNTIME_EXECUTION_CONTRACTS.md
```

Regle :

```text
Markdown = vue derivee lisible
YAML = source principale
```

### 3. Add validator

Creer :

```text
scripts/validate_runtime_execution_contracts.py
```

Le validateur doit etre purement statique :

- pas de service systemd;
- pas de port probe;
- pas de healthcheck live;
- pas de secret;
- pas d'ecriture hors stdout/stderr;
- exit non-zero si contrat invalide.

### 4. Add tests

Creer :

```text
tests/governance/test_runtime_execution_contracts_validator.py
```

Verifier au minimum :

- happy path;
- duplicate contract;
- missing module;
- missing wrapper;
- missing machine;
- missing runtime map key;
- missing entrypoint;
- missing test path;
- invalid enum;
- absolute path blocked;
- secret-like value blocked.

### 5. Extend CI

Modifier :

```text
.github/workflows/gh-actions-registry-validation.yml
```

Ajouts :

- path trigger sur `registry/runtime_execution_contracts.yaml`;
- path trigger sur `scripts/validate_runtime_execution_contracts.py`;
- path trigger sur tests du validateur;
- step `python3 scripts/validate_runtime_execution_contracts.py`.

### 6. Machine alias implementation

Ne pas renommer les machines.

Option recommandee :

- ajouter plus tard un champ `aliases` et/ou `runtime_map_key` a `registry/machines_registry.yaml`;
- mettre a jour le reader machine pour exposer ces alias;
- valider `machine_target` + `runtime_map_key` via le nouveau validateur.

Cette etape peut etre separee si elle augmente trop le scope.

### 7. Runtime health integration

Apres validation statique seulement :

- lire `runtime_execution_contracts.yaml` depuis `runtime_health`;
- filtrer les contrats applicables a la machine courante;
- reporter les contrats applicables sans les executer;
- ne jamais auto-heal dans cette phase.

## Non-scope for next GO

Le prochain GO ne doit pas encore :

- deplacer des scripts;
- renommer des modules;
- installer des wrappers runtime;
- demarrer ou arreter des services;
- executer du trading;
- supprimer des `.pyc` ou `__pycache__` sans lot hygiene dedie;
- fermer le parent.

## Acceptance gates

Le prochain GO peut etre accepte si :

- `registry/runtime_execution_contracts.yaml` existe;
- le validateur passe localement;
- les tests du validateur passent;
- le workflow CI reference le validateur;
- aucun secret n'est ajoute;
- aucun runtime n'est modifie;
- les index globaux restent inchanges sauf demande explicite separee.

## Reprise

Point de reprise exact :

```text
Partir du draft de 20_RUNTIME_EXECUTION_CONTRACT_DRAFT.md.
Ajouter le YAML source, le validateur statique, les tests et le branchement CI.
Garder la migration runtime et les facades operateur pour des GOs ulterieurs.
```
