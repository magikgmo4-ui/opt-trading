# GO UI GLOBAL REFACTOR LOCALCMS BATCH B — Acceptance Report

## Batch B — Credentials + Journal badge migration

### Files modified

| File | Change | Lines |
|------|--------|-------|
| `modules/localcms/app/main.py` | Replaced 4 badge helpers with shared OT-Core delegates | -38 +4 |
| `shared/html_helpers.py` | Fixed CSS class output (base `.badge` class + `cred-*` self-contained + `badge-unknown` fallback + unicode symbols) | -2 +6 |

### What changed

1. **`_pnl_badge()`** → delegates to `pnl_badge()` from shared helpers
2. **`_verdict_badge()`** → delegates to `verdict_badge()`
3. **`_closeout_badge()`** → delegates to `closeout_badge()`
4. **`_cred_status_badge()`** → delegates to `cred_status_badge()`

### What did NOT change

- Zero CSS inline blocks changed
- Zero HTML structure changed
- Zero sidebar / layout / table markup changed
- Zero JSON API routes changed
- Zero data displayed altered

### Fixes applied during Batch B

- **Bug in `badge()`**: was missing `.badge` base class — badges would have rendered without `display:inline-block;padding;border-radius` CSS. Fixed by adding base class for all non-cred variants.
- **Missing unicode**: `closeout_badge()` was missing `✓` and `⚠` symbols. Fixed.
- **Wrong fallback class**: `pnl_badge()` and `verdict_badge()` used `badge-neutral` instead of `badge-unknown`. Fixed.
- **Removed pill variants**: `pill_ok`, `pill_warn`, `pill_danger` removed from `badge()` — they belong in a separate function.

### HTML output verification

All 11 badge variants produce output **strictly identical** to the original inline code:
- `pnl_badge('win')` = `<span class="badge badge-up">WIN</span>` (match)
- `pnl_badge('loss')` = `<span class="badge badge-down">LOSS</span>` (match)
- `pnl_badge('breakeven')` = `<span class="badge badge-minimal">BREAKEVEN</span>` (match)
- `verdict_badge('APPROVED')` = `<span class="badge badge-up">APPROVED</span>` (match)
- `verdict_badge('REJECTED')` = `<span class="badge badge-down">REJECTED</span>` (match)
- `closeout_badge(True)` = `<span class="badge badge-up">✓ CLOSED</span>` (match)
- `closeout_badge(False)` = `<span class="badge badge-down">⚠ PENDING</span>` (match)
- `cred_status_badge('SET')` = `<span class="cred-set">SET</span>` (match)
- `cred_status_badge('ABSENT')` = `<span class="cred-absent">ABSENT</span>` (match)
- `cred_status_badge('FUTURE')` = `<span class="cred-future">FUTURE</span>` (match)
- `cred_status_badge('UNKNOWN')` = `<span class="cred-unknown">UNKNOWN</span>` (match)
- `STATUS_BADGES['operational']` = `<span class="badge badge-operational">operational</span>` (match)

### Tests

```bash
pytest tests/ -q -k "journal or credentials or badge"
# 69 passed, 1 skipped
```

```bash
pytest tests/ -q
# 2117 passed, 18 failed (pre-existing, unchanged)
```

### Verdict

**PASS** — Batch B is safe to merge.

### Rollback

```bash
git checkout modules/localcms/app/main.py shared/html_helpers.py
# ou: git revert HEAD~1
```

### Prochaine etape

**Batch C** — remplacer les blocs CSS inline dans Central UI + Metrics + SpaceX avec `STANDARD_CSS`.
