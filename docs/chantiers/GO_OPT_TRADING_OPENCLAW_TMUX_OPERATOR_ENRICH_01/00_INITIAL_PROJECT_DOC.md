# GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_ENRICH_01

## Contexte

`modules/openclaw_tmux_operator/` existe et fonctionne (PASS GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01).
GAP-02 identifié dans le closeout du GO parent : enrichissement logs + health aggregator multi-machine.

## Périmètre

Enrichir `modules/openclaw_tmux_operator/` en lecture seule :

- `session-logs` — étendre aux logs admin-trading via SSH (actuellement local seulement)
- `health-aggregate` — ajouter tmux réel (non dry-run) via SSH multi-machines
- `machine-status` — enrichir avec runtime_health age + fleet_status JSON par machine
- Nouveaux tests unitaires couvrant les enrichissements

## Hors scope

- Aucune exécution IA ou write tmux
- Ne pas modifier `scripts/ai/workers/orchestration/`
- Ne pas modifier CI workflows
- Ne pas ouvrir de bridge runtime

## Commandes actuelles (base)

```
fleet-status, machine-status, tmux-status, attach-hint,
logs, session-logs, health-all, health-aggregate,
openclaw-health, openclaw-probe
```

## Livrable attendu

- `cmd.sh` enrichi
- `health_aggregate.py` — tmux réel multi-machines via SSH
- Tests unitaires PASS
- `90_REPRISE.md` closeout

## Dépendances

- PR #618 / #623 / #624 — mergées, non modifiées
- `runtime_health/fleet_orchestrator.py` — consommé en lecture seule
- SSH db-layer ↔ admin-trading validé (GAP-01 PASS)
