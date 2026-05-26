# FAILURE_LOGS_ANALYSIS_POLICY

## 1. Goal
Provide a controlled and safe mechanism for OpenClaw to analyze GitHub Actions failure logs, identify the root cause, and suggest remediation steps without performing any mutations.

## 2. Core Constraints
- **Read-Only Analysis**: The analysis must only read data (metadata, job lists, logs).
- **No Automatic Mutations**: No automatic patching, pushing, or merging is allowed.
- **Human in the Loop**: Suggested next actions must be validated by a human operator.
- **Privacy and Security**: Never log or expose secrets, tokens, or sensitive environment variables found in logs.
- **Tooling First**: Use established API bridges and CLI tools.

## 3. Workflow
1. **Detection**: Triggered when a run reaches a terminal failure state (FAIL, BLOCKED, NEEDS_HUMAN_REVIEW).
2. **Data Collection**: Fetch run metadata and job details.
3. **Log Retrieval**: Fetch logs for failed jobs/steps.
4. **Extraction**: Identify error patterns using regex or keyword matching.
5. **Classification**: Map extracted errors to a canonical failure type.
6. **Reporting**: Generate a structured report with suggested next steps.

## 4. Safety Invariants
- `dangerous_action_executed` must always be `false`.
- Fallback to `UNKNOWN_FAILURE` if no pattern matches.
- No direct bypass of GitHub Actions environment restrictions.
