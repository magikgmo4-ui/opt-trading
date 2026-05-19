# 20_POST_MERGE_REPRISE — GO child 1

## GO ID

`GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_POST_MERGE_REPRISE_01`

## Phase

Phase 8 — Reprise post-merge

## Objectif

Figer l'etat post-merge, creer un fichier de reprise independant, verifier `sot/mainline`, confirmer les modules presents, confirmer le produit utilisable depuis mainline.

## Actions attendues

1. Git precheck depuis `sot/mainline`.
2. Creer branche `go/GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_POST_MERGE_REPRISE_01`.
3. Verifier modules presents :
   - `modules/tradingview_observer/`
   - `modules/tradingview_observer_openclaw/`
4. Verifier gitignore `output/.gitignore` protege bien `*.json`.
5. Executer `product_sanity.ps1` (12/12 attendu).
6. Creer `docs/reprise/TV_OBSERVER_POST_MERGE_REPRISE.md`.
7. Commit + push.

## Invariants

- Ne pas rouvrir le parent ferme.
- Ne pas modifier admin-trading.
- Ne pas committer outputs live.

## Statut

PENDING
