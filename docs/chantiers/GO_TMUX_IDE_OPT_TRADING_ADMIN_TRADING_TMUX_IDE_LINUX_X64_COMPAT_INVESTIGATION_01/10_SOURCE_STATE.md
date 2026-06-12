---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
machine: cursor-ai + admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
status: active
scope: doc-only
captured_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/20_NPM_METADATA.md
---

# 10_SOURCE_STATE

## Etat GitHub

`#321` est deja merged :

```text
merge commit: 5c827261
merged_at: 2026-05-12T05:44:42Z
```

## Etat local cursor-ai

```text
sot/mainline @ 5c827261
worktree clean avant ouverture du GO
```

Branche ouverte :

```text
go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
```

## Etat admin-trading

Commande :

```powershell
ssh admin-trading "cd /opt/trading && git fetch origin --prune && git pull --rebase origin sot/mainline && git status --short --branch && git rev-parse --short HEAD"
```

Sortie utile :

```text
## sot/mainline...origin/sot/mainline
5c82726
```

Conclusion :

- `admin-trading:/opt/trading` est propre et aligne
- l'investigation porte uniquement sur le packaging `tmux-ide`

## RISKS

- À qualifier.
