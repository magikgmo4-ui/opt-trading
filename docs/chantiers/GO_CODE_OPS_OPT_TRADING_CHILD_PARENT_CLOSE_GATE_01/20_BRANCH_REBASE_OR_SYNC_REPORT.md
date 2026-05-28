---
doc_id: GO_CODE_OPS_OPT_TRADING_CHILD_PARENT_CLOSE_GATE_01_REBASE_REPORT
doc_type: rebase_report
repo: opt-trading
go_id: GO_CODE_OPS_OPT_TRADING_CHILD_PARENT_CLOSE_GATE_01
updated_at: 2026-05-28
---

# 20_BRANCH_REBASE_OR_SYNC_REPORT

## État pré-rebase

| Champ | Valeur |
|---|---|
| Branche | `go/GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01` |
| Dernier commit local | `774caf44` |
| Ahead de sot/mainline | 20 |
| Behind de sot/mainline | 28 |
| Working tree | clean (untracked : .claude/, artifacts/, secrets/) |

## Commande exécutée

```bash
git rebase origin/sot/mainline
```

## Résultat

```text
Rebasage (20/20) — succès sans conflit
```

## État post-rebase

| Champ | Valeur |
|---|---|
| Ahead de sot/mainline | 20 |
| Behind de sot/mainline | 0 |
| Nouveau HEAD | `60362609` |
| Conflits | aucun |
| Working tree | clean |

## Verdict

```text
REBASE_CLEAN — branche alignée sur origin/sot/mainline.
Push requis : git push --force-with-lease
```
