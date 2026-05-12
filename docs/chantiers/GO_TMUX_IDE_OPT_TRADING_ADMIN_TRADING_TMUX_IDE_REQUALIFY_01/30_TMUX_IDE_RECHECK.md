---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01_30_TMUX_IDE_RECHECK
doc_type: chantier/tool_check
repo: opt-trading
machine: admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01
status: active
scope: doc-only
captured_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_REQUALIFY_01/40_NEXT_DECISION.md
---

# 30_TMUX_IDE_RECHECK

## Commande executee

```powershell
ssh admin-trading "cd /opt/trading && npx -y tmux-ide --version"
```

## Sortie

```text
npm ERR! code EBADPLATFORM
npm ERR! notsup Unsupported platform for @opentui/core-darwin-arm64@0.1.107: wanted {"os":"darwin","arch":"arm64"} (current: {"os":"linux","arch":"x64"})
npm ERR! notsup Valid OS:    darwin
npm ERR! notsup Valid Arch:  arm64
npm ERR! notsup Actual OS:   linux
npm ERR! notsup Actual Arch: x64

npm ERR! A complete log of this run can be found in:
npm ERR!     /home/ghost/.npm/_logs/2026-05-12T05_27_12_864Z-debug-0.log
```

## Interpretation

`tmux-ide` reste non qualifiable via `npx` sur `admin-trading`.

Le blocage n'est plus Git ou desk-pro. Il est maintenant technique et specifique au package resolu par `npx` :

```text
@opentui/core-darwin-arm64@0.1.107
current platform: linux x64
```

## Decision immediate

Ne pas installer `tmux-ide`.

Ne pas creer `ide.yml`.

Il faut d'abord investiguer la compatibilite Linux x64 / packaging `tmux-ide` ou choisir une methode d'installation compatible.
