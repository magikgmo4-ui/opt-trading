---
doc_id: RUNTIME_SCRIPTS_NORMALIZATION_EXECUTION_CONTRACT_AUDIT_40
doc_type: TEST_DISCOVERY_HYGIENE
repo: opt-trading
project: opt-trading
module: runtime_scripts_normalization
go_id: GO_OPT_TRADING_RUNTIME_SCRIPTS_NORMALIZATION_CHILD_EXECUTION_CONTRACT_AUDIT_01
status: open
lifecycle_stage: audit_doc_only
topic_keys:
  - opt-trading
  - tests
  - pytest
  - hygiene
  - runtime_health
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-31
links:
  - scripts/ai/workers/kill_switch_fullstop_test.py
  - tests/runtime_health/test_warn_classification.py
  - tests/runtime_health/test_cursor_ai_windows.py
  - tests/test_desk_pro_health_classification.py
---

# 40_TEST_DISCOVERY_HYGIENE

## Scope

Ce fichier documente l'hygiene de decouverte de tests pour le futur validateur execution contracts.

Ce GO n'a pas lance de suite de tests runtime et n'a pas execute de healthcheck live. Le lot reste doc-only.

## Baseline reportee

Le trunk ZIP inspecte precedemment portait cette baseline cible :

```text
107 passed
26 passed
55 passed
---
188 passed
```

Cette baseline doit rester une reference historique tant que les commandes exactes ne sont pas rejouees dans un GO de validation.

## Static discovery findings

### No root pytest config observed

Aucun de ces fichiers n'a ete trouve a la racine locale :

```text
pyproject.toml
pytest.ini
setup.cfg
tox.ini
```

Donc la decouverte pytest globale depend probablement des conventions par defaut et des chemins passes en ligne de commande.

### `kill_switch_fullstop_test.py` risk

Fichier concerne :

```text
scripts/ai/workers/kill_switch_fullstop_test.py
```

Constat statique :

- le nom matche une convention de decouverte `*_test.py`;
- le fichier contient du code top-level;
- le fichier lit `data/runtime_health/kill_switch.state`;
- le fichier appelle `exit(0)` au top-level selon l'etat du fichier.

Risque :

```text
pytest global peut collecter/executer ce script comme test et perturber la collection.
```

Decision draft :

- renommer le script hors pattern test dans un GO dedie; ou
- ajouter une configuration pytest explicite; ou
- deplacer le test reel sous `tests/ai/workers/` avec fonctions pytest sans `exit()` top-level.

Pas de changement dans ce GO.

## Generated Python artifacts

Le trunk ZIP inspecte precedemment contenait des artefacts Python generes :

```text
108 dossiers __pycache__
371 fichiers .pyc
```

Ces fichiers ne doivent pas etre transportes dans les patchs ou bundles futurs.

Decision draft :

- verifier `.gitignore` et mecanisme de build/zip;
- exclure `__pycache__/` et `*.pyc` du transport trunk;
- ne pas utiliser ces artefacts comme preuve runtime.

## Targeted tests to preserve

Le futur validateur execution contracts devrait rester compatible avec les tests cibles existants :

| Test path | Role |
| --- | --- |
| `tests/runtime_health/test_warn_classification.py` | classification WARN/PASS et map runtime |
| `tests/runtime_health/test_cursor_ai_windows.py` | resolution Windows/cursor-ai/fleet |
| `tests/test_desk_pro_health_classification.py` | classification sante Desk Pro |
| `tests/governance/test_registry_source_of_truth_contract.py` | contrat source-of-truth registry |
| `tests/openclaw/test_validate_runtime_security_all.py` | garde runtime security |

## Future test plan

Tests a ajouter dans le GO d'implementation :

```text
tests/governance/test_runtime_execution_contracts_validator.py
```

Cas minimaux :

- contrat valide minimal;
- `contract_id` duplique;
- `module_name` absent;
- `wrapper_id` absent;
- `machine_target` absent;
- `runtime_map_key` non resolu;
- `entrypoint` inexistant;
- test reference inexistant;
- `risk` invalide;
- `status` invalide;
- path absolu non autorise;
- pattern secret detecte.

## CI hygiene requirement

Le futur workflow CI doit rester read-only :

```text
permissions: contents: read
```

Il ne doit pas demander de secret, ne doit pas executer de runtime live, et ne doit pas demarrer de service.
