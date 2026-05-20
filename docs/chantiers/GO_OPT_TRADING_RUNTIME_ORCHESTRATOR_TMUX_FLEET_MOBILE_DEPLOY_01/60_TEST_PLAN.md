# 60 — Test plan

## Cadre de validation

Les niveaux ci-dessous distinguent :

- preuves locales executables depuis ce workspace
- validations distantes a realiser depuis le reseau operateur

Cette passe ne suppose pas que les niveaux SSH/mobile ont deja ete executes.

## Niveau 0 — Git et scope

```bash
git status --short --branch
git diff --check
git diff --name-only
```

Critere : branche attendue, pas de dirty tree hors scope, pas de secret.

## Niveau 0b — Preuve locale tmux

```powershell
python -m pytest tests\tmux\test_health_check.py -q
```

Critere : la liste des sessions attendues inclut `fleet-status` et les tests
locaux passent.

## Niveau 0c — Preuve locale operator dry-run

```powershell
python modules\openclaw_tmux_operator\scripts\health_aggregate.py --dry-run --machines db-layer,admin-trading
```

Critere : JSON valide, `unreachable_machines=[]`, aucune ecriture runtime.

## Niveau 0d — Existence scripts tmux

```powershell
$sessionScripts = 'openclaw-core','screeners','strict-workers','trading-pipeline','market-data','apps-connectors','desk-pro','kg-repo','localcms-ui','fleet-status'
$topScripts = 'start_all.sh','stop_all.sh','restart_session.sh','health_aggregator.sh','attach.sh'
```

Critere : tous les scripts references existent dans le repo local.

## Niveau 0e — Sanity bash Linux

```bash
bash scripts/tmux/sanity.sh
```

Critere : passe sur un host Linux/WSL correctement configure.
Note : sur cette machine Windows, `bash` est relie a WSL sans distribution
installee ; ce niveau est donc bloque ici mais reste valide comme preuve cible
sur environnement Linux.

## Ordre d'execution distante recommande

La prochaine passe distante doit suivre cet ordre strict :

1. preflight SSH/repo sur `db-layer` puis `admin-trading`
2. OpenClaw `health` / `probe` sur `db-layer`
3. fleet dry-run sur `db-layer`
4. verification tmux sur `db-layer`
5. verification tmux sur `admin-trading`
6. watchdog read-only sur `admin-trading`
7. smoke mobile reel seulement apres validation des etapes 1 a 6

Capturer pour chaque etape :

- commande exacte
- host cible
- sortie brute utile
- verdict `PASS` / `WARN` / `FAIL` / `BLOCKED`

## Niveau 1 — OpenClaw db-layer

Preflight minimal a executer avant le niveau 1 :

```bash
ssh db-layer 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
ssh admin-trading 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
```

Critere : repo present sur les deux hosts ; etat Git observable ; aucune
correction automatique.

```bash
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"'
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"'
```

Critere : `health` OK, `probe` OK.

## Niveau 2 — Fleet

```bash
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
```

Critere : `unreachable=[]`, `failing=[]`, WARN seulement `EXPECTED`.

## Niveau 3 — tmux db-layer

```bash
ssh db-layer 'tmux ls'
ssh db-layer 'tmux has-session -t openclaw-core'
ssh db-layer 'tmux list-windows -t openclaw-core'
```

Critere : session existe, fenetres attendues visibles.

## Niveau 4 — tmux admin-trading

```bash
ssh admin-trading 'tmux ls'
ssh admin-trading 'tmux has-session -t screeners || true'
ssh admin-trading 'tmux has-session -t desk-pro || true'
```

Critere : sessions P0 presentes ou gaps documentes.

Verification complementaire si le protocole tmux-ide est utilise plus tard :

```bash
ssh admin-trading 'cd /opt/trading && test ! -e ide.yml'
```

Critere : aucune collision avec un artefact `ide.yml` non attendu.

## Niveau 5 — Mobile

Depuis mobile (ou simulation) :

```bash
ssh db-layer
tmux attach -t openclaw-core
```

Critere : attach fonctionne, detach fonctionne, session survit a deconnexion.

## Niveau 6 — Desk Pro watchdog

```bash
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh run-once'
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh status'
```

Critere : no alert spam, status lisible.

## Niveau 7 — strict-workers readonly

```bash
cd /opt/trading
scripts/ai/workers/run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
```

Critere : validation passee, aucun write runtime, argument positionnel respecte.

## Sorties a conserver dans la reprise

- `git status --short --branch` sur `db-layer`
- `git status --short --branch` sur `admin-trading`
- `gateway_openclaw/scripts/cmd.sh health`
- `gateway_openclaw/scripts/cmd.sh probe`
- `fleet_orchestrator.py --dry-run`
- `tmux ls` sur `db-layer`
- `tmux ls` sur `admin-trading`
- `scripts/deskpro_watchdog.sh run-once`
- `scripts/deskpro_watchdog.sh status`
