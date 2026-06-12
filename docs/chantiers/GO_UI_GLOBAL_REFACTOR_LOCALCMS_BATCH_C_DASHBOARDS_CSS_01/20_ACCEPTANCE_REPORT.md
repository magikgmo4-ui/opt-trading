# GO UI GLOBAL REFACTOR LOCALCMS BATCH C — Acceptance Report

## Batch C — Central UI + Metrics + SpaceX CSS blocks → STANDARD_CSS

### Fichiers modifies

| Fichier | Change | Details |
|---------|--------|---------|
| `modules/localcms/app/main.py` | CSS inline → STANDARD_CSS | 3 pages: `ui_index()`, `_metrics_html()`, `_spacex_html()` |
| `shared/html_design_system.py` | +classes | `.card-row`, `.card-pass/fail/blue/win/loss/neutral`, `.info-grid/info-card`, `.summary-card .bar` |

### Pages migrees

| Page | Ancien CSS (lignes) | Nouveau | Surcharge page |
|------|---------------------|---------|----------------|
| Central UI | 57 lignes | `{STANDARD_CSS}` | Aucune |
| Metrics | 37 lignes | `{STANDARD_CSS}` + 1 regle | `.card-row > .card { flex: 1; ... }` |
| SpaceX | 30 lignes | `{STANDARD_CSS}` + 3 regles | `.num 24px`, `table margin`, `th,td padding 8px` |

### Standard CSS couvre maintenant

- Layout : sidebar, nav, main (LIGHT_CSS)
- Badges : 16 variants (BADGE_CSS)
- Cards : summary-card, domain-card, kpi (CARD_CSS)
- Tables : standard + hover + links (TABLE_CSS)
- Misc : notice, links-bar, code-block, info-grid, info-card, card-row, card-pass/fail/win/loss/blue/neutral, auto-refresh (MISC_CSS)

### Reduction CSS inline

| Bloc | Avant | Apres |
|------|-------|-------|
| Central UI CSS | 57 lignes | 3 lignes |
| Metrics CSS | 37 lignes | 4 lignes |
| SpaceX CSS | 30 lignes | 5 lignes |
| **Total** | **124 lignes** | **12 lignes** |

### Tests

```bash
pytest tests/ -q -k "localcms or journal or metrics or spacex or ui or html"
# 685 passed, 8 failed (pre-existing, unchanged)

pytest tests/ -q
# 2117 passed, 18 failed (pre-existing, unchanged)
```

### Verdict

**PASS** — Batch C is safe to merge.

### Rollback

```bash
git checkout modules/localcms/app/main.py shared/html_design_system.py
# ou: git revert HEAD
```

### Prochaine etape

**Batch D** — migrer CSS blocks restants (Credentials, Journal, Journal Detail) + migrer Desk Pro, perf_app, webhook_server.
