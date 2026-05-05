---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01_30_TEST_PROCEDURE
doc_type: chantier/test_procedure
repo: opt-trading
machine: cursor-ai
status: active
links:
  - modules/tradingview_observer/templates/alert_webhook_template_v1.json
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEMPLATE_01/30_TEST_PROCEDURE.md
---

# 30_TEST_PROCEDURE — Procedure de test safe

## Mode de test

Ce GO documente la procedure de test safe. Le test lui-meme est manuel (pas d'execution automatique). L'operateur execute les etapes dans son environnement local.

## Niveaux de test

### Niveau 1 — Validation JSON sans envoi (Option B)

Test sans endpoint, validation du template uniquement.

**Etapes** :

```powershell
# 1. Charger le template
$templatePath = "modules/tradingview_observer/templates/alert_webhook_template_v1.json"
$template = Get-Content $templatePath -Raw | ConvertFrom-Json

# 2. Verifier le schema
if ($template.schema -ne "opt_trading_tradingview_alert_template_v1") {
    Write-Host "FAIL: schema mismatch"
} else {
    Write-Host "PASS: schema=$($template.schema)"
}

# 3. Verifier les flags securite
@(
    @{Name="trade_allowed"; Expected=$false; Actual=$template.trade_allowed},
    @{Name="admin_trading_runtime"; Expected=$false; Actual=$template.admin_trading_runtime},
    @{Name="mode"; Expected="test_only"; Actual=$template.mode},
    @{Name="signal"; Expected="TEST_ONLY"; Actual=$template.signal}
) | ForEach-Object {
    if ($_.Actual -eq $_.Expected) {
        Write-Host "PASS: $($_.Name)=$($_.Actual)"
    } else {
        Write-Host "FAIL: $($_.Name) expected=$($_.Expected) actual=$($_.Actual)"
    }
}

# 4. Verifier les placeholders TradingView
$json = Get-Content $templatePath -Raw
@("{{ticker}}", "{{exchange}}", "{{interval}}", "{{close}}", "{{volume}}", "{{time}}") | ForEach-Object {
    if ($json -match [regex]::Escape($_)) {
        Write-Host "PASS: placeholder $_ present"
    } else {
        Write-Host "FAIL: placeholder $_ missing"
    }
}

Write-Host "Niveau 1 termine"
```

### Niveau 2 — Test avec mock local (Option A)

Test avec endpoint mock local `127.0.0.1:9999`.

**Etapes** :

```powershell
# 1. Lancer le listener mock (dans un terminal separe)
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://127.0.0.1:9999/tv-test/")
$listener.Start()
Write-Host "Mock listening on http://127.0.0.1:9999/tv-test/ — attente de requete..."

# 2. Dans un autre terminal, envoyer le payload
$template = Get-Content "modules/tradingview_observer/templates/alert_webhook_template_v1.json" -Raw | ConvertFrom-Json
# Remplacer les placeholders par des valeurs test
$template.ticker = "TEST_TICKER"
$template.exchange = "TEST_EXCHANGE"
$template.price = "100.00"
$template.volume = "1000"
$template.time = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")

$body = $template | ConvertTo-Json -Depth 10
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:9999/tv-test" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 5
    Write-Host "PASS: mock responded: $($response | ConvertTo-Json)"
} catch {
    Write-Host "FAIL: $($_.Exception.Message)"
}

# 3. Verifier que le mock a recu le payload (terminal 1)
# Le listener affiche "Received payload: ..."
# Verifier que trade_allowed=false est present dans le payload recu

# 4. Arreter le listener (terminal 1)
$listener.Stop()
Write-Host "Mock stopped"
```

### Niveau 3 — Validation de non-regression admin-trading

Verifier qu'aucun fichier admin-trading n'est touche.

```bash
# Aucun fichier hors docs/ bundles/
git diff --name-only | grep -vE "^(docs/|bundles/)"

# Aucun secret
git diff | grep -iE "(password|secret|token|key=|api_key|\.env)"

# Aucun endpoint de production
git diff | grep -iE "https?://" | grep -v "127.0.0.1" | grep -v "localhost"
```

## Criteres PASS/FAIL

### Niveau 1

- **PASS** : tous les checks schema, flags, placeholders sont PASS.
- **FAIL** : un check echoue → corriger le template avant de continuer.

### Niveau 2

- **PASS** : le mock recoit le payload, repond 200, `trade_allowed=false` est confirme.
- **FAIL** : le mock ne recoit rien, ou le payload contient `trade_allowed=true`.

### Niveau 3

- **PASS** : aucun fichier hors docs/bundles, aucun secret, aucun endpoint production.
- **FAIL** : un fichier non-doc est detecte ou un secret est present → revert.

## Ce que ce test ne fait pas

- Ne teste pas un endpoint de production.
- Ne declenche pas d'alerte TradingView reelle.
- Ne connecte pas admin-trading.
- Ne modifie pas `webhook_server.py`.
- Ne cree pas de service systemd.
