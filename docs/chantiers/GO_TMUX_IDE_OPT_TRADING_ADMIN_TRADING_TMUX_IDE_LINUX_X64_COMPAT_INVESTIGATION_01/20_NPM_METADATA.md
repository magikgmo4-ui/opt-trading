---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01_20_NPM_METADATA
doc_type: chantier/package_metadata
repo: opt-trading
machine: cursor-ai
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
status: active
scope: doc-only
captured_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/30_LINUX_X64_PROBES.md
---

# 20_NPM_METADATA

## `tmux-ide@latest`

Commande :

```powershell
npm view tmux-ide@latest version dist-tags dependencies optionalDependencies peerDependencies bin os cpu --json
```

Sortie utile :

```json
{
  "version": "2.1.5",
  "dist-tags": { "latest": "2.1.5" },
  "dependencies": {
    "@opentui/core": "^0.1.88",
    "@opentui/core-darwin-arm64": "^0.1.88",
    "@opentui/solid": "^0.1.88",
    "node-pty": "1.2.0-beta.12"
  },
  "bin": {
    "tmux-ide": "bin/cli.ts"
  }
}
```

Conclusion :

- `tmux-ide@2.1.5` declare `@opentui/core-darwin-arm64` comme dependance normale
- cette dependance normale force son installation meme sur Linux x64

## Paquets natifs OpenTUI

Commandes :

```powershell
npm view @opentui/core-darwin-arm64@0.1.107 version os cpu dist.tarball --json
npm view @opentui/core-linux-x64@0.1.107 version os cpu dist.tarball --json
```

Sorties utiles :

```json
{
  "version": "0.1.107",
  "os": ["darwin"],
  "cpu": ["arm64"]
}
```

```json
{
  "version": "0.1.107",
  "os": ["linux"],
  "cpu": ["x64"]
}
```

Conclusion :

- le paquet Linux x64 existe
- le probleme n'est pas l'absence de binaire Linux x64 OpenTUI
- le probleme est la dependance obligatoire Darwin arm64 ajoutee par `tmux-ide@2.x`

## `@opentui/core`

Commande :

```powershell
npm view @opentui/core@0.1.107 dependencies optionalDependencies os cpu --json
```

Sortie utile :

```json
{
  "optionalDependencies": {
    "@opentui/core-linux-x64": "0.1.107",
    "@opentui/core-win32-x64": "0.1.107",
    "@opentui/core-darwin-x64": "0.1.107",
    "@opentui/core-linux-arm64": "0.1.107",
    "@opentui/core-win32-arm64": "0.1.107",
    "@opentui/core-darwin-arm64": "0.1.107"
  }
}
```

Conclusion :

- `@opentui/core` gere correctement les binaires natifs en optionalDependencies
- `tmux-ide@2.x` contourne ce modele en ajoutant `@opentui/core-darwin-arm64` comme dependance obligatoire

## Versions `tmux-ide`

Versions publiees :

```text
1.0.0
1.1.0
1.2.0
1.2.1
1.3.1
2.0.0
2.1.0
2.1.1
2.1.2
2.1.3
2.1.4
2.1.5
```

Balayage dependencies :

```text
1.0.0 core=False linux=False forced_darwin=False
1.1.0 core=False linux=False forced_darwin=False
1.2.0 core=False linux=False forced_darwin=False
1.2.1 core=False linux=False forced_darwin=False
1.3.1 core=False linux=False forced_darwin=False
2.0.0 core=True linux=False forced_darwin=True
2.1.0 core=True linux=False forced_darwin=True
2.1.1 core=True linux=False forced_darwin=True
2.1.2 core=True linux=False forced_darwin=True
2.1.3 core=True linux=False forced_darwin=True
2.1.4 core=True linux=False forced_darwin=True
2.1.5 core=True linux=False forced_darwin=True
```

Conclusion :

- toutes les versions `2.x` publiees forcent `@opentui/core-darwin-arm64`
- les versions `1.x` ne portent pas cette dependance

## RISKS

- À qualifier.
