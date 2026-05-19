---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01_30_LINUX_X64_PROBES
doc_type: chantier/probes
repo: opt-trading
machine: admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
status: active
scope: doc-only
captured_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/40_DECISION.md
---

# 30_LINUX_X64_PROBES

## Probe `latest`

Commande precedente requalifiee :

```powershell
ssh admin-trading "cd /opt/trading && npx -y tmux-ide --version"
```

Resultat :

```text
npm ERR! code EBADPLATFORM
npm ERR! notsup Unsupported platform for @opentui/core-darwin-arm64@0.1.107: wanted {"os":"darwin","arch":"arm64"} (current: {"os":"linux","arch":"x64"})
```

Interpretation :

- `tmux-ide@latest` pointe vers `2.1.5`
- `2.1.5` force la dependance Darwin arm64
- Linux x64 rejette correctement ce paquet avec `EBADPLATFORM`

## Probe `tmux-ide@1.3.1`

Commande :

```powershell
ssh admin-trading "cd /opt/trading && npx -y tmux-ide@1.3.1 --version"
```

Sortie :

```text
tmux-ide v1.3.1
```

Metadata :

```json
{
  "version": "1.3.1",
  "dependencies": {
    "js-yaml": "^4.1.1"
  },
  "bin": {
    "tmux-ide": "bin/cli.js"
  }
}
```

Interpretation :

- `tmux-ide@1.3.1` est executable sur `admin-trading` Linux x64 pour `--version`
- ce probe ne valide pas encore `doctor`, `validate`, ni la compatibilite fonctionnelle avec un futur `ide.yml`

## Etat Git apres probes

Commande :

```powershell
ssh admin-trading "cd /opt/trading && git status --short --branch && git rev-parse --short HEAD"
```

Sortie :

```text
## sot/mainline...origin/sot/mainline
5c82726
```

Conclusion :

- les probes `npx` n'ont pas modifie le worktree
- aucune installation repo n'a ete effectuee
