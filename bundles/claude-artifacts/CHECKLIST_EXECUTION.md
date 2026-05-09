# CHECKLIST_EXECUTION — Claude Artifacts Operator Pack

Checklist d'execution standard pour operateur cursor-ai.

## Avant tout commit

- [ ] `git status --short --branch` — branche attendue ?
- [ ] `git diff --stat` — fichiers dans docs/ ou bundles/ uniquement ?
- [ ] `git diff --cached --name-only | grep -vE "^(docs/|bundles/)"` — aucun fichier runtime ?
- [ ] `git diff --cached | grep -iE "(password|secret|token|key=|api_key|\.env)"` — aucun secret ?
- [ ] `trade_allowed=false` preserve si template JSON touche ?
- [ ] `admin_trading_runtime=false` preserve si template JSON touche ?

## Avant tout push

- [ ] Commit message au format `docs: <message>` ?
- [ ] Branche nommee `go/GO_OPT_TRADING_CURSOR_AI_<DESCRIPTION>_<XX>` ?
- [ ] Aucun fichier force-ajoute sans raison documentee ?

## Avant toute PR

- [ ] Diff verifie : doc-only, no runtime, no secrets ?
- [ ] `git diff sot/mainline...HEAD --stat` — cohérent ?
- [ ] Inbox creee dans `docs/index/inbox/` ?
- [ ] Chantier complet : structure canonique (`00_GO_OPEN.md`, `10_SOURCE_STATE.md`, `20_OPERATOR_PACK_SPEC.md`, `30_ARTIFACTS_INDEX.md`, `40_USAGE_WORKFLOW.md`, `90_CLOSEOUT.md`) ou structure legacy equivalent documentee ?
- [ ] Closeout contient verdict PASS/FAIL et prochain GO ?

## Apres merge

- [ ] `git fetch origin --prune` execute ?
- [ ] `git checkout sot/mainline && git pull --rebase origin sot/mainline` execute ?
- [ ] Branche source supprimee (local + remote) ?
- [ ] Reprise mise a jour dans `bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md` ?

## Liste de verification rapide

```bash
# Pre-commit
echo "=== Pre-commit checks ==="
echo "Branch: $(git branch --show-current)"
echo "Non-doc files:"
git diff --cached --name-only | grep -vE "^(docs/|bundles/)" || echo "  (none)"
echo "Secrets:"
git diff --cached | grep -iE "(password|secret|token|key=|api_key|\.env)" || echo "  (none)"

# Pre-push
echo "=== Pre-push checks ==="
echo "Last commit: $(git log --oneline -1)"
echo "Diff stat:"
git diff --stat origin/$(git branch --show-current) 2>$null || echo "  (no remote tracking)"

# Post-merge
echo "=== Post-merge checks ==="
git fetch origin --prune
echo "Local branches: $(git branch | grep -c .)"
```
