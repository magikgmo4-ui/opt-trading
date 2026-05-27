---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RUNTIME_REPLAY_01_OPENING
doc_type: opening
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RUNTIME_REPLAY_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
source_kind: canonical
created_at: 2026-05-27
updated_at: 2026-05-27
---

# 00 — Opening: runtime replay (healthcheck PyYAML fix)

## Contexte

- Base repo : `sot/mainline@de76e947` (merge PR #864)
- Fix precedent (repo) : `GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01` (MERGED)
- Parent : `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- Etat parent : `CLOSEOUT_BLOCKED`

## Objectif

Prouver en runtime reel (hosts) que le fix PyYAML est effectif :

- wrapper `scripts/fleet_orchestrator.sh` choisit un python capable de `import yaml`
- la machine map n'est plus silencieusement vide a cause de PyYAML manquant
- STEP 5 peut etre rejoue et re-classifie (au minimum: sans le blocage PyYAML)

## Contraintes

- Ne pas modifier les index globaux.
- Ne pas fermer le parent.
- Ne pas traiter : fleet stale/unreachable, Telegram allowlist, secrets/artifacts, mobile smoke write, watchdog 11–12.
- Read-only par defaut ; toute action d'ecriture doit etre explicitement annoncee et acceptee.

## Livrables

- Runbook de commandes read-only (ssh) et captures.
- Doc de resultats : `RUNTIME_REPLAY_STATUS`, `STEP_5_STATUS`, `REMAINING_GAP`, `PARENT_CLOSE_GATE_STATUS`.
