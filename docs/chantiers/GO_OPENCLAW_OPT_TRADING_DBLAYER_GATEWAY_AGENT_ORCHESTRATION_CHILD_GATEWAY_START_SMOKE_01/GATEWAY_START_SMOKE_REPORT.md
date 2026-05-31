---
doc_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_CHILD_GATEWAY_START_SMOKE_01_SMOKE_REPORT
doc_type: smoke_report
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_DBLAYER_GATEWAY_AGENT_ORCHESTRATION_CHILD_GATEWAY_START_SMOKE_01
machine: db-layer
produced_at: 2026-05-31T02:10 UTC
---

# GATEWAY_START_SMOKE_REPORT — OpenClaw Gateway db-layer

## Résultats

| Check | Commande | Résultat |
| --- | --- | --- |
| Session tmux créée | `tmux new-session -d -s openclaw-gateway` | PASS |
| Gateway listening | `openclaw gateway run --bind loopback --port 18789` | PASS — `ws://127.0.0.1:18789` |
| RPC probe | `openclaw gateway status` | PASS — `RPC probe: ok` |
| Health : Telegram | `openclaw health` | PASS — `@ghost_admin_trading_bot (1026ms)` |
| Health : agents | `openclaw health` | PASS — `orchestrateur (default), builder, reviewer, lab, codexoauth` |
| Health : heartbeat | `openclaw health` | PASS — `30m (orchestrateur)` |

## Logs gateway (extrait)

```
02:10:09 [canvas] host mounted at http://127.0.0.1:18789/__openclaw__/canvas/
02:10:10 [heartbeat] started
02:10:10 [health-monitor] started
02:10:10 [gateway] agent model: openai/gpt-5.4
02:10:10 [gateway] listening on ws://127.0.0.1:18789, ws://[::1]:18789 (PID 100106)
02:10:10 [telegram] [default] starting provider (@ghost_admin_trading_bot)
```

## Configuration active

```text
Gateway bind   : loopback (127.0.0.1)
Port           : 18789
Session tmux   : openclaw-gateway (user openclaw)
Agent model    : openai/gpt-5.4
Agent default  : orchestrateur
Agents dispo   : orchestrateur, builder, reviewer, lab, codexoauth
Config         : /home/openclaw/.openclaw/openclaw.json
```

## Warnings non bloquants

```
- systemd user services unavailable (no systemctl --user) — tmux suffit
- Telegram groupPolicy=allowlist, groupAllowFrom vide — normal (pas de groupe actif)
- Update available v2026.5.28 (current v2026.3.11) — hors scope
```

## Verdict

```
SMOKE = PASS
Gateway OpenClaw opérationnel sur db-layer ws://127.0.0.1:18789
Agent orchestrateur disponible — prêt pour CHILD_AGENT_FIRST_ORCHESTRATION_JOB_01
```
