---
doc_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01_REFACTOR_BATCH_PLAN
doc_type: batch_plan
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: planning
topic_keys:
  - refactor_batch
  - safe_refactor
  - code_ops
  - phased_plan
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 50_REFACTOR_BATCH_PLAN

## Objectif

Définir comment passer de l'audit au refactor sans casser l'existant.

## Principe

```text
Audit -> Registre -> Décision -> Test lock -> Batch refactor -> Validation -> Closeout
```

## Phases

### Phase 0 — Parent doc-only

Statut actuel :

- créer le parent ;
- documenter la méthode ;
- ne pas modifier le code.

Verdict attendu :

```text
PASS_PARENT_OPENED_DOC_ONLY
```

### Phase 1 — Inventaire

Sous-GO candidat :

```text
GO_CODE_OPS_OPT_TRADING_CHILD_CODE_INVENTORY_01
```

Livrables :

- inventaire fichiers ;
- entrypoints ;
- validateurs ;
- schémas ;
- carte de risque ;
- candidats registre.

### Phase 2 — Registre initial

Sous-GO candidat :

```text
GO_CODE_OPS_OPT_TRADING_CHILD_CODE_REGISTRY_01
```

Livrables :

- registre Markdown ou JSON ;
- validateur de registre si nécessaire ;
- tests de registre si nécessaire.

### Phase 3 — Audit anti-doublon

Sous-GO candidat :

```text
GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01
```

Livrables :

- groupes suspects ;
- preuve consommateur ;
- décisions ;
- liste des fusions sûres ;
- liste bloquée.

### Phase 4 — Compatibilité

Sous-GO candidat :

```text
GO_CODE_OPS_OPT_TRADING_CHILD_COMPATIBILITY_MATRIX_01
```

Livrables :

- matrice remplie ;
- commandes de validation ;
- limitations Windows/Bash/WSL/tmux/GHA.

### Phase 5 — Premier batch sûr

Sous-GO candidat :

```text
GO_CODE_OPS_OPT_TRADING_CHILD_SAFE_REFACTOR_BATCH_01
```

Critères pour entrer en batch :

- inventaire terminé ;
- registre minimal présent ;
- doublon ou normalisation cible prouvée ;
- tests existants ou ajoutés ;
- rollback trivial ;
- aucune surface critique inconnue.

## Types de batch autorisés

| Type | Exemple | Risque |
|---|---|---|
| doc-only registry | ajouter registre sans changer code | low |
| test lock | ajouter test avant refactor | low/medium |
| helper extraction | extraire fonction répétée | medium |
| CLI output normalization | uniformiser JSON/stdout | high |
| path migration | déplacer fichier | high |
| deletion | supprimer obsolète | high/blocked |

## Batch interdit au départ

- suppression ;
- renommage massif ;
- refactor multi-surface ;
- changement CLI ;
- changement schéma JSON ;
- modification de workflow CI ;
- normalisation performance sans mesure.

## Format de proposition batch

```text
BATCH_ID:
OBJECT:
FILES:
RATIONALE:
PROOF:
TESTS_BEFORE:
TESTS_AFTER:
COMPATIBILITY:
ROLLBACK:
RISK:
VERDICT_TARGET:
```

## Critères de sortie parent

Le parent peut être fermé seulement si :

- le registre existe ;
- les doublons majeurs sont qualifiés ;
- la matrice compatibilité existe ;
- au moins un batch sûr est défini ou explicitement différé ;
- les prochaines actions sont assignables à des sous-GO.

## Invariants

- Un batch = une intention claire.
- Pas de batch qui mélange registre, suppression et refactor runtime.
- Pas de PR large non réversible.
- Pas de refactor sans preuve consommateur.
