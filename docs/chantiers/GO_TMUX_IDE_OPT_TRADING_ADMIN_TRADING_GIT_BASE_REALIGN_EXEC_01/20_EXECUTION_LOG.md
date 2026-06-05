---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01_20_EXECUTION_LOG
doc_type: chantier/execution_log
repo: opt-trading
machine: admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01
status: active
scope: exec-ssh
executed_at: À_CAPTURER
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/10_BEFORE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/30_AFTER_STATE.md
---

# 20_EXECUTION_LOG

## Prérequis avant exécution

- [ ] `10_BEFORE_STATE.md` — re-probe live rempli
- [ ] Worktree clean confirmé (aucun fichier modifié non commité)
- [ ] Aucune branche locale avec travail non poussé sur admin-trading

---

## Séquence d'exécution

À exécuter depuis cursor-ai (terminal Windows / PowerShell) **en une seule session SSH** :

### Étape 1 — Fetch et prune

```bash
ssh admin-trading 'cd /opt/trading && git fetch origin --prune 2>&1'
```

Sortie réelle :
```
À_CAPTURER
```

---

### Étape 2 — Vérifier si sot/mainline existe en local

```bash
ssh admin-trading 'cd /opt/trading && git branch -a | grep sot/mainline'
```

Sortie réelle :
```
À_CAPTURER
```

---

### Étape 3 — Basculer sur sot/mainline

Si la branche locale existe :
```bash
ssh admin-trading 'cd /opt/trading && git switch sot/mainline 2>&1'
```

Si la branche locale n'existe pas (créer en tracking remote) :
```bash
ssh admin-trading 'cd /opt/trading && git switch --track origin/sot/mainline 2>&1'
```

Sortie réelle :
```
À_CAPTURER
```

---

### Étape 4 — Pull rebase sur origin/sot/mainline

```bash
ssh admin-trading 'cd /opt/trading && git pull --rebase origin sot/mainline 2>&1'
```

Sortie réelle :
```
À_CAPTURER
```

---

### Étape 5 — Vérification finale

```bash
ssh admin-trading 'cd /opt/trading && echo "=branch=" && git branch --show-current && echo "=status=" && git status --short --branch && echo "=log=" && git log --oneline -5'
```

Sortie réelle :
```
À_CAPTURER
```

---

## Règles de sécurité pendant l'exécution

- Si le worktree n'est PAS clean à l'étape 1 : STOP — documenter et ne pas continuer.
- Si `git pull --rebase` produit des conflits : STOP — ne pas forcer, documenter l'état.
- Ne rien exécuter hors de cette séquence.
- Ne pas lancer d'autres commandes (pas de reset hard, pas de force push, pas d'installation).

---

## Résultat global

- Timestamp d'exécution : À_CAPTURER
- Durée : À_CAPTURER
- Résultat : `PASS` / `FAIL` / `STOP` — À_CAPTURER
- Notes : À_CAPTURER

## RISKS

- À qualifier.
