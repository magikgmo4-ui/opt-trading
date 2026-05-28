---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01_SEMIAUTO_PROTOCOL
doc_type: semiauto_loop_protocol
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: open
updated_at: 2026-05-28
---

# 40_SEMIAUTO_LOOP_PROTOCOL

## Objectif

Formaliser la boucle opérateur ↔ agent ↔ IDE ↔ repo ↔ PR.
Ce document est la spécification. La mise en œuvre est dans le child GO.

## La boucle canonique

```
[1] Opérateur humain valide un plan
       ↓
[2] ChatGPT émet un GO_PROMPT (contexte + contraintes + livrables)
       ↓
[3] IDE / OpenClaw exécute (code, git, tests)
       ↓
[4] Preuves produites : PR / diff / rapport / test results
       ↓
[5] Retour opérateur : screenshot + export + 7_CANONICAL_STATE
       ↓
[6] ChatGPT analyse l'état, émet NEXT_GO ou closeout
       ↓
[7] Opérateur approuve ou redirige → retour à [1] ou [2]
```

## Phases de la boucle

### Phase humaine (H)

| Étape | Responsable | Format |
|---|---|---|
| Validation du plan | Opérateur | message texte + GO_PROMPT |
| Revue de la PR | Opérateur | GitHub PR review |
| Décision merge | Opérateur | `gh pr merge` |
| Décision rollback | Opérateur | `git revert` ou instruction |
| Validation post-merge | Opérateur | screenshot + 7_CANONICAL_STATE |

### Phase agent (A)

| Étape | Responsable | Format |
|---|---|---|
| Exécution GO | Claude Code / IDE | commits + push |
| Rapport d'état | Claude Code | 17_RESUME_POINT + diff |
| Tests | Claude Code | `pytest` / `bash -n` |
| Création PR | Claude Code | `gh pr create` |
| Merge PR | Claude Code (sur instruction) | `gh pr merge` |

## Conditions de stop

L'agent doit stopper et demander validation humaine si :
- un test échoue de manière inattendue ;
- un conflit git ne peut pas être résolu sans décision de domaine ;
- une suppression de fichier non prévue dans le GO_PROMPT est requise ;
- un fichier hors scope du GO_PROMPT est modifié ;
- une permission ou secret est manquant ;
- le scope dépasse ce qui a été validé.

## Conditions de merge

Un PR peut être mergé automatiquement (sur instruction opérateur explicite) si :
- tous les tests CI PASS ;
- le diff est limité au scope du GO_PROMPT ;
- aucun fichier hors scope modifié ;
- whitespace check PASS ;
- rapport de validation produit.

## Conditions de rollback

Déclencher un rollback si :
- un test de régression échoue après merge ;
- un consommateur se plaint d'une interface cassée ;
- un comportement runtime inattendu est détecté.

Méthode : `git revert <merge_commit>` ou nouvelle PR corrective.

## Invariants de la boucle

- Le gate humain ne peut pas être bypassé.
- Un GO_PROMPT doit avoir des `LIVRABLES` explicites.
- Un GO_PROMPT doit avoir des `VALIDATIONS` explicites.
- Un rapport doit toujours contenir un `17_RESUME_POINT`.
- Aucun agent ne peut merger sans instruction humaine explicite.

## Livrable child GO

```text
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01
→ protocole détaillé + exemples
→ templates GO_PROMPT + retour opérateur
→ tests de la boucle sur un GO pilote
```
