# 56 — Resultats validation strict read-only (1 a 10)

## Contexte

Validation runtime distante executee en mode strictement read-only sur les deux machines le 2026-05-23 :

- `db-layer`
- `admin-trading`

Contraintes respectees :

- aucune ecriture volontaire (watchdog 11-12 non execute)
- aucun restart systemd
- aucun deploy
- aucun acces Google Sheets
- aucune modification runtime

## Verdict global

```text
STRICT_READ_ONLY_1_10 = PASS_WITH_WARNINGS
TOTAL = 6 PASS / 4 WARN / 0 FAIL / 0 BLOCKED
CLOSEOUT = BLOCKED_BY_WARNINGS
GATEWAY = NON_INCRIMINE
WATCHDOG_11_12 = NOT_RUN_STRICT_READ_ONLY
NEXT_FIX_GO = GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
```

Le GO ne doit pas etre ferme en `PASS_FULL` tant que les warnings ci-dessous ne
sont pas corriges ou explicitement acceptes.

## Tableau de preuves (1 a 10)

| Etape | Surface | Verdict | Preuve / lecture |
|---:|---|---|---|
| 1 | `db-layer` repo preflight | WARN | `sot/mainline...origin/sot/mainline` ; untracked: `.claude/`, `artifacts/backtests/`, `secrets/` |
| 2 | `admin-trading` repo preflight | WARN | `sot/mainline...origin/sot/mainline` ; untracked: `secrets/` |
| 3 | OpenClaw health (`db-layer`) | WARN | `Gateway Health OK` ; Telegram OK ; warning: allowlist Telegram vide (groupAllowFrom/allowFrom empty) |
| 4 | OpenClaw probe (`db-layer`) | PASS | `Reachable: yes` ; loopback `ws://127.0.0.1:18789` connect+RPC OK ; gateway identifie `db-layer` |
| 5 | fleet/runtime health (`db-layer`) | WARN | `opt-trading-runtime-health.service` + timer actifs ; wrapper choisit `/opt/trading/venv/bin/python3` en priorite mais PyYAML absent ; `/usr/bin/python3` a PyYAML 6.0.1 ; gateway non incrimine |
| 6 | `tmux ls` `db-layer` | PASS | sessions presentes: `fleet-status`, `kg-repo`, `localcms-ui`, `openclaw-core`, `strict-workers` |
| 7 | `tmux has-session openclaw-core` | PASS | `rc=0` |
| 8 | `tmux ls` `admin-trading` | PASS | sessions presentes: `apps-connectors`, `desk-pro`, `market-data`, `screeners`, `trading-pipeline` |
| 9 | `tmux has-session desk-pro` | PASS | `rc=0` |
| 10 | `tmux has-session screeners` | PASS | `rc=0` |

## Warnings (gaps a conserver)

1. Hygiene repo distante
   - `db-layer`: untracked `.claude/`, `artifacts/backtests/`, `secrets/`
   - `admin-trading`: untracked `secrets/`

2. OpenClaw / Telegram allowlist
   - `groupPolicy=allowlist` avec allowlist vide => messages de groupe droppes silencieusement

3. Runtime healthcheck (fleet / healthcheck)
   - le chemin d execution systemd/wrapper peut echouer car le venv prioritaire ne charge pas PyYAML
   - requalifier STEP 5 en `PASS` seulement apres correction durable (hors strict read-only)

## Non faits (hors scope)

- watchdog `11-12` (ecrit sous `/opt/trading/tmp/`)
- smoke mobile reel
- correction durable `PyYAML / venv / wrapper / EnvironmentFiles` (GO dedie)
