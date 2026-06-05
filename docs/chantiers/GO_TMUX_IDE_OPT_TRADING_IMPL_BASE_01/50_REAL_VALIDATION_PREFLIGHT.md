---
doc_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01_50_REAL_VALIDATION_PREFLIGHT
doc_type: chantier/validation
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01
status: active
scope: doc-only
validated_at: 2026-05-11
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/20_TARGET_TOPOLOGY_CHECK.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/40_IMPL_OPENING_GATES.md
---

# 50_REAL_VALIDATION_PREFLIGHT

## Objet

Executer un preflight reel, strictement read-only, depuis `cursor-ai` vers `admin-trading`
pour verifier les gates d'ouverture de `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`.

## Commandes executees

### Probe SSH minimal

```bash
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 admin-trading "hostname && whoami && pwd"
```

### Probe repo + prerequis

```bash
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 admin-trading "bash -lc 'if [ -d /opt/trading ]; then echo REPO_DIR_OK; cd /opt/trading; git rev-parse --is-inside-work-tree; git branch --show-current; git status --short --branch; else echo REPO_DIR_MISSING; fi; echo ---; command -v tmux || true; tmux -V || true; command -v node || true; node -v || true; command -v npm || true; npm -v || true; command -v tmux-ide || true; tmux-ide --version || true'"
```

### Probe remote/upstream + ide.yml

```bash
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 admin-trading "cd /opt/trading && git remote -v | sed -n '1,4p' && echo --- && git status --porcelain=v1"
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 admin-trading "cd /opt/trading && git rev-parse --abbrev-ref HEAD && git rev-parse --abbrev-ref --symbolic-full-name @{u}"
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 admin-trading "find /opt/trading -maxdepth 3 \( -name ide.yml -o -name '*.ide.yml' -o -name '.tmux-ide*' \) -print 2>/dev/null"
```

## Resultats bruts utiles

### Transport et shell

- `hostname`: `admin-trading`
- `whoami`: `ghost`
- `pwd`: `/home/ghost`

Verdict:

- `cursor-ai -> SSH -> admin-trading` = PASS

### Repo cible

- `/opt/trading` existe
- `git rev-parse --is-inside-work-tree` = `true`
- remote `origin` = `https://github.com/magikgmo4-ui/opt-trading.git`

### Etat Git machine cible

- branche courante: `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01`
- upstream: `origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01`
- `git status --porcelain=v1` vide

Lecture retenue:

- repo propre
- branche locale non canonique pour demarrer `GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01`
- upstream inattendu par rapport au nom de branche local

### Prerequis binaires

- `tmux`: present (`tmux 3.3a`)
- `node`: present (`v18.20.4`)
- `npm`: present (`9.2.0`)
- `npx`: present (`9.2.0`)
- `tmux-ide`: absent

### Fichiers d'initialisation

- aucun `ide.yml` trouve sous `/opt/trading` (maxdepth 3)
- aucun fichier `.tmux-ide*` trouve sous `/opt/trading` (maxdepth 3)

## Conclusion preflight

Le preflight reel valide la topologie reseau et la machine cible, mais n'ouvre pas encore
la phase d'implementation.

Raison:

- la machine cible n'est pas sur une branche canonique de depart pour ce GO
- `tmux-ide` n'est pas installe
- aucun `ide.yml` de base n'est encore pose

## RISKS

- À qualifier.
