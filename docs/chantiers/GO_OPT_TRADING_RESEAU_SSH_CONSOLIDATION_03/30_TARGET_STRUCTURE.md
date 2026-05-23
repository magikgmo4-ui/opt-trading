---
doc_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01_TARGET_STRUCTURE
doc_type: target_structure
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01
status: pass
mode: doc-only
surface: modules
source_kind: canonical_decision
machine_owner: db-layer
---

# 30_TARGET_STRUCTURE

## Target

One top-level canonical SSH family module, with explicit internal implementation and temporary prerequisite compatibility.

## Proposed structure

```text
modules/
  reseau_ssh/                           <- unique canonical top-level SSH family module
    README.md
    scripts/                            <- operator facade + canonical short aliases
    modules/
      reseau_ssh/
        reseau_ssh_step2/               <- active internal WireGuard/firewall implementation

  reseau_ssh_step1b/                    <- transitional prerequisite module
    README.md
    scripts/
    modules/
      reseau_ssh/
        reseau_ssh_step1b/

scripts/
  reseau_ssh/                           <- legacy rollback / transition backend only
```

## Role split

| Path | Target role |
| --- | --- |
| `modules/reseau_ssh` | canonical family facade |
| nested `reseau_ssh_step2` | internal active implementation |
| `modules/reseau_ssh_step1b` | temporary prerequisite for baseline SSH preparation |
| `scripts/reseau_ssh` | rollback and explicit legacy transition only |

## Why this structure

- it matches the current proven command dispatch in `modules/reseau_ssh/scripts/cmd.sh`
- it respects the current registry state where `reseau_ssh` is the recognized module
- it avoids prematurely flattening `step2` or deleting `step1b`
- it preserves current operator continuity on short aliases

## Not allowed in this GO

- no top-level resurrection of `reseau_ssh_step2` as a standalone module
- no deletion of `modules/reseau_ssh_step1b`
- no archive move of `scripts/reseau_ssh`
- no registry rewrite

## Physical follow-up expected later

If a later GO proves wrappers and callers safe enough, the next physical lot may:

1. reduce duplicate step2 installers
2. tighten the legacy `scripts/reseau_ssh` role
3. optionally absorb or retire `step1b` commands after caller retirement proof

## Verdict

`PASS`
