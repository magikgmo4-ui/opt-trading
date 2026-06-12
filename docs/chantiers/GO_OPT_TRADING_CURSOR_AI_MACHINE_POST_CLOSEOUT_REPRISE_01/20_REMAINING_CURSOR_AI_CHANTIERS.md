# 20_REMAINING_CURSOR_AI_CHANTIERS

## Chantiers cursor-ai restants

### Priorite 1 — Merge final TradingView MCP

Les branches `ALERT_WEBHOOK_TEMPLATE_01` et `PARENT_CLOSEOUT_01` doivent etre mergees dans sot/mainline pour completement absorber le parent cursor-ai.

### Priorite 2 — Live artifacts / Claude cowork

| Branche | GO propose |
|---|---|
| `go/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01` | `GO_OPT_TRADING_CURSOR_AI_CLAUDE_COWORK_LIVE_ARTIFACTS_REVIEW_01` |
| `go/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01` | (inclus dans le meme GO) |

But : reviser les artefacts live / cowork / IDE bundle cote cursor-ai : utile, a merger, reference, ou a supprimer.

### Priorite 3 — Nettoyage map cursor-ai

| GO propose | But |
|---|---|
| `GO_OPT_TRADING_CURSOR_AI_MACHINE_MAP_STALE_LINES_REVIEW_01` | Nettoyer ou annoter les entrees cursor-ai devenues historiques dans MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md |

### Priorite 4 — Reprise Bundles (optionnel)

| GO propose | But |
|---|---|
| `GO_OPT_TRADING_CURSOR_AI_BUNDLES_POST_MERGE_REPRISE_01` | Confirmer que Bundles est integre dans sot/mainline et documenter le point de reprise bundle |

## Hors scope cursor-ai

- ClickUp (fantome, hors lot actif)
- Admin-trading (bloc separe, a ne pas ouvrir maintenant)
- Student (machine separee)
- DB-layer (machine separee)
- Fantome (machine separee)

## RISKS

- À qualifier.
