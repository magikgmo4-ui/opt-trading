# GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_MERGED_SCOPE_BYPASS_01

## Goal
Prevent `gate/no-lock-overlap` from blocking new PRs on `FILE_SCOPE` entries owned by GOs already merged into `sot/mainline`.

## Problem
The current gate scans all `FILE_SCOPE.txt` files, including merged historical GOs. That creates false-positive lock conflicts for follow-up workstreams.

## Scope
- `.github/workflows/gated-pr.yml`
- this chantier documentation
- bundle metadata for the GO

## Expected Result
Only active, non-merged GO scopes can block a PR in `gate/no-lock-overlap`.
