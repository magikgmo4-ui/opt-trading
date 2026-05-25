# BRANCH_PROTECTION_REQUIRED_CHECKS

## Réglage recommandé

GitHub:

```text
Settings
-> Rules
-> Rulesets ou Branch protection
-> Target branch: sot/mainline
```

Activer:

```text
Require a pull request before merging
Require approvals
Dismiss stale pull request approvals when new commits are pushed
Require status checks to pass
Require branches to be up to date before merging
Do not allow force pushes
Do not allow deletions
```

Option recommandé:

```text
Require merge queue
Require review from Code Owners
```

## Required status checks

À ajouter après le premier run du workflow:

```text
gate/preflight
gate/file-scope
gate/no-lock-overlap
gate/tests
```

## Note

Les noms de jobs doivent rester stables, sinon les required checks configurés dans GitHub peuvent devenir invalides.
