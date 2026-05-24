# RISK ASSESSMENT: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_01

## Security Risks
- **GitHub Token exposure**: Ensure tokens are read from environment variables and never logged.
- **Unauthorized Dispatch**: Use the validated registry and a mandatory `orchestrable_by_openclaw: true` flag.

## Operational Risks
- **Rate Limiting**: GitHub API has rate limits. Polling should be spaced (e.g., every 10-30s).
- **Infinite Loops**: Implement timeouts for run status polling.
- **Partial Failure**: A workflow might "pass" but fail to produce specific artifacts.

## Mitigations
- **ReadOnly first**: Only `workflow_dispatch` on low-risk, dry-run jobs initially.
- **Safety Gate**: Hardcoded check against `orchestrable_by_openclaw` flag in the registry.
- **Manual Oversight**: OpenClaw only triggers; merge/apply remains manual.
