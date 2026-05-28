# Test Plan

1. Run `git diff --check`.
2. Open PR from this branch and confirm gated workflow executes.
3. Verify `gate/no-lock-overlap` still passes for normal cases.
4. Verify a follow-up GO can touch files previously claimed only by a merged or retired GO without a false overlap failure.
