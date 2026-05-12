---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01_40_NEXT_DECISION
doc_type: chantier/decision
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01
status: active
scope: doc-only
decided_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/90_CLOSEOUT.md
---

# 40_NEXT_DECISION

## Decision

**BLOCKED technique.**

La requalification leve le blocage Git precedent, mais confirme que `tmux-ide` n'est toujours pas executable sur `admin-trading` via `npx`.

## Ce qui est debloque

- `admin-trading:/opt/trading` est sur `sot/mainline`
- la branche desk-pro active a ete mergee
- les tests desk-pro post-merge sont PASS
- le worktree distant est propre

## Ce qui reste bloque

- `tmux-ide` absent
- `npx -y tmux-ide --version` echoue avec `EBADPLATFORM`
- `ide.yml` absent et ne doit pas etre cree tant que l'outil n'est pas qualifie

## Prochaine suite recommandee

Ouvrir un GO technique cible sur le packaging `tmux-ide` :

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_COMPAT_INVESTIGATION_01
```

Objectif :

- identifier pourquoi `npx tmux-ide` tire `@opentui/core-darwin-arm64`
- trouver une version ou une installation compatible Linux x64
- seulement ensuite reprendre installation / `ide.yml` / doctor / validate
