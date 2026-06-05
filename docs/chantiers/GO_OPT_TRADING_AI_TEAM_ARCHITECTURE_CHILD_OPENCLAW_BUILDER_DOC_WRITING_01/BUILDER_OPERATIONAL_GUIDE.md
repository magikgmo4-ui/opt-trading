# BUILDER_OPERATIONAL_GUIDE

## Purpose

This guide defines how to use the OpenClaw builder for controlled documentation-oriented jobs.

## Allowed use

```text
ALLOWED:
- dry-run documentation planning
- structured response generation
- child GO documentation support
- gate-based execution
- execution log production
- closeout support
```

## Forbidden use

```text
FORBIDDEN:
- SSH execution
- runtime patching
- global index modification
- pushing branches without closeout
- gateway token repair inside documentation jobs
- hidden mutation
```

## Operator sequence

```text
1. Start from sot/mainline clean.
2. Open a dedicated child branch.
3. Create 00_INITIAL_PROJECT_DOC.md.
4. Create a gate document.
5. Pass the gate explicitly.
6. Invoke builder only inside the allowed scope.
7. Log the builder response.
8. Verify mutation=false and ssh=false where applicable.
9. Close the child with 90_CHILD_CLOSEOUT.md.
10. Push branch and open PR.
```

## Minimum precheck

```bash
git fetch --all --prune
git switch sot/mainline
git pull --rebase
test -z "$(git status --short)"
```

## Required artifacts

```text
00_INITIAL_PROJECT_DOC.md
01_*_GATE.md or 01_*_MATRIX.md
02_*_EXECUTION_LOG.md or 02_*_DECISION.md
90_CHILD_CLOSEOUT.md
```

## Warning

A previous direct gateway call produced a `gateway token mismatch`. This guide does not resolve that issue. It documents the controlled usage boundary only.

## RISKS

- À qualifier.
