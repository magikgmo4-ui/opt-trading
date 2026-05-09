---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01_MERGE_COMMANDS
doc_type: merge_commands
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 40_MERGE_COMMANDS - Merge Commands

## Pré-merge (read-only)

```bash
cd /opt/trading

# Vérifier l'état
git status --short --branch
git log --oneline -5 sot/mainline
git log --oneline -5 go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01

# Vérifier les conflits potentiels
git merge-tree $(git merge-base sot/mainline go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01) sot/mainline go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01 2>/dev/null | head -50

# Compter les fichiers
git diff --stat sot/mainline...go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01 | tail -3
```

## Option A: squash-merge (RECOMMANDÉ)

```bash
cd /opt/trading

# Créer la branche de merge depuis mainline
git checkout sot/mainline
git pull origin sot/mainline
git checkout -b merge/admin-trading-sequence

# Squash-merge
git merge --squash go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01

# Vérifier les fichiers staged
git diff --cached --stat

# Commit
git commit -m "admin-trading: producer/consumer contracts, adapter, smoke

- signal_event V1 contract defined
- visual_context V1 contract defined
- desk_snapshot format documented
- signal_event V0→V1 adapter (modules/desk_pro/signal_event_adapter.py)
- 40/40 tests passed
- 8/8 child GOs PASS
- 68 files, ~6111 lines added
- runtime side effects: NONE"

# Push
git push -u origin merge/admin-trading-sequence

# Créer la PR
gh pr create --base sot/mainline --title "admin-trading: producer/consumer contracts, adapter, smoke" --body-file docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_SEQUENCE_PR_MERGE_01/20_PR_BODY.md
```

## Option B: merge commit classique

```bash
cd /opt/trading

git checkout sot/mainline
git pull origin sot/mainline
git merge go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_SEQUENCE_CLOSEOUT_01

# Vérifier
git log --oneline -5

# Push
git push origin sot/mainline
```

## Post-merge

```bash
# Vérifier les tests après merge
cd /opt/trading
python -m pytest tests/test_signal_event_adapter.py tests/test_admin_trading_contract_compatibility_smoke.py -q

# Vérifier que mainline est propre
git status --short --branch
```

## Interdictions

- ❌ `git push --force`
- ❌ Merge sans revue
- ❌ Merge sans `GO_MERGE` explicite
- ❌ Modifier les fichiers pendant le merge
