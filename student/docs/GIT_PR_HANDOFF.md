# Git / PR Handoff

GitHub push and PR creation could not be completed from this machine because HTTPS authentication is not configured and `gh` is not installed.

## Current Branch

- branch: `student`

## Commits Prepared On `student`

- `9573419` `student: add pull request summary variants`
- `821f15a` `student: refresh canonical references and command ownership`
- `9d56f42` `student: rewire wrappers and canonical shortcut installs`
- `96489f6` `student: add migration and duplicate cleanup guides`
- `e7a5482` `student: consolidate canonical workspace and planning docs`

## Push Command

```bash
cd /opt/trading
git push -u origin student
```

## Suggested Pull Request Base

- base: `sot/mainline`
- head: `student`

## Suggested PR Body Sources

- full: `/opt/trading/student/docs/PR_STUDENT_CONSOLIDATION.md`
- short: `/opt/trading/student/docs/PR_STUDENT_CONSOLIDATION_SHORT.md`
- manager: `/opt/trading/student/docs/PR_STUDENT_CONSOLIDATION_MANAGER.md`

## Example With GitHub CLI

```bash
gh pr create --base sot/mainline --head student --title "student: consolidate canonical workspace" --body-file /opt/trading/student/docs/PR_STUDENT_CONSOLIDATION.md
```
