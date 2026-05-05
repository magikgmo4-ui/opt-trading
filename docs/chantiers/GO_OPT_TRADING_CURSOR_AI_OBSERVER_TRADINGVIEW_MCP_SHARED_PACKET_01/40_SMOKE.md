# 40_SMOKE — Smoke local shared packet

## Contexte

Smoke leger execute depuis `sot/mainline` apres creation du script `export_shared_packet.ps1`.

## Resultats attendus

| Check | Attendu | Obtenu |
|-------|---------|--------|
| Bridge packet existe | PASS (genere si absent) | |
| Dry-run affiche actions | PASS | |
| Export vers staging | PASS | |
| Fichier horodate cree | PASS | |
| `latest_bridge_packet.json` copie | PASS | |
| Dossier staging ignore par git | PASS | |

## Smoke reel

```powershell
cd C:\Users\ghost\opt-trading\modules\tradingview_observer

.\export_shared_packet.ps1 -DryRun

.\export_shared_packet.ps1

Test-Path C:\Users\ghost\opt-trading\_shared_packets\tradingview_observer\*\latest_bridge_packet.json
```

## Verdict

- Si tout PASS : `SMOKE_PASS`
- Si dry-run OK mais export reel impossible (permissions) : `PARTIAL_ENV`
