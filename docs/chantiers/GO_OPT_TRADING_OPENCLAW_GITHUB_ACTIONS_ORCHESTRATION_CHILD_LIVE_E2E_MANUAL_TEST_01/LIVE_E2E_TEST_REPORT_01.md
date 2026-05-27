# LIVE_E2E_TEST_REPORT_01

## Metadata

| Field | Value |
|---|---|
| GO | `GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_LIVE_E2E_MANUAL_TEST_01` |
| Date | `2026-05-26` |
| Operator | `OpenCode` |
| Repo | `magikgmo4-ui/opt-trading` |
| Workflow | `strict-workers-smoke.yml` |
| Job ID | `strict-worker-readonly-smoke` |
| Run ID | `26486400740` |

## Environment Validation

Command:

```bash
python3 scripts/openclaw_gh_actions_live_env.py validate --verbose
```

Observed result:

```text
GITHUB_TOKEN=OK
GITHUB_REPOSITORY=OK
bridge_available=OK
registry_available=OK
All env vars and dependencies present.
```

Verdict: `PASS`

## Live Dispatch

Command:

```bash
python3 scripts/openclaw_gh_actions_orchestrate.py --job-id strict-worker-readonly-smoke --ref sot/mainline --wait 10 --timeout 300 --interval 20
```

Observed result:

```text
Workflow dispatch triggered successfully.
Run discovered: 26486400740
Run status: completed
Conclusion: success
Classification: PASS
```

Verdict: `PASS`

## Run Info Proof

Command:

```bash
python3 scripts/openclaw_gh_actions_live_env.py run-info --run-id 26486400740
```

Observed result:

```json
{
  "run_id": 26486400740,
  "status": "completed",
  "conclusion": "success",
  "html_url": "https://github.com/magikgmo4-ui/opt-trading/actions/runs/26486400740",
  "workflow": null,
  "display_title": "Strict Workers - Smoke Test"
}
```

Verdict: `PASS`

## Pipeline Proof

Command:

```bash
python3 scripts/openclaw_gh_actions_live_env.py pipeline --run-id 26486400740 --job-id strict-worker-readonly-smoke
```

Observed result:

```json
{
  "run_id": 26486400740,
  "html_url": "https://github.com/magikgmo4-ui/opt-trading/actions/runs/26486400740",
  "job_id": "strict-worker-readonly-smoke",
  "workflow": null,
  "status": "completed",
  "conclusion": "success",
  "classification": "PASS",
  "logs_available": true,
  "probable_cause": null,
  "next_action": "ready_for_human_review"
}
```

Verdict: `PASS`

## Failure Analysis

Only fill if classification is `FAIL`.

Command:

```bash
python3 scripts/openclaw_gh_actions_live_env.py pipeline --run-id <RUN_ID> --job-id <JOB_ID> --analyze
```

Observed result:

```json
Not executed because pipeline classification was PASS.
```

## Safety Checks

| Check | Result |
|---|---|
| Workflow modified | `false` |
| Patch applied | `false` |
| Push to `sot/mainline` | `false` |
| dangerous_action_executed | `false` |

## Final Verdict

| Item | Verdict |
|---|---|
| Environment valid | `PASS` |
| Real dispatch executed | `PASS` |
| `run-info` proved | `PASS` |
| `pipeline` proved | `PASS` |
| Safe execution preserved | `PASS` |

## Conclusion

Controlled live E2E proof completed successfully on a real GitHub Actions run. The chain validated environment loading, real workflow dispatch, `run-info`, and `pipeline` classification without any dangerous mutation.
