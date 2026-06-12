---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01_10_BEFORE_STATE
doc_type: chantier/before_state
repo: opt-trading
machine: admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01
status: active
scope: doc-only
captured_at: À_CAPTURER
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01/10_SOURCE_STATE.md
---

# 10_BEFORE_STATE

## État Git connu avant exécution (ETAT_DECLARE)

Source : `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_01/10_SOURCE_STATE.md`, capturé 2026-05-11.

| Champ | Valeur observée |
| --- | --- |
| machine | admin-trading |
| répertoire | `/opt/trading` |
| remote origin | `https://github.com/magikgmo4-ui/opt-trading.git` |
| branche courante | `go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01` |
| upstream | `origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01` |
| worktree | propre (clean) |
| SSH | PASS (utilisateur `ghost`) |

> Classification : ETAT_DECLARE — issu du GO parent, probe 2026-05-11. Pas de re-probe live dans ce fichier.

---

## Re-probe live avant exécution — À CAPTURER

Commande à exécuter depuis cursor-ai avant toute opération :

```bash
ssh admin-trading 'cd /opt/trading && echo "=hostname=" && hostname && echo "=pwd=" && pwd && echo "=branch=" && git branch --show-current && echo "=status=" && git status --short --branch && echo "=remote=" && git remote -v && echo "=log=" && git log --oneline -5'
```

Sortie réelle :

```
À_CAPTURER
```

> Remplir ce champ avant de lancer l'étape 20_EXECUTION_LOG.

## RISKS

- À qualifier.
