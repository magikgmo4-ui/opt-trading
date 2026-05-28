---
doc_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_01_INVENTORY_PLAN
doc_type: plan
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_DBLAYER_REPO_HYGIENE_QUARANTINE_01
parent_go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01
status: open
mode: PLAN_ONLY
source_kind: canonical
updated_at: 2026-05-28
---

# 10 — Inventory plan (read-only): untracked sur db-layer:/opt/trading

## Principe

Objectif = inventaire complet des untracked + metadonnees minimales, sans lire le contenu sensible (secrets), et sans aucune ecriture.

## Commandes autorisees (read-only)

```bash
ssh db-layer 'hostname; whoami; pwd'
ssh db-layer 'cd /opt/trading && git status --short --branch'
ssh db-layer 'cd /opt/trading && git ls-files --others --exclude-standard | sort'
```

## Inventaire detaille (metadonnees seulement)

Pour chaque racine untracked identifiee (`.claude/`, `artifacts/backtests/`, `secrets/`) :

```bash
ssh db-layer 'cd /opt/trading && find .claude -type f -maxdepth 3 -printf "%p\t%s\t%TY-%Tm-%TdT%TH:%TM:%TS\n" | head -n 200'
ssh db-layer 'cd /opt/trading && find artifacts/backtests -type f -maxdepth 5 -printf "%p\t%s\t%TY-%Tm-%TdT%TH:%TM:%TS\n" | head -n 400'
ssh db-layer 'cd /opt/trading && find secrets -type f -maxdepth 2 -printf "%p\t%s\t%TY-%Tm-%TdT%TH:%TM:%TS\n"'
```

Regles :
- Pas de `cat` / `sed -n` sur `secrets/*`.
- Pas de `tar` / `zip` / `cp` / `mv` / `rm`.
- Pas de `git clean`, pas de `git add`.

## Classification (sans lecture contenu)

Classifier par pattern de chemin + extension :

- `secrets/*.json`, `secrets/*.env`, `secrets/*key*` => SENSITIVE_SECRET (bloquant)
- `artifacts/backtests/**/*.csv`, `**/*.md`, `**/*.json` => ARTIFACT_OUTPUT (a quarantiner)
- `.claude/**/*.lock`, `.claude/**/cache*` => TOOLING_STATE (a quarantiner)

## Format de preuve (a coller dans le futur GO d’execution)

Exiger un tableau inventaire (CSV ou markdown) :

| Path | Bytes | MTime | Class | ActionCandidate |
|---|---:|---|---|---|

ActionCandidate (plan-only) :
- `KEEP_LOCAL_UNTRACKED` (si justifie)
- `QUARANTINE_OUTSIDE_REPO` (preferer)
- `REMOVE_AFTER_BACKUP` (jamais sans accord explicite)

## Sortie attendue

```text
INVENTORY_STATUS = READY_TO_RUN (read-only)
EXECUTION_ALLOWED = NO
```
