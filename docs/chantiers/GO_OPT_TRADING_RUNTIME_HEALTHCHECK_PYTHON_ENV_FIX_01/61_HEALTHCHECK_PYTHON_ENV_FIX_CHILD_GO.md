---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_PARENT_ATTACHMENT_NOTE
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
source_kind: canonical
updated_at: 2026-05-26
---

# 61 — Child GO attachment: runtime healthcheck Python env fix

## Context (parent)

Parent runtime :

```text
GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
```

Etat runtime etabli par les evidences :

- strict read-only 1–10 : `PASS_WITH_WARNINGS`
- mobile smoke read-only : `PASS_WITH_WARNINGS`
- le WARN structurel prioritaire reste le STEP 5 (runtime health / orchestrator), a solidifier avant close-gate.

Sources parent :

- `90_REPRISE.md`
- `58_FLEET_HYGIENE_AUDIT.md`
- `59_MOBILE_SMOKE_RESULTS.md`

## Objective (child)

```text
GO = GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
ROLE = GO_CHILD_ATTACHED_TO_PARENT
```

Objectif borne :

- eliminer l ambiguity Python/PyYAML dans les wrappers systemd runtime health
  (choix d un python capable d `import yaml`)
- ne pas toucher fleet stale/unreachable, Telegram allowlist, secrets/untracked, watchdog 11–12

## Patch scope

- `scripts/runtime_healthcheck.sh` (deja aligne sur le principe "python avec yaml")
- `scripts/fleet_orchestrator.sh` (aligne sur le meme principe)

## Validation (local repo)

```text
git diff --check = PASS
bash -n scripts/runtime_healthcheck.sh = PASS
bash -n scripts/fleet_orchestrator.sh = PASS
pytest tests/runtime_health/test_warn_classification.py tests/runtime_health/test_cursor_ai_windows.py = PASS
```

## Remaining gap / close gate impact

- Ce patch ne prouve pas un deploy runtime ; il supprime un risque structurel cote repo (wrappers).
- Close-gate parent reste interdit tant que STEP 5 n est pas rejoue sur runtime et tant que fleet demeure `WARN`.
