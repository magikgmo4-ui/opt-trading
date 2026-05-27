# 10_TEST_PLAN

## Objectif

Prouver en execution reelle que la chaine OpenClaw GitHub Actions sait :
- lire l'environnement live (`GITHUB_TOKEN`, `GITHUB_REPOSITORY`)
- recuperer un `run-info` sur un vrai run GitHub Actions
- produire un resultat `pipeline` sur ce meme run

## Preconditions

1. `GITHUB_TOKEN` est exporte dans le shell
2. `GITHUB_REPOSITORY` est exporte au format `owner/repo`
3. le workflow cible supporte `workflow_dispatch`
4. le workflow cible est non destructif
5. aucun patch n'est applique automatiquement

## Commandes

### 1. Validation environnement

```bash
python3 scripts/openclaw_gh_actions_live_env.py validate --verbose
```

### 2. Reference du job orchestrable

```bash
python3 scripts/openclaw_gh_actions_orchestrate.py --list-jobs
```

Choisir un job/workflow a faible risque et deja autorise.

### 3. Declenchement controle du run reel

```bash
python3 scripts/openclaw_gh_actions_orchestrate.py --job-id <JOB_ID> --ref sot/mainline --wait 10 --timeout 300 --interval 20
```

Capturer le `run_id` retourne dans la sortie.

### 4. Preuve `run-info`

```bash
python3 scripts/openclaw_gh_actions_live_env.py run-info --run-id <RUN_ID>
```

### 5. Preuve `pipeline`

```bash
python3 scripts/openclaw_gh_actions_live_env.py pipeline --run-id <RUN_ID> --job-id <JOB_ID>
```

### 6. Analyse optionnelle si FAIL

```bash
python3 scripts/openclaw_gh_actions_live_env.py pipeline --run-id <RUN_ID> --job-id <JOB_ID> --analyze
```

## Expected Results

1. `validate --verbose` retourne `all_valid=true`
2. `--list-jobs` montre au moins un job orchestrable
3. le workflow se declenche sans mutation repo locale
4. `run-info` retourne `run_id`, `status`, `conclusion`, `html_url`
5. `pipeline` retourne une `classification`
6. `dangerous_action_executed` reste `false`

## Failure Handling

1. Si `validate` echoue : ne pas lancer le run ; corriger l'environnement
2. Si le workflow n'apparait pas : verifier permissions `gh`/GitHub et `workflow_dispatch`
3. Si `pipeline` retourne `FAIL` : capturer l'analyse, ne rien appliquer
4. Si `pipeline` retourne `BLOCKED` : documenter la cause et fermer le GO en `BLOCKED` si necessaire

## Invariants

- no workflow modification
- no patch application
- no push to `sot/mainline`
- no merge
- `dangerous_action_executed: false`
