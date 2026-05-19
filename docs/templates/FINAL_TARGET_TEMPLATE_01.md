---
template_id: FINAL_TARGET_TEMPLATE_01
go_id: GO_OPT_TRADING_GOVERNANCE_PARENT_MASTER_TARGET_CONTINUITY_01
doc_type: template
surface: doc-only
created_at: 2026-05-19
---

# FINAL_TARGET_TEMPLATE_01

## Usage

Ce template définit la structure d'un **master target**.
Chaque GO doit référencer son `master_target_id` dans son frontmatter.

## Frontmatter GO standard

```yaml
---
go_id: GO_EXAMPLE_01
master_target_id: MT_EXAMPLE
parent_go: GO_PARENT_01
status: open
surface: doc-only
created_at: 2026-05-19
---
```

## Structure d'un master target

```markdown
# MT_<NAME>

## Objectif final

Une phrase décrivant le résultat ultime visé.

## Critères de succès

- [ ] Critère 1
- [ ] Critère 2

## GOs contributeurs

| GO | Status | Livrable |
|---|---|---|
| `GO_FIRST_01` | merged | Première pierre |
| `GO_CURRENT_01` | open | En cours |

## Continuity

Prochain GO logique : `GO_NEXT_01`
```

## Règles de propagation

1. **Création** : le premier GO d'un master target crée l'entrée dans le registre.
2. **Référencement** : chaque GO suivant porte `master_target_id` dans son frontmatter.
3. **Mise à jour** : à chaque merge, le `current_go` du registre est mis à jour.
4. **Retirement** : quand le dernier GO est clos, le target passe à `RETIRED`.
5. **Interdit** : un GO ne peut pas référencer un master_target_id inexistant.
