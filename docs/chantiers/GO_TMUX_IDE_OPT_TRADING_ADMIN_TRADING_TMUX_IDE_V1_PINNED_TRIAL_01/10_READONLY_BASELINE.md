# 10_READONLY_BASELINE

## 1_MASTER_TARGET

Documenter la baseline read-only de `admin-trading` avant le trial pinne `tmux-ide@1.3.1`.

## 7_CANONICAL_STATE

Probe lance depuis :

```text
C:\wtmuxv1
```

Branche :

```text
go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_V1_PINNED_TRIAL_01
```

Source :

```text
origin/sot/mainline @ 024ce217
```

## 8_ADMIN_TRADING_BASELINE

| Commande autorisee | Resultat | Exit |
| --- | --- | --- |
| `hostname` | `admin-trading` | 0 |
| `uname -a` | `Linux admin-trading 6.1.0-44-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.164-1 (2026-03-09) x86_64 GNU/Linux` | 0 |
| `command -v tmux` | `/usr/bin/tmux` | 0 |
| `tmux -V` | `tmux 3.3a` | 0 |
| `command -v node` | `/usr/bin/node` | 0 |
| `node --version` | `v18.20.4` | 0 |
| `command -v npm` | `/usr/bin/npm` | 0 |
| `npm --version` | `9.2.0` | 0 |
| `command -v npx` | `/usr/bin/npx` | 0 |

## 9_PRIOR_ATTEMPT_NOTE

Un premier essai SSH avant allumage de la machine a echoue sur :

```text
ssh: connect to host 192.168.0.111 port 22: Connection timed out
```

Apres allumage de `admin-trading`, les probes read-only ci-dessus passent.

## 12_INVARIANTS

- Aucune installation effectuee.
- Aucun fichier distant cree.
- Aucun `ide.yml` cree.
- Aucun runtime modifie.

## 17_RESUME_POINT

La baseline admin-trading est compatible avec un trial non destructif via `npx`.

## RISKS

- À qualifier.
