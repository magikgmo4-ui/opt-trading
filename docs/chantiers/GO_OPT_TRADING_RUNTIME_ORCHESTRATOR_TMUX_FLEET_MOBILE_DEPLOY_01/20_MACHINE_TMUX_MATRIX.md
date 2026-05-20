# 20 — Matrice machines / tmux

## Matrice principale

| Machine | Rôle | Sessions tmux | Priorité | Auto-restart |
|---|---|---|---|---|
| db-layer | OpenClaw MAIN + données + fleet | openclaw-core, fleet-status, apps-connectors, kg-repo, localcms-ui | P0/P1/P2 | limité |
| admin-trading | Runtime trading + Desk Pro | screeners, desk-pro, market-data, strict-workers, trading-pipeline | P0/P1/P2/P3 | limité |
| fantome | Opérateur secondaire | operator-secondary, isolated-tests | P2 | non |
| student | Sandbox | sandbox, ollama-lab | P3 | non |
| cursor-ai | Windows IDE/patch | aucun forcé | n/a | n/a |
| mobile | Terminal SSH/tmux | aucun local | opérateur | n/a |

## Sessions existantes dans le repo

| Session | Script | Existe |
|---|---|---|
| openclaw-core | `scripts/tmux/sessions/openclaw-core.sh` | ✅ |
| screeners | `scripts/tmux/sessions/screeners.sh` | ✅ |
| desk-pro | `scripts/tmux/sessions/desk-pro.sh` | ✅ |
| market-data | `scripts/tmux/sessions/market-data.sh` | ✅ |
| strict-workers | `scripts/tmux/sessions/strict-workers.sh` | ✅ (DRY_RUN=1) |
| trading-pipeline | `scripts/tmux/sessions/trading-pipeline.sh` | ✅ |
| apps-connectors | `scripts/tmux/sessions/apps-connectors.sh` | ✅ |
| kg-repo | `scripts/tmux/sessions/kg-repo.sh` | ✅ |
| localcms-ui | `scripts/tmux/sessions/localcms-ui.sh` | ✅ |
| fleet-status | `scripts/tmux/sessions/fleet-status.sh` | ✅ |

## Gaps

- `operator-secondary`, `isolated-tests`, `sandbox`, `ollama-lab` : optionnels, P2/P3
- presence repo confirmee ; existence distante des sessions tmux reste a verifier via SSH hors de cet environnement
