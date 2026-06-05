---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01_40_DECISION
doc_type: chantier/decision
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
status: active
scope: doc-only
decided_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/90_CLOSEOUT.md
---

# 40_DECISION

## Decision

`tmux-ide@latest` / `tmux-ide@2.x` est **non compatible en l'etat** avec `admin-trading` Linux x64 via `npx`, a cause d'une dependance obligatoire erronee vers `@opentui/core-darwin-arm64`.

## Methode compatible identifiee

La seule voie compatible observee pendant ce GO est :

```text
npx -y tmux-ide@1.3.1 --version
```

Cette voie prouve seulement que la CLI `1.3.1` demarre sur Linux x64. Elle ne suffit pas encore pour autoriser installation durable, `ide.yml`, `doctor` ou `validate`.

## Options

| Option | Decision | Raison |
| --- | --- | --- |
| Installer `tmux-ide@latest` | rejetee | `EBADPLATFORM` confirme |
| Forcer `@opentui/core-linux-x64` avec `tmux-ide@2.x` | non retenue | `tmux-ide` declare toujours Darwin arm64 en dependance normale |
| Utiliser `tmux-ide@1.3.1` en pin explicite | candidate | `--version` PASS sur Linux x64 |
| Attendre/fixer upstream `tmux-ide@2.x` | candidate | solution propre pour latest |

## Prochaine suite recommandee

Ouvrir un GO d'essai controle avec `tmux-ide@1.3.1` pinne :

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_V1_PINNED_TRIAL_01
```

Objectif :

- tester `npx -y tmux-ide@1.3.1` sur commandes non destructives
- verifier les commandes disponibles
- decider si `ide.yml` peut etre cree pour cette version
- ne pas installer globalement tant que `doctor` / `validate` ne sont pas compris

## RISKS

- À qualifier.
