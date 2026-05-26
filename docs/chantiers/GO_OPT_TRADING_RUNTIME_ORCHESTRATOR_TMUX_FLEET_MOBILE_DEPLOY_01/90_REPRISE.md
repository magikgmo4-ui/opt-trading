---
doc_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01_REPRISE
doc_type: reprise
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
source_kind: canonical
updated_at: 2026-05-26
---

# 90_REPRISE

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` et au
produit final total voulu :

- runtime operateur distant
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Telegram screener inbound
- Telegram notification outbound multi-destinations
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## Etat de cette passe

Ce chantier conserve les preuves de validation runtime distante strict read-only
1 a 10.

Deux passes sont a considerer :

- `2026-05-23` : validation 1 a 10 `PASS_WITH_WARNINGS` (reference historique).
- `2026-05-26` : incident runtime `db-layer` (gateway down + tmux absent) puis
  recovery minimal via `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_DB_LAYER_GATEWAY_RECOVERY_01`,
  suivi d'un replay 1 a 10 `PASS_WITH_WARNINGS`.

Verdict global (passe `2026-05-23`) :

```text
STRICT_READ_ONLY_1_10 = PASS_WITH_WARNINGS
TOTAL = 6 PASS / 4 WARN / 0 FAIL / 0 BLOCKED
CLOSEOUT = BLOCKED_BY_WARNINGS
GATEWAY = NON_INCRIMINE
WATCHDOG_11_12 = NOT_RUN_STRICT_READ_ONLY
NEXT_FIX_GO = GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
```

Le GO ne doit pas etre ferme en `PASS_FULL`. Les warnings restent a traiter
dans un GO de correction separe, en priorite le mismatch Python/PyYAML du
runtime healthcheck.

Verdict global (passe `2026-05-26` post-recovery) :

```text
STRICT_READ_ONLY_1_10 = PASS_WITH_WARNINGS
RUNTIME_LOCK = LEVE_PARTIELLEMENT
RECOVERY_GO = GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_DB_LAYER_GATEWAY_RECOVERY_01
EVIDENCE = 57_DB_LAYER_GATEWAY_RECOVERY_RESULTS.md
WATCHDOG_11_12 = NOT_RUN_STRICT_READ_ONLY
```

## Preuves repo relues

- `modules/runtime_health/fleet_orchestrator.py`
- `scripts/tmux/sessions/fleet-status.sh`
- `scripts/tmux/sessions/openclaw-core.sh`
- `scripts/tmux/sessions/screeners.sh`
- `scripts/tmux/sessions/desk-pro.sh`
- `scripts/tmux/health_check.py`
- `tests/tmux/test_health_check.py`
- `modules/gateway_openclaw/scripts/cmd.sh`
- `modules/openclaw_tmux_operator/scripts/cmd.sh`

## Constats reels

- `fleet-status` existe deja dans `scripts/tmux/sessions/`
- `modules/openclaw_tmux_operator/` existe deja dans le repo
- `scripts/tmux/health_check.py` attend deja 10 sessions, dont `fleet-status`
- validation distante strict read-only 1 a 10 executee : `PASS_WITH_WARNINGS`
- gateway/OpenClaw joignable et non incrimine
- watchdog 11-12 non execute car il ecrit sous `/opt/trading/tmp/`
- le smoke mobile physique reste non prouve

## Validation distante strict read-only 1 a 10

Source detaillee : `56_STRICT_READ_ONLY_VALIDATION_RESULTS_1_10.md`.

Passe `2026-05-23` :

| Etape | Surface | Verdict | Preuve / lecture |
|---:|---|---|---|
| 1 | `db-layer` repo preflight | WARN | branche OK `sot/mainline...origin/sot/mainline` ; untracked `.claude/`, `artifacts/backtests/`, `secrets/` |
| 2 | `admin-trading` repo preflight | WARN | branche OK ; untracked `secrets/` |
| 3 | OpenClaw health | WARN | `Gateway Health OK`, Telegram OK, mais warning allowlist Telegram vide |
| 4 | OpenClaw probe | PASS | `Reachable: yes`, loopback WS OK, RPC OK, gateway identifie `db-layer` |
| 5 | fleet/runtime health | WARN | mismatch Python/PyYAML + wrapper/systemd ; gateway non incrimine |
| 6 | `tmux ls db-layer` | PASS | sessions presentes : `fleet-status`, `kg-repo`, `localcms-ui`, `openclaw-core`, `strict-workers` |
| 7 | `openclaw-core` session | PASS | `rc=0` |
| 8 | `tmux ls admin-trading` | PASS | sessions presentes : `apps-connectors`, `desk-pro`, `market-data`, `screeners`, `trading-pipeline` |
| 9 | `desk-pro` session | PASS | `rc=0` |
| 10 | `screeners` session | PASS | `rc=0` |

Synthese :

```text
6 PASS
4 WARN
0 FAIL
0 BLOCKED
```

Passe `2026-05-26` (post-recovery db-layer) :

Source : `57_DB_LAYER_GATEWAY_RECOVERY_RESULTS.md`.

| Etape | Surface | Verdict | Preuve / lecture |
|---:|---|---|---|
| 1 | `db-layer` repo preflight | WARN | repo drift: branche GO active + modified/untracked (`.claude/`, `artifacts/backtests/`, `secrets/`) |
| 2 | `admin-trading` repo preflight | WARN | untracked `secrets/` |
| 3 | OpenClaw health | WARN | health OK ; warning allowlist Telegram vide |
| 4 | OpenClaw probe | PASS | `Reachable: yes` ; RPC ok |
| 5 | fleet/runtime health | WARN | `fleet_status: WARN` (stale/unreachable) |
| 6 | `tmux ls db-layer` | PASS | session `openclaw-core` presente (user ghost) |
| 7 | `openclaw-core` session | PASS | `rc=0` |
| 8 | `tmux ls admin-trading` | PASS | sessions presentes : `apps-connectors`, `desk-pro`, `market-data`, `screeners`, `trading-pipeline` |
| 9 | `desk-pro` session | PASS | `rc=0` |
| 10 | `screeners` session | PASS | `rc=0` |

Synthese :

```text
7 PASS
3 WARN
0 FAIL
0 BLOCKED
```

## Validation distante (historique repo)

Une passe sur `origin/sot/mainline` mentionne une validation distante SSH (prod)
le 2026-05-19. Cette section reprend ces elements comme historique; les
verifications restent a re-executer si le contexte runtime change.

- `tmux ls` ghost sur db-layer : 5 sessions (fleet-status, kg-repo, localcms-ui, openclaw-core, strict-workers)
- `tmux ls` openclaw sur db-layer : 1 session (openclaw-gateway)
- `gateway_openclaw health` : OK (Telegram ok)
- `gateway_openclaw probe` : Reachable yes (db-layer identifie)
- SSH admin-trading depuis db-layer : PASS — 5 sessions (apps-connectors, desk-pro, market-data, screeners, trading-pipeline)

## Validation locale

Commandes executees dans cette passe :

```powershell
python -m pytest tests\tmux\test_health_check.py -q
python modules\openclaw_tmux_operator\scripts\health_aggregate.py --dry-run --machines db-layer,admin-trading
python -m unittest tests.mobile.test_mobile_smoke -v
```

Resultat :

```text
32 passed in 0.14s
health_aggregate dry-run OK : unreachable_machines=[] ; total=2 ; aucune ecriture runtime
mobile smoke unit tests OK (skipped=12 si `bash` indisponible)
```

## Validation locale complementaire

Commande executee :

```powershell
$sessionScripts = 'openclaw-core','screeners','strict-workers','trading-pipeline','market-data','apps-connectors','desk-pro','kg-repo','localcms-ui','fleet-status'
$topScripts = 'start_all.sh','stop_all.sh','restart_session.sh','health_aggregator.sh','attach.sh'
```

Resultat :

```text
TMUX script existence check PASS
```

## Gap environnement local

Commande tentee :

```powershell
bash scripts/tmux/sanity.sh
```

Resultat :

```text
bloque sur cette machine Windows : bash pointe vers WSL sans distribution installee
```

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce point de reprise
sert seulement a transmettre l'etat local du chantier runtime, sans fermer
prematurement l'umbrella.

## Prochain item Kanban exact

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## Gaps encore ouverts

- hygiene repo distante : untracked `.claude/`, `artifacts/backtests/`,
  `secrets/` sur `db-layer` ; untracked `secrets/` sur `admin-trading`
- OpenClaw / Telegram : `groupPolicy=allowlist` avec `groupAllowFrom` /
  `allowFrom` vide ; risque de messages Telegram de groupe droppes
  silencieusement
- runtime healthcheck : `opt-trading-runtime-health.service` et timer presents,
  mais `/opt/trading/venv/bin/python3` ne charge pas PyYAML alors que
  `/usr/bin/python3` le charge ; STEP 5 reste `WARN`
- watchdog 11-12 non execute dans cette validation strict read-only
- mobile SSH/tmux reel non valide dans cette passe
- closeout umbrella final bloque par runtime + Bot Vision/headless +
  collectors/API + implementation Sheets globale

## Checklist distante rejouable

Cette checklist reste disponible comme protocole de replay si le contexte
runtime change. Pour la validation strict read-only deja documentee, seules les
lignes 1 a 10 ont ete utilisees ; 11 a 12 restent hors scope.

Ordre d'execution :

```text
1. preflight repo sur db-layer
2. preflight repo sur admin-trading
3. openclaw health/probe sur db-layer
4. fleet dry-run sur db-layer
5. tmux checks sur db-layer
6. tmux checks sur admin-trading
7. (optionnel) deskpro watchdog sur admin-trading (ecrit sous /opt/trading/tmp/)
8. mobile smoke reel seulement si 1 a 6 sont stables (et 7 si utilise)
```

Captures a conserver :

- sortie `git status --short --branch`
- sortie `health`
- sortie `probe`
- sortie `fleet_orchestrator.py --dry-run`
- sortie `tmux ls` sur les deux hosts
- sortie `deskpro_watchdog.sh run-once` et `status`

## Tableau de resultats template

Copier ce bloc lors d'une prochaine passe distante :

```md
| Etape | Host | Commande | Sortie utile | Verdict | Gap / note |
|---|---|---|---|---|---|
| 1 | `db-layer` | `test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch` | a renseigner | PENDING | |
| 2 | `admin-trading` | `test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch` | a renseigner | PENDING | |
| 3 | `db-layer` | `sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"` | a renseigner | PENDING | |
| 4 | `db-layer` | `sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"` | a renseigner | PENDING | |
| 5 | `db-layer` | `cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run` | a renseigner | PENDING | |
| 6 | `db-layer` | `tmux ls` | a renseigner | PENDING | |
| 7 | `db-layer` | `tmux has-session -t openclaw-core` | a renseigner | PENDING | |
| 8 | `admin-trading` | `tmux ls` | a renseigner | PENDING | |
| 9 | `admin-trading` | `tmux has-session -t desk-pro || true` | a renseigner | PENDING | |
| 10 | `admin-trading` | `tmux has-session -t screeners || true` | a renseigner | PENDING | |
```

Version strict read-only (1 a 10) : utiliser uniquement les lignes 1 a 10
ci-dessus et noter `WATCHDOG_SKIPPED` dans la colonne "Gap / note".

Version watchdog optionnel (11 a 12) : ajouter ensuite les deux lignes
suivantes (ecrit sous `/opt/trading/tmp/`) :

```md
| 11 | `admin-trading` | `cd /opt/trading && bash scripts/deskpro_watchdog.sh run-once` | a renseigner | PENDING | WRITE_TMP |
| 12 | `admin-trading` | `cd /opt/trading && bash scripts/deskpro_watchdog.sh status` | a renseigner | PENDING | WRITE_TMP |
```

Interpretation minimale :

- `PASS` = resultat conforme et comprehensible
- `WARN` = resultat lisible mais gap ou ecart non bloquant
- `FAIL` = verification ratee
- `BLOCKED` = commande non executable depuis le contexte courant

## Bloc operateur compact

Bloc unique de reference pour la prochaine execution distante :

```bash
# 1
ssh db-layer 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
# 2
ssh admin-trading 'test -d /opt/trading && cd /opt/trading && pwd && git status --short --branch'
# 3
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh health"'
# 4
ssh db-layer 'sudo -iu openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh probe"'
# 5
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
# 6
ssh db-layer 'tmux ls'
# 7
ssh db-layer 'tmux has-session -t openclaw-core'
# 8
ssh admin-trading 'tmux ls'
# 9
ssh admin-trading 'tmux has-session -t desk-pro || true'
# 10
ssh admin-trading 'tmux has-session -t screeners || true'
# 11
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh run-once'
# 12
ssh admin-trading 'cd /opt/trading && bash scripts/deskpro_watchdog.sh status'
```

Note : `deskpro_watchdog.sh run-once/status` effectue des lectures reseau locales
(`curl` sur `127.0.0.1:8010`) et ecrit sous `/opt/trading/tmp/` (log + pid).
Si un protocole strictement sans ecriture est requis, ne pas executer 11/12.

## Next GO recommande apres validation runtime

- `GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01` (correction durable
  Python/PyYAML du wrapper/systemd runtime healthcheck)

## Autres GO dependants

- `GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01` (avant mobile)
- `GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01` (apres OpenClaw)
