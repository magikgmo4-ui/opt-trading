---
doc_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01_CODE_REGISTRY_SPEC
doc_type: registry_spec
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: design
topic_keys: [code_registry, registry_schema, code_ops, governance]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 20_CODE_REGISTRY_SPEC

## Objectif

Définir le registre canonique du code pour soutenir le refactor structurant.

Le registre ne remplace pas le code. Il sert à :

- identifier les rôles réels ;
- réduire les doublons ;
- éviter les scripts orphelins ;
- relier code, tests, docs et consommateurs ;
- préparer les refactors sûrs.

## Format recommandé

Fichier cible candidat :

```text
docs/registry/CODE_REGISTRY.md
```

ou, si le registre doit devenir exploitable par outil :

```text
docs/registry/code_registry.json
```

Le choix final doit être décidé après inventaire.

## Schéma canonique minimal

| Champ | Type | Obligatoire | Description |
|---|---|---:|---|
| `code_id` | string | oui | identifiant stable |
| `path` | string | oui | chemin repo |
| `role` | enum | oui | rôle contrôlé |
| `surface` | enum | oui | zone produit ou technique |
| `status` | enum | oui | état lifecycle |
| `entrypoint` | bool | oui | exécutable directement |
| `imported_by` | list | non | consommateurs détectés |
| `tests` | list | non | tests associés |
| `docs` | list | non | docs/runbooks associés |
| `inputs` | list | non | fichiers/arguments/sources attendus |
| `outputs` | list | non | fichiers/stdout/JSON produits |
| `compatibility` | list | non | plateformes validées |
| `duplicate_group` | string | non | groupe anti-doublon |
| `risk_level` | enum | oui | low/medium/high/blocked |
| `next_action` | enum | oui | keep/refactor/extract/deprecate/delete_candidate/block |

## Rôles contrôlés

```text
runtime
cli
validator
adapter
schema
collector
orchestrator
wrapper
helper
test
doc_runbook
generated_artifact
unknown
```

## Statuts contrôlés

```text
ACTIVE
CANDIDATE
EXPERIMENTAL
DEPRECATED
DUPLICATE_SUSPECT
DELETE_CANDIDATE
BLOCKED_UNKNOWN_CONSUMER
ARCHIVED
```

## Actions contrôlées

```text
KEEP
REGISTER_ONLY
ADD_TEST
EXTRACT_SHARED_HELPER
MERGE_WITH_CANONICAL
DEPRECATE_WITH_NOTICE
DELETE_AFTER_PROOF
BLOCKED_NEEDS_OWNER
BLOCKED_NEEDS_CONSUMER_AUDIT
```

## Exemple Markdown

| code_id | path | role | status | entrypoint | tests | risk_level | next_action |
|---|---|---|---|---:|---|---|---|
| `strategy_registry_validator` | `tools/strategy/validate_strategy_registry.py` | validator | ACTIVE | oui | `tests/strategy/...` | high | KEEP |
| `openclaw_runtime_security_aggregator` | `tools/openclaw/validate_runtime_security_all.py` | validator | ACTIVE | oui | `tests/openclaw/...` | high | KEEP |

## Exemple JSON

```json
{
  "schema_version": "0.1.0",
  "updated_at": "2026-05-20",
  "entries": [
    {
      "code_id": "strategy_registry_validator",
      "path": "tools/strategy/validate_strategy_registry.py",
      "role": "validator",
      "surface": "strategy",
      "status": "ACTIVE",
      "entrypoint": true,
      "imported_by": [],
      "tests": ["tests/strategy/test_validate_strategy_registry.py"],
      "docs": [],
      "inputs": ["docs/strategy/registry"],
      "outputs": ["stdout", "exit_code"],
      "compatibility": ["debian", "windows_powershell"],
      "duplicate_group": null,
      "risk_level": "high",
      "next_action": "KEEP"
    }
  ]
}
```

## Règles d'identifiant

`code_id` doit être :

- stable ;
- explicite ;
- sans dépendance au chemin si possible ;
- en snake_case ;
- unique dans le registre ;
- non basé sur un nom temporaire de branche.

## Règles anti-régression

Un fichier ne peut passer à `DEPRECATED`, `DUPLICATE_SUSPECT` ou `DELETE_CANDIDATE` que si le registre mentionne :

- raison ;
- preuve ;
- consommateur canonique de remplacement ;
- test de non-régression ;
- date de décision ;
- owner logique.

## Validation du registre

Validateur futur candidat :

```text
tools/code_ops/validate_code_registry.py
```

Critères :

- identifiants uniques ;
- chemins existants ;
- rôles valides ;
- statuts valides ;
- pas de `DELETE_CANDIDATE` sans preuve ;
- pas de `MERGE_WITH_CANONICAL` sans cible ;
- tests référencés existants si déclarés.

## Invariants

- Le registre documente ; il ne décide pas seul.
- La réalité du repo prime sur le registre.
- Un fichier absent du registre n'est pas automatiquement obsolète.
- Un doublon suspect n'est pas un doublon prouvé.
