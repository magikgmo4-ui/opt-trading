# Implementation Spec

## Change
Add a small helper inside `gate/no-lock-overlap` to detect whether a competing GO has already been merged into `sot/mainline`.

## Detection Strategy
1. Check merge commits on `origin/sot/mainline` for the standard GitHub merge message ending in `go/<GO_ID>`.
2. If the remote branch still exists, also accept it as merged when the branch tip is an ancestor of `origin/sot/mainline`.

## Behavior
- Skip overlap checks for merged GO scopes.
- Keep overlap checks unchanged for active GO scopes.
