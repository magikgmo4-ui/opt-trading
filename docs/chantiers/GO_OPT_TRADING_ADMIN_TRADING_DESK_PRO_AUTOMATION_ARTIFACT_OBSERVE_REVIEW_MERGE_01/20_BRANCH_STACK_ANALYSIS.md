---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01_20_BRANCH_STACK_ANALYSIS
doc_type: chantier/analysis
repo: opt-trading
machine: cursor-ai
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01
status: active
scope: doc-only
analyzed_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_REVIEW_MERGE_01/30_REVIEW_MERGE_PLAN.md
---

# 20_BRANCH_STACK_ANALYSIS

## Stack constatee

```text
6373d455  merge-base avec origin/sot/mainline
1a52bb0d  feat: add admin-trading desk pro dry-run artifact output
eadc6f57  docs: record admin-trading desk pro artifact observation
2908ff32  docs: record admin-trading desk pro artifact stability window
```

Branches correspondantes :

| Branche | Commit | Role |
| --- | --- | --- |
| `...ARTIFACT_OUTPUT_01` | `1a52bb0d` | implementation artifact writer + tests |
| `...ARTIFACT_OBSERVE_01` | `eadc6f57` | observation artefacts apres trigger |
| `...ARTIFACT_STABILITY_WINDOW_01` | `2908ff32` | observation stabilite supplementaire |

## Ecarts contre `origin/sot/mainline`

```text
OUTPUT_01            19 / 1
OBSERVE_01           19 / 2
STABILITY_WINDOW_01  19 / 3
```

Interpretation :

- `origin/sot/mainline` a avance de `19` commits depuis `6373d455`
- `STABILITY_WINDOW_01` contient `3` commits propres a merger
- ouvrir une PR depuis `OBSERVE_01` laisserait `2908ff32` hors PR

## Surface du diff depuis le merge-base

Diff du head complet `STABILITY_WINDOW_01` depuis `6373d455` :

```text
13 files changed, 624 insertions(+), 1 deletion(-)
```

Chemins concernes :

```text
M .gitignore
A docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01/90_CLOSEOUT.md
A docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01/00_START.md
A docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01/20_ARTIFACT_OUTPUT_SPEC.md
A docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01/30_IMPLEMENTATION_NOTES.md
A docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01/40_TEST_RESULTS.md
A docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01/50_TIMER_REVALIDATION.md
A docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01/60_GAPS_AND_NEXT_DECISION.md
A docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01/90_CLOSEOUT.md
A docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_STABILITY_WINDOW_01/90_CLOSEOUT.md
M modules/desk_pro/desk_pro_dry_run.sh
M modules/desk_pro/dry_run.py
A tests/test_desk_pro_artifact_output.py
```

## Conflit apparent

`git merge-tree` entre `origin/sot/mainline` et `origin/go/...ARTIFACT_STABILITY_WINDOW_01` n'a remonte aucun marqueur de conflit.

Conclusion :

- le risque de conflit Git apparent est faible
- le merge doit quand meme passer par une PR normale, car le diff contient du code dans `modules/desk_pro`

## Tests declares par la branche source

Le closeout `ARTIFACT_OUTPUT_01` declare :

```text
62 passed in 0.31s
```

Commande source :

```bash
PYTHONPATH=/opt/trading python -m pytest \
  tests/test_signal_event_adapter.py \
  tests/test_admin_trading_contract_compatibility_smoke.py \
  tests/test_desk_pro_dry_run.py \
  tests/test_desk_pro_artifact_output.py \
  -q
```

Ce GO n'a pas reexecute ces tests localement, car il est doc-only et ne merge pas encore la branche fonctionnelle.
