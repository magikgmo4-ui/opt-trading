---
doc_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01_WRAPPERS_AUDIT
doc_type: audit_matrix
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
status: pass
mode: doc-only
surface: wrappers
source_kind: repo_read
machine_owner: db-layer
---

# 20_WRAPPERS_AUDIT

## Wrapper matrix

| Wrapper publisher | Published aliases | Current target | Status |
| --- | --- | --- | --- |
| `modules/reseau_ssh/scripts/install_canonical_shortcuts.sh` | `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` | `modules/reseau_ssh/scripts/*` | `CANONICAL_ACTIVE` |
| `modules/reseau_ssh/scripts/install_shortcuts.sh` | `menu-reseau_ssh_step2`, `cmd-reseau_ssh_step2`, `sanity-reseau_ssh_step2` | `modules/reseau_ssh/scripts/*` | `COMPAT_ACTIVE` |
| nested `reseau_ssh_step2/scripts/install_shortcuts_linux.sh` | `menu-reseau_ssh_step2`, `cmd-reseau_ssh_step2`, `sanity-reseau_ssh_step2` | nested `reseau_ssh_step2/scripts/*` | `COMPAT_DUPLICATE_INSTALLER` |
| `modules/reseau_ssh_step1b/scripts/install_shortcuts.sh` | `menu-reseau_ssh_step1b`, `cmd-reseau_ssh_step1b`, `sanity-reseau_ssh_step1b` | `modules/reseau_ssh_step1b/scripts/*` | `STEP1B_COMPAT_ACTIVE` |
| `scripts/reseau_ssh/install_reseau_ssh.sh` | `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh` | delegates to canonical installer when present, otherwise legacy `scripts/reseau_ssh/*` | `LEGACY_DELEGATING_INSTALLER` |

## Registry alignment

Registry proof found:

- `registry/modules_registry.yaml` mentions `reseau_ssh`
- `13_MODULES_NORMALIZED_REGISTRY_CROSSCHECK.csv` shows `reseau_ssh = yes`, `reseau_ssh_step1b = no`
- `registry/wrappers_registry.yaml` contains:
  - `cmd-reseau_ssh`
  - `menu-reseau_ssh`
  - `sanity-reseau_ssh`
  - `cmd-reseau_ssh_step2`
  - `menu-reseau_ssh_step2`
  - `sanity-reseau_ssh_step2`

No wrapper registry proof was found in this GO for `*_step1b` aliases.

## External wrapper conclusions

- short aliases are canonically owned by `modules/reseau_ssh`
- suffixed step2 aliases are still explicitly tolerated as transition wrappers
- step1b still owns only its own suffixed wrapper family
- legacy `install_reseau_ssh.sh` is no longer the desired publisher, but it is still a safe compat entry because it delegates to the canonical installer first

## Compatibility decision input

Keep temporarily:

- `menu/cmd/sanity-reseau_ssh`
- `menu/cmd/sanity-reseau_ssh_step2`
- `menu/cmd/sanity-reseau_ssh_step1b`
- `scripts/reseau_ssh/install_reseau_ssh.sh`

Do not promote:

- nested step2 installer as the primary publisher
- step1b installers as canonical family publishers
- legacy `scripts/reseau_ssh` as canonical module surface

## Verdict

`PASS`
