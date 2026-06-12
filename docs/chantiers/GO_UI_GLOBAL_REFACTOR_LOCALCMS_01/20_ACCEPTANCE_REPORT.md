# GO UI GLOBAL REFACTOR LOCALCMS 01 — Acceptance Report

## Batch A — Shared Helpers + Design System

### Files created

| File | Lines | Description |
|------|-------|-------------|
| `shared/html_helpers.py` | 197 | Reusable HTML generation functions (badge, card, table, page_shell, sidebar_nav, etc.) |
| `shared/html_design_system.py` | 134 | CSS constants, palette, standard CSS blocks (LIGHT_CSS, BADGE_CSS, TABLE_CSS, etc.) |
| `docs/chantiers/GO_UI_GLOBAL_REFACTOR_LOCALCMS_01/00_INITIAL_PROJECT_DOC.md` | — | Full 5-phase refactor plan with inventory |

### Files modified

**None.** This is a strictly additive patch. No existing file was modified.

### Verdict

**PASS** — Batch A is safe to merge.

### Verification

```bash
python3 -c "from shared.html_helpers import badge, card, table; print(badge('OK', 'up'))"
# => <span class="badge-up">OK</span>

python3 -c "from shared.html_design_system import LIGHT_CSS; print(len(LIGHT_CSS))"
# => 1084

python3 -c "from shared.html_helpers import *; from shared.html_design_system import *; print('ALL_IMPORTS_OK')"
# => ALL_IMPORTS_OK
```

### Test commands

```bash
python3 -m pytest tests/ -x -q
./scripts/verify_all.sh
grep -rn "response_class=HTMLResponse" --include="*.py" | grep -v __pycache__ | wc -l
```

### Rollback

```bash
git checkout shared/html_helpers.py shared/html_design_system.py
# ou: rm shared/html_helpers.py shared/html_design_system.py
```
