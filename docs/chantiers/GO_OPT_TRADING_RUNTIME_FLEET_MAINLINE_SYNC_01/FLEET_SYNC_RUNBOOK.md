# Fleet Sync Runbook — `sot/mainline` @ `615d387a`

## Target commit

```
615d387a8ef9c5b9dffb3a9c734e1920382bdc1e
docs(github-actions): validate ruleset enforcement probe
```

## Pre-flight

```bash
# Vérifier l'accès SSH à chaque machine
ssh admin-trading "hostname"
ssh student "hostname"
ssh db-layer "hostname"
# cursor-ai : accessible via ssh ou accès direct
```

## admin-trading

```bash
ssh admin-trading
cd /opt/trading
git fetch origin --prune
git switch sot/mainline
git pull --ff-only origin sot/mainline
git log -1 --oneline
# Attendu : 615d387a docs(github-actions): validate ruleset enforcement probe
```

## student

```bash
ssh student
cd /opt/trading
git fetch origin --prune
git switch sot/mainline
git pull --ff-only origin sot/mainline
git log -1 --oneline
# Attendu : 615d387a
```

## db-layer

```bash
ssh db-layer
cd /opt/trading
git fetch origin --prune
git switch sot/mainline
git pull --ff-only origin sot/mainline
git log -1 --oneline
# Attendu : 615d387a
```

## cursor-ai (si accessible)

```bash
ssh cursor-ai
cd /opt/trading
git fetch origin --prune
git switch sot/mainline
git pull --ff-only origin sot/mainline
git log -1 --oneline
# Attendu : 615d387a
```

## Post-sync verification

```bash
# Depuis n'importe quelle machine
git log -1 --oneline
# doit afficher : 615d387a docs(github-actions): validate ruleset enforcement probe
```

## Si une machine échoue

- Vérifier l'accès réseau / SSH
- Vérifier les modifications locales non commitées (`git status --short`)
- Ne pas forcer le pull si des modifications locales existent — les stasher d'abord
- Documenter l'écart dans le closeout du GO
