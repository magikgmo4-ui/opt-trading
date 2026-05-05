# 40_SMOKE — Smoke statique template

## Contexte

Smoke statique uniquement — pas de creation d'alerte reelle.

## Verifications

| Check | Resultat |
|-------|----------|
| Template JSON valide | PASS |
| Champs documents | PASS |
| Producer de test documente | PASS |
| Regles de securite specifiees | PASS |
| Aucun admin-trading reference | PASS |
| Aucun live JSON tracke | PASS |

## Validation statique

```powershell
cd C:\Users\ghost\opt-trading\modules\tradingview_observer

# Valider le JSON
Get-Content templates\alert_webhook_template_v1.json | ConvertFrom-Json | Out-Null
Write-Host "Template JSON valid"
```

## Verdict

`SMOKE_STATIC_PASS` — le template est valide statiquement. Le test dynamique (creation d'alerte reelle) necessite `-AllowMutation` et un receiver local, ce qui est hors scope de ce smoke.
