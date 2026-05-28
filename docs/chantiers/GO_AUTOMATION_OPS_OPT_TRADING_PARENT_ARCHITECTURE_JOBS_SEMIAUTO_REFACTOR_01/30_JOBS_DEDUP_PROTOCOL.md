---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01_DEDUP_PROTOCOL
doc_type: dedup_protocol
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: open
updated_at: 2026-05-28
---

# 30_JOBS_DEDUP_PROTOCOL

## Objectif

Définir la méthode pour qualifier les doublons entre jobs avant toute suppression.
Aucun job ne peut être supprimé sans preuve et sans cette qualification.

## Règle fondamentale

> On ne supprime pas un job non qualifié.

## Classifications de doublon

| Classification | Définition |
|---|---|
| `EXACT_DUPLICATE` | même trigger, même logique, même output — un seul suffit |
| `FUNCTIONAL_DUPLICATE` | même intention, implémentation différente — décision requise |
| `WRAPPER_VARIANT` | l'un enveloppe l'autre, les deux servent des contextes distincts |
| `LEGACY_REPLACED` | ancien job remplacé par un nouveau, aucun consommateur actif |
| `SCOPE_SPLIT` | apparemment dupliqué mais scopes distincts (ex. CI vs local) |
| `FALSE_POSITIVE` | ressemble à un doublon mais rôles distincts — KEEP sans action |

## Méthode de qualification

Pour chaque paire de jobs suspects :

1. **Comparer les triggers** — si différents → SCOPE_SPLIT probable
2. **Comparer les outputs** — si identiques → EXACT_DUPLICATE probable
3. **Grep consommateurs** — si l'un n'a pas de consommateur → LEGACY_REPLACED probable
4. **Lire les permissions** — si différentes → WRAPPER_VARIANT probable
5. **Lire les logs/artefacts** — si l'un ne produit rien → candidat à DEPRECATE

## Table de décision

| Classification | Action par défaut | Condition de suppression |
|---|---|---|
| EXACT_DUPLICATE | MERGE_WITH_CANONICAL | preuve + test du remplaçant |
| FUNCTIONAL_DUPLICATE | KEEP_BOTH + documenter | décision explicite |
| WRAPPER_VARIANT | KEEP_BOTH | N/A — rôles distincts |
| LEGACY_REPLACED | DEPRECATE_WITH_NOTICE | grep import négatif confirmé |
| SCOPE_SPLIT | KEEP_BOTH | N/A |
| FALSE_POSITIVE | KEEP | N/A |

## Preuve requise avant suppression

- `git grep` négatif sur le job_id / path dans tous les fichiers appelants ;
- confirmation que le remplaçant produit les mêmes outputs ;
- test ou smoke du remplaçant PASS ;
- rollback documenté (branche ou revert).

## Critères BLOCKED

Bloquer la qualification si :
- consommateur inconnu ;
- output non documenté ;
- permissions non comprises ;
- dépendance externe non maîtrisée.

## Livrable child GO

```text
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
→ table de qualification par paire suspecte
→ décisions documentées
→ plan de nettoyage par batch
```
