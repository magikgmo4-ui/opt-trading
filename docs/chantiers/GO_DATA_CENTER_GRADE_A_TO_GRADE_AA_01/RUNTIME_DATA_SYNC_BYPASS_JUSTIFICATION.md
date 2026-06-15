# Runtime Data Sync — Bypass Justification

PR #1170 synchronizes runtime data views and purges stale signal artifacts.

## Scope

- data/data_center/**
- data/telegram_screener/**

## Gate behavior

The file-scope and no-lock-overlap gates are expected to fail because this PR touches a large number of runtime data files, not source code.

## Risk

No runtime code, service, registry, collector, or scheduling logic is intentionally modified.

## Rollback

Revert the merge commit or revert PR #1170.

## Merge decision

Bypass is acceptable only after confirming the changed files remain limited to data/runtime artifacts plus this justification document.
