# DeepSeek Student Backend Audit

This note captures what can likely be reduced later inside `/opt/trading/student/scripts/deepseek_student/` now that `wrappers/` is the official `deepseek_student` facade.

## Current Intended Split

- official operator facade:
  - `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh`
  - `/opt/trading/student/scripts/wrappers/deepseek_student_menu.sh`
  - `/opt/trading/student/scripts/wrappers/deepseek_student_sanity_check.sh`
- backend/helper scope:
  - `/opt/trading/student/scripts/deepseek_student/cmd.sh`
  - `/opt/trading/student/scripts/deepseek_student/deepseek_student_cmd.sh`
  - `/opt/trading/student/scripts/deepseek_student/menu.sh`
  - `/opt/trading/student/scripts/deepseek_student/sanity_check.sh`

## Keep For Now

- `/opt/trading/student/scripts/deepseek_student/cmd.sh`
  - currently used by `deepseek_hub_cmd.sh` for canonical `roadmap` backend dispatch
- `/opt/trading/student/scripts/deepseek_student/deepseek_student_cmd.sh`
  - still carries focused backend actions: `sanity`, `pull`, `test`, `roadmap`

## Likely Deprecation Candidates

- `/opt/trading/student/scripts/deepseek_student/menu.sh`
  - low-value generic module wrapper menu
  - not the preferred operator entrypoint anymore
- `/opt/trading/student/scripts/deepseek_student/sanity_check.sh`
  - still wired for alias installation, but no longer the preferred exposed sanity command

## Possible Future Simplifications

1. keep `cmd.sh` as a thin backend dispatch only
2. stop exposing `menu.sh` and `sanity_check.sh` via global shortcuts outside migration needs
3. document `deepseek_student/deepseek_student_cmd.sh` as internal helper scope
4. later, fold backend-only functions into a smaller internal layer if no direct callers remain

## Removal Rule

Do not delete backend files until all of the following are true:

- no global shortcut points to them
- no hub command calls them directly except through approved backend dispatch
- no docs recommend them as operator entrypoints
- runtime checks still pass after a staged test
