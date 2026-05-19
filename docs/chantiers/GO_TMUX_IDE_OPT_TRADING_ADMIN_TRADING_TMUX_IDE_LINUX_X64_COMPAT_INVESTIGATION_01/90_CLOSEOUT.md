---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01_90_CLOSEOUT
doc_type: chantier/closeout
repo: opt-trading
machine: cursor-ai + admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
status: active
scope: doc-only
verdict: PARTIAL_PASS
checked_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/20_NPM_METADATA.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/30_LINUX_X64_PROBES.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/40_DECISION.md
---

# 90_CLOSEOUT

## Verdict

**PARTIAL_PASS**

## Resultats

| Critere | Etat |
| --- | --- |
| cause `EBADPLATFORM` identifiee | PASS |
| `tmux-ide@latest` compatible Linux x64 | FAIL |
| toutes versions `2.x` compatibles Linux x64 | FAIL, dependance Darwin forcee |
| paquet OpenTUI Linux x64 disponible | PASS |
| `tmux-ide@1.3.1 --version` sur admin-trading | PASS |
| installation durable effectuee | non |
| `ide.yml` cree | non |
| worktree admin-trading apres probes | clean |

## Conclusion

Le probleme vient du packaging `tmux-ide@2.x`, pas de la machine Linux x64 ni de l'absence d'un paquet natif OpenTUI Linux.

`tmux-ide@1.3.1` est une voie candidate car la CLI demarre sur `admin-trading`, mais elle doit etre testee dans un GO separe avant toute adoption.

## Point de reprise

```text
admin-trading:/opt/trading
branch: sot/mainline
HEAD: 5c82726
tmux-ide@latest: FAIL EBADPLATFORM
tmux-ide@2.x: forced @opentui/core-darwin-arm64
tmux-ide@1.3.1: --version PASS
ide.yml: absent
decision: trial pin 1.3.1 before install or ide.yml
```

## Commit et PR

```bash
git add docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01/ \
        docs/index/inbox/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01.md
git commit -m "docs: investigate tmux-ide linux x64 compatibility"
git push -u origin go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_LINUX_X64_COMPAT_INVESTIGATION_01
```

PR titre : `docs: investigate tmux-ide linux x64 compatibility`
