# STATE — GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01

## 7_CANONICAL_STATE

```text
GitHub Actions d'abord.
Registry repo ensuite.
Dedup jobs non-trading ensuite.
OpenClaw orchestration seulement après.
```

## 13_ESTABLISHED

- Le repo cible est `magikgmo4-ui/opt-trading`.
- La branche canonique est `sot/mainline`.
- Le chantier est un `GO_MASTER_PROJECT_PLAN`.
- Le master target est `github_actions_openclaw`.
- Des workflows GitHub Actions existent déjà.
- Un registre des jobs non-trading existe déjà.
- Le chantier doit commencer par inventaire + dédoublonnage.

## 14_HYPOTHESIS

- Certains jobs non-trading peuvent être mappés directement à des workflows GitHub Actions existants.
- Certains jobs devront rester OpenClaw-only.
- Certains jobs devront être ajoutés comme `workflow_dispatch` dry-run.

## 15_REMAINING_GAP

- Valider toute la liste `.github/workflows/*.yml`.
- Extraire les jobs réels depuis chaque workflow.
- Compléter le mapping entre non-trading jobs et GitHub Actions.
- Tester les workflows existants en PR et `workflow_dispatch`.
- Définir les nouveaux jobs à créer dans un child GO.

## 16_TODO

1. Appliquer le bundle sur branche dédiée.
2. Vérifier `git diff --check`.
3. Vérifier YAML parse.
4. Vérifier que les registres sont lisibles.
5. Lancer PR test.
6. Lire les résultats Actions.
7. Ouvrir child GO pour les jobs manquants.
