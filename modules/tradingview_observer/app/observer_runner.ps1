# TradingView Observer Runner
param([switch]$AllowMutation, [string]$OutputDir = "")
$ErrorActionPreference = 'Stop'
$TV_CLI = "$env:USERPROFILE\.claude\tools\tradingview-mcp\src\cli\index.js"
$CDP_URL = "http://127.0.0.1:9222/json/version"

if (-not $OutputDir) { $OutputDir = Join-Path $PSScriptRoot "..\output" -Resolve }
if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Force $OutputDir | Out-Null }

function Tv { & node $TV_CLI @args 2>$null | Out-String | ConvertFrom-Json }

function Export-Json($Data, $Path) {
    $Data | Add-Member '_exported_at' (Get-Date -Format 'o') -Force
    $Data | ConvertTo-Json -Depth 10 | Out-File $Path -Encoding utf8
    "  -> $Path"
}

$m = if ($AllowMutation) { "MUTATION" } else { "READ-ONLY" }
Write-Host "[MODE] $m"
Write-Host ""

# 1. CDP check
Write-Host "[1/6] CDP check..."
try { $c = (Invoke-WebRequest $CDP_URL -UseBasicParsing -TimeoutSec 5).Content | ConvertFrom-Json; Write-Host "  OK: $($c.Browser)" -ForegroundColor Green }
catch { Write-Host "  FAIL: port 9222 closed" -ForegroundColor Red; exit 1 }

# 2. tv status
Write-Host "[2/6] tv status..."
try { $s = Tv status; Write-Host "  OK: $($s.chart_symbol) $($s.chart_resolution)" -ForegroundColor Green; Export-Json $s "$OutputDir\latest_status.json" }
catch { Write-Host "  FAIL: $_" -ForegroundColor Red; $s = @{success=$false;error="$_"} }

# 3. tv quote
Write-Host "[3/6] tv quote..."
try { $q = Tv quote; Write-Host "  OK: $($q.symbol) close=$($q.close)" -ForegroundColor Green; Export-Json $q "$OutputDir\latest_quote.json" }
catch { Write-Host "  FAIL: $_" -ForegroundColor Red; $q = @{success=$false;error="$_"} }

# 4. tv state
Write-Host "[4/6] tv state..."
try { $st = Tv state; Write-Host "  OK: $($st.symbol) studies=$($st.studies.Count)" -ForegroundColor Green; Export-Json $st "$OutputDir\latest_state.json" }
catch { Write-Host "  FAIL: $_" -ForegroundColor Red; $st = @{success=$false;error="$_"} }

# 5. tv alert list
Write-Host "[5/6] tv alert list..."
try { $a = Tv alert list; Write-Host "  OK: $($a.alert_count) alerts" -ForegroundColor Green; Export-Json $a "$OutputDir\latest_alert_inventory.json" }
catch { Write-Host "  FAIL: $_" -ForegroundColor Red; $a = @{success=$false;error="$_"} }

# 6. tv values
Write-Host "[6/6] tv values..."
try { $v = Tv values; Write-Host "  OK: $($v.study_count) studies" -ForegroundColor Green; Export-Json $v "$OutputDir\latest_values.json" }
catch { Write-Host "  FAIL: $_" -ForegroundColor Red; $v = @{success=$false;error="$_"} }

# Combined report
[ordered]@{exported_at=(Get-Date -Format 'o'); mode=$m; status=$s; state=$st; quote=$q; alert_inventory=$a; values=$v} | ConvertTo-Json -Depth 10 | Out-File "$OutputDir\latest_report.json" -Encoding utf8

Write-Host ""
Write-Host "=== Exports ===" -ForegroundColor Cyan
Get-ChildItem "$OutputDir\latest_*.json" | ForEach-Object { Write-Host "  $($_.Name) ($([math]::Round($_.Length/1KB,1)) KB)" }
