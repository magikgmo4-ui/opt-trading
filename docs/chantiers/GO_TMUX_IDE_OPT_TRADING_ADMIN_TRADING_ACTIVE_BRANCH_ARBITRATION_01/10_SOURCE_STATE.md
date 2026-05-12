---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
machine: cursor-ai + admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01
status: active
scope: doc-only
captured_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/20_BRANCH_ANALYSIS.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01/10_SOURCE_STATE.md
---

# 10_SOURCE_STATE

## Etat cursor-ai

Branche locale de travail ouverte depuis `sot/mainline` :

```text
## go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01
```

Historique local immediat :

```text
c28b9bd2 Merge pull request #311 from magikgmo4-ui/go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01
c867e632 Merge pull request #312 from magikgmo4-ui/go/GO_COLLECTORS_HELPER_EXTRACTION_IMPL_06
2205dc5e refactor: replace binance _ensure_errors_artifact with ensure_file from collectors_core
```

Etat canonique local :

- `origin/sot/mainline` sur `cursor-ai` : `c28b9bd2`
- repo local propre avant redaction

## Probe SSH principale

Commande de lecture executee le `2026-05-12` :

```bash
ssh admin-trading "cd /opt/trading && hostname && pwd && git branch --show-current && git status --short --branch && git remote -v && git log --oneline -8"
```

Sortie utile :

```text
admin-trading
/opt/trading
go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01
## go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01...origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01
origin https://github.com/magikgmo4-ui/opt-trading.git (fetch)
origin https://github.com/magikgmo4-ui/opt-trading.git (push)
eadc6f5 docs: record admin-trading desk pro artifact observation
1a52bb0 feat: add admin-trading desk pro dry-run artifact output
6373d45 Merge pull request #304 from magikgmo4-ui/go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01
80672ad merge: admin-trading desk pro automation sequence
```

## Probe branche locale et branches voisines

Commande executee :

```bash
ssh admin-trading "cd /opt/trading && git branch -vv"
```

Extrait utile :

```text
* go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01 eadc6f5 [origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01] docs: record admin-trading desk pro artifact observation
  go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01  1a52bb0 [origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01] feat: add admin-trading desk pro dry-run artifact output
  sot/mainline                                                             6373d45 [origin/sot/mainline: en retard de 13] Merge pull request #304 from magikgmo4-ui/go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01
```

## Hash captures a distance

Commande executee :

```bash
ssh admin-trading "cd /opt/trading && echo =HEAD= && git rev-parse --short HEAD && echo =ORIGIN_MAIN= && git rev-parse --short origin/sot/mainline && echo =MERGE_BASE= && git merge-base origin/sot/mainline HEAD"
```

Sortie :

```text
=HEAD=
eadc6f5
=ORIGIN_MAIN=
c28b9bd
=MERGE_BASE=
6373d455c47b7519c6009cab0ef91db22764702e
```

## Etat constate

| Champ | Valeur | Nature |
| --- | --- | --- |
| machine cible | `admin-trading` | ETAT_VERIFIE |
| repertoire | `/opt/trading` | ETAT_VERIFIE |
| branche active | `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01` | ETAT_VERIFIE |
| HEAD actif | `eadc6f5` | ETAT_VERIFIE |
| upstream actif | `origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01` | ETAT_VERIFIE |
| branche parente de chaine | `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01 @ 1a52bb0` | ETAT_VERIFIE |
| `origin/sot/mainline` sur la machine | `c28b9bd` | ETAT_VERIFIE |
| merge-base branche active / mainline | `6373d455` | ETAT_VERIFIE |

## Correction du precedent signal "ahead 1"

Le GO precedent avait capture :

```text
## go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01...origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01 [devant 1]
```

Le probe courant montre un etat different et plus precis :

```text
## go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01...origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01
```

Conclusion source-state :

- le `+1` etait l'ecart entre `OBSERVE_01` et `OUTPUT_01`
- au `2026-05-12`, ce commit n'est plus seulement local : il est deja pousse sur `origin/...OBSERVE_01`
- le risque de perte immediate par abandon du worktree actif n'est donc plus un risque de commit non pousse
