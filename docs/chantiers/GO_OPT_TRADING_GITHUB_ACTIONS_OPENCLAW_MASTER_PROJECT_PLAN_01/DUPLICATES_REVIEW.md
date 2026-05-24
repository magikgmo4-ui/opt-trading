# DUPLICATES_REVIEW — GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01

## Objet

Comparer les jobs GitHub Actions existants avec le registre des jobs non-trading.

## Doublons / réutilisations déjà détectés

| GitHub Actions workflow | Job non-trading couvert | Décision |
|---|---|---|
| `.github/workflows/strict-workers-validate.yml` | `strict-worker-job-packet-validate` | `REUSE` |
| `.github/workflows/strict-workers-validate.yml` | `strict-worker-model-registry-check` | `WRAP_IN_ACTION` |
| `.github/workflows/strict-workers-validate.yml` | `strict-worker-task-index-check` | `WRAP_IN_ACTION` |
| `.github/workflows/strict-workers-smoke.yml` | `strict-worker-readonly-smoke` | `REUSE` |
| `.github/workflows/openclaw-mcp-policy-static-validator.yml` | OpenClaw MCP policy validator | `REUSE` |
| `.github/workflows/openclaw-mcp-policy-static-validator.yml` | `repo-diff-check` via `git diff --check` | `PARTIAL_REUSE` |

## À ne pas recréer directement

- `strict-worker-job-packet-validate`
- `strict-worker-readonly-smoke`
- `repo-diff-check` sans raison claire
- OpenClaw MCP policy static validator

## Jobs candidats encore à analyser

- `repo-doc-frontmatter-lint`
- `repo-doc-link-check`
- `repo-go-index-audit`
- `repo-closeout-eligibility-check`
- `scheduler-config-validate`
- `github-actions-job-registry-check`
- `github-actions-workflow-dispatch-smoke`
