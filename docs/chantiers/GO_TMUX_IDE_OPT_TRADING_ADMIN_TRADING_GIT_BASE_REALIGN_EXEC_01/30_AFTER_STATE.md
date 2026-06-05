---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01_30_AFTER_STATE
doc_type: chantier/after_state
repo: opt-trading
machine: admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01
status: active
scope: doc-only
captured_at: À_CAPTURER
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/20_EXECUTION_LOG.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/90_CLOSEOUT.md
---

# 30_AFTER_STATE

## État attendu après réalignement réussi

| Champ | Valeur attendue |
| --- | --- |
| branche | `sot/mainline` |
| upstream | `origin/sot/mainline` |
| HEAD | ≥ `6373d455` (PR #304) |
| worktree | clean |
| status | `## sot/mainline...origin/sot/mainline` |

---

## État capturé après exécution — À CAPTURER

Commande de vérification finale :

```bash
ssh admin-trading 'cd /opt/trading && echo "=hostname=" && hostname && echo "=branch=" && git branch --show-current && echo "=upstream=" && git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null && echo "=head=" && git rev-parse --short HEAD && echo "=status=" && git status --short --branch && echo "=log=" && git log --oneline -5'
```

Sortie réelle :
```
À_CAPTURER
```

---

## Critères PASS pour l'état après

- [ ] `git branch --show-current` retourne `sot/mainline`
- [ ] `git status` retourne worktree clean
- [ ] HEAD ≥ `6373d455`
- [ ] upstream = `origin/sot/mainline`
- [ ] Aucun conflit résiduel

---

## Classification

- branche après : ETAT_VERIFIE si sortie git ci-dessus est remplie, sinon ETAT_DECLARE
- upstream après : ETAT_VERIFIE si sortie git ci-dessus est remplie, sinon ETAT_DECLARE

## RISKS

- À qualifier.
