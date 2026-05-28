# Implementation Spec

## Change
Add a small helper inside `gate/no-lock-overlap` to detect whether a competing GO is inactive.

## Detection Strategy
1. Check merge commits on `origin/sot/mainline` for the standard GitHub merge message ending in `go/<GO_ID>`.
2. If the remote branch no longer exists, treat the GO as retired/inactive.
3. If the remote branch still exists, also accept it as inactive when the branch tip is an ancestor of `origin/sot/mainline`.

## Behavior
- Skip overlap checks for inactive GO scopes.
- Keep overlap checks unchanged for active GO scopes.
