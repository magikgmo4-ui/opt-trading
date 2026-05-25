---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01_ROLLBACK
doc_type: rollback_plan
---

# Rollback Plan — Required Checks

## Si un required check bloque une PR légitime

### Cas 1 : false positive (check qui échoue alors qu'il devrait passer)

1. Vérifier les logs du check : `gh run view <RUN_ID> --log`
2. Si c'est un bug dans `gated-pr.yml`, ouvrir un hotfix GO pour corriger
3. En attendant, le merge peut être débloqué via bypass admin (si configuré)
   - Settings > Rules > Rulesets > cliquer le ruleset > approuver le bypass
4. Si bypass impossible et urgence : désactiver temporairement le ruleset

### Cas 2 : PR multi-GO légitime (plusieurs chantiers)

Les jobs `gate/file-scope` et `gate/no-lock-overlap` rejettent les PR qui modifient plusieurs GOs.
Si ce comportement doit être assoupli :

1. Modifier `gate/file-scope` pour autoriser N GO (avec N configurable)
2. Modifier `gate/no-lock-overlap` pour utiliser la même N
3. PR de correctif avec `FILE_SCOPE` adapté

### Cas 3 : required check manquant (check absent mais requis)

Si GitHub indique "x expected — Waiting for status to be reported" :

1. Vérifier que le nom du check dans le ruleset correspond exactement au `name:` du job YAML
2. Noms actuels : `gate/preflight`, `gate/file-scope`, `gate/no-lock-overlap`, `gate/tests`
3. Vérifier que le workflow se déclenche bien sur `pull_request` (et pas seulement `push`)

## Désactivation d'urgence

```bash
# 1. Désactiver le ruleset via l'UI GitHub
# Settings > Rules > Rulesets > "Required checks — sot/mainline" > Disable

# 2. Ou supprimer la branch protection rule
# Settings > Branches > sot/mainline > Delete

# 3. Après résolution, réactiver
```

## Restauration après rollback

1. Réappliquer le ruleset avec les mêmes paramètres
2. Tester avec une micro-PR docs-only
3. Vérifier que les 4 checks sont requis et passent
