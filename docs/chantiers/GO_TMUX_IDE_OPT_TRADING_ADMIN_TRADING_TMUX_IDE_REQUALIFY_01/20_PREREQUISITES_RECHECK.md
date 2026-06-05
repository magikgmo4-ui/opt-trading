---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01_20_PREREQUISITES_RECHECK
doc_type: chantier/prerequisites_check
repo: opt-trading
machine: admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01
status: active
scope: doc-only
captured_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/30_TMUX_IDE_RECHECK.md
---

# 20_PREREQUISITES_RECHECK

## Commande executee

```powershell
ssh admin-trading "cd /opt/trading && tmux -V && node --version && npm --version && npx --version && command -v tmux-ide || true && test -f ide.yml && echo IDE_YML_PRESENT || echo IDE_YML_ABSENT"
```

## Sortie

```text
tmux 3.3a
v18.20.4
9.2.0
9.2.0
IDE_YML_ABSENT
```

## Interpretation

| Critere | Etat |
| --- | --- |
| `tmux` | PASS, `3.3a` |
| `node` | PASS, `v18.20.4` |
| `npm` | PASS, `9.2.0` |
| `npx` | PASS, `9.2.0` |
| executable `tmux-ide` local | absent |
| `ide.yml` | absent |

Les prerequis systeme de base sont disponibles, mais `tmux-ide` et `ide.yml` ne sont toujours pas presents.

## RISKS

- À qualifier.
