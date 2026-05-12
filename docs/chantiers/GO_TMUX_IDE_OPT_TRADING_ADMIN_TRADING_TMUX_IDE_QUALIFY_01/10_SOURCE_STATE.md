---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01_10_SOURCE_STATE
doc_type: chantier/source_state
repo: opt-trading
machine: cursor-ai + admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01
status: blocked
scope: doc-only
captured_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01/30_AFTER_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01/60_ADMIN_TRADING_PROBE_RESULTS.md
---

# 10_SOURCE_STATE

## État cursor-ai — sot/mainline (ETAT_DECLARE)

- base : `sot/mainline`
- HEAD cursor-ai : ≥ `6373d455` (PR #304 merge, 2026-05-12)
- PR #305 mergée (ETAT_DECLARE — user 13_ESTABLISHED)
- branche de travail créée : `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_QUALIFY_01`

Vérification locale à capturer :

```bash
# Sur cursor-ai
git status --short --branch
git log --oneline -5
```

Sortie réelle :
```
À_CAPTURER
```

---

## État admin-trading:/opt/trading — Git (ETAT_DECLARE)

Source : `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_GIT_BASE_REALIGN_EXEC_01` (PASS documenté).

| Champ | Valeur attendue après réalignement |
| --- | --- |
| branche | `sot/mainline` |
| upstream | `origin/sot/mainline` |
| worktree | clean |
| HEAD | ≥ `6373d455` |

Re-probe Git live (capturée 2026-05-12) :

```bash
ssh admin-trading "cd /opt/trading && hostname && pwd && git branch --show-current && git status --short --branch && git log --oneline -5"
```

Sortie réelle :
```
## go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01...origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01 [devant 1]
```

```
ETAT_VERIFIE — 2026-05-12
Machine: admin-trading
Path: /opt/trading
Branch actuelle:
go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01
Status:
## go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01...origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01 [devant 1]
Conclusion:
La base Git canonique attendue pour ce GO n'est pas disponible.
admin-trading n'est pas sur sot/mainline.
Ne pas poursuivre l'installation ou la qualification tmux-ide tant que cette branche active n'est pas arbitrée.
```

> **STOP — branche ≠ sot/mainline et worktree ahead 1 : ce GO est BLOCKED.**
> Ne pas reset, ne pas switch, ne pas pull sans arbitrage : travail actif possible.

---

## SSH — ETAT_DECLARE (confirmé 2026-05-11)

- SSH cursor-ai → admin-trading : PASS
- utilisateur : `ghost`
- répertoire : `/opt/trading`
