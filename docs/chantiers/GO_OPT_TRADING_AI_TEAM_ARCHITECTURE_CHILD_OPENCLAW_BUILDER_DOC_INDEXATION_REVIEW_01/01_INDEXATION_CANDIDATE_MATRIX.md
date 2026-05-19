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
| Local child folder | Keep as local reference | KEEP_AS_SOURCE_OF_RECORD     | Already valid and traceable                        | Low                                             |
| docs/index/inbox   | Add short pointer later | OPTIONAL_POINTER_RECOMMENDED | Could improve discoverability                      | Must remain separate and lightweight            |
| GO_INDEX           | Global index entry      | NO_ACTION                    | Not required for local adoption                    | High; global index mutation                     |
| ACTIVE_STREAMS     | Active stream entry     | NO_ACTION                    | Chain is closed                                    | Could falsely reopen closed stream              |
| NEXT_GO            | Next GO candidate       | NO_ACTION_IN_THIS_CHILD      | Optional pointer GO can be opened manually         | Could create unnecessary continuation           |
| REPRISE            | Restart pointer         | NO_ACTION                    | Not a canonical restart surface                    | Could pollute global restart state              |
| BRANCH_STATE       | Branch state update     | NO_ACTION                    | Merge history is sufficient                        | Could duplicate PR/merge history                |

## Review criteria

```text
DISCOVERABILITY = improves future reuse
AUTHORITY_CLARITY = does not create false global authority
NON_DUPLICATION = does not duplicate closed child artifacts
LOW_MUTATION = avoids broad global edits
NECESSITY = required, not decorative
```

## Final verdict

```text
INDEXATION_REVIEW_STATUS = PASS
FINAL_DECISION = LOCAL_REFERENCE_ONLY_WITH_OPTIONAL_INBOX_POINTER_RECOMMENDED
```
