---
doc_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_DB_LAYER_GATEWAY_RECOVERY_01_RESULTS
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_DB_LAYER_GATEWAY_RECOVERY_01
status: open
source_kind: canonical
updated_at: 2026-05-26
---

# 57 — DB-layer gateway recovery results

## Objective

Restaurer le runtime minimal requis pour rejouer le protocole strict read-only 1–10 de
`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` :

- tmux server sur `db-layer` (user `ghost`)
- session tmux `openclaw-core` sur `db-layer`
- OpenClaw gateway joignable via loopback
- port `127.0.0.1:18789` listening
- `openclaw gateway health` OK
- `openclaw gateway probe` OK (RPC ok)

Contraintes respectees :

- pas de watchdog 11–12
- pas d'ecriture sous `/opt/trading/tmp/`
- pas de modification secrets
- pas de live trade

## Etat avant recovery (observations)

### Symptoms

- `openclaw gateway health` / `probe` en echec sur `db-layer`
- port 18789 non listening
- tmux server absent sur `db-layer` (socket `/tmp/tmux-1000/default` absent)

### Evidence (extraits)

```bash
ssh db-layer 'tmux ls || true'
```

```text
error connecting to /tmp/tmux-1000/default (No such file or directory)
```

```bash
ssh db-layer 'ss -lntp 2>/dev/null | grep 18789 || true'
```

```text
(vide)
```

```bash
ssh db-layer 'pgrep -af openclaw || true'
```

```text
(aucun process openclaw)
```

## Action recovery (controlee)

### A1 — demarrage OpenClaw gateway (user openclaw)

```bash
ssh db-layer 'sudo -n -u openclaw bash -lc "cd /opt/trading && bash modules/gateway_openclaw/scripts/cmd.sh start"'
```

Notes :

- le module `gateway_openclaw` demarre une session tmux `openclaw-gateway` sous l'utilisateur `openclaw`
- log attendu sous `/home/openclaw/.openclaw/logs/gateway_foreground.log`

### A2 — restauration tmux minimal (user ghost)

Creation d'un tmux server et d'une session `openclaw-core` cote `ghost` (support protocole 1–10).

```bash
ssh db-layer 'cd /opt/trading && tmux has-session -t openclaw-core >/dev/null 2>&1 || tmux new-session -d -s openclaw-core -n core "while true; do date -u +%FT%TZ; sudo -n -u openclaw bash -lc \"openclaw gateway health\" >/dev/null 2>&1 && echo [OK] gateway || echo [DOWN] gateway; sleep 30; done"'
```

## Etat apres recovery (preuves)

### B1 — port 18789 listening

```bash
ssh db-layer 'ss -lnt | grep 18789 || echo "port 18789 not listening"'
```

```text
LISTEN 0 511 127.0.0.1:18789 0.0.0.0:*
LISTEN 0 511 [::1]:18789 [::]:*
```

### B2 — gateway health OK (avec warnings)

```bash
ssh db-layer 'sudo -n -u openclaw bash -lc "openclaw gateway health"'
```

```text
Gateway Health
OK (...)
Telegram: ok (...)
```

Warning attendu :

- `channels.telegram.groupPolicy is "allowlist" but groupAllowFrom (and allowFrom) is empty`

### B3 — gateway probe OK

```bash
ssh db-layer 'sudo -n -u openclaw bash -lc "openclaw gateway probe"'
```

```text
Reachable: yes
Targets
Local loopback ws://127.0.0.1:18789
  Connect: ok (...) · RPC: ok
```

Note :

- un probe immediatement apres start peut afficher `RPC: failed - timeout` ; un second probe apres quelques secondes doit passer.

### B4 — tmux sessions presentes

```bash
ssh db-layer 'tmux has-session -t openclaw-core; echo rc=$?'
```

```text
rc=0
```

```bash
ssh db-layer 'sudo -n -u openclaw bash -lc "tmux ls || true"'
```

```text
openclaw-gateway: 1 windows (...)
```

## Replay strict read-only 1–10 (post-recovery)

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
STRICT_READ_ONLY_1_10 = PASS_WITH_WARNINGS
RUNTIME_LOCK = LEVE_PARTIELLEMENT
```

## Cause racine confirmee

- `db-layer`: OpenClaw gateway down + absence de tmux server -> port 18789 non listening -> health/probe impossibles -> protocole 1–10 bloque.

## Remaining gaps (post-recovery)

- `db-layer` repo drift (branche GO active, modified/untracked dont `secrets/`)
- `admin-trading` hygiene (untracked `secrets/`)
- OpenClaw warning allowlist Telegram vide
- fleet_orchestrator `WARN` (machines stale/unreachable)
- mobile smoke reel : NOT_PROVEN (hors scope 1–10)
