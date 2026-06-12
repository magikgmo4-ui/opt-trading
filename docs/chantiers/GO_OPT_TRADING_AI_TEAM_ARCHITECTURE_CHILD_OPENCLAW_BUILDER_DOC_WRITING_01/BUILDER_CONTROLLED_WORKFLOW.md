# BUILDER_CONTROLLED_WORKFLOW

## Workflow goal

Standardize how a builder child GO moves from intention to closeout without uncontrolled mutation.

## Workflow

```text
START
  -> verify sot/mainline clean
  -> create child branch
  -> create child GO directory
  -> write 00_INITIAL_PROJECT_DOC.md
  -> write gate or review matrix
  -> pass gate / decision
  -> execute allowed builder task or documentary review
  -> write execution log / decision
  -> verify invariants
  -> write closeout
  -> push branch
  -> open PR
  -> merge to sot/mainline
END
```

## Gate rules

A gate must make explicit:

```text
MODE
MUTATION_ALLOWED
SSH_ALLOWED
RUNTIME_PATCH_ALLOWED
INDEX_GLOBAL_ALLOWED
PASS_CRITERIA
FAIL_CRITERIA
```

## Execution log rules

An execution log must include:

```text
context
request
response
verification
verdict
warnings
next step
```

## Closeout rules

A closeout must include:

```text
CHILD_STATUS
artifacts
commits
established results
warnings
invariants
NEXT_GO
RESUME_POINT
```

## Stop conditions

```text
STOP_IF:
- working tree dirty before execution
- wrong branch
- missing gate
- SSH requested
- runtime patch requested
- global index modification requested
- builder response is unstructured when structure was required
```

## RISKS

- À qualifier.
