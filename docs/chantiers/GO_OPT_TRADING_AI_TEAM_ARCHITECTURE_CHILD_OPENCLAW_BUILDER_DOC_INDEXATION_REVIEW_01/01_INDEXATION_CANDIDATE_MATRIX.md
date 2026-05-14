# 01_INDEXATION_CANDIDATE_MATRIX

## Source

```text
SOURCE_CHAIN = BUILDER_DOCUMENTATION_CHAIN
SOURCE_STATUS = COMPLETE_MERGED_PASS
SOURCE_ADOPTION = DOC_PACK_ADOPTED_LOCAL
```

## Candidate surfaces

| Surface            | Candidate action        | Decision | Reason                                             | Risk                                  |
| ------------------ | ----------------------- | -------- | -------------------------------------------------- | ------------------------------------- |
| Local child folder | Keep as local reference | PENDING  | Already valid and traceable                        | Low                                   |
| docs/index/inbox   | Add short pointer later | PENDING  | Could improve discoverability                      | Must not create duplicate authority   |
| GO_INDEX           | Global index entry      | PENDING  | May be useful if builder docs become canonical     | High; global index mutation           |
| ACTIVE_STREAMS     | Active stream entry     | PENDING  | Probably not needed after chain close              | Could falsely reopen closed stream    |
| NEXT_GO            | Next GO candidate       | PENDING  | Only if indexation action is approved              | Could create unnecessary continuation |
| REPRISE            | Restart pointer         | PENDING  | Only if adoption becomes canonical restart surface | Could pollute global restart state    |
| BRANCH_STATE       | Branch state update     | PENDING  | Usually unnecessary after merge                    | Could duplicate PR/merge history      |

## Review criteria

```text
DISCOVERABILITY = improves future reuse
AUTHORITY_CLARITY = does not create false global authority
NON_DUPLICATION = does not duplicate closed child artifacts
LOW_MUTATION = avoids broad global edits
NECESSITY = required, not decorative
```

## Initial verdict

```text
INDEXATION_REVIEW_STATUS = IN_PROGRESS
FINAL_DECISION = PENDING
```
