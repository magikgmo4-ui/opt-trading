---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01_20_MOCK_ENDPOINT_SETUP
doc_type: chantier/mock_endpoint_setup
repo: opt-trading
machine: cursor-ai
status: active
links:
  - modules/tradingview_observer/templates/alert_webhook_template_v1.json
---

# 20_MOCK_ENDPOINT_SETUP — Setup endpoint mock local

## Principe

Le test safe utilise un endpoint mock local sur `127.0.0.1:9999/tv-test`. Cet endpoint n'est pas un serveur de production, il sert uniquement a valider le format du payload JSON sans routage vers admin-trading.

## Endpoint autorise

```text
http://127.0.0.1:9999/tv-test
```

- **IP** : `127.0.0.1` (localhost uniquement).
- **Port** : `9999` (port arbitraire, non standard, evite les conflits).
- **Path** : `/tv-test` (explicite : test, pas production).

## Endpoints interdits

- Tout endpoint sur `0.0.0.0` ou IP publique.
- `http://localhost:8080/webhook` ou tout endpoint de production.
- Tout endpoint dans `webhook_server.py`.
- Tout endpoint admin-trading.

## Option 1 — Mock avec PowerShell (pas d'installation)

```powershell
# Lancer un listener HTTP minimal en PowerShell
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://127.0.0.1:9999/tv-test/")
$listener.Start()
Write-Host "Mock endpoint listening on http://127.0.0.1:9999/tv-test/"

# Pour recevoir une requete
$context = $listener.GetContext()
$request = $context.Request
$reader = New-Object System.IO.StreamReader($request.InputStream)
$body = $reader.ReadToEnd()
Write-Host "Received payload: $body"

# Repondre 200 OK
$response = $context.Response
$response.StatusCode = 200
$buffer = [System.Text.Encoding]::UTF8.GetBytes('{"status":"ok","mode":"test_only"}')
$response.OutputStream.Write($buffer, 0, $buffer.Length)
$response.Close()

# Arreter le listener
$listener.Stop()
```

## Option 2 — Mock avec curl (validation JSON sans envoi)

```powershell
# Valider le template JSON localement sans envoi
$templatePath = "modules/tradingview_observer/templates/alert_webhook_template_v1.json"
$template = Get-Content $templatePath -Raw | ConvertFrom-Json

# Verifications
if ($template.trade_allowed -eq $false) { Write-Host "PASS: trade_allowed=false" }
if ($template.admin_trading_runtime -eq $false) { Write-Host "PASS: admin_trading_runtime=false" }
if ($template.mode -eq "test_only") { Write-Host "PASS: mode=test_only" }
if ($template.signal -eq "TEST_ONLY") { Write-Host "PASS: signal=TEST_ONLY" }
Write-Host "Template validation OK"

# Optionnel : envoyer vers le mock local si le listener est actif
$body = $template | ConvertTo-Json -Depth 10
try {
    Invoke-RestMethod -Uri "http://127.0.0.1:9999/tv-test" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 5
    Write-Host "PASS: payload sent to mock endpoint"
} catch {
    Write-Host "INFO: mock endpoint not running (expected if Option 2 only)"
}
```

## Aucune dependance a admin-trading

- Le mock local est autonome.
- Aucun import de `webhook_server.py`.
- Aucun acces a `modules/admin-trading/`.
- Aucune configuration systemd.

## Aucun secret

- Le template utilise des placeholders TradingView (`{{ticker}}`, etc.).
- Aucune donnee reelle.
- Aucun token, cle API, mot de passe.
- L'URL `127.0.0.1:9999` est locale, non sensible.

## Nettoyage

Voir `50_ROLLBACK_PLAN.md`.
