# TradingView Observer - Product Sanity (12 checks)
# Verifie l'integrite complete du produit local.
# Usage: .\product_sanity.ps1
param([int]$TimeoutSec = 10)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

$MOD = $PSScriptRoot
$OC_MOD = Join-Path $MOD "..\tradingview_observer_openclaw"
$TV_MCP = "$env:USERPROFILE\.claude\tools\tradingview-mcp\src\cli\index.js"
$OUTPUT = Join-Path $MOD "output"
$PassCount = 0
$FailCount = 0
$StartTime = Get-Date

function Write-Check($Num, $Label, $Ok, $Detail) {
    $ts = (Get-Date).ToString("HH:mm:ss")
    if ($Ok) {
        Write-Host "[$ts] [$Num] [PASS] $Label" -ForegroundColor Green
        $script:PassCount++
    } else {
        Write-Host "[$ts] [$Num] [FAIL] $Label  -  $Detail" -ForegroundColor Red
        $script:FailCount++
    }
}

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  TradingView Observer - Product Sanity" -ForegroundColor Cyan
Write-Host "  Started: $($StartTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Wrapper present
$wrapperExists = Test-Path (Join-Path $MOD "cmd.ps1")
Write-Check 1 "Wrapper present" $wrapperExists "modules/tradingview_observer/cmd.ps1"
if (-not $wrapperExists) {
    Write-Host "  FATAL: wrapper missing - cannot continue" -ForegroundColor Red
    exit 1
}

# 2. OpenClaw skill present
$ocExists = Test-Path (Join-Path $OC_MOD "run.ps1")
Write-Check 2 "OpenClaw skill present" $ocExists "modules/tradingview_observer_openclaw/run.ps1"

# 3. tradingview-mcp CLI present
$tvExists = Test-Path $TV_MCP
Write-Check 3 "tradingview-mcp CLI present" $tvExists "$TV_MCP"

# 4. output/.gitignore present
$giExists = Test-Path (Join-Path $OUTPUT ".gitignore")
Write-Check 4 "output/.gitignore present" $giExists "protects live JSON from commits"

# 5. Wrapper sanity PASS
$wrapperSanityOK = $false
if ($tvExists) {
    try {
        $sanityResult = & (Join-Path $MOD "cmd.ps1") -Sanity 2>&1
        $sanityOK = ($LASTEXITCODE -eq 0)
        Write-Check 5 "cmd.ps1 sanity PASS" $sanityOK "exit code=$LASTEXITCODE"
        $wrapperSanityOK = $sanityOK
    } catch {
        Write-Check 5 "cmd.ps1 sanity PASS" $false $_.Exception.Message
    }
} else {
    Write-Check 5 "cmd.ps1 sanity" $false "skipped - tradingview-mcp missing"
}

# 6. Wrapper snapshot PASS
$snapshotOK = $false
if ($wrapperSanityOK) {
    try {
        $snapResult = & (Join-Path $MOD "cmd.ps1") -Snapshot 2>&1
        $snapOK = ($LASTEXITCODE -eq 0)
        Write-Check 6 "cmd.ps1 snapshot PASS" $snapOK "exit code=$LASTEXITCODE"
        $snapshotOK = $snapOK
    } catch {
        Write-Check 6 "cmd.ps1 snapshot PASS" $false $_.Exception.Message
    }
} else {
    Write-Check 6 "cmd.ps1 snapshot" $false "skipped - sanity failed"
}

# 7. Bridge packet export PASS
if ($snapshotOK) {
    try {
        $bridgeResult = & (Join-Path $MOD "export_bridge_packet.ps1") 2>&1
        $bridgeOK = ($LASTEXITCODE -eq 0)
        Write-Check 7 "export_bridge_packet.ps1 PASS" $bridgeOK "exit code=$LASTEXITCODE"
    } catch {
        Write-Check 7 "export_bridge_packet.ps1 PASS" $false $_.Exception.Message
    }
} else {
    Write-Check 7 "export_bridge_packet.ps1" $false "skipped - snapshot failed"
}

# 8. OpenClaw run.ps1 PASS (sanity)
if (Test-Path (Join-Path $OC_MOD "run.ps1")) {
    try {
        $ocResult = & (Join-Path $OC_MOD "run.ps1") sanity 2>&1
        $ocOK = ($LASTEXITCODE -eq 0)
        Write-Check 8 "OpenClaw run.ps1 PASS" $ocOK "exit code=$LASTEXITCODE"
    } catch {
        Write-Check 8 "OpenClaw run.ps1 PASS" $false $_.Exception.Message
    }
} else {
    Write-Check 8 "OpenClaw run.ps1" $false "openclaw module missing"
}

# 9. latest_report.json exists
$reportExists = Test-Path (Join-Path $OUTPUT "latest_report.json")
Write-Check 9 "latest_report.json exists" $reportExists "output/latest_report.json"

# 10. latest_bridge_packet.json exists
$bridgeExists = Test-Path (Join-Path $OUTPUT "latest_bridge_packet.json")
Write-Check 10 "latest_bridge_packet.json exists" $bridgeExists "output/latest_bridge_packet.json"

# 11. Git: no live JSON tracked
try {
    $gitStatus = & git -C $MOD status --short -- output/ 2>&1
    $trackedFiles = $gitStatus -split "`n" | Where-Object { $_ -match "latest_.*\.json" }
    $noLiveJson = ($trackedFiles.Count -eq 0)
    Write-Check 11 "Git: no live JSON tracked" $noLiveJson "tracked=$($trackedFiles.Count) files"
} catch {
    Write-Check 11 "Git: no live JSON tracked" $false "git check failed: $_"
}

# 12. No mutation allowed by scripts
$scripts = @(
    (Join-Path $MOD "cmd.ps1"),
    (Join-Path $MOD "sanity_check.ps1"),
    (Join-Path $MOD "app\observer_runner.ps1"),
    (Join-Path $OC_MOD "run.ps1")
)
$mutationCheckOK = $true
$mutationDetail = ""
foreach ($script in $scripts) {
    if (-not (Test-Path $script)) { continue }
    $content = Get-Content $script -Raw
    if ($content -notmatch "AllowMutation" -and $content -notmatch "read-only" -and $script -ne (Join-Path $MOD "app\observer_runner.ps1")) {
        # observer_runner supports AllowMutation as a gated flag - that's fine
    }
    if ($content -match "alert_create|alert_delete" -and $content -notmatch "AllowMutation|FORBIDDEN|forbidden") {
        $mutationCheckOK = $false
        $mutationDetail += "$(Split-Path $script -Leaf); "
    }
}
Write-Check 12 "No unguarded mutation in scripts" $mutationCheckOK "$mutationDetail"

$duration = [math]::Round(((Get-Date) - $StartTime).TotalSeconds, 1)
$color = if ($FailCount -eq 0) { "Green" } elseif ($FailCount -le 2) { "Yellow" } else { "Red" }

Write-Host ""
Write-Host "================================================" -ForegroundColor $color
Write-Host "  $PassCount PASS / $FailCount FAIL - ${duration}s" -ForegroundColor $color
Write-Host "================================================" -ForegroundColor $color

if ($FailCount -eq 0) {
    Write-Host "  Status: PRODUCT SANITY PASS" -ForegroundColor Green
} elseif ($FailCount -le 2) {
    Write-Host "  Status: PRODUCT SANITY PARTIAL" -ForegroundColor Yellow
    Write-Host "  Some checks depend on runtime state (TV Desktop, CDP)." -ForegroundColor Yellow
} else {
    Write-Host "  Status: PRODUCT SANITY FAIL" -ForegroundColor Red
}

exit $FailCount
