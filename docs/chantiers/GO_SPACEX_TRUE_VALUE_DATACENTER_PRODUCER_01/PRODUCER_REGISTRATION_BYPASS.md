# Producer Registration Bypass — Justification

## Conflict

`no-lock-overlap` gate fails because files under `data/data_center/_registry/` and `data/data_center/_contracts/` are claimed by `GO_DATA_CENTER_GRADE_A_TO_GRADE_AA_01` (which uses `data/data_center/**` in its FILE_SCOPE).

## Why acceptable

- This GO adds a new producer entry, which necessarily touches the shared registry file
- `GO_DATA_CENTER_GRADE_A_TO_GRADE_AA_01` was a runtime data sync — its scope was deliberately broad
- The overlap is at the registry/contracts level only, not on runtime data views
- Future GOs should narrow `GO_DATA_CENTER_GRADE_A_TO_GRADE_AA_01`'s scope to exclude `_registry/**` and `_contracts/**`

## Merge decision

Admin bypass acceptable — both GOs legitimately need access to `data/data_center/` for different subdirectories.
