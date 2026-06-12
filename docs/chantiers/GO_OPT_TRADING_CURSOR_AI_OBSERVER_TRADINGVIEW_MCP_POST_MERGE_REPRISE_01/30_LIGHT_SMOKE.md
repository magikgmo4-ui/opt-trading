# 30_LIGHT_SMOKE — Smoke leger post-merge

## Contexte

Smoke leger execute depuis `sot/mainline` apres merge PR #200.

## Resultats attendus

| Check | Attendu | Obtenu |
|-------|---------|--------|
| `sanity_check.ps1` | 9/9 PASS si TV Desktop ouvert, ou CDP check FAIL si TV ferme | |
| `cmd.ps1 -Snapshot` | 5/5 JSON exportes si TV ouvert | |
| `product_sanity.ps1` | Au moins checks 1-4, 9-12 toujours PASS ; 5-8 dependent du runtime TV | |
| OpenClaw `run.ps1 sanity` | 9/9 PASS si TV ouvert | |
| Git: live JSON non trackes | 0 fichiers | |
| Admin-trading inchange | Aucun fichier admin-trading, webhook, systemd modifie | |

## Smoke reel

```powershell
cd C:\Users\ghost\opt-trading\modules\tradingview_observer

.\sanity_check.ps1
# Si CDP FAIL : PARTIAL_ENV (TV Desktop non ouvert) — ce n'est pas un FAIL produit.
# Si CDP PASS : continuer.

.\cmd.ps1 -Snapshot

.\product_sanity.ps1

cd C:\Users\ghost\opt-trading\modules\tradingview_observer_openclaw

.\run.ps1 sanity
```

## Verdict

- Si CDP ouvert et tout PASS : `LIGHT_SMOKE_PASS`
- Si CDP ferme mais checks hors TV PASS : `PARTIAL_ENV` (TradingView Desktop non ouvert, produit OK)
- Si checks hors TV FAIL : `FAIL` (produit corrompu ou incomplet)

## RISKS

- À qualifier.
