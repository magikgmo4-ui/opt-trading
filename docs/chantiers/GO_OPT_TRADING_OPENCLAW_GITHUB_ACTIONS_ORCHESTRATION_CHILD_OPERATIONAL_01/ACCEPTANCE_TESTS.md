---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01_ACCEPTANCE
doc_type: acceptance_tests
---

# Acceptance Tests — Operational Orchestration

## Test 1 : Import bridge OK

```bash
python3 -c "from modules.openclaw_github_actions_bridge.app.bridge import GitHubActionsBridge; print('PASS')"
```

**Expected :** `PASS`

## Test 2 : Registry load + filter orchestrable jobs

```bash
python3 scripts/openclaw_gh_actions_orchestrate.py --list-jobs
```

**Expected :** Liste des jobs avec `orchestrable_by_openclaw=true`

## Test 3 : Trigger workflow_dispatch on low-risk job

```bash
python3 scripts/openclaw_gh_actions_orchestrate.py --job-id github-actions-job-registry-check
```

**Expected :** `[PASS] Workflow triggered successfully`

## Test 4 : Poll run + get conclusion

Le script doit poller jusqu'à completion et retourner status + conclusion.

**Expected :** status=completed, conclusion=success

## Test 5 : Classification

| Conclusion | Classe attendue |
|---|---|
| `success` | PASS |
| `failure` | FAIL |
| `cancelled` | BLOCKED |
| `action_required` | NEEDS_HUMAN_REVIEW |

## Test 6 : Aucune mutation dangereuse

Vérifier qu'après exécution :
- Aucun fichier modifié localement (sauf le rapport)
- Aucun push effectué
- Aucun merge effectué
- Aucun patch appliqué

```bash
git diff --name-only  # doit être vide (rapport déjà commit)
```

## Test 7 : PR gate/* checks

La PR qui livre ce GO doit passer :
- `gate/preflight` ✅
- `gate/file-scope` ✅
- `gate/no-lock-overlap` ✅
- `gate/tests` ✅
