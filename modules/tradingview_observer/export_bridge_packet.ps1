# TradingView Observer > Bridge Packet V1
# Dry-run only. No transfer, no SSH, no admin-trading mutation.
# Reads output/latest_report.json, produces output/latest_bridge_packet.json.
# Usage: .\export_bridge_packet.ps1 [-Json]
param([switch]$Json)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$MOD = $PSScriptRoot
$OUTPUT_DIR = Join-Path $MOD "output"
$REPORT_PATH = Join-Path $OUTPUT_DIR "latest_report.json"
$BRIDGE_PATH = Join-Path $OUTPUT_DIR "latest_bridge_packet.json"

if (-not (Test-Path $REPORT_PATH)) {
    Write-Error "latest_report.json not found at $REPORT_PATH — run observer export first."
    exit 1
}

try {
    $report = Get-Content $REPORT_PATH -Raw -Encoding UTF8 | ConvertFrom-Json
} catch {
    Write-Error "Failed to parse latest_report.json: $_"
    exit 1
}

$status = $report.status
$state  = $report.state
$quote  = $report.quote
$alerts = $report.alert_inventory
$values = $report.values

$now = (Get-Date).ToString("o")

# Alert summary
$alertTotal = 0
$alertActive = 0
$alertExpired = 0
$alertUnknown = 0

if ($alerts.PSObject.Properties['alert_count']) {
    $alertTotal = [int]$alerts.alert_count
}
if ($alerts.PSObject.Properties['alerts']) {
    foreach ($a in $alerts.alerts) {
        if ($a.PSObject.Properties['active']) {
            if ($a.active -eq $true) { $alertActive++ } else { $alertExpired++ }
        } else {
            $alertUnknown++
        }
    }
}

# Quote summary (no raw OHLC — synthèse seulement)
$quoteSummary = @{}
if ($quote.PSObject.Properties['symbol'])   { $quoteSummary['symbol'] = $quote.symbol }
if ($quote.PSObject.Properties['close'])    { $quoteSummary['close']  = $quote.close }
if ($quote.PSObject.Properties['exchange']) { $quoteSummary['exchange'] = $quote.exchange }
if ($quote.PSObject.Properties['type'])     { $quoteSummary['type']     = $quote.type }

# State summary
$studiesCount = 0
if ($state.PSObject.Properties['studies']) {
    $studiesCount = @($state.studies).Count
}

$visibleValuesCount = 0
$allStudies = @()
if ($state.PSObject.Properties['studies']) {
    foreach ($s in $state.studies) {
        $allStudies += $s.name
    }
}
if ($values.PSObject.Properties['studies']) {
    $visibleValuesCount = @($values.studies).Count
}

# Limits (from Phase 2 findings)
$limits = @{
    webhook_payload_visible      = $false
    alert_delete_programmatic    = "partial"
    trading_mutation_allowed     = $false
}

$bridge = [ordered]@{
    schema          = "tradingview_observer_bridge_v1"
    source_machine  = "cursor-ai"
    source_module   = "modules/tradingview_observer"
    generated_at    = $now
    symbol          = if ($status.PSObject.Properties['chart_symbol']) { $status.chart_symbol } else { "" }
    timeframe       = if ($status.PSObject.Properties['chart_resolution']) { $status.chart_resolution } else { "" }
    quote           = $quoteSummary
    state_summary   = @{
        studies_count       = $studiesCount
        studies_names       = $allStudies
        visible_values_count = $visibleValuesCount
    }
    alerts_summary  = @{
        total   = $alertTotal
        active  = $alertActive
        expired = $alertExpired
        unknown = $alertUnknown
    }
    limits          = $limits
    raw_files       = @{
        latest_report  = "not_embedded — see output/latest_report.json"
        latest_quote   = "not_embedded — see output/latest_quote.json"
        latest_state   = "not_embedded — see output/latest_state.json"
        latest_values  = "not_embedded — see output/latest_values.json"
        latest_alerts  = "not_embedded — see output/latest_alert_inventory.json"
    }
    transfer_policy = "dry-run only — no automated transfer, no admin-trading ingestion, no SSH"
}

$bridgeJson = $bridge | ConvertTo-Json -Depth 6
$bridgeJson = $bridgeJson -replace "`r`n", "`n"
[System.IO.File]::WriteAllText($BRIDGE_PATH, $bridgeJson, [System.Text.UTF8Encoding]::new($false))

$fileInfo = Get-Item $BRIDGE_PATH
$sizeKB = [math]::Round($fileInfo.Length / 1024, 1)

if ($Json) {
    Write-Output $bridgeJson
} else {
    Write-Host "Bridge packet V1 exported:" -ForegroundColor Green
    Write-Host "  Path  : $BRIDGE_PATH" -ForegroundColor Cyan
    Write-Host "  Size  : ${sizeKB} KB" -ForegroundColor Cyan
    Write-Host "  Symbol: $($bridge.symbol) @ $($bridge.timeframe)min" -ForegroundColor Cyan
    Write-Host "  Alerts: $alertTotal total, $alertActive active" -ForegroundColor Cyan
    Write-Host "  Status: dry-run only — no transfer executed" -ForegroundColor Yellow
}
